import json
import boto3
from collections import Counter

# global variables
lambda_client = boto3.client('lambda')
sc_counter = Counter() # status code counter

def invoke_lambda(function_name, payload):
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=payloadBytesArr
    )
    sc_counter[response['StatusCode']] += 1


# This lambda function acts as a map state. It is non-blocking (unlike stock-ml-invoke-multiple-lambdas)
# This lambda should only be used for map states which can be run concurrently (like a map of tickers).
def lambda_handler(event, context):
    default_lfns = ['stock-ml-polygon-fact-table-incremental']
    lfn_names = event.get('LambdaFunctionNames', default_lfns) 
    tickers = event.get('tickers',[])
    exchange = event.get('exchange','XNAS')
    date_str = event.get('date', '2022-01-13')
    
    for ticker in tickers:
        payload = {
            'GetTickerSeries': { 'tickers' : [ticker] },
            'exchange': exchange,
            'date': date_str
        }
        for lfn in lfn_names:
            invoke_lambda(lfn, payload)

    return dict(sc_counter)
