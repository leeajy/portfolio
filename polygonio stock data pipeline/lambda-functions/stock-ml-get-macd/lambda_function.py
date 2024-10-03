import requests
import pandas as pd
import json
import os
import stockml as sml
import boto3

# global variables
bucket= 'stock-ml-1'
path= 'polygon/macd'
s3_resource = boto3.resource('s3')
lambda_client = boto3.client('lambda')

api_key = os.getenv('api_key')

def lambda_handler(event, context):
    ticker = event.get('ticker', 'AAPL')
    date_str = event.get('date','')
    partition = int(event.get('partition', 0))
    partition += 1

    if date_str:
      url = f"https://api.polygon.io/v1/indicators/macd/{ticker}?timestamp={date_str}&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=asc&apiKey={api_key}"
    
    else:
        url = f"https://api.polygon.io/v1/indicators/macd/{ticker}?timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=asc&apiKey={api_key}"  
    
    response = requests.get(url)

    if response.status_code == 200:
        results = json.loads(response.text)
        results = pd.DataFrame(results['results'])

        data = bytes(results.to_csv(index=False, header=True), encoding='utf-8')

        output_path = f"{path}/{ticker}"
        sml.to_csv(data, output_path, partition_size=134217728)
        
        next_url = json.loads(response.text).get("next_url")

        if next_url:
            payload = {
                'nextUrl' : next_url,
                'partition' : partition,
                'ticker' : ticker,
                'date_str' : date_str
            }

            payloadStr = json.dumps(payload)
            payloadBytesArr = bytes(payloadStr, encoding = 'utf8')
            response = lambda_client.invoke(
                FunctionName='stock-ml-get-macd',
                InvocationType = "Event",
                Payload = payloadBytesArr
            )
        else:
            return {
                'statusCode' : 200
            }
    else:
        return {
            'statusCode' : response.status_code,
        }
