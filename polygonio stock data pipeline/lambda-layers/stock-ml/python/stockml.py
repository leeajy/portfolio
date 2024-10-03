import boto3

# Global variables
bucket = 'stock-ml-1'
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket)

# Sorting function
def return_key(elem):
    return elem.key

def create_new_partition(key: str, data: bytes):
    # if there is a newline byte at the end of data, remove it
    if data[-1:] == b'\n':
        data = data[:-1]
    new_partition = bucket.Object(key=key)
    new_partition.put(Body=data)

def validate_data(data: bytes):
    if not isinstance(data, bytes):
        raise TypeError(f'Data is of type {type(data)}, not bytes.')
    
def to_csv(data: bytes, path: str, partition_size: int):
    # Check if data is valid.
    validate_data(data)

    # Get list of partitions.
    objs = list(bucket.objects.filter(Prefix=path))
    
    # Check if partition exists. If not, create a new partition.
    if len(objs) == 0:
        name = '000001'
        # if path ends with a /, remove it.
        if path.endswith('/'):
            path = path[:-1]
        create_new_partition(f"{path}/{name}.csv", data) 
        return
    
    # Get latest partition.
    latest_partition_key = sorted(objs, key=return_key)[-1].key
    latest_partition = bucket.Object(key=latest_partition_key)
    
    # Get size of partition. 
    latest_partition_size = latest_partition.content_length
    
    # If latest_partition_size is greater than input partition_size, create a new partition.
    if latest_partition_size > partition_size:
        latest_name = int(latest_partition_key.split('/')[-1].split('.')[0])
        new_name = str(latest_name + 1).zfill(6)
        create_new_partition(f"{path}/{new_name}.csv", data) 
        return
    # Otherwise, append to current partition.
    else:
        body = latest_partition.get()['Body']
        # header row must be removed from data when appending
        data = bytes('\n' + '\n'.join(str(data).split('\\n')[1:-1]), encoding='utf-8')
        new_body = body.read() + data
        latest_partition.put(Body=new_body)
