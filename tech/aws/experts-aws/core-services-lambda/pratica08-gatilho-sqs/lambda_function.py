# Importando bibliotecas
import boto3
import logging
from utils.log import log_config
import json
import os

# Instanciando objeto de logging
logger = logging.getLogger('lambda_logger')
logger = log_config(logger, flag_stream_handler=True)

# Retornando variáveis de ambiente da função
try:
    QUEUE_NAME = os.environ['QUEUE_NAME']
    MAX_QUEUE_MSGS = os.environ['MAX_QUEUE_MSGS']
    DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
except KeyError as ke:
    # Definindo padrões para auxiliar testes locais
    QUEUE_NAME = 'rock-albuns-messages'
    MAX_QUEUE_MSGS = 10
    DYNAMODB_TABLE = 'rock-albuns'

# Instanciando recursos via boto3
sqs = boto3.resource('sqs')
dynamodb = boto3.resource('dynamodb')

# Definindo função handler
def lambda_handler(event, context):

    # Coletando objeto de fila via recurso sqs
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    messages = event['Records']
    logger.debug(f'Mensagens coletadas por evento: {len(messages)}')
    
    # Iterando sobre chunck de mensagens
    for message in messages:
        # Coletando parâmetros do evento
        message_id = message['messageId']
        message_body = message['body']
        
        # Escrevendo no dynamodb
        table = dynamodb.Table(DYNAMODB_TABLE)
        try:
            response = table.put_item(Item=json.loads(message_body))
            logger.info(f'Mensagem {message_id} - {message_body} inserida com sucesso na tabela {DYNAMODB_TABLE} do DynamoDB')   
        except Exception as e:
            logger.error(f'Erro ao inserir mensagem {message_body} na tabela {DYNAMODB_TABLE} do DynamoDB. Exception: {e}')
            raise e


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica08-gatilho-sqs'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)