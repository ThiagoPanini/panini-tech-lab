# Importando bibliotecas
import json
from utils.log import log_config
import logging
import os

# Função para retornar os campos do schema
def get_schema(schema, key='fields'):
    names = [field['name'] for field in schema[key]]
    types = [field['type'] for field in schema[key]]
    
    return names, types

# Definindo função
def lambda_handler(event, context):
    
    # Instanciando e configurando objeto de log
    logger = logging.getLogger()
    logger = log_config(logger)
    
    logger.debug(f'Coletando parâmetros do Avro Schema')
    try:
        namespace = event['namespace']
        name = event['name']
    except Exception as e:
        logger.error(f'Erro ao coletar parâmetros. Exception: {e}')
        
    logger.debug(f'Coletando atributos do schema')
    try:
        fields, types = get_schema(schema=event)
        logger.info(f'A tabela {namespace}.{name} possui {len(fields)} campos')
    except Exception as e:
        logger.error(f'Erro ao coletar schema. Exception: {e}')
    
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps(','.join(fields))
    }


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica02-modulos-adicionais'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)