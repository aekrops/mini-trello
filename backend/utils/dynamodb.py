import boto3


def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        endpoint_url="http://dynamodblocal:8000",
        region_name="eu-west-1",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )


def get_dynamodb_table(table_name):
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)


def get_items_by_table(table_name):
    table = get_dynamodb_table(table_name)
    response = table.scan()
    return response.get("Items", [])
