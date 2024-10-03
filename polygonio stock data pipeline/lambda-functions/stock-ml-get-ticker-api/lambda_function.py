import json
import requests
import pandas as pd
import os
import boto3
from io import StringIO 

# global variables
s3_resource = boto3.resource('s3')
bucket = 'stock-ml-1'
lambda_client = boto3.client('lambda')

# this lambda function re-invokes itself via next_url.
def lambda_handler(event, context):
    # original input
    ticker_type = event.get('tickerType','CS')
    exchange = event.get('exchange','XNAS')
    date_str = event.get('date', '2022-01-13')
    
    # re-invocation inputs
    next_url = event.get('nextUrl')
    partition = int(event.get('partition', 0))
    partition += 1 
    
    # change exchange str to code
    if exchange == 'nasdaq':
        exchange = 'XNAS'
    
    if next_url:
        api_tickers = next_url
    else:
        api_tickers = f"https://api.polygon.io/v3/reference/tickers?type={ticker_type}&exchange={exchange}&date={date_str}" \
            "&active=true&sort=ticker&order=asc&limit=1000" 
    # add api key to call
    api_key = os.getenv('api_key')
    api_tickers += f"&apiKey={api_key}"
    
    response = requests.get(api_tickers)
    
    print(response.status_code)
    if response.status_code == 200:
        results = json.loads(response.text)["results"]
        results_df = pd.DataFrame(results)
        
        csv_buffer = StringIO()
        results_df.to_csv(csv_buffer)
        s3_resource.Object(bucket, f'polygon/tickers/{exchange}/{ticker_type}/{date_str}/{partition}.csv').put(Body=csv_buffer.getvalue())
        
        next_url = json.loads(response.text).get("next_url")
        
        if next_url:
            payload = {
                'nextUrl': next_url,
                'partition': partition,
                'exchange': exchange, 
                'tickerType': ticker_type,
                'date': date_str
            }
            payloadStr = json.dumps(payload)
            payloadBytesArr = bytes(payloadStr, encoding='utf8')
            response = lambda_client.invoke(
                FunctionName='stock-ml-get-ticker-api',
                InvocationType='RequestResponse',
                Payload=payloadBytesArr
            )
            return {
                'statusCode': 200
            }
        else:
            return {
                'statusCode': 200
            }
