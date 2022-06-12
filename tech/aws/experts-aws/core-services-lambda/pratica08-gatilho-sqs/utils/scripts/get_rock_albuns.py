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
import sys

# Leitura de argumentos de sript
import argparse

# Requisições e parsing de html
import requests
from bs4 import BeautifulSoup

# Logging
import logging
from ..log import log_config


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
parser.add_argument('--log-step', '-l', required=False, default=5, type=int)
parser.add_argument('--save-mode', '-s', required=False, default='interval')
parser.add_argument('--output', '-o', required=False, default='local', type=str)
parser.add_argument('--file-path', '-p', required=False, default=os.path.expanduser('~'), type=str)
parser.add_argument('--local-file', '-f', required=False, type=str)
parser.add_argument('--num-objects', '-n', required=False, default=-1, type=int)
parser.add_argument('--s3-bucket', '-s3b', required=False, type=str)
parser.add_argument('--s3-prefix', '-s3p', required=False, type=str)
parser.add_argument('--destination', '-d', required=False, default='s3', type=str)

args = parser.parse_args()
