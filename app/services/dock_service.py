from http import HTTPStatus

import requests
from requests.auth import HTTPBasicAuth


def dock_token(request_id, url, app_client, app_secret):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    auth = HTTPBasicAuth(app_client, app_secret)
    try:
        response = requests.post(url, headers=header, auth=auth, timeout=10)
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            return data['access_token']
        else:
            raise
    except Exception as e:
        print('{}| Error while generating DOCK token: {}'.format(request_id, e.args))
        raise


def create_loc_invoice(request_id, emissor, token, body):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    try:
        payload = {
                "idAccount": int(emissor['id_account']['S']),
                "key": emissor['emissor_key']['S'],
                "locType": "COB",
                "idTx": body['idtx'],
                "payee": {
                    "zipCode": body['cep'],
                    "city":  body['cidade'],
                    "state": body['estado'],
                    "address": str(body['endereco'] + ', ' + body['numero'])
                }
        }
        response = requests.post(emissor['url_loc']['S'], headers=header, json=payload, timeout=10)
        if response.status_code == HTTPStatus.CREATED:
            return response.json()
        if response.status_code == HTTPStatus.CONFLICT:
            print('{}| generating again idtx {} because 409'.format(request_id,  body['idtx']))
            body['idtx'] = str('R' + body['idtx'][0:24:] + body['idtx'][24+1::])
            print('{}| generated new idtx {} because 409'.format(request_id, body['idtx']))
            return create_loc_invoice(request_id, emissor, token, body)
        else:
            raise
    except Exception as e:
        print('{}| Error while generating LOC INVOICE: {}'.format(request_id, e.args))
        raise
