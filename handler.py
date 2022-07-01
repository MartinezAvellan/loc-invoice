import json


def handler(event, context):
    print("event: ", str(event))
    print("context: ", str(context))

    try:
        if type(event) is str:
            message = json.loads(event)
        elif type(event) is dict:
            message = event
    except Exception as e:
        print(e)


if __name__ == '__main__':
    eeeee = {'Records': [
        {'messageId': 'cf0e1c23-d502-49b0-9925-041b6713a91c',
         'receiptHandle': 'AQExsFoQ6Xuorg==',
         'body': '{\n\t"name":"call loc invoice",\n\t"sqs":"sqs trigger",\n\t"teste":"message 1"\n}',
         'attributes': {'ApproximateReceiveCount': '1',
                        'SentTimestamp': '1656683229596',
                        'SenderId': 'AIDAYT3YFZIESZ6X7UGX6',
                        'ApproximateFirstReceiveTimestamp':
                            '1656683229603'},
         'messageAttributes': {},
         'md5OfBody': '45e8efe9436699a64fdb011c8c9c48e3',
         'eventSource': 'aws:sqs',
         'eventSourceARN': 'arn:aws:sqs:sa-east-1:592420653577:loc-invoice',
         'awsRegion': 'sa-east-1'}
    ]}

    handler(eeeee, None)
