# Importando bibliotecas
import boto3

# Definindo variáveis do projeto
BUCKET = 'aws-experts-dx6sdjz2j7ro-sa-east-1'
KEY = 'lambda/tests/rock_albuns.csv'

def lambda_handler(event, context):
    
    # Criando client s3
    s3_client = boto3.client('s3')
    
    # Realizando a leitura do objeto
    r = s3_client.get_object(Bucket=BUCKET, Key=KEY)
    data = r['Body'].read().decode()
    
    print(data)
    
    return None
