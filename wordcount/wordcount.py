import boto3
import json
import os
from datetime import datetime, timezone

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        print("🚀 Lambda function triggered")
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"📦 File: {bucket}/{key}")

        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')

        word_count = len(content.split())
        print(f"🔢 Word count: {word_count}")

        table.put_item(Item={
            'FileName': key,
            'Timestamp': datetime.now(timezone.utc).isoformat(),
            'Size': len(content.encode('utf-8')),
            'ContentType': response['ContentType'],
            'WordCount': word_count


        })   

        print("✅ DynamoDB item stored")

        return {"statusCode": 200, "body": "Word count stored successfully"}
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"statusCode": 500, "body": str(e)}
    

                                
