import json
import base64
import time
import boto3
import os

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://localstack:4566")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "pdf-bucket")

def get_client(service):
    return boto3.client(
        service,
        endpoint_url=AWS_ENDPOINT,
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

def ensure_bucket():
    s3 = get_client("s3")
    try:
        s3.create_bucket(Bucket=S3_BUCKET)
        print(f"Bucket '{S3_BUCKET}' created")
    except Exception:
        pass  # вже існує

def listen():
    sqs = get_client("sqs")
    s3 = get_client("s3")
    ensure_bucket()
    print("pdf_saver listening...")

    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5,
        )
        messages = response.get("Messages", [])
        for msg in messages:
            body = json.loads(msg["Body"])
            pdf_bytes = base64.b64decode(body["pdf"])
            key = f"profiles/{body['user_id']}.pdf"

            s3.put_object(Bucket=S3_BUCKET, Key=key, Body=pdf_bytes)
            print(f"Saved to S3: {key}")

            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"],
            )

if __name__ == "__main__":
    time.sleep(5)
    listen()
