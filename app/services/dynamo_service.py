import boto3
from boto3.dynamodb.conditions import Attr

from app.utils.constants import REGION
from app.utils.utils import token_time


class DynamoService(object):
    def __init__(self, table):
        self.dynamodb_client = boto3.client('dynamodb', region_name=REGION)
        self.table = table

    def find_emissor(self, key, value):
        response = self.dynamodb_client.get_item(
            TableName=self.table,
            Key={
                key: {'S': value}
            })
        return response['Item']

    def update_emissor(self, key, value, token):
        response = self.dynamodb_client.update_item(
            TableName=self.table,
            Key={
                key: {'S': value}
            },
            UpdateExpression='SET #token = :token, #token_time= :token_time',
            ExpressionAttributeNames={
                "#token": "token",
                "#token_time": "token_time"
            },
            ExpressionAttributeValues={
                ':token': {'S': token},
                ':token_time': {'S': token_time()}
            },
            ReturnValues='UPDATED_NEW'
        )
