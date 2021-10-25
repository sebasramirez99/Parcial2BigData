import time
import boto3


DATABASE = 'YahooFinances'
TABLE = 'finances'

def handler(event, context):
    query = 'MSCK REPAIR TABLE `finances`;'
    client = boto3.client('athena')

    # Execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        }
    )
    return response