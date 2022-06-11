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

# Leitura de argumentos de sript
import argparse

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
parser.add_argument('--online', '-o', required=False, default=True, type=bool,
                    help='Execução online de requisição ou leitura local de arquivo json')
parser.add_argument('--num-pages', '-n', required=False, default=5, type=int,
                    help='Número total de páginas a serem extraídas nas requisições online')
parser.add_argument('--page-log', '-l', required=False, default=5, type=int)
parser.add_argument('--file-path', '-p', required=False, default=os.path.expanduser('~'), type=str)
parser.add_argument('--file-name', '-f', required=False, default='rock_albuns_complete.json', type=str)

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
PAGES = args.num_pages
HEADERS = ['banda', 'album', 'ano']
PAGE_LOG = args.page_log
FILE_PATH = args.file_path
FILE_NAME = args.file_name


"""
---------------------------------------------------
----------- 2. WEB SCRAPPING DE ÁLBUNS ------------
        2.1 Definindo função de extração
---------------------------------------------------
"""

# Obtenção de dados de álbuns de rock (online ou local)
def get_rock_albuns(online=True, base_url=BASE_URL, pages=PAGES, headers=HEADERS, 
                    page_log=PAGE_LOG, **kwargs):
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

    # Validando modo de obtenção dos dados
    if online:
        # Iterando sobre as páginas do site
        logger.info(f'Modo online: iterando sobre um total de {PAGES} páginas do site')
        rock_albuns = []
        for page in range(1, PAGES + 1):
            # Gerando url de requisição de acordo com a página
            request_url = BASE_URL + str(page)
            log_condition = (PAGE_LOG > 0) and (page % PAGE_LOG == 0)

            # Coletando conteúdo html e aplicando tratamento
            logger.debug(f'Realizando requisição para a página {page} do site. Total de registros coletados: {len(rock_albuns)}') if log_condition else None
            html_content = requests.get(url=request_url)
            soup = BeautifulSoup(html_content.text, 'lxml')

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

        # Comunicação final ao usuário
        logger.info(f'Foram extraídos {len(rock_albuns)} registros de álbuns de rock')

        # Verificando salvamento de arquivo
        if kwargs['save']:
            file_path = kwargs['file_path'] if 'file_path' in kwargs else FILE_PATH
            file_name = kwargs['file_name'] if 'file_name' in kwargs else FILE_NAME
            with open(os.path.join(file_path, file_name), 'w', encoding='utf-8') as f:
                f.write(json.dumps(rock_albuns, ensure_ascii=False))

    else:
        # Modo batch: a leitura dos dados será realizada através de arquivo local
        logger.info(f'Modo batch: realizando a leitura local de arquivo JSON contendo álbuns de rock')
        file_path = kwargs['file_path'] if 'file_path' in kwargs else FILE_PATH
        file_name = kwargs['file_name'] if 'file_name' in kwargs else FILE_NAME

        # Realizando a leitura do arquivo
        try:
            with open(os.path.join(file_path, file_name), 'rb') as f:
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
    rock_albuns_data = get_rock_albuns(online=True, save=True)
