import json
import boto3
import base64
import os
import time
from datetime import datetime, timezone


s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body =json.loads(event['body'])
        file_content = base64.b64decode(body['file'])
        filename = body['filename']
        content_type = body.get('content_type', 'application/octet-stream')
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body= file_content,
            ContentType=content_type
        )
        table.put_item(Item={
            'FileName': filename,
            'Timestamp': datetime.now(timezone.utc).isoformat(),
            'Size': len(file_content),
            'ContentType': content_type
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File uploaded and metadata store in DynDb'})
          
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
