from app.services.dock_service import dock_token
from app.services.dynamo_service import DynamoService
from app.utils.constants import EMISSOR_INVOICE_KEY_DYNAMO, DATABASE_NAME
from app.utils.utils import token_is_expired

dynamo = DynamoService(DATABASE_NAME)


class NewToken(object):
    def __init__(self):
        self.token = None
        self.emissor = None

    def get_token(self, request_id, body):
        if self.token is None:

            if self.emissor is None:
                self.emissor = dynamo.find_emissor(EMISSOR_INVOICE_KEY_DYNAMO, body['cnpj_cedente'])

            if token_is_expired(self.emissor['token_time']['S']):
                self.token = dock_token(request_id, self.emissor['url_token']['S'], self.emissor['app_client']['S'], self.emissor['app_secret']['S'])
                dynamo.update_emissor(EMISSOR_INVOICE_KEY_DYNAMO, body['cnpj_cedente'], self.token)
            else:
                self.token = self.emissor['token']['S']

            return self.token, self.emissor
        else:
            if self.emissor is None:
                self.emissor = dynamo.find_emissor(EMISSOR_INVOICE_KEY_DYNAMO, body['cnpj_cedente'])

            return self.token, self.emissor
