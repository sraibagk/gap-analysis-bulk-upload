import csv
import re
import json
import boto3
from taxonomy import *
from dateutil import parser
from datetime import datetime
from dateRegex import *
    
def read_csv(bucketName,fileName) :
    s3 = boto3.resource('s3', 
            aws_access_key_id= 'AKIAT4D3PKB6ZMWLAJ7A', 
            aws_secret_access_key= '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', 
            region_name= 'ap-south-1'
    )

    bucket = s3.Bucket(bucketName)
    obj = bucket.Object(key=fileName)
    response = obj.get()

    data = response['Body'].read().decode('utf-8').splitlines() 
    #print ("RESPONSE ::: ", data)
    file_read = csv.reader(data,delimiter='|') 

    list_CSV =''
    #list_CSV = list(file_read)
    json_object ={}
    headers = next(file_read)
    for head in headers :
        if head.lower() =='Gross Block '.lower() or head.lower()== 'Gross '.lower() or head.lower().find('gross') != -1:       
            list_CSV = list(file_read)
            print("FAR report found")
            json_object = process_FAR_report(list_CSV)
            break
    
    if list_CSV =='' :
        print("No FAR report found")

    return json_object

def convertToDate (date_string) :
    date_time =parser.parse(date_string)
    #print("date_time ::: ", date_time)
    datetime_str = date_time.strftime("%m/%d/%Y")
    #print("Date ::: ", datetime_str)
    return datetime_str  

def searchDateFromString(dateString) :
    #print("dateString :::", dateString)
    for regEx in dateRegExTosearch :
        dtRegex = re.compile(regEx)
        dt = dtRegex.search(dateString)
        if dt != None:
            date =convertToDate(dt.group())
            return date
    if dt == None:
            raise Exception ("Could not extract date from date string :: ", dateString)        #break
        

def process_FAR_report(input_csv) :
        dateIndex = 0
        index =0
        output_json = {}
        new_date =""
        for row in input_csv:
            #print (row)
            for i in range(len(row)):
                if dateIndex !=2 :
                    for dateregEx in dateRegExs :
                        if (re.match(dateregEx, row[i])) :
                            dateIndex += 1
                            break

                    if(dateIndex==2):
                        index = i 
                        dateString = row[i]
                        new_date = searchDateFromString(dateString)
                        break
                    else:
                        continue  

                if dateIndex ==2 :    
                    if (row[i].strip()).lower() in buildings_taxonomy  :
                        output_json ["Date"] = new_date
                        amt = row[index]
                        data =[]
                        if "Buildings" in output_json:
                            data = output_json["Buildings"]
                            data.append({row[i] : amt })
                            output_json ["Buildings"] = data
                        else: 
                            data.append({row[i] : amt })
                            output_json ["Buildings"] = data
                        break
                    if (row[i].strip()).lower() in plant_and_machinery_taxonomy :
                        output_json ["Date"] = new_date
                        amt = row[index]
                        data =[]
                        if "Plant and Machinery" in output_json:
                            data = output_json["Plant and Machinery"]
                            data.append({row[i] : amt })
                            output_json ["Plant and Machinery"] = data
                        else :
                            data.append({row[i] : amt })
                            output_json ["Plant and Machinery"] = data
                        break    
                    if (row[i].strip()).lower() in office_equipments_taxonomy :
                        output_json ["Date"] = new_date
                        amt = row[index]
                        data =[] 
                        if "Office Equipments" in output_json:
                            data = output_json["Office Equipments"]
                            data.append({row[i] : amt })
                            output_json ["Office Equipments"] = data
                        else: 
                            data.append({row[i] : amt })
                            output_json ["Office Equipments"] = data
                        break
                    if (row[i].strip()).lower() in furniture_and_fixtures_taxonomy :
                        output_json ["Date"] = new_date
                        amt = row[index]
                        data =[] 
                        if "Furniture & Fixtures" in output_json:
                            data = output_json["Furniture & Fixtures"]
                            data.append({row[i] : amt })
                            output_json ["Furniture & Fixtures"] = data
                        else: 
                            data.append({row[i] : amt })
                            output_json ["Furniture & Fixtures"] = data
                        break
                    
        if dateIndex == 2 and len(output_json)==0 :
                print ("Taxonmomy not matched for FAR report found")            

        if dateIndex == 0  :  
            print ("No matching date regex found")          
        return  output_json
