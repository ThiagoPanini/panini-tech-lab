# Importando bibliotecas
import boto3
import logging
import os
import json

# Definindo variáveis de uso
LOG_FORMAT = '%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s'
ALBUM_YEAR_FILTER = 1990

# Definindo função para configuração de objeto logger
def log_config(logger, level=logging.DEBUG, log_format=LOG_FORMAT):

    # Configurando level e formatação do objeto
    logger.setLevel(level)
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    return logger

# Definindo função handler
def lambda_handler(event, context):
    
    # Configurando log
    logger = logging.getLogger('lambda_logger')
    logger = log_config(logger)
    
    logger.debug(f'Inicializando client s3 via boto3')
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
    
    # Realizando leitura do objeto
    logger.debug(f'Realizando leitura do objeto de entrada inserido no s3')
    try:
        r = s3_client.get_object(Bucket=bucket_name, Key=input_obj_key)
        input_data = r['Body'].read().decode()
        logger.info(f'Dados de entrada lidos com sucesso')
    except Exception as e:
        logger.error(f'Erro ao realizar a leitura do objeto. Exception: {e}')
    
    # Preparando arquivo de entrada em formato tratável
    logger.debug(f'Preparando arquivo de entrada')
    try:
        input_list = input_data.split('\n')
        input_list_prep = [e.replace('\r', '').split(';') for e in input_list]
        logger.info(f'Arquivo de texto transformado em lista com {len(input_list_prep)} elementos')
    except Exception as e:
        logger.error(f'Erro ao preparar arquivo de entrada. Exception: {e}')
        
    # Filtrando apenas álbuns
    logger.debug(f'Iterando sobre registros do arquivo e filtrando albuns lançados após {ALBUM_YEAR_FILTER}')
    output_list = []
    try:
        for line in input_list_prep[1:]:
            if int(line[2]) >= ALBUM_YEAR_FILTER:
                output_list.append(line)
        logger.info(f'Registros filtrados com sucesso. Restaram {len(output_list)} elementos na lista')
    except Exception as e:
        logger.error(f'Erro ao filtrar registros. Exception: {e}')

    # Realizando preparação final para adição de cabeçalho e transformação de lista em texto
    logger.debug(f'Transformando lista final em arquivo csv a ser escrito no s3')
    try:
        output_data_str = ''
        header = input_list_prep[0]
        output_list.insert(0, header)
        for line in output_list:
            output_data_str += ';'.join(line)
            output_data_str += '\n'
        logger.info(f'Arquivo final preparado com sucesso e pronto para ser escrito no s3')
    except Exception as e:
        logger.error(f'Erro ao aplicar transformações em dados filtrados. Exception: {e}')
    
    # Escrevendo saída no s3
    logger.debug(f'Escrevendo dados filtrados no S3')
    try:
        obj_name = input_obj_key.split('/')[-1]
        output_obj_name = ''.join(obj_name.split('.')[:-1]) + '_prep.csv'
        output_obj_key = 'lambda/output/' + output_obj_name
        output_data = output_data_str.encode(encoding='UTF-8')
        r = s3_client.put_object(Bucket=bucket_name, Key=output_obj_key, Body=output_data)
    except Exception as e:
        logger.error(f'Erro ao escrever dados no s3 (output_obj_key). Exception: {e}')
    
    return {
        'statusCode': 200,
        'Body': json.dumps(output_data_str)
    }