import pandas as pd
import awswrangler as wr
import os
from collections import Counter
import ast
import requests

# global variables
bucket= 'whale-shark'
counter_path = f"s3://{bucket}/word-counts"


def word_count(author):
    df = wr.s3.read_csv(path=counter_path)
    df = df[df['author'] == author]
    df = df['Counter'].transform(lambda x: Counter(ast.literal_eval(x)))
    counts = df.agg(sum)
    words = counts.most_common(15)
    output_str = ""
    place = 1

    for word, count in words:
        output_str += f"{place}. {word}: {count}\n"
        place += 1

    return output_str


def lambda_handler(event, context):
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
