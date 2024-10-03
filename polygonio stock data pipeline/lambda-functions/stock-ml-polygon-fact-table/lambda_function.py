import json
import awswrangler as wr
import stockml as sml

# global variables
bucket = 'stock-ml-1'


def lambda_handler(event, context):
    ticker = event.get('ticker','AAPL')
    
    # open close data
    df_oc = wr.s3.read_csv(f"s3://stock-ml-1/polygon/open-close/{ticker}/")
    # ema data
    df_ema = wr.s3.read_csv(f"s3://stock-ml-1/polygon/ema/{ticker}/")
    # rsi data
    df_rsi = wr.s3.read_csv(f"s3://stock-ml-1/polygon/rsi/{ticker}/")
    # merge rsi and ema by timestamp
    df_indicators = df_ema.merge(df_rsi, how='left', left_on='timestamp', 
                                             right_on='timestamp',
                                             suffixes=('_ema','_rsi'))
    # get date from timestamp
    df_indicators["date"] = df_ema["timestamp"].str.split(' ').str[0]
    # merge open/close dataframe with indicators dataframe
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

    
    print(response)
    return {
        'statusCode': 200,
    }
