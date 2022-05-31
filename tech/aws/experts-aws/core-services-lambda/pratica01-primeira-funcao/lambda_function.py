import json

def lambda_handler(event, context):
    
    # Retornando informações sobre a banda
    print(f'Próxima música da playlist: {event["musica"]}')
    print(f'Autor: {event["banda"]} - Álbum: {event["album"]}')

    
    return {
        'statusCode': 200,
        'body': json.dumps('Voce esta ouvindo sua musica preferida!')
    }