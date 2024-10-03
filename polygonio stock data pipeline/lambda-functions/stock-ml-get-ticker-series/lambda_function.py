import json
import boto3
import pandas as pd
import numpy as np

s3_resource = boto3.resource('s3')
bucket_str='stock-ml-1'
bucket = s3_resource.Bucket(bucket_str)

def lambda_handler(event, context):
    # temporary - return shorter ticker list for prototyping
    tickers = [ 'AMD']
    tickers = [tickers]
    return {
        'statusCode': 200,
        'tickers': tickers
    }
    

def lambda_handler_2(event, context):
    return_partitions = event.get('returnPartitions', 8)
    ticker_type = event.get('tickerType','CS')
    exchange = event.get('exchange','nasdaq')
    date_str = event.get('date', '2022-01-13')
    
    if exchange == 'nasdaq':
        exchange = 'XNAS'
    
    prefix=f'polygon/tickers/{exchange}/{ticker_type}/{date_str}/'
    objects = bucket.objects.filter(Prefix=prefix)
    
    df0 = pd.DataFrame(columns=['ticker']) 

    for object in objects:
        key = object.key                                                                                                                                                                 # ex. 'events/2022-08-02'
        file = s3_resource.Object(bucket_str, key)
        body = file.get()['Body']
        df_temp = pd.read_csv(body)
        df_temp = df_temp[['ticker']]
        df0 = pd.concat([df0,df_temp])
    
    tickers = df0['ticker'].tolist()
    
    blacklist = []
    
    tickers = list(set(tickers) - set(blacklist))
    
    tickers = sorted(tickers)
    
    # split tickers into partitions if requested
    if return_partitions:
        tickers = [x.tolist() for x in np.array_split(tickers, return_partitions)]
    else:
        tickers = [tickers]
    return {
        'statusCode': 200,
        'tickers': tickers
    }
