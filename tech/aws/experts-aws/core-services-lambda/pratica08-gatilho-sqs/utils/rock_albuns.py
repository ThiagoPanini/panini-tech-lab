"""
---------------------------------------------------
------------ SCRIPT: get_rock_albuns.py -----------
---------------------------------------------------
Script responsável por realizar a extração, via web
scrapping, de álbuns de rocks armazenados no site
dr.loudness-war.info. A utilização deste script se
faz presente para simular uma espécie de input de
diversos eventos (álbuns de rock em formato json)
para serviços da AWS (Lambda e SQS)

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Logging e variáveis do projeto
2. Web Scrapping de álbuns
    2.1 Definindo função de extração
    2.2 Executando código no main
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 10/06/2022


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Bibliotecas padrão
from distutils.sysconfig import PREFIX
import os
import json
import boto3
from time import sleep

# Leitura de argumentos de sript
import argparse

# Requisições e parsing de html
import requests
from bs4 import BeautifulSoup

# Logging
import logging
from log import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
        1.2 Parsing de argumentos do script
---------------------------------------------------
"""

# Criando parser
parser = argparse.ArgumentParser()

# Valores default para argumentos
DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rock_albuns_scrapping_pg1-6000.json')

# Adicionando argumentos
parser.add_argument('--mode', '-m', required=False, default='check', type=str) # procurar como restringir argumentos
parser.add_argument('--page-start', '-s', required=False, default=1, type=int)
parser.add_argument('--page-end', '-e', required=False, default=20, type=int)                    
parser.add_argument('--log-step', '-l', required=False, default=5, type=int)
parser.add_argument('--file', '-f', required=False,  default=DEFAULT_FILE, type=str)
parser.add_argument('--destination', '-d', required=False, default='s3', type=str)
parser.add_argument('--num-objects', '-n', required=False, default=10, type=int)
parser.add_argument('--bucket', '-b', required=False, type=str)
parser.add_argument('--prefix', '-p', required=False, default='', type=str)
parser.add_argument('--queue-name', '-q', required=False, default='rock-albuns-messages', type=str)
parser.add_argument('--table', '-t', required=False, default='rock-albuns', type=str)

args = parser.parse_args()


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
  1.2 Parâmetros do scripte configuração de log
---------------------------------------------------
"""

# Definindo variáveis do projeto
BASE_URL = 'https://dr.loudness-war.info/album/list/'
HEADERS = ['banda', 'album', 'ano']

# Extraindo parâmetros de execução do script
MODE = args.mode
PAGE_START = args.page_start
PAGE_END = args.page_end
LOG_STEP = args.log_step
LOCAL_FILE = args.file
N_OBJS = args.num_objects
DESTINATION = args.destination
S3_BUCKET = args.bucket
S3_PREFIX = args.prefix
SQS_QUEUE = args.queue_name
DYNAMODB_TABLE = args.table

# Validando argumentos de acordo com o cenário
S3_BUCKET = 'aws-experts-dx6sdjz2j7ro-sa-east-1' if S3_BUCKET is None else S3_BUCKET

# Configurando objeto logger
logger = logging.getLogger(__file__)
logger = log_config(logger, flag_stream_handler=True)


"""
---------------------------------------------------
---------- 2. CLASSES DE PROCESSAMENTO ------------
        2.1 Requisição de álbuns de rock
