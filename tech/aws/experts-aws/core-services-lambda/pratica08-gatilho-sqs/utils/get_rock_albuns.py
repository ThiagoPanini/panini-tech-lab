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
from dataclasses import dataclass
import os
import json
import boto3

# Leitura de argumentos de sript
import argparse
from numpy import save

# Requisições e parsing de html
import requests
from bs4 import BeautifulSoup

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
        1.2 Parsing de argumentos do script
---------------------------------------------------
"""

# Criando parser
parser = argparse.ArgumentParser()

# Adicionando argumentos
parser.add_argument('--request-mode', '-r', required=False, default='online', type=str)
parser.add_argument('--page-start', '-ps', required=False, default=1, type=int)
parser.add_argument('--page-end', '-pe', required=False, default=20, type=int)                    
parser.add_argument('--page-log', '-pl', required=False, default=5, type=int)
parser.add_argument('--save-mode', '-s', required=False, default='interval')
parser.add_argument('--output', '-o', required=False, default='local', type=str)
parser.add_argument('--file-path', '-p', required=False, default=os.path.expanduser('~'), type=str)
parser.add_argument('--local-file', '-f', required=False, type=str)
parser.add_argument('--s3-bucket', '-b', required=False, type=str)
parser.add_argument('--s3-key', '-k', required=False, type=str)

args = parser.parse_args()


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
        1.2 Logging e variáveis do projeto
---------------------------------------------------
"""

# Definindo função para configurar objeto de log do código
def log_config(logger, level=logging.DEBUG, 
               log_format='%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s',
               log_filepath=os.path.join(os.getcwd(), 'exec_log/execution_log.log'),
               flag_file_handler=False, flag_stream_handler=False, filemode='a'):
    """
    Função que recebe um objeto logging e aplica configurações básicas ao mesmo
    
    Parâmetros
    ----------
    :param logger: objeto logger criado no escopo do módulo [type: logging.getLogger()]
    :param level: level do objeto logger criado [type: level, default=logging.DEBUG]
    :param log_format: formato do log a ser armazenado [type: string]
    :param log_filepath: caminho onde o arquivo .log será armazenado 
        [type: string, default='exec_log/execution_log.log']
    :param flag_file_handler: define se será criado um arquivo de armazenamento de log
        [type: bool, default=False]
    :param flag_stream_handler: define se as mensagens de log serão mostradas na tela
        [type: bool, default=True]
    :param filemode: tipo de escrita no arquivo de log [type: string, default='a' (append)]
    
    Retorno
    -------
    :return logger: objeto logger pré-configurado
    """

    # Setting level for the logger object
    logger.setLevel(level)

    # Creating a formatter
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Creating handlers
    if flag_file_handler:
        log_path = '/'.join(log_filepath.split('/')[:-1])
        if not os.path.isdir(log_path):
            os.makedirs(log_path)

        # Adding file_handler
        file_handler = logging.FileHandler(log_filepath, mode=filemode, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if flag_stream_handler:
        # Adding stream_handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)    
        logger.addHandler(stream_handler)

    return logger

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger, flag_stream_handler=True)

# Definindo variáveis do projeto
BASE_URL = 'https://dr.loudness-war.info/album/list/'
HEADERS = ['banda', 'album', 'ano']
FILE_NAME = 'rock_albuns_scrapping.json'

# Coletando argumentos do script (parâmetros da função)
REQUEST_MODE = args.request_mode
PAGE_START = args.page_start
PAGE_END = args.page_end
PAGE_LOG = args.page_log
SAVE_PARAMS = {
    'save_mode': args.save_mode,
    'output': args.output,
    'file_path': args.file_path,
}

# Definindo variáveis do arquivo de saída no s3
BUCKET = args.s3_bucket
KEY = args.s3_key


"""
---------------------------------------------------
----------- 2. WEB SCRAPPING DE ÁLBUNS ------------
        2.1 Definindo função de extração
---------------------------------------------------
"""

# Salvando dados no s3
def save_rock_albuns(data, file_name, save_params):

    # Validando salvamento local dos dados
    if save_params['output'] == 'local':
        with open(os.path.join(save_params['file_path'], file_name), 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
    
    # Validando salvamento em bucket s3 na AWS
    elif save_params['output'] == 's3':
        s3_client = boto3.client('s3')
        try:
            response = s3_client.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(data, ensure_ascii=False))
        except Exception as e:
            raise e


