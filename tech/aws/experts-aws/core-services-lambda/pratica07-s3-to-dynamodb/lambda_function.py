# Importando bibliotecas
import boto3
import logging
from utils.log import log_config
import json
import os

# Instanciando objeto de logging
logger = logging.getLogger('lambda_logger')
logger = log_config(logger, flag_stream_handler=True)

# Definindo variáveis para configuração da tabela no DynamoDB (em caso de criação)
TABLE_NAME = 'rock-albuns'
PARTITION_KEY = 'banda'
SORT_KEY = 'album'
KEY_SCHEMA = [
    {
        'AttributeName': PARTITION_KEY,
        'KeyType': 'HASH'
    },
    {
        'AttributeName': SORT_KEY,
        'KeyType': 'RANGE'
    }
]
ATTRIBUTE_DEF = [
    {
        'AttributeName': PARTITION_KEY,
        'AttributeType': 'S'
    },
    {
        'AttributeName': SORT_KEY,
        'AttributeType': 'S'
    }
]
PROVISIONED_THROUGHPUT = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

# Definindo função handler
def lambda_handler(event, context):

    # Criando variáveis através do evento recebido como parâmetro
    logger.debug(f'Extraindo informações do evento de put no s3')
    try:
        s3_info = event['Records'][0]['s3']
        bucket_name = s3_info['bucket']['name']
        obj_key = s3_info['object']['key']
        logger.info(f'Evento de inserção no s3 a ser tratado nesta função Lambda: {bucket_name}/{obj_key}')
    except Exception as e:
        logger.error(f'Erro ao extrair informações de evento na função. Exception: {e}')
        raise e
    
    # Instanciando client s3
    s3_client = boto3.client('s3')

    logger.debug(f'Lendo objeto {obj_key}')
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=obj_key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        logger.error(f'Erro ao realizar a leitura de objeto JSON. Exception: {e}')
        raise e

    # Listando tabelas do dynamodb
    dynamodb = boto3.resource('dynamodb')
    logger.debug(f'Listando tabelas existentes no DynamoDB')
    try:
        tables = [table.name for table in dynamodb.tables.all()]
    except Exception as e:
        logger.error(f'Erro ao listar tabelas do DynamoDB via boto3 client. Exception: {e}')
        raise e

    # Validando existência da tabela rock-albuns e criando
    if TABLE_NAME not in tables:
        logger.debug(f'Tabela {TABLE_NAME} não existente no DynamoDB. Iniciando processo de criação')
        try:
            table = dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=KEY_SCHEMA,
                AttributeDefinitions=ATTRIBUTE_DEF,
                ProvisionedThroughput=PROVISIONED_THROUGHPUT
            )
            logger.debug(f'Status da tabela {table.name}: {table.table_status}')
            logger.debug(f'Aguardando a completude da criação da tabela {table.name}')
            table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
            table = dynamodb.Table(TABLE_NAME)
            logger.info(f'Status atualizado da tabela {table.name}: {table.table_status}')
        except Exception as e:
            logger.error(f'Erro ao criar tabela {TABLE_NAME} no DynamoDB. Exception: {e}')
            raise e
    else:
        # Tabela já existe no dynamodb
        table = dynamodb.Table(TABLE_NAME)
        logger.info(f'Tabela {TABLE_NAME} existe e será considerada como alvo das inserções de itens')
    
    # Criando variáveis de controle para processo de ingestão
    error_count = 0
    error_threshold = 2
    flag_threshold = False
    put_item_verbose = 1
    error_items = []
    status_code = 200

    # Iterando sobre elementos do JSON aninhado
    for line in json_data:
        try:
            # Inserindo registro na tabela do DynamoDB
            response = table.put_item(Item=line)
            if put_item_verbose > 0:
                logger.info(f'Registro {line} inserido com sucesso na tabela')
        
        except Exception as e:
            # Inserindo registro com falha em lista para posterior debugging
            error_count += 1
            error_items.append(line)

            # Comunicando erro ao usuário (se aplicável)
            if put_item_verbose > 0:
                logger.warning(f'Erro ao inserir registro {line} na tabela {TABLE_NAME} do DynamoDB. Exception: {e}')
            
            # Contabilizando erro e validando limite de erros estabelecido 
            if error_count >= error_threshold:
                logger.error(f'Quantidade máxima de erros alcançada ({error_count}). Encerrando processo de escrita de itens')
                flag_threshold = True
                break
            else:
                # Caso o limite não tenha sido atingido, passar para próximo item do laço
                pass
    
    # Validando resultado
    if error_count == 0 and not flag_threshold:
        logger.info(f'Todos os {len(json_data)} registros foram inseridos com sucesso na tabela do DynamoDB')
        status_code = 200
    elif error_count > 0 and flag_threshold:
        pass
    else:
        logger.warning(f'Foram inseridos {len(json_data) - error_count} registros com sucesso e {error_count} com falhas')
        status_code = 417

    return {
        'status_code': status_code,
        'body': json_data
    }
    

"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica07-s3-to-dynamodb'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)