---------------------------------------------------
"""

class ManageRockAlbuns():

    def __init__(self, log_step=5):
        self.log_step = log_step
        pass
    
    def save_local_data(self, data, file_path, file_name):
        """
        """

        # Criando diretório caso existente
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        
        # Salvando arquivo em formato json aninhado (lista de dicts)
        data_path = os.path.join(file_path, file_name)
        try:
            with open(data_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
            logger.info(f'Arquivo salvo com sucesso em {data_path}')
        except Exception as e:
            logger.error(f'Erro ao salvar arquivo em {data_path}. Exception: {e}')
    
    
    def load_local_data(self, file_path, file_name):
        """
        """

        # Realizando leitura do arquivo
        try:
            data_path = os.path.join(file_path, file_name)
            with open(data_path, 'rb') as f:
                rock_albuns = json.loads(f.read().decode('utf-8'))
            logger.info(f'Arquivo {file_name} lido com sucesso contendo {len(rock_albuns)} objetos')
        except Exception as e:
            logger.error(f'Erro ao realizar a leitura do arquivo {file_name} do caminho {file_path}. Exception: {e}')
            raise e
        
        return rock_albuns


    def web_scrapping(self, page_start, page_end, log_step, 
                      base_url=BASE_URL, **kwargs):
        """
        """

        # Informações sobre o processo
        logger.debug(f'Iniciando processo de webscrapping de álbuns de rock no site {base_url}')
        logger.info(f'Extração da página {page_start} até a página {page_end} com mensagens de log a cada {self.log_step} páginas')

        # Criando variáveis de controle
        rock_albuns = []
        request_error_count = 0
        request_error_limit = kwargs['request_error_limit'] if 'request_error_limite' in kwargs else 10
        request_wait = kwargs['request_wait'] if 'request_wait' in kwargs else 2

        # Validando diretório de salvamento do processo
        file_path = kwargs['file_path'] if 'file_path' in kwargs else os.path.dirname(os.path.abspath(__file__))

        # Iterando sobre as páginas do site
        for page in range(page_start, page_end + 1):
            # Gerando url de requisição e flag de log
            request_url = base_url + str(page)
            log_condition = (self.log_step > 0) and (page % self.log_step == 0)

            # Coletando conteúdo html e transformando via BeautifulSoup
            logger.debug(f'Realizando requisição para a página {page}. Objetos extraídos até o momento: {len(rock_albuns)}') if log_condition else None
            try:
                html_content = requests.get(url=request_url)
                soup = BeautifulSoup(html_content.text, features='html.parser')
            except Exception as e:
                logger.warning(f'Erro ao requisitar a url {request_url}. Exception: {e}')
                request_error_count += 1
                if request_error_count >= request_error_limit:
                    logger.error(f'Quantidade limite de error atingida ({request_error_limit}). Subindo última exceção e encerrando programa')
                    raise e
                else:
                    sleep(request_wait)
                    pass

            # Extraindo tabelas do site
            site_tables = soup.find_all('table')

            # Extraindo conteúdo das tabelas
            tr_data = site_tables[0].find_all('tr')
            td_data = [tr.find_all('td') for tr in tr_data]

            # Iterando sobre cada elemento e transformando em json aninhado
            for row in td_data[1:]:
                content = [c.text.strip() for c in row][:3] # Coleta apenas das informações de banda, álbum e ano
                json_content = {h: v for h, v in zip(HEADERS, content)}
                rock_albuns.append(json_content)

        # Finalizando etapa de extração
        file_name = f'rock_albuns_scrapping_pg{page_start}-{page_end}.json'
        self.save_local_data(data=rock_albuns, file_path=file_path, file_name=file_name)


    def rock_data_to_s3(self, bucket, prefix, nested_json, n_objs):
        """
        """

        # Transformando json aninhado (caso necessário)
        nested_json = [nested_json] if type(nested_json) != list else nested_json
        
        # Comunicando o total de iterações no laço
        total_objs = len(nested_json)
        if n_objs == -1:
            logger.debug(f'Realizando o PUT para todos os {total_objs} objetos JSON do arquivo consolidado com mensagens de log a cada {self.log_step} chamadas')
        else:
            logger.debug(f'Iterando sobre {n_objs} dos {total_objs} objetos JSON do arquivo consolidado com mensagens de log a cada {self.log_step} chamadas')

        # Iterando sobre cada registro e escrevendo no s3
        s3_client = boto3.client('s3')
        for album in nested_json[:n_objs]:
            # Condição de logging
            idx = nested_json.index(album) + 1
            log_condition = (self.log_step > 0) and (idx % self.log_step == 0)
            idx_name = str(idx).zfill(len(str(total_objs)))

            # Inserindo objeto no bucket
            logger.debug(f'Realizando o PUT para o objeto {idx} do JSON aninhado') if log_condition else None
            file_name = f'rock_album_{idx_name}.json'
            obj_key = prefix + file_name
            try:
                response = s3_client.put_object(Bucket=bucket, Key=obj_key, Body=json.dumps(album))        
            except Exception as e:
                logger.warning(f'Erro ao realizar o PUT para o objeto {obj_key}. Exception: {e}')
                raise e

        logger.info(f'Processo de inserção no s3 finalizado com sucesso')


    def rock_data_to_sqs(self):
        """
        """

        # Instanciando client do sqs e coletando url da fila
        sqs = boto3.client('sqs')
        response = sqs.get_queue_url(QueueName=SQS_QUEUE)
        queue_url = response['QueueUrl']

        print(queue_url)


    def count_dynamodb_items(self, table):
        """
        """

        # Validando quantidade de itens no dynamodb
        logger.debug(f'Validando itens presentes na tabela {table} do DynamoDB')
        sleep(5)
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.scan(TableName=table, Select='COUNT')
        total_itens = response['Count']

        # Comunicando
        logger.info(f'A tabela {table} do DynamoDB possui {total_itens} itens')
        
        return total_itens

       

"""
Ideias:
    - [x] Método para webscrapping
    - [x] Método para salvar dados localmente
    - [x] Método para carregar dados localmente
    - [x] Método para inserir dados no s3
    - [ ] Método para inserir dados no sqs
    - [ ] Método para gerenciar put dos dados (s3 ou sqs)
    - [x] Método para validar dados no dynamodb

    - Script para escolher caminhos conforme inputs

    1. Webscrapping -> Salvar dados
    2. Leitura dados -> Carga no s3/sqs > Valida dynamodb

