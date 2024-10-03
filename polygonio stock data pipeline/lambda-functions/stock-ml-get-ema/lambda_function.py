# exponential moving average

import requests
import pandas as pd
import json
import os
import stockml as sml 

# global variables
bucket= 'stock-ml-1'
path= 'polygon/ema'

api_key = os.getenv('api_key')

#{window}-moving average (window = 50 --> 50-day moving average)
# each row holds the moving average value from that specific day

def lambda_handler(event, context):
    ticker = event.get('ticker', 'AAPL')
    timestamp = event.get('date', '')
    timespan = event.get('timespan', 'day')
    window = event.get('window', 50)
    # return_response: if this value is True, return the response of the api instead of saving to s3.
    return_response = event.get('returnResponse', False)

    if not timestamp:
        url = f"https://api.polygon.io/v1/indicators/ema/{ticker}?&timespan={timespan}&adjusted=true&window={window}&series_type=close&order=desc&limit=1000&apiKey={api_key}"
    else:
        url = f"https://api.polygon.io/v1/indicators/ema/{ticker}?timestamp={timestamp}&timespan={timespan}&adjusted=true&window={window}&series_type=close&order=desc&limit=1000&apiKey={api_key}"

    response = requests.get(url)
    
    if response.status_code == 200:
        results = json.loads(response.text)
        try:
            results = pd.DataFrame(results['results']['values'])
            results['timestamp'] = pd.to_datetime(results['timestamp'], unit = 'ms')
            
            if return_response:
                return {
                'responseJson': results.to_json(),
                'statusCode' : response.status_code
                }
            else:
                data = bytes(results.to_csv(index=False, header=True), encoding='utf-8')
                output_path = f"{path}/{ticker}"
                sml.to_csv(data, output_path, partition_size=134217728)
                return {
                    'statusCode' : response.status_code,
                }
        except KeyError:
                error = "No key 'values'"
                return {
                    'statusCode' : 400,
                    'error': error
                }

    else:
        return {
            'statusCode' : response.status_code,
            'error' : response.text
        }
