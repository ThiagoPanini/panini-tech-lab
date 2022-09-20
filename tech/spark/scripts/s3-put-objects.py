"""
SCRIPT: s3-put-objects.py

CONTEXTO:
---------
Script criado para auxiliar o upload de arquivos locais
para um destino s3 especificado pelo usuário. O código
aqui alocado considera que o usuário tenha acesso
programático de escrita no bucket de destino, utilizando
como principal meio, o SDK boto3.

OBJETIVO:
---------
Proporcionar uma forma fácil, rápida e eficiente para
transferência de arquivos locais para um bucket s3 na
AWS, respeitando a hierarquia local de pastas existente.

TABLE OF CONTENTS:
------------------
1. Preparação inicial do script
    1.1. Importação das bibliotecas
    1.2. Configuração do objeto logger
    1.3. Coleta e validação dos argumentos
2. Programa principal
    2.1 Validando argumentos do script
    2.2 Instanciando client s3 do boto3
    2.3 Iterando sobre arquivos do diretório


------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1. Importação das bibliotecas
---------------------------------------------------"""

# Importando bibliotecas
import sys
import argparse
import logging
import os
import boto3


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.2. Configuração do objeto logger
---------------------------------------------------"""

# Instanciando objeto de logging
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# Configurando formato das mensagens no objeto
log_format = "%(levelname)s;%(asctime)s;%(filename)s;"
log_format += "%(lineno)d;%(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(log_format,
                              datefmt=date_format)

# Configurando stream handler do objeto de log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.3. Definição e coleta dos argumentos
---------------------------------------------------"""

# Criando objeto para parse dos argumentos
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    usage="python s3-put-objects.py <local_path> <bucket_name>",
    description="Script criado para auxiliar o upload de arquivos locais " +
                "para um destino s3 especificado pelo usuário. O código " +
                "aqui alocado considera que o usuário tenha acesso " +
                "programático de escrita no bucket de destino, utilizando " +
                "como principal meio, o SDK boto3."
)

# Adicionando argumento: --version
parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"{os.path.splitext(parser.prog)[0]} 0.1"
)

# Adicionando argumento: --path
parser.add_argument(
    "-p", "--path",
    dest="path",
    type=str,
    help="Diretório local onde os dados a serem inseridos " +
         "no s3 estão armazenados",
    required=True
)

# Adicionando argumento: --bucket
parser.add_argument(
    "-b", "--bucket",
    dest="bucket",
    type=str,
    help="Nome do bucket alvo do processo de escrita na AWS",
    required=True
)

# Adicionando argumento: --bucket-prefix
parser.add_argument(
    "-bp", "--bucket-prefix",
    dest="bucket_prefix",
    type=str,
    default="",
    help="Prefixo de folder no s3 para upload dos arquivos",
    required=False
)

# Coletando argumentos do script
args = parser.parse_args()


"""---------------------------------------------------
--------------- 2. PROGRAMA PRINCIPAL ----------------
---------------------------------------------------"""

if __name__ == "__main__":

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
            2.1 Validando argumentos do script
    -----------------------------------------------"""

    # Validando diretório local
    path_msg = f"Argumento --path ({args.path})"
    try:
        # Coletando informações do diretório
        valid_path = os.path.isdir(args.path)
        files_in_path = os.listdir(args.path)

    except TypeError as te:
        logger.error(f"{path_msg} inválido.")
        raise te

    except FileNotFoundError as fnf:
        logger.error(f"{path_msg} aponta pra um diretório inexistente. " +
                     "Insira um diretório existente para upload dos arquivos.")
        raise fnf

    except NotADirectoryError as nade:
        logger.error(f"{path_msg} não foi identificado como um diretório. " +
                     "Insira um diretório existente para upload dos arquivos.")
        raise nade

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
            2.2 Instanciando client s3 do boto3
    -----------------------------------------------"""
    try:
        s3_client = boto3.client("s3")
    except Exception as e:
        logger.error("Erro ao inicializar client s3 via boto3")
        raise e

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
        2.3 Iterando sobre arquivos do diretório
    -----------------------------------------------"""

    # Iterando sobre diretório
    logger.debug(f"Iniciando processo de escrita em bucket {args.bucket}")
    logger.debug(f"Iterando sobre arquivos do diretório {args.path}")
    for path, dirs, files in os.walk(args.path):
        # Iterando sobre cada arquivo e realizando upload
        for name in files:
            # Preparando variáveis de destino no s3
            file_prefix = os.path.splitext(name)[0]
            if args.bucket_prefix != "":
                bucket_prefix = args.bucket_prefix + "/" \
                    if args.bucket_prefix[-1] != "/" \
                    else args.bucket_prefix

            # Montando chave de objeto
            obj_key = bucket_prefix + file_prefix + "/" + name

            # Montando caminho completo do arquivo local
            filepath = os.path.join(path, name)

            # Realizando upload de stream binária já em buffer
            try:
                with open(filepath, 'rb') as f:
                    s3_client.put_object(
                        Bucket=args.bucket,
                        Body=f,
                        Key=obj_key
                    )
                logger.info(f"Arquivo {name} inserido com sucesso ({obj_key})")

            except Exception as e:
                logger.warning("Erro ao realizar upload via put_object() " +
                               f"de arquivo {filepath} no destino {obj_key} " +
                               f"em bucket {args.bucket}. Exception: {e}")
                raise e
