# Importando bibliotecas
import boto3
import json
import os

# Definindo variáveis do projeto
BUCKET = ''
KEY = 'data/rock-albuns/csv/favoritos.csv'

def lambda_handler(event, context):
    
    # Criando client s3
    s3_client = boto3.client('s3')
    
    # Realizando a leitura do objeto
    r = s3_client.get_object(Bucket=BUCKET, Key=KEY)
    data = r['Body'].read().decode()
    
    print(data)
    
    return None


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica03-integracao-s3'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)