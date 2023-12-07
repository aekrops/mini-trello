import boto3


def create_card_table():
    # Initialize a boto3 DynamoDB resource
    dynamodb = boto3.resource('dynamodb',
                              region_name='dummy-region',  # Replace with any string
                              aws_access_key_id='dummy',  # Dummy access key for local
                              aws_secret_access_key='dummy',  # Dummy secret key for local
                              endpoint_url='http://localhost:8000')  # URL for DynamoDB Local

    # Create the table
    table = dynamodb.create_table(
        TableName='Cards',
        KeySchema=[
            {
                'AttributeName': 'card_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'card_id',
                'AttributeType': 'S'  # String type
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName='Cards')

    print("Table 'Cards' created successfully.")


if __name__ == '__main__':
    create_card_table()