# Obtenção de dados de álbuns de rock (online ou local)
def get_rock_albuns(request_mode, page_start, page_end, page_log, 
                    save_params=SAVE_PARAMS):
    """
    Função responsável por realizar a obtenção de dados relacionados a álbuns de rock
    a serem utilizados como alvo de posteriores análises e integrações envolvendo
    funções Lambda na AWS. Esta função conta com parâmetros criados especificamente
    para facilitar o trabalho de obtenção dos dados, seja através do modo online, onde
    a bibioteca requests é utilizada para webscrapping em um site que consolida álbuns
    de rock, ou então no modo batch onde é proposta a leitura local de um arquivo JSON
    já processado previamente.

    Parameters
    ----------
    :param online:
        Flag booleana para guiar a forma com que os dados serão obtidos.
        * online=True: obtenção é dada via webscrapping em site externo
        * online=False: obtenção é dada via leitura local de arquivo JSON
        [type: bool, default=True]

    :param base_url:
        URL base de requisição no modo online para webscrapping
        [type: str, default='https://dr.loudness-war.info/album/list/']

    :param pages:
        Quantidade de páginas que serão analisadas nas requisições
        [type: int, default=20]
    
    :param headers:
        Cabeçalhos que serão utilizados como chaves na montagem
        do arquivo JSON gerado após as requisições
        [type: list, default=['banda', 'album', 'ano']]

    :param page_log:
        Quantidade de páginas iteradas até que uma mensagem de log
        seja mostrada ao usuário
        [type: int, default=5]

    :kwarg save: 
        Flag booleano para salvamento do conteúdo extraído
        [type: bool, default=False]

    :kwarg file_path:
        Diretório de destino (modo online) ou de leitura (modo batch)
        do arquivo JSON local
        [type: str, default=os.path.join(os.getcwd(), 'tech\\aws\\experts-aws\\core-services-lambda\\pratica08-gatilho-sqs\\resources\\files')]

    :kwarg file_name:
        Nome do arquivo de destino (modo online) ou de leitura (modo batch)
        [type: str, default=rock_albuns_complete.json]
    """

    # Extraindo parâmetros de salvamento dos dados
    file_path = save_params['file_path']

    # Validando modo de obtenção dos dados
    if request_mode == 'online':
        # Iterando sobre as páginas do site
        logger.info(f'Modo online: iterando da página {page_start} até a página {page_end} do site')
        rock_albuns = []
        i = 0
        for page in range(page_start, page_end + 1):
            # Gerando url de requisição de acordo com a página
            request_url = BASE_URL + str(page)
            log_condition = (page_log > 0) and (page % page_log == 0)

            # Coletando conteúdo html e aplicando tratamento
            logger.debug(f'Realizando requisição para a página {page} do site. Total de registros coletados: {len(rock_albuns)}') if log_condition else None
            html_content = requests.get(url=request_url)
            soup = BeautifulSoup(html_content.text, features='html.parser')

            # Extraindo tabelas do site
            site_tables = soup.find_all('table')

            # Extraindo conteúdo das tabelas do site
            tr_data = site_tables[0].find_all('tr')
            td_data = [tr.find_all('td') for tr in tr_data]

            # Tratando e transformando conteúdo em lista do Python
            for row in td_data[1:]:
                content = [c.text.strip() for c in row][:3] # Coleta apenas os três primeiros elementos (banda, álbum e ano)
                json_content = {h: v for h, v in zip(HEADERS, content)}
                rock_albuns.append(json_content)

                # Salvando dados arquivo a arquivo (se aplicável)
                save_rock_albuns(data=json_content, file_name=FILE_NAME, save_params=save_params) if save_params['save_mode'] == 'file' else None

            # Salvando dados página a página (se aplicável)
            file_name = f'{os.path.splitext(FILE_NAME)[0]}_pg{page}.json'
            save_rock_albuns(data=rock_albuns, file_name=file_name, save_params=save_params) if save_params['save_mode'] == 'page' else None

            # Salvando dados página a página (se aplicável)
            if save_params['save_mode'] == 'interval' and log_condition and i > 0:
                file_name = f'{os.path.splitext(FILE_NAME)[0]}_pg{page_start}-{page}.json'
                save_rock_albuns(data=rock_albuns, file_name=file_name, save_params=save_params)

                # Removendo arquivo anterior
                try:
                    old_filename = f'{os.path.splitext(FILE_NAME)[0]}_pg{page_start}-{page - page_log}.json'
                    os.remove(os.path.join(save_params['file_path'], old_filename))
                except FileNotFoundError as fe:
                    pass

            i += 1

        # Comunicação final ao usuário
        logger.info(f'Foram extraídos {len(rock_albuns)} registros de álbuns de rock')

    else:
        # Modo local: a leitura dos dados será realizada através de arquivo local
        logger.info(f'Modo local: realizando a leitura local de arquivo JSON contendo álbuns de rock')
        try:
            with open(args.local_file, 'rb') as f:
                rock_albuns = json.loads(f.read().decode('utf-8'))
            logger.info(f'Conteúdo de arquivo JSON lido com sucesso. Total de registros: {len(rock_albuns)}')
        except Exception as e:
            logger.error(f'Erro ao realizar a leitura do arquivo JSON. Exception: {e}')
            raise e

    # Retorno do conteúdo
    return rock_albuns


"""
---------------------------------------------------
----------- 2. WEB SCRAPPING DE ÁLBUNS ------------
          2.2 Executando código no main
---------------------------------------------------
"""

if __name__ == '__main__':
    # Coletando dados
    rock_albuns_data = get_rock_albuns(
        request_mode=REQUEST_MODE,
        page_start=PAGE_START,
        page_end=PAGE_END,
        page_log=PAGE_LOG,
        save_params=SAVE_PARAMS
    )

    # Iterando sobre cada registro
    for album in rock_albuns_data[:2]:
        print(album)
