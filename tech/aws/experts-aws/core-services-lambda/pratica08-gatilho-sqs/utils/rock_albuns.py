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

# Adicionando argumentos
parser.add_argument('--mode', '-m', required=False, default='get', type=str) # procurar como restringir argumentos
parser.add_argument('--page-start', '-s', required=False, default=1, type=int)
parser.add_argument('--page-end', '-e', required=False, default=20, type=int)                    
parser.add_argument('--log-step', '-l', required=False, default=5, type=int)

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

    def __init__(self):
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
            logger.info(f'Arquivo {file_name} salvo com sucesso em {file_path}')
        except Exception as e:
            logger.error(f'Erro ao salvar arquivo em {data_path}. Exception: {e}')
    
    
    def load_local_data(self, data, file_path, file_name):
        """
        """

        # Realizando leitura do arquivo
        try:
            data_path = os.path.join(file_path, file_name)
            with open(data_path, 'rb') as f:
                rock_albuns = json.loads(f.read().decode('utf-8'))
            logger.info(f'Arquivo {file_name} lido com sucesso')
        except Exception as e:
            logger.error(f'Erro ao realizar a leitura do arquivo {file_name} do caminho {file_path}. Exception: {e}')

        return rock_albuns


    def web_scrapping(self, page_start, page_end, log_step, 
                      base_url=BASE_URL, **kwargs):
        """
        """

        # Informações sobre o processo
        logger.debug(f'Iniciando processo de webscrapping de álbuns de rock no site {base_url}')
        logger.info(f'Extração da página {page_start} até a página {page_end} com mensagens de log a cada {log_step} páginas')

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
            log_condition = (log_step > 0) and (page % log_step == 0)

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


    def rock_data_to_s3(self, bucket, key, body, n_objs):
        """
        """

        # Transformando json aninhado (caso necessário)
        body = [body] if type(body) != list else body
        
        # Comunicando o total de iterações no laço
        total_objs = len(nested_json)
        if NUM_OBJS == -1:
            logger.debug(f'Realizando o PUT para todos os {total_objs} objetos JSON do arquivo consolidado')
        else:
            logger.debug(f'Iterando sobre {NUM_OBJS} dos {total_objs} objetos JSON do arquivo consolidado')

        # Iterando sobre cada registro e escrevendo no s3
        s3_client = boto3.client('s3')
        for album in nested_json[:NUM_OBJS]:
            # Condição de logging
            idx = nested_json.index(album) + 1
            log_condition = (LOG_STEP > 0) and (idx % LOG_STEP == 0)
            idx_name = str(idx).zfill(len(str(total_objs)))

            # Comunicando
            logger.debug(f'Realizando o PUT para o objeto {idx} do JSON aninhado') if log_condition else None
            
            # Inserindo objeto no bucket
            obj_key = f'{PREFIX}rock_album_{idx_name}.json'
            try:
                response = s3_client.put_object(Bucket=BUCKET, Key=obj_key, Body=json.dumps(album))        
            except Exception as e:
                logger.warning(f'Erro ao realizar o PUT para o objeto {obj_key}. Exception: {e}')
                raise e

"""
Ideias:
    - [x] Método para webscrapping
    - [x] Método para salvar dados localmente
    - [x] Método para carregar dados localmente
    - [ ] Método para inserir dados no s3
    - [ ] Método para inserir dados no sqs
    - [ ] Método para gerenciar put dos dados (s3 ou sqs)
    - [ ] Método para validar dados no dynamodb

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
    # Inicializando objeto da classe
    rock = ManageRockAlbuns()
    
    # Verificando requisição dos dados de álbuns de rock
    if MODE == 'get':
        rock.web_scrapping(
            page_end=PAGE_END,
            page_start=PAGE_START,
            log_step=LOG_STEP
        )

