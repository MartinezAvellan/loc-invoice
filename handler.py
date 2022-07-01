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
    eeeee = {}
    handler(eeeee, None)
