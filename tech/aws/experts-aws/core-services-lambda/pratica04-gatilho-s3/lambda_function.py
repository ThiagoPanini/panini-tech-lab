# Importando bibliotecas
import boto3
import logging
from utils.log import log_config
import os
import json

# Criando e configurando logger
logger = logging.getLogger('lambda_logger')
logger = log_config(logger, flag_stream_handler=True)

# Definindo função handler
def lambda_handler(event, context):
    
    # Inicializando client s3 via boto3
    s3_client = boto3.client('s3')
    
    # Extraindo dados do objeto a partir do evento
    logger.debug(f'Extraindo informações do evento de put no s3')
    try:
        s3_info = event['Records'][0]['s3']
        bucket_name = s3_info['bucket']['name']
        input_obj_key = s3_info['object']['key']
        logger.info(f'Bucket: {bucket_name}. Objeto de entrada: {input_obj_key}')
    except Exception as e:
        logger.error(f'Erro ao extrair informações do evento. Exception: {e}')
        raise e
    
    # Realizando leitura do objeto
    logger.debug(f'Realizando leitura do objeto CSV de entrada inserido no s3')
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=input_obj_key)
        csv_data = response['Body'].read().decode('utf-8').replace('\r', '').split('\n')
        logger.info(f'Dados de entrada lidos com sucesso e transformados em lista do Python')
    except Exception as e:
        logger.error(f'Erro ao realizar a leitura do objeto. Exception: {e}')
        raise e
        
    # Transformando objeto csv em json
    logger.debug(f'Transformando arquivo original em objeto do tipo JSON')
    try:
        csv_sep = ';'
        headers = csv_data[0].split(csv_sep)
        values = [line.split(csv_sep) for line in csv_data[1:]]
        json_data = [{h: v for h, v in zip(headers, line)} for line in values]
        logger.info(f'Objeto JSON gerado com sucesso: {json_data}')
    except Exception as e:
        logger.error(f'Erro ao transformar conteúdo em objeto JSON. Exception: {e}')
        raise e
    
    # Escrevendo saída no s3
    logger.debug(f'Escrevendo objeto JSON no S3')
    try:
        obj_name = input_obj_key.split('/')[-1]
        output_obj_name = ''.join(obj_name.split('.')[:-1]) + '.json'
        output_obj_key = 'lambda/output/' + output_obj_name
        r = s3_client.put_object(Bucket=bucket_name, Key=output_obj_key, Body=json.dumps(json_data))
        logger.info(f'Arquivo {output_obj_key} escrito com sucesso em bucket {bucket_name}')
    except Exception as e:
        logger.error(f'Erro ao escrever dados no s3 (output_obj_key). Exception: {e}')
        raise e
    
    return {
        'statusCode': 200,
        'Body': json_data
    }


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica04-gatilho-s3'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)