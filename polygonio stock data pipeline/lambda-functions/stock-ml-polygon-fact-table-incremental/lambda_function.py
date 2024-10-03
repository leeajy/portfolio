import json
import boto3
import pandas as pd
import stockml as sml
import numpy as np

# global variables
bucket = 'stock-ml-1'
lambda_client = boto3.client('lambda')

def default_df(function_name):
    # return a df of NaNs based on the function
    if function_name == 'stock-ml-daily-open-close':
        columns = ['status', 'from', 'symbol', 'open', 'high', 'low', 'close', 'volume',
                   'afterHours', 'preMarket']
    elif function_name == 'stock-ml-get-ema':
        columns = ['timestamp', 'value']
    elif function_name == 'stock-ml-get-rsi':
        columns = ['timestamp', 'value']
    return pd.DataFrame(np.nan, index=[0], columns=columns)

def invoke_lambda_df(function_name, payload):
    # return a df of the response text
    payloadStr = json.dumps(payload)
    payloadBytesArr = bytes(payloadStr, encoding='utf8')
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=payloadBytesArr
    )
    payload = json.loads(response['Payload'].read())
    response_json = payload.get('responseJson')
    if response_json:
        return pd.read_json(response_json, dtype = False)
    else:
        return default_df(function_name)


def lambda_handler(event, context):
    tickers = event.get('GetTickerSeries').get('tickers',[])
    exchange = event.get('exchange','XNAS')
    date_str = event.get('date', '2022-01-13')
    
    ticker = tickers[0]
    
    payload = {
        'returnResponse' : True,
        'ticker': ticker,
        'date': date_str,
    }
    
    # open close data
    df_oc = invoke_lambda_df('stock-ml-daily-open-close', payload)
    # ema data
    df_ema = invoke_lambda_df('stock-ml-get-ema', payload)
    # rsi data
    df_rsi = invoke_lambda_df('stock-ml-get-rsi', payload)
    # merge rsi and ema by timestamp
    df_indicators = df_ema.merge(df_rsi, how='left', left_on='timestamp', 
                                             right_on='timestamp',
                                             suffixes=('_ema','_rsi'))
    # get date from timestamp
    df_indicators["date"] = df_ema["timestamp"].astype(str).str.split(' ').str[0]
    # merge open/close dataframe with indicators dataframe (merge only allowed with non-NaNs)
    df_all = df_oc.merge(df_indicators, how='left', left_on='from', 
                                             right_on='date')
    # remove unnecessary columns
    df_all = df_all.drop(columns=['status', 'timestamp', 'from'])
    # filter NaNs using masking
    df_all = df_all[df_all['value_ema'].notnull()]
    df_all = df_all[df_all['value_rsi'].notnull()]
    
    # order by datetime 
    df_all = df_all.sort_values(by='date', ascending=True)
    
    # drop duplicates
    df_all = df_all.drop_duplicates()
    
    # round all columns
    df_all = df_all.round(2)
    
    # write df_all to s3
    output_path = f"polygon/fact/{ticker}/"
    data = bytes(df_all.to_csv(index=False, header=True), encoding='utf-8')
    sml.to_csv(data, output_path, partition_size=134217728)

    return {
        'statusCode': 200,
    }
