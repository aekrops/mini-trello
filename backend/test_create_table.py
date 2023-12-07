import logging
from typing import Any
from typing import List as Lt

import boto3

logger = logging.getLogger(__name__)


class List:
    def __init__(self, name: str, items: Lt[Any] = None):
        self.name = name
        self.items = items if items else []

    def save(self) -> None:
        """Saves the list to the DynamoDB"""
        try:
            table = ddb.Table('Lists')
            item = {"name": self.name, "items": self.items}
            table.put_item(Item=item)
        except Exception as e:
            logger.error(f"Error saving list {e}")


def create_card_table():
    # Define attribute definitions and key schema for the table
    attribute_definitions = [
        {
            'AttributeName': 'card_id',
            'AttributeType': 'S'  # 'S' for string type
        }
    ]

    key_schema = [
        {
            'AttributeName': 'card_id',
            'KeyType': 'HASH'  # 'HASH' for partition key
        }
    ]

    # Define provisioned throughput (optional for DynamoDB Local)
    provisioned_throughput = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

    # Create the DynamoDB table
    table = ddb.create_table(
        TableName="Cards",
        AttributeDefinitions=attribute_definitions,
        KeySchema=key_schema,
        ProvisionedThroughput=provisioned_throughput  # Comment this out if using DynamoDB Local
    )

    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='Cards')


def create_label_table():
    # Define attribute definitions and key schema for the Labels table
    attribute_definitions = [
        {
            'AttributeName': 'name',
            'AttributeType': 'S'  # 'S' for string type
        }
    ]

    key_schema = [
        {
            'AttributeName': 'name',
            'KeyType': 'HASH'  # 'HASH' for partition key
        }
    ]

    # Define provisioned throughput (optional for DynamoDB Local)
    provisioned_throughput = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

    # Create the DynamoDB table for Labels
    table = ddb.create_table(
        TableName="Labels",
        AttributeDefinitions=attribute_definitions,
        KeySchema=key_schema,
        ProvisionedThroughput=provisioned_throughput  # Comment this out if using DynamoDB Local
    )

    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='Labels')


def create_list_table():
    # Define attribute definitions and key schema for the Lists table
    attribute_definitions = [
        {
            'AttributeName': 'name',
            'AttributeType': 'S'  # 'S' for string type
        }
    ]

    key_schema = [
        {
            'AttributeName': 'name',
            'KeyType': 'HASH'  # 'HASH' for partition key
        }
    ]

    # Define provisioned throughput (optional for DynamoDB Local)
    provisioned_throughput = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

    # Create the DynamoDB table for Lists
    table = ddb.create_table(
        TableName="Lists",
        AttributeDefinitions=attribute_definitions,
        KeySchema=key_schema,
        ProvisionedThroughput=provisioned_throughput  # Comment this out if using DynamoDB Local
    )

    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='Lists')


def create_columns_for_list_table():
    lists = [
        List(name="To Do"),
        List(name="In Progress"),
        List(name="Done")
    ]
    [i.save() for i in lists]


region_name = "eu-west-1"
aws_access_key_id = "dummy"  # Dummy access key for local
aws_secret_access_key = "dummy"  # Dummy secret key for local
endpoint_url = "http://localhost:8000"

ddb = boto3.resource(
    'dynamodb',
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_secret_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

create_label_table()
create_list_table()
create_card_table()

