import json
import requests
import pandas as pd
import os
import boto3

s3_resource = boto3.resource('s3')
bucket = 'the-guppy'


def lambda_handler(event, context):
    ticker = event.get('ticker','GOOGL')
    gte_date = event.get('gte.date', '2022-01-01')
    
    api_financials = f"https://api.polygon.io/vX/reference/financials?ticker={ticker}" + \
    f"&filing_date.gte={gte_date}&include_sources=false&sort=filing_date&limit=100"
    
    # add api key to call
    api_key = os.getenv('api_key')
    api_financials += f"&apiKey={api_key}"
    
    response = requests.get(api_financials)
    
    print(response.status_code)
    if response.status_code == 200:
        results = json.loads(response.text)['results']
        results_df = pd.DataFrame(results)
        
        if results_df.shape[0] == 0:
            return {
            'statusCode': 400,
            'error': 'No '
            }
        else:
            financials_df = pd.json_normalize(results_df['financials'])
            results_df = pd.concat([results_df, financials_df], axis=1)
            results_df['ticker']=ticker
            results_df = results_df.astype(str)
            results_list = results_df.values.tolist()
            
            return {
                'statusCode': 200,
                'results_list': results_list
            }
    else:
        return {
            'statusCode': response.status_code,
            'error': response.text
        }

