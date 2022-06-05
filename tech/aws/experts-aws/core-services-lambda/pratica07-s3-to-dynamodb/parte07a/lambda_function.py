# Importando bibliotecas
import boto3
import logging
from utils.log import log_config
import json

# Instanciando objeto de logging
logger = logging.getLogger('lambda_logger')
logger = log_config(logger, flag_stream_handler=True)

# Definindo variáveis do projeto
CSV_SEP = ';'

# Definindo função handler
def lambda_handler(event, context):

    # Criando variáveis através do evento recebido como parâmetro
    logger.debug(f'Extraindo informações do evento de put no s3')
    try:
        put_event = event['Records'][0]['s3']
        bucket_name = put_event['bucket']['name']
        obj_key = put_event['object']['key']
        logger.info(f'Evento de inserção no s3 a ser tratado nesta função Lambda: {bucket_name}/{obj_key}')
    except Exception as e:
        logger.error(f'Erro ao extrair informações de evento na função. Exception: {e}')
        raise e
    
    # Instanciando client s3
    s3_client = boto3.client('s3')
    
    logger.debug(f'Lendo objeto {obj_key} e realizando a transformação em JSON')
    try:
        # Lendo dados brutos em CSV
        response = s3_client.get_object(Bucket=bucket_name, Key=obj_key)
        csv_data = response['Body'].read().decode('utf-8').replace('\r', '').split('\n')
        
        # Transformando CSV em JSON
        headers = csv_data[0].split(CSV_SEP)
        values = [line.split(CSV_SEP) for line in csv_data[1:]]
        json_data = [{h: v for h, v in zip(headers, line)} for line in values]
    except Exception as e:
        logger.error(f'Erro ao ler e transformar dados CSV em JSON. Exception: {e}')
        raise e
        
    logger.debug(f'Escrevendo arquivo JSON em folder específico do bucket')
    try:
        # Extraindo variáveis de saída do objeto
        obj_name = obj_key.split('/')[-1]
        output_obj_key = 'lambda/output_json/' + obj_name.split('.')[0] + '.json'
        
        # Executando método PUT do client s3
        r = s3_client.put_object(Bucket=bucket_name, Key=output_obj_key, Body=json.dumps(json_data))
        logger.info(f'Objeto {output_obj_key} escrito com sucesso no bucket {bucket_name}')
    except Exception as e:
        logger.error(f'Erro ao escrever arquivo JSON em bucket do s3. Exception: {e}')
        raise e
        
    # Invocando função Lambda de forma assíncrona
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:sa-east-1:596533897380:function:experts-aws-lambda-107b'    ,
        InvocationType='Event',
        Payload=json.dumps(json_data)
    )

    return {
        'status_code': 200,
        'body': json.dumps(json_data)
    }


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

event = {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "aws-experts-dx6sdjz2j7ro-sa-east-1",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::aws-experts-dx6sdjz2j7ro-sa-east-1"
        },
        "object": {
          "key": "lambda/input/rock_albuns.csv",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}

if __name__ == '__main__':
    lambda_handler(event, None)