import json 

def processFARforSameYear(far_json):
    json_output ={}
    json_size = len(far_json)
    #print( "json_size ::",json_size)
    for num in range(json_size-1) :
        far = far_json[num]
        next_far = far_json[num+1]
        #print("DATE FAR :: ", far["Date"], "DATE FAR 1:: ",next_far["Date"])
        if far["Date"] != next_far["Date"] and far["Date"] > next_far["Date"]:
            #print ("JSON :: ", json.dumps(far_json[num]))
            json_output = far_json[num]
            break
        else :
            #print("DATE FAR :: ", far["Date"], "DATE FAR 1:: ",next_far["Date"])
            for json_key in far :
                for far_json_key in next_far :
                    if far_json_key == "Date" and json_key == far_json_key:
                        break
                    if far_json_key == "amount_unit" and json_key == far_json_key:
                        break
                    if json_key == far_json_key :
                        json_obj = far[json_key]
                        far_json_obj = next_far[far_json_key]
                    
                        for taxonomy_json in json_obj :
                            for taxonomy_far_json in far_json_obj :
                                for taxonomy_json_key in taxonomy_json.keys() :
                                    for taxonomy_far_json_key in taxonomy_far_json.keys() :
                                        if taxonomy_json_key == taxonomy_far_json_key :
                                            far_amt = taxonomy_json[taxonomy_json_key].replace(',', '')
                                            far1_amt = taxonomy_far_json[taxonomy_far_json_key].replace(',', '')
                                            far_sum = float(far_amt) + float(far1_amt)
                                            #print("SUM :: ", far_sum)
                                            #print ("taxonomy_json :: ", taxonomy_json_key ," :: ", taxonomy_json[taxonomy_json_key])
                                            #print ("taxonomy_far_json :: ", taxonomy_far_json_key, " :: ",taxonomy_far_json[taxonomy_far_json_key])
                                            taxonomy_far_json.update({taxonomy_far_json_key : str(far_sum)})
                                        break
                        break        
    return json_output
