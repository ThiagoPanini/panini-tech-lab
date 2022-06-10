# Importando bibliotecas
import boto3
import json
import logging
from utils.log import log_config
import os

# Inicializando logger
logger = logging.getLogger('lambda_logger')
logger = log_config(logger, flag_stream_handler=True)

# Definindo função handler
def lambda_handler(event, context):
    
    # Inicializando client boto3
    ec2_client = boto3.client('ec2')
    
    # Retornando todas as regiões AWS
    try:
        regions_info = ec2_client.describe_regions()['Regions']
        regions = [r['RegionName'] for r in regions_info]
    except Exception as e:
        logger.error(f'Erro ao listar regiões AWS. Exception: {e}')
        raise e
        
    # Iterando sobre as regiões
    logger.debug(f'Iterando sobre as {len(regions)} regiões AWS em busca de volumes EBS não vinculados')
    for region in regions:
        # Criando recurso ec2 na região do loop
        ec2 = boto3.resource('ec2', region_name=region)
        
        # Listando volumes não vinculados ('staus = disponível')
        volumes = ec2.volumes.filter(
            Filters=[{
                'Name': 'status',
                'Values': ['available']
            }]
        )

        # Iterando sobre volumes disponíveis (não vinculados)
        for volume in volumes:
            v = ec2.Volume(volume.id)
            try:
                logger.debug(f'Identificado volume EBS {v.id} de {v.size} GiB não vinculado')
                v.delete()
                logger.info(f'Volume EBS {v.id} deletado com sucesso')
            except Exception as e:
                logger.error(f'Erro ao deletar volume EBS {volume.id}. Exception: {e}')


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica06-elimina-ebs'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)