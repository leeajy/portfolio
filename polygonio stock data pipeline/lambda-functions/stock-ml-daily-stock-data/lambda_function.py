import json
import boto3
from datetime import datetime, timedelta

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    state_machine_arn = "arn:aws:states:us-east-2:913902556403:stateMachine:stock-ml-daily-stock-data"
  
    date_utc = datetime.strptime(event.get('time'),"%Y-%m-%dT%XZ")
    # convert to local time
    date_str = (date_utc - timedelta(hours=7)).strftime('%Y-%m-%d')

    state_machine_input = {
        "exchange": "nasdaq",
        "date": date_str
    }

    payloadStr = json.dumps(state_machine_input)

    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=payloadStr,
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Execution for step function {state_machine_arn} has started.')
    }
