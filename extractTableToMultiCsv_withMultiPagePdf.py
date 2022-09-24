import boto3
import time
from csvReader import *
import sys
from jsonProcessor import *
import re
import pathlib

def startJob(s3BucketName, objectName):
    response = None
    #client = boto3.client('textract')
    response = client.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        },
        FeatureTypes = ['TABLES']
    )
    return response["JobId"]

def isJobComplete(jobId):
    # For production use cases, use SNS based notification 
    # Details at: https://docs.aws.amazon.com/textract/latest/dg/api-async.html
    time.sleep(5)
    #client = boto3.client('textract')
    response = client.get_document_analysis(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status

def getJobResults(jobId):
    pages = []
    #client = boto3.client('textract')
    response = client.get_document_analysis(JobId=jobId)
    
    pages.append(response)
    print("Resultset page recieved::::: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']
    while(nextToken):
        response = client.get_document_analysis(JobId=jobId, NextToken=nextToken)
        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
    return pages

def generate_table_csv(table_result, blocks_map):
    rows = get_rows_columns_map(table_result, blocks_map)
    
    # get cells.
    csvTable = ''
    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            if text.lower() =='Gross Block '.lower() or text.lower()== 'Gross '.lower() or text.lower() =='Gross Block'.lower(): 
                csvTable = writeToCSV(rows)
                break
            else :
                if text.lower().find('gross') != -1:
                    csvTable = writeToCSV(rows)
                    break
    #csv += '\n\n\n'
    return csvTable

def writeToCSV(table_rows) :
    csv = ''
    for row_index, cols in table_rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + "|"
        csv += '\n'
        
    #csv += '\n\n\n'
    return csv


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text

# Document
s3 = boto3.resource('s3', 
            aws_access_key_id= 'AKIAT4D3PKB6ZMWLAJ7A', 
            aws_secret_access_key= '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', 
            region_name= 'ap-south-1'
)

client = boto3.client('textract',
            aws_access_key_id= 'AKIAT4D3PKB6ZMWLAJ7A', 
            aws_secret_access_key= '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', 
            region_name= 'ap-south-1')

s3_client = boto3.client('s3', 
            aws_access_key_id= 'AKIAT4D3PKB6ZMWLAJ7A', 
            aws_secret_access_key= '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', 
            region_name= 'ap-south-1'
)

amount_unit = [r'\bthousands\b', r'\bthousand\b', r'\blakhs\b', r'\blakh\b', r'\blac\b', r'\bcrore\b', r'\bcr.\b', r'\bcr\b', r'\bcrores\b']

s3BucketName = input ("Enter Bucket name :: ")

s3_response = s3_client.list_objects_v2(Bucket=s3BucketName)
files = s3_response.get("Contents")
for file in files:
    if file['Size'] !=0 and pathlib.Path(file['Key']).suffix == ".pdf":
        print("Processing File ",file['Key'])
        try :
            documentName = file['Key']
            jobId = startJob(s3BucketName, documentName)
            #print("Started job with id: {}".format(jobId))
            jsonArr = []
            if(isJobComplete(jobId)):
                response = getJobResults(jobId)

                blocks_map = {}
                table_blocks = []
                page_no =0
                for resultPage in response:
                    #print("BLOCKS :: ", resultPage["Blocks"] )
                    for block in resultPage["Blocks"]:
                        blocks_map[block['Id']] = block
                        if block['BlockType'] == "TABLE":
                            #print ("Confidence level :: ", block['Confidence'])
                            table_blocks.append(block)
                    
                if len(table_blocks) <= 0:
                    print( "<b> NO Table FOUND </b>")

                csv = ''
                amt_unit = 'None'
                for index, table in enumerate(table_blocks):
                    csv = generate_table_csv(table, blocks_map)
                    if csv != '' :
                        output_file = documentName.rstrip(".pdf") + '_table_' + str(index+1) +'.csv'
                        obj = s3.Object(s3BucketName, output_file)
                        obj.put(Body=csv)
                        print('Generated CSV FILE: ', output_file)
                        #find unit for insurance amount
                        page_no = table['Page']
                        #amt_unit = 'None'
                        #print("PAGE :: ",page_no)
                        for resultPage in response:
                            for block in resultPage["Blocks"]:
                                if block['Page']== page_no :
                                    if block['BlockType'] == "LINE":
                                        text = block['Text']
                                        for unit in amount_unit :
                                            unitRegex = re.compile(unit)
                                            ut = re.search(unitRegex, text.lower())
                                            if ut !=None :
                                                amt_unit = ut.group()
                                                break
                                            
                        json_data = read_csv(s3BucketName, output_file)
                        if len(json_data) !=0 :
                            json_data["amount_unit"] = amt_unit
                            jsonArr.append(json_data)
                            
                if len(jsonArr) !=0 :
                    sorted_json_data = sorted(jsonArr, key=lambda k: k['Date'], reverse=True)
                    if len(sorted_json_data) > 1 :
                        json_output = processFARforSameYear(sorted_json_data)
                        obj = s3.Object(s3BucketName, documentName.rstrip(".pdf")+'.json')
                        obj.put(Body=json.dumps(json_output))
                        print("Generated Json inside :: ", s3BucketName," " ,documentName.rstrip(".pdf")+'.json')
                    else :
                        obj = s3.Object(s3BucketName, documentName.rstrip(".pdf")+'.json')
                        obj.put(Body=json.dumps(sorted_json_data[0]))
                        print("Generated Json inside :: ", s3BucketName," " ,documentName.rstrip(".pdf")+'.json')
                #else :
                    #print("NO FAR report found")
            sys.stdout.flush()
                            
        except Exception as exp:
            print("##### Exception occured while processing file ::", documentName ," Exception :: ", exp)





 
