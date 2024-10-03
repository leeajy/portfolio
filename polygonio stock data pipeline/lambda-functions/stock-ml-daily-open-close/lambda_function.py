import json
import requests
import os
import boto3
import pandas as pd
import stockml as sml

# global variables
s3_resource = boto3.resource('s3')
bucket = 'stock-ml-1'


def lambda_handler(event, context):
    ticker = event.get('ticker','AAPL')
    date = event.get('date', '2022-09-16')
    # return_response: if this value is True, return the response of the api instead of saving to s3.
    return_response = event.get('returnResponse', False)
    
    api_open_close = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true" 
    
    # add api key to call
    api_key = os.getenv('api_key')
    api_open_close += f"&apiKey={api_key}"
    
    response = requests.get(api_open_close)
    
    print(response.status_code)
    if response.status_code == 200:
        results = json.loads(response.text)
        
        results_df = pd.DataFrame([results])
        results_df = results_df.astype(str)
        
        # API will not have afterHours key if this function is called before 8 PM ET. 
        columns_1 = ['status', 'from', 'symbol', 'open', 'high', 'low', 'close', 'volume',
        'afterHours', 'preMarket']
        columns_2 = ['status', 'from', 'symbol', 'open', 'high', 'low', 'close', 'volume',
        'afterHours', 'preMarket', 'otc']
        columns_api = results_df.columns.tolist()
        
        # check that columns of result match expected values
        if columns_api != columns_1 and columns_api != columns_2:
            raise Exception('API response has been changed. Check API response.')  
        
        if return_response:
            return {
            'responseJson': results_df.to_json(),
            'statusCode' : response.status_code
            }
        else:
            data = bytes(results_df.to_csv(index=False, header=True), encoding='utf-8')
            # append result to S3 using awswrangler
            output_path = f"polygon/open-close/{ticker}"
            response = sml.to_csv(data, output_path, partition_size=134217728)
            return {
                'statusCode': 200
            }
    else:
        return {
            'statusCode': response.status_code,
            'error': response.text
        }
