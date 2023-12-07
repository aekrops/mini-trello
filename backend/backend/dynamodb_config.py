import boto3
from django.conf import settings


def setup_dynamodb():
    boto3.setup_default_session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_ACCESS_KEY_ID,
        region_name=settings.AWS_REGION,
    )
    # Create and return the DynamoDB resource with the endpoint_url specified
    return boto3.resource('dynamodb', endpoint_url='http://localhost:8000')  # For DynamoDB Local
