# Importando bibliotecas=
import boto3
import json
import logging
from utils.log import log_config
import sys
from decimal import Decimal

# Definindo variáveis de arquivo json no s3
BUCKET_NAME = 'aws-experts-dx6sdjz2j7ro-sa-east-1'
OBJ_KEY = 'data/iot-devices/iot_devices.json'
JSON_CHUNK_SIZE = 10000

# Definindo variáveis de tabela do dynamodb
TABLE_NAME = 'iot-devices'
DYNAMO_CREATE_DICT = {
    'partition_key': {
        'name': 'device_id',
        'type': 'HASH',
        'attr_type': 'N'
    },
    'sort_key': {
        'name': 'timestamp',
        'type': 'RANGE',
        'attr_type': 'N'
    }
}
#KEY_SCHEMA = {'AttributeName': key_dict['name'], 'KeyType': key_dict['type'] for key_dict in DYNAMO_CREATE_DICT}

# Configurando logger
logger = logging.getLogger('lambda_function')
logger = log_config(logger, flag_stream_handler=True)

# Função para leitura de arquivo JSON
def read_iot_json_data(client, bucket_name, obj_key):
    # Lendo arquivo json do S3
    logger.debug(f'Lendo objeto do s3: {bucket_name}/{obj_key}')
    try:
        # Conteúdo bruto decodificado (formato string)
        response = client.get_object(Bucket=bucket_name, Key=obj_key)
        raw_content = response['Body'].read().decode('utf-8')

        # Transformação de jsons aninhados em lista e leitura individual
        nested_json = raw_content.split('\n')[:JSON_CHUNK_SIZE]
        json_data = [json.loads(json.dumps(line), parse_float=Decimal) for line in nested_json]
        logger.info(f'Arquivo json lido com sucesso. Quantidade total de elementos: {len(json_data)}. Tamanho total em bytes: {sys.getsizeof(json_data)}')
    except Exception as e:
        logger.error(f'Erro ao ler arquivo json. Exception: {e}')
        raise e

    return json_data or None

# Definindo função handler
def lambda_handler(event, context):

    # Criando client do s3 e objeto python para o bucket
    s3_client = boto3.client('s3')
    json_data = read_iot_json_data(
        client=s3_client, 
        bucket_name=BUCKET_NAME, 
        obj_key=OBJ_KEY
    )
    
    # Listando tabelas do dynamodb
    dynamodb = boto3.resource('dynamodb')
    tables = [table.name for table in dynamodb.tables.all()]
    
    # Criando tabela do dynamo, caso não exista
    if TABLE_NAME not in tables:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'device_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'device_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        print(f'Table status: {table.table_status}')
        print(f'Waiting for {table.name} to complete creating...')
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
        print(f'Table status: {dynamodb.Table(TABLE_NAME).table_status}')
        
    # Inserindo elementos na tabela
    sample = json_data[10]
    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(Item=sample)
    print(table)
    print(response)
    
    
# Executando função
if __name__ == '__main__':
    lambda_handler(None, None)