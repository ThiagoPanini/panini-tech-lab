import json
import os

def lambda_handler(event, context):
    
    # Retornando informações sobre a banda
    print(f'Próxima música da playlist: {event["musica"]}')
    print(f'Autor: {event["banda"]} - Álbum: {event["album"]}')

    
    return {
        'statusCode': 200,
        'body': json.dumps('Voce esta ouvindo sua musica preferida!')
    }


"""
---------------------------------------------------
------------ BLOCO DE TESTES DA FUNÇÃO ------------
     Configurando eventos e testando execução
---------------------------------------------------
"""

# Definindo variáveis para leitura de evento de teste
LAMBDA_PATH = os.path.join(os.getcwd(), 'tech/aws/experts-aws/core-services-lambda')
FUNCTION_REF = 'pratica01-primeira-funcao'
EVENT_PATH = 'resources/tests/test-event.json'

# Lendo evento de teste
with open(os.path.join(LAMBDA_PATH, FUNCTION_REF, EVENT_PATH)) as f:
    event = json.load(f)

if __name__ == '__main__':
    lambda_handler(event=event, context=None)