"""

"""
---------------------------------------------------
-------------- 3. EXECUÇÃO DO SCRIPT --------------
        3.1 Requisitanto e 
---------------------------------------------------
""" 

if __name__ == '__main__':
    """
    O módulo main deste script é responsável por aplicar
    e gerenciar toda a lógica de execução baseada nas
    diferentes possibilidades mapeadas pelo usuário. 
    Contendo três principais modos (get, put e check),
    os métodos da classe ManageRockAlbuns são executados
    de acordo com os inputs fornecidos pelo usuário de
    modo a proporcionar os outputs solicitados. 
    Em detalhes, temos:

    --mode = "get"
        Este modo pode ser executado quando há a intenção
        de aplicar o processo de webscrapping para 
        obtenção de dados relacionados a álbuns de rock
        direto da fonte. Este modo possui configurações
        próprias que, quando parametrizadas, agem de 
        modo a resultar em um arquivo JSON com o conteúdo
        solicitado. 
        
        * Parâmetros necessários neste modo:
        --page-start, --page-end e --log-step
        
        * Exemplo de execução de script:
        python3 rock_albuns.py --mode "get" --page-start 1 --page-end 10 --log-step 5
    
    ------------------------------------------------------

    --mode = "put"
        Este modo considera a leitura de um arquivo JSON
        salvo localmente (output do modo "get") para
        envio iterativo à um bucket s3 ou à uma fila 
        do sqs. 
        
        * Parâmetros necessários neste modo:
        --file, --destination, --num-objects, --bucket
        --prefix e --queue

        * Exemplos de execução de script:
        python3 rock_albuns.py --mode "put" --file "./rock_albuns_scrapping_pg1-6000.json" --destination "s3" --bucket "aws-experts-dx6sdjz2j7ro-sa-east-1" --prefix "lambda/output/" --num-objects 10 --log-step 1
        python3 rock_albuns.py --mode "put" --file "./rock_albuns_scrapping_pg1-6000.json" --destination "sqs" --queue-name "rock-albuns-messages"

    ------------------------------------------------------

    --mode = "check"
        Por fim, como a lógica final envolve a inserção
        de itens no dynamodb, este modo tem como objetivo
        a realização da contagem de itens na tabela alvo.
        
        * Parâmetros necessários neste modo:
        --table

        * Exemplo de execução de script
        python3 rock_albuns.py --mode "check" --table "rock-albuns"
    """

    # Inicializando objeto da classe
    rock = ManageRockAlbuns(log_step=LOG_STEP)
    
    # Validando modos
    if MODE == 'get':
        rock_albuns = rock.web_scrapping(
            page_end=PAGE_END,
            page_start=PAGE_START,
            log_step=LOG_STEP
        )

    elif MODE == 'put':
        # Coletando arquivo json aninhado
        rock_albuns = rock.load_local_data(
            file_path=os.path.dirname(LOCAL_FILE),
            file_name=os.path.basename(LOCAL_FILE)
        )

        # Iterando sobre seu conteúdo
        if DESTINATION == 's3':
            rock.rock_data_to_s3(
                bucket=S3_BUCKET,
                prefix=S3_PREFIX,
                nested_json=rock_albuns,
                n_objs=N_OBJS
            )
        elif DESTINATION == 'sqs':
            pass

    elif MODE == 'check':
        # Retornando itens inseridos no DynamoDB
        table_items = rock.count_dynamodb_items(
            table=DYNAMODB_TABLE
        )
