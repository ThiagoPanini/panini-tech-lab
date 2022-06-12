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
from time import sleep

# Leitura de argumentos de sript
import argparse
from numpy import save

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
parser.add_argument('--file', '-f', required=False, type=str)
parser.add_argument('--destination', '-d', required=False, default='s3', type=str)
parser.add_argument('--log-step', '-l', required=False, default=5, type=int)
parser.add_argument('--num-objects', '-n', required=False, default=-1, type=int)

parser.add_argument('--s3-bucket', '-s3b', required=False, type=str)
parser.add_argument('--s3-prefix', '-s3p', required=False, type=str)

args = parser.parse_args()


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
        1.2 Parâmetros do script e logging
---------------------------------------------------
"""

# Coletando argumentos do script (parâmetros da função)
FILE = args.file
DEST = args.destination
LOG_STEP = args.log_step
NUM_OBJS = args.num_objects
S3_BUCKET = args.s3_bucket
S3_PREFIX = args.s3_prefix

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger, flag_stream_handler=True)


"""
---------------------------------------------------
----------- 2. WEB SCRAPPING DE ÁLBUNS ------------
        2.1 Definindo função de extração
---------------------------------------------------
"""

class PutRockAlbuns()