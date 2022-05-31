# Importando bibliotecas
import boto3
import json
import logging
from utils.log import log_config

# Inicializando logger
logger = logging.getLogger('lambda_logger')
logger = log_config(logger)

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
        exit()
        
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