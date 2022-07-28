from datetime import datetime
import json
import uuid

import boto3

from app.utils.constants import DATE_FORMAT


def get_request_id(event, context):
    try:
        if event and event['Records'][0]['messageAttributes']['request_id']['stringValue']:
            return uuid.UUID(event['Records'][0]['messageAttributes']['request_id']['stringValue']).hex
        elif context and context.aws_request_id:
            return context.aws_request_id
        else:
            return uuid.uuid1()
    except Exception:
        return uuid.uuid1()


def is_str_or_dict(message):
    if type(message) is str:
        return json.loads(message)
    elif type(message) is dict:
        return message


def send_sqs_message(request_id, file_name, sqs_name, message):
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=sqs_name)
        response = queue.send_message(MessageBody=message, MessageAttributes={
            'request_id': {
                'DataType': 'String',
                'StringValue': str(request_id)
            }
        })
        sqs_message = "Send to SQS [SQS_QRCODE_INVOICE] {}. HTTPStatusCode: {} - MessageId: {}".format(
            sqs_name,
            response.get('ResponseMetadata')["HTTPStatusCode"],
            response.get('MessageId')
        )
        print('{}|{}| result: {}'.format(request_id, file_name, sqs_message))
    except Exception as e:
        raise Exception('send_sqs_message({}, {}): {}'.format(sqs_name, message, e))


def token_time():
    now = datetime.now()
    return now.strftime(DATE_FORMAT)


def token_is_expired(token_time_date):
    start = datetime.strptime(token_time_date, DATE_FORMAT)
    end = datetime.strptime(token_time(), DATE_FORMAT)
    diff = end - start
    diff_in_minutes = int(diff.total_seconds() / 60)
    if diff_in_minutes <= 50:
        return False
    else:
        return True
