import json
import awswrangler as wr
import boto3

# global variables
bucket = 'stock-ml-1'
s3 = boto3.resource("s3")


def lambda_handler(event, context):
    subset = event.get('subset', ['date'])
    full_path = event.get('fullPath','s3://stock-ml-1/polygon/fact/AMD/000001.csv')
    
    if full_path.endswith('/'):
        raise ValueError('argument must be a full path (single file).') 
    
    df = wr.s3.read_csv(full_path)
    
    # drop duplicates
    df = df.drop_duplicates(subset=subset)
    
    # round all columns
    df = df.round(2)
    
    # drop NaNs
    df = df.dropna()
    
    # delete current file
    key = full_path.split('stock-ml-1/')[1]
    obj = s3.Object(bucket, key)
    obj.delete()
    
    # write new file
    data = bytes(df.to_csv(index=False, header=True), encoding='utf-8')
    obj.put(Body = data)
    
    return {
        'statusCode': 200,
    }
