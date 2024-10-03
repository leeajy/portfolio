import requests
import pandas as pd
import json
import os
import stockml as sml
import numpy as np

# global variables
bucket= 'stock-ml-1'
path= 'polygon/news'

api_key = os.getenv('api_key')

def lambda_handler(event, context):
    ticker = event.get('ticker', 'AAPL')
    date_str = event.get('date','')
    # return_response: if this value is True, return the response of the api instead of saving to s3.
    return_response = event.get('returnResponse', False)

    url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&published_utc={date_str}&limit=100&sort=published_utc&apiKey={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        results = json.loads(response.text)
        # If there are results, save to csv
        if results['results']:      
            results_df = pd.DataFrame(results['results'])
            columns_api = results_df.columns.tolist()
            # Ensure all columns are present. If not, add column to results_df with NaN
            columns = ['id', 'publisher', 'title', 'author', 'published_utc', 'article_url', 'tickers', 'amp_url',
            'image_url', 'description', 'keywords']
            for column in columns:
                if column not in columns_api:
                    results_df[column] = pd.Series(np.nan)
            # Rearrange columns
            results_df = results_df[['id', 'publisher', 'title', 'author', 'published_utc', 'article_url', 'tickers', 'amp_url',
            'image_url', 'description', 'keywords']]
            
            if return_response:
                return {
                'responseJson': results_df.to_json(),
                'statusCode' : response.status_code
                }
            else:
                data = bytes(results_df.to_csv(index=False, header=True), encoding='utf-8')
                output_path = f"{path}/{ticker}"
                sml.to_csv(data, output_path, partition_size=134217728)
                return {
                    'statusCode' : response.status_code,
                }
    else:
        return {
            'statusCode' : response.status_code,
        }
