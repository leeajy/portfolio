import json
import boto3
from collections import Counter

# global variables
lambda_client = boto3.client('lambda')
sc_counter = Counter() # status code counter

def invoke_lambda(function_name, payload):
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    # request response to prevent concurrency. 
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=payloadBytesArr
    )
    sc_counter[response['StatusCode']] += 1


# this lambda function invokes various lambda functions.
def lambda_handler(event, context):
    default_lfns = ['stock-ml-daily-open-close', 'stock-ml-get-ema', 'stock-ml-get-news', 'stock-ml-get-rsi']
    lfn_names = event.get('LambdaFunctionNames', default_lfns) 
    tickers = event.get('GetTickerSeries').get('tickers',[])
    exchange = event.get('exchange','XNAS')
    date_str = event.get('date', '2022-01-13')
    
    for ticker in tickers:
        payload = {
            'ticker': ticker,
            'date': date_str,
        }
        for lfn in lfn_names:
            invoke_lambda(lfn, payload)

    return dict(sc_counter)
