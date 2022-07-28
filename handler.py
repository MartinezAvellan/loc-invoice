import json

from app.services.dock_service import create_loc_invoice
from app.services.token_service import NewToken
from app.utils.constants import SQS_QRCODE_INVOICE
from app.utils.utils import get_request_id, is_str_or_dict, send_sqs_message

new_token = NewToken()


def handler(event, context):
    request_id = get_request_id(event, context)
    message = is_str_or_dict(event)
    try:
        body = is_str_or_dict(message['Records'][0]['body'])
        token, emissor = new_token.get_token(request_id, body)
        body['loc'] = create_loc_invoice(request_id, emissor, token, body)
        send_sqs_message(request_id, body['file_name'], SQS_QRCODE_INVOICE, json.dumps(body))
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    eeeee = {'Records': [
        {'messageId': 'c03477e0-ca4e-4aa6-9a4e-92fde65338ed',
         'receiptHandle': 'AQEBwKqicQcoNIBxOvSZP0gPpDhStbEBQ==',
         'body': '{"file_name": "EcosyInstdePagamentoSA29042022.txt", '
                 '"bucket_name": "read-invoice", '
                 '"nome_cedente": "Banco EC S.A.", '
                 '"cnpj_cedente": "33264668000103", '
                 '"data_geracao": "29042022", '
                 '"nome_cliente": "FABILANIA SANDES", '
                 '"cpf_cnpj": "99958773414", '
                 '"conta": "682680", '
                 '"cep": "71505235", '
                 '"cidade": "Barueri", '
                 '"estado": "DF", '
                 '"endereco": "Av. Tambore", '
                 '"numero": "267", "complemento": "Complemento", '
                 '"valor_fatura": "00000000204655", '
                 '"idtx": "QT332646680001032904202200000000001"}',
         'attributes': {
             'ApproximateReceiveCount': '1',
             'SentTimestamp': '1656769309277',
             'SenderId': 'AIDAYT3YFZIESZ6X7UGX6',
             'ApproximateFirstReceiveTimestamp': '1656769309287'
         }, 'messageAttributes': {
            'request_id': {
                'stringValue': 'b2afa9b2-fa0c-11ec-b2b5-50e0853f09c7',
                'stringListValues': [],
                'binaryListValues': [],
                'dataType': 'String'}},
         'md5OfMessageAttributes': 'ce883ec81ef758f8dab223045c034f4d',
         'md5OfBody': '4603b0f2f1c3bda4cc035441cb2b5249',
         'eventSource':
             'aws:sqs',
         'eventSourceARN': 'arn:aws:sqs:sa-east-1:592420653577:loc-invoice',
         'awsRegion': 'sa-east-1'}
    ]}

    handler(eeeee, None)
