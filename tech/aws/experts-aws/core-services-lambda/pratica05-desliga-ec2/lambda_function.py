# Importando bibliotecas
import boto3
import json
import logging
from utils.log import log_config

# Configurando log
logger = logging.getLogger('lambda_logger')
logger = log_config(logger)

# Definindo função handler
def lambda_handler(event, context):
    
    # Inicializando client ec2
    ec2_client = boto3.client('ec2')
    
    # Listando todas as regiões AWS da conta
    logger.debug(f'Listando todas as regiões de uma conta AWS com o client EC2')
    try:
        regions_info = ec2_client.describe_regions()['Regions']
        regions = [r['RegionName'] for r in regions_info]
        logger.info(f'Foram obtidas {len(regions)} regiões no processo de listagem')
    except Exception as e:
        logger.error(f'Erro ao listar regiões. Exception: {e}')
        exit()
        
    # Iterando sobre cada região da AWS e inicializando um recurso específico para cada
    logger.debug(f'Iniciando processo de interação para encerramento de instâncias')
    stopped_instances = []
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        
        # Coletando instâncias EC2 na região com status running
        instances = ec2.instances.filter(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running']        
            }]
        )
        
        # Validando a existência de instâncias em execução
        for instance in instances:
            try:
                instance.stop()
                stopped_instances.append(instance.id)
                logger.info(f'Instância {instance.id} encerrada na região {region}')
            except Exception as e:
                logger.error(f'Erro ao encerrar instância {instance.id} na região {region}. Exception: {e}')
                
    # Verificando ações realizadas
    if len(stopped_instances) > 0:
        logger.info(f'Foram desligadas {len(stopped_instances)} instâncias EC2 no processo')
    else:
        logger.info('Nenhuma instância EC2 em execução no momento. Função finalizada.')
    
    return {
        'statusCode': 200,
        'body': stopped_instances
    }