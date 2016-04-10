import boto3
import json
import sys

# Tutorial (more thorough): http://boto3.readthedocs.org/en/latest/guide/dynamodb.html

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")


# create a new table
"""
test_table = dynamodb.create_table(
    TableName='test-table',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'last_name',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

test_table.meta.client.get_waiter('table_exists').wait(TableName='test-table')
"""

# connect to existing tables
templates_table = dynamodb.Table('surgery-concierge-templates')
surgeries_table = dynamodb.Table('surgery-concierge-surgeries')
test_table = dynamodb.Table('test-table')


# add a new item
# note that if an item has the same key, this function will simply overwrite it
data = {'v1' : 'key1', 'v2' : 'key3'}
json_data = json.dumps(data)
test_table.put_item(
    Item={
        'username' : 'Tadas',
        'last_name' : 'A',
        'v' : json_data
    }
)

# updating item
data = {'v1' : 'key1', 'v2' : 'key2', 'v3' : 'key3'}
json_data = json.dumps(data)
test_table.update_item(
    Key={
        'username': 'Tadas',
        'last_name': 'A'
    },


    UpdateExpression='SET v = :val1',
    ExpressionAttributeValues={
        ':val1': json_data
    }
)

# get item
response = test_table.get_item(
    Key={
        'username': 'Tadas',
        'last_name': 'A'
    }
)
item = response['Item']
print item


#delete item
test_table.delete_item(
    Key={
        'username': 'Tadas',
        'last_name': 'A'
    }
)
