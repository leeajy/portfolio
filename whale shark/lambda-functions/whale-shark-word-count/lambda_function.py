# when triggered, calculate the word count. 
# input args: event["user"], event["date-option"]

import json
import boto3
import pandas as pd
from collections import Counter
import ast
import requests
import os
s3_resource = boto3.resource('s3')

def word_count(author):
    timeframe_prefix = ''
    prefix = 'word_count/' + timeframe_prefix
    
    bucket_str='whale-shark'
    bucket = s3_resource.Bucket(bucket_str)
    objects = bucket.objects.filter(Prefix=prefix)
    
    df0 = pd.DataFrame(columns=['Author','Counter']) 

    for object in objects:
        key = object.key                                                                                                                                                                 # ex. 'events/2022-08-02'
        counter = s3_resource.Object(bucket_str, key)
        body = counter.get()['Body']
        df_temp = pd.read_csv(body)
        df0 = pd.concat([df0,df_temp])
        
    df0 = df0[df0['Author'] == author] 
    
    df1 = df0['Counter'].transform(lambda x: Counter(ast.literal_eval(x)))
    
    counts = df1.agg(sum)
    
    words = counts.most_common(10)
    
    output_str = ""
    place = 1
    
    for word, count in words:
        output_str += f"{place}. {word}: {count}\n"
        place += 1 
    
    return output_str


def lambda_handler(event, context):
    print(event)
    ws_bot_token=os.getenv('ws_bot_token')
    
    ######### CALCULATE WORD COUNT BASED ON USER
    author = int(event["user"])
    output_str = word_count(author)
    
    
    ######### RESPOND TO INTERACTION
    
    interaction_token = event['interaction_token']
    
    application_id = event['application_id']
    
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
    
    
    json = {
        "content": output_str
        }
    
    
    # authorization
    headers = {
        "Authorization": f"Bot {ws_bot_token}"
    }
        
        
    r = requests.post(url, headers=headers, json=json)
    print(r)
    print(r.reason)
    print(r.content)


    return {
        'statusCode': 200
    }
