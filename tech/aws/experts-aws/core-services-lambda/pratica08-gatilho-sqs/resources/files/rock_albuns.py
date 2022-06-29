"""
---------------------------------------------------
------------- SCRIPT: rock_albuns.py --------------
---------------------------------------------------
Script responsável por gerenciar as atividades
relacionadas a utilização de funções Lambda em
conjunto com serviços como s3 e sqs. A grande lógica
deste script envolve a realização de três principais
ações:
1. Extração de dados de álbuns de rock via web scrapping
2. Put no S3 ou envio de mensagens desses dados via SQS
3. Validação de inserções realizadas no DynamoDB

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Logging e variáveis do projeto
2. Classe de gerenciamento de ações
    2.1 Extraindo e enviando álbuns de rock
3. Execução do script
    3.1 Gerenciando opções e coordenando execução
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 13/06/2022


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

# Valores default para argumentos
DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rock_albuns_scrapping_pg1-6000.json')

# Adicionando argumentos
parser.add_argument('--mode', '-m', required=False, default='test', type=str) # procurar como restringir argumentos
parser.add_argument('--page-start', '-s', required=False, default=1, type=int)
parser.add_argument('--page-end', '-e', required=False, default=20, type=int)                    
parser.add_argument('--log-step', '-l', required=False, default=5, type=int)
parser.add_argument('--file', '-f', required=False,  default=DEFAULT_FILE, type=str)
parser.add_argument('--destination', '-d', required=False, default='sqs', type=str)
parser.add_argument('--num-objects', '-n', required=False, default=10, type=int)
parser.add_argument('--bucket', '-b', required=False, type=str)
parser.add_argument('--prefix', '-p', required=False, default='', type=str)
parser.add_argument('--queue-name', '-q', required=False, default='rock-albuns-messages', type=str)
parser.add_argument('--interval', '-i', required=False, default=0.1, type=float)
parser.add_argument('--table', '-t', required=False, default='rock-albuns', type=str)

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
LOCAL_FILE = args.file
N_OBJS = args.num_objects
DESTINATION = args.destination
S3_BUCKET = args.bucket
S3_PREFIX = args.prefix
SQS_QUEUE = args.queue_name
SQS_INTERVAL = args.interval
DYNAMODB_TABLE = args.table

# Validando argumentos de acordo com o cenário
S3_BUCKET = 'aws-experts-dx6sdjz2j7ro-sa-east-1' if S3_BUCKET is None else S3_BUCKET

# Configurando objeto logger
logger = logging.getLogger(__file__)
logger = log_config(logger, flag_stream_handler=True)


"""
---------------------------------------------------
------- 2. CLASSE DE GERENCIAMENTO DE AÇÕES -------
     2.1 Extraindo e enviando álbuns de rock
---------------------------------------------------
"""

class ManageRockAlbuns():

    def __init__(self, log_step=5):
        self.log_step = log_step
        pass
    
    def save_local_data(self, data, file_path, file_name):
        """
        Realiza o salvamento de dados extraídos no método
        de web scrapping em formato json em diretório local

        Parâmetros
        ----------
        :param data:
            Conteúdo extraído obtido em um formato de lista
            formada por dicionários representando, individualmente,
            álbuns de rock extraídos via web scrapping. Este
            formato configura um arquivo JSON aninhado.
            [type: list]

        :param file_path:
            Diretório de salvamento do arquivo JSON
            [type: str]

        :param file_name:
            Nome do arquivo JSON a ser salvo
            [type: str]
        """

        # Criando diretório caso existente
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        
        # Salvando arquivo em formato json aninhado (lista de dicts)
        data_path = os.path.join(file_path, file_name)
        try:
            # Removendo duplicatas
            dedup_data = [dict(d) for d in set([frozenset(i.items()) for i in data])]
            with open(data_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(dedup_data, ensure_ascii=False))
            logger.info(f'Arquivo salvo com sucesso em {data_path}')
        except Exception as e:
            logger.error(f'Erro ao salvar arquivo em {data_path}. Exception: {e}')
    
    
    def load_local_data(self, file_path, file_name):
        """
        Realiza a leitura de arquivo JSON salvo localmente

        Parâmetros
        ----------
        :param file_path:
            Diretório de carregamento do arquivo JSON
            [type: str]

        :param file_name:
            Nome do arquivo JSON a ser lido
            [type: str]
        """

        # Realizando leitura do arquivo
        try:
            data_path = os.path.join(file_path, file_name)
            with open(data_path, 'rb') as f:
                rock_albuns = json.loads(f.read().decode('utf-8'))
            logger.info(f'Arquivo {file_name} lido com sucesso contendo {len(rock_albuns)} objetos')
        except Exception as e:
            logger.error(f'Erro ao realizar a leitura do arquivo {file_name} do caminho {file_path}. Exception: {e}')
            raise e
        
        return rock_albuns


    def web_scrapping(self, page_start, page_end, base_url=BASE_URL, 
                      headers=HEADERS, **kwargs):
        """
        Método responsável por aplicar o processo de web 
        scrapping de modo a extrair dados de álbuns de
        rock devidamente preparados em formato JSON. Os
        dados brutos são extraídos utilizando as libs
        requests e BeautifulSoup do python para obtenção
        de um body de requisição em formato HTML e sua 
        posterior transformação via parser do BeautifulSoup.

        O processo de transformação foi construído com base
        nas tags de tabelas do site origem, permitindo
        a efetiva listagem dos dados necessários para a 
        proposta desta atividade.

        Os parâmetros deste método foram pensados para
        propor a maior facilidade possível ao usuário
        que pretende testar suas funcionalidades, seja
        aplicando o processo de web scrapping em todo
        o site ou então em um conjunto reduzido de páginas.

        Como o site é dividido em um grande número de
        páginas (cada uma contendo os registros de
        álbuns de rock em tabelas), os parâmetros de início
        e final de página atuam de modo a propor uma
        extração dinâmica de conteúdo.

        Parâmetros
        ----------
        :param page_start:
            Página de início das requisições. O usuário pode
            utilizar este parâmetro para iniciar da primeira
            página (page_start=1) ou então continuar um 
            processo paralisado previamente (page_start=n)
            [type: int]

        :param page_end:
            Página de finalização das requisições. Até a 
            construção deste código, o site contava com
            aproximadamente 6000 páginas disponíveis com
            informações de álbuns de rock. Iterar por todas
            estas pode ser um processo demorado e, dessa forma
            este parâmetro pode auxiliar na extração de um
            conjunto reduzido de dados. As mensagens de log
            são mostradas ao usuário a cada self.log_step 
            iterações (atributo da classe)
            [type: int]

        :param base_url:
            URL básica do site alvo do processo de web
            scrapping. Este parâmetro é configurado como
            padrão no próprio código. Qualquer alteração em
            seu conteúdo pode configurar em erros críticos
            nas funcionalidades da classe, dado que toda a 
            lógica de extração e transformação do conteúdo
            foi criada com base nas características do site
            aqui definido.
            [type: str, default='https://dr.loudness-war.info/album/list/']

        :param headers:
            As informações contidos no site alvo da extração
            envolvem parâmetros que não serão utilizados
            posteriormente dentro das propostas desta atividade.
            Desta forma, o parâmetro headers tem por objetivo
            definir o cabeçalho dos valores extraídos no processo
            de transformação do conteúdo da página, sendo composto
            pelas informações de "banda", "álbum" e "ano". Assim
            como o parâmetro base_url, o parâmetro headers é
            definido de maneira fixa neste código. Qualquer
            alteração em seu conteúdo pode configurar em graves
            erros nas funcionalidades aqui consolidadas.
            [type: list, default=["banda", "album", "ano"]]

        **kwargs:
        :arg request_error_limit:
            Define um número máximo de erros de requisição
            durante o processo de webscrapping. A cada exceção
            obtida, um contador de erros é incrementado no laço
            de repetição configurado entre a página de início 
            (page_start) e a página de finalização (page_end).
            Quando este contador superar o número definido 
            por este argumento, o método será encerrado de
            maneira forçada.
            [type: int, default=10]

        :arg request_wait:
            Define o tempo de espera (em segundos) até
            que uma próxima requisição seja realizada caso
            uma exceção seja retornada no método.Em linhas
            gerais, um dos grandes motivadores de
            erros de requisição envolvendo múltiplas 
            requisições sequências é o curto tempo entre
            requisições. Dessa forma, sempre que um erro
            é obtido (e este não ultrapassa o limite
            definido), um tempo de espera é configurado
            até que a próxima requisição seja realizada.
            [type: int, default=2]

        :arg file_path:
            Diretório local a ser utilizado para salvar
            o arquivo obtido com o processo de scrapping.
            [type: str, default=os.path.dirname(os.path.abspath(__file__))]
        """

        # Informações sobre o processo
        logger.debug(f'Iniciando processo de webscrapping de álbuns de rock no site {base_url}')
        logger.info(f'Extração da página {page_start} até a página {page_end} com mensagens de log a cada {self.log_step} páginas')

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
            log_condition = (self.log_step > 0) and (page % self.log_step == 0)

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
                json_content = {h: v for h, v in zip(headers, content)}
                rock_albuns.append(json_content)

        # Finalizando etapa de extração
        file_name = f'rock_albuns_scrapping_pg{page_start}-{page_end}.json'
        self.save_local_data(data=rock_albuns, file_path=file_path, file_name=file_name)


    def rock_data_to_s3(self, bucket, prefix, nested_json, n_objs):
        """
        Método utilizado para iterar sobre cada elemento
        JSON dentro da lista de dicionários e realizar
        chamadas de put para um bucket definido no s3.

        Parâmetros
        ----------
        :param bucket:
            Nome do bucket alvo da escrita de objetos
            [type: str]

        :param prefix:
            Prefixo (folder) para escrita dos objetos
            [type: str]

        :param nested_json:
            Conteúdo a ser iterado para escrita no s3
            e representado como um JSON aninhado gerado
            a partir do processo de webscrapping.
            [type: list]

        :param n_objs:
            Define um limite de iteração de conteúdos
            da lista para escrita no s3. Considerando
            a quantidade de elementos totais extráidos
            no processo de webscrapping, este limitador
            pode atuar de forma positiva para testes
            em um cenário reduzido de elementos.
            [type: int]
        """

        # Transformando json aninhado (caso necessário)
        nested_json = [nested_json] if type(nested_json) != list else nested_json
        
        # Comunicando o total de iterações no laço
        total_objs = len(nested_json)
        if n_objs == -1:
            logger.debug(f'Realizando o PUT no s3 para todos os {total_objs} objetos JSON do arquivo consolidado com mensagens de log a cada {self.log_step} chamadas')
        else:
            logger.debug(f'Iterando sobre {n_objs} dos {total_objs} objetos JSON do arquivo consolidado com mensagens de log a cada {self.log_step} chamadas')

        # Iterando sobre cada registro e escrevendo no s3
        s3_client = boto3.client('s3')
        for album in nested_json[:n_objs]:
            # Condição de logging
            idx = nested_json.index(album) + 1
            log_condition = (self.log_step > 0) and (idx % self.log_step == 0)
            idx_name = str(idx).zfill(len(str(total_objs)))

            # Inserindo objeto no bucket
            logger.debug(f'Realizando o PUT para o objeto {idx} do JSON aninhado') if log_condition else None
            file_name = f'rock_album_{idx_name}.json'
            obj_key = prefix + file_name
            try:
                response = s3_client.put_object(Bucket=bucket, Key=obj_key, Body=json.dumps(album))        
            except Exception as e:
                logger.warning(f'Erro ao realizar o PUT para o objeto {obj_key}. Exception: {e}')
                raise e

        logger.info(f'Processo de inserção no s3 finalizado com sucesso')


    def rock_data_to_sqs(self, queue, nested_json, n_objs, interval):
        """
        Método utilizado para iterar sobre cada elemento
        JSON dentro da lista de dicionários e realizar
        o envio dos objetos como mensagens para fila no SQS.

        Parâmetros
        ----------
        :param queue:
            Nome da fila alvo da escrita das mensagens no SQS.
            A obtenção de um objeto de fila do recurso sqs do
            boto3 é feita a partir da chamada do método
            get_queue_url(), onde o principal parâmetro é
            justamente o nome da fila.
            [type: str]

        :param nested_json:
            Conteúdo a ser iterado para escrita no s3
            e representado como um JSON aninhado gerado
            a partir do processo de webscrapping.
            [type: list]

        :param n_objs:
            Define um limite de iteração de conteúdos
            da lista para escrita no s3. Considerando
            a quantidade de elementos totais extráidos
            no processo de webscrapping, este limitador
            pode atuar de forma positiva para testes
            em um cenário reduzido de elementos.
            [type: int]

        :param interval:
            Define um intervalo de "mensagens/segundo"
            para a escrita no SQS. A escrita de múltiplas 
            mensagens pode ser um processo a ser analisado
            e acompanhado de perto. Dessa forma, este 
            parâmetro pode ser utilizado para configurar
            um fluxo de mensagens que seja adequado para
            a visualização e acompanhamento dos envios.
            Como exemplos de configurações, interval=1 
            indica o envio de 1 mensagem por segundo. Já
            interval=0.1 indica o envio de 10 mensagens
            por segundo.
            [type: float]
        """

        # Instanciando client do sqs e coletando url da fila
        sqs = boto3.client('sqs')
        response = sqs.get_queue_url(QueueName=queue)
        queue_url = response['QueueUrl']

        # Comunicando o total de iterações no laço
        total_objs = len(nested_json)
        if n_objs == -1:
            logger.debug(f'Enviando todos os {total_objs} objetos JSON para fila SQS com logs a cada {self.log_step} chamadas')
        else:
            logger.debug(f'Enviando {n_objs} dos {total_objs} objetos JSON para fila SQS com logs a cada {self.log_step} chamadas')

        # Iterando sobre objetos JSON e enviando-os pra fila
        for album in nested_json[:n_objs]:

            # Enviando mensagem para a fila
            logger.debug(f'Enviando mensagem {album}')
            try:
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=json.dumps(album, ensure_ascii=False)
                )
            except Exception as e:
                logger.warning(f'Erro ao enviar mensagem: {album}. Exception: {e}')
                pass

            # Intervalo de envio
            sleep(interval)


    def count_dynamodb_items(self, table):
        """
        Como o último passo desta atividade envolve
        a escrita de objetos em tabela do DynamoDB,
        este método visa facilitar o acompanhamento
        do usuário através da contagem de itens
        presentes em uma tabela alvo do DynamoDB.

        Parâmetros
        ----------
        :param table:
            Tabela alvo da contagem de itens no DynamoDB
            [type: str]
        """

        # Validando quantidade de itens no dynamodb
        logger.debug(f'Validando itens presentes na tabela {table} do DynamoDB')
        sleep(5)
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.scan(TableName=table, Select='COUNT')
        total_itens = response['Count']

        # Comunicando
        logger.info(f'A tabela {table} do DynamoDB possui {total_itens} itens')
        
        return total_itens
       


"""
---------------------------------------------------
-------------- 3. EXECUÇÃO DO SCRIPT --------------
   3.1 Gerenciando opções e coordenando execução
---------------------------------------------------
""" 

if __name__ == '__main__':
    """
    O módulo main deste script é responsável por aplicar
    e gerenciar toda a lógica de execução baseada nas
    diferentes possibilidades mapeadas pelo usuário. 
    Contendo três principais modos (get, put e check),
    os métodos da classe ManageRockAlbuns são executados
    de acordo com os inputs fornecidos pelo usuário de
    modo a proporcionar os outputs solicitados. 
    Em detalhes, temos:

    --mode = "get"
        Este modo pode ser executado quando há a intenção
        de aplicar o processo de webscrapping para 
        obtenção de dados relacionados a álbuns de rock
        direto da fonte. Este modo possui configurações
        próprias que, quando parametrizadas, agem de 
        modo a resultar em um arquivo JSON com o conteúdo
        solicitado. 
        
        * Parâmetros necessários neste modo:
        --page-start, --page-end e --log-step
        
        * Exemplo de execução de script:
        python3 rock_albuns.py --mode "get" --page-start 1 --page-end 10 --log-step 5
    
    ------------------------------------------------------

    --mode = "put"
        Este modo considera a leitura de um arquivo JSON
        salvo localmente (output do modo "get") para
        envio iterativo à um bucket s3 ou à uma fila 
        do sqs. 
        
        * Parâmetros necessários neste modo:
        --file, --destination, --num-objects, --bucket
        --prefix e --queue

        * Exemplos de execução de script:
        python3 rock_albuns.py --mode "put" --file "./rock_albuns_scrapping_pg1-6000.json" --destination "s3" --bucket "aws-experts-dx6sdjz2j7ro-sa-east-1" --prefix "lambda/output/" --num-objects 10 --log-step 1
        python3 rock_albuns.py --mode "put" --file "./rock_albuns_scrapping_pg1-6000.json" --destination "sqs" --queue-name "rock-albuns-messages" --num-objects 5 --interval 0.1

    ------------------------------------------------------

    --mode = "check"
        Por fim, como a lógica final envolve a inserção
        de itens no dynamodb, este modo tem como objetivo
        a realização da contagem de itens na tabela alvo.
        
        * Parâmetros necessários neste modo:
        --table

        * Exemplo de execução de script
        python3 rock_albuns.py --mode "check" --table "rock-albuns"
    """

    # Inicializando objeto da classe
    rock = ManageRockAlbuns(log_step=LOG_STEP)
    
    # Validando modos
    if MODE == 'get':
        rock.web_scrapping(
            page_end=PAGE_END,
            page_start=PAGE_START,
            log_step=LOG_STEP
        )

    elif MODE == 'put':
        # Coletando arquivo json aninhado
        rock_albuns = rock.load_local_data(
            file_path=os.path.dirname(LOCAL_FILE),
            file_name=os.path.basename(LOCAL_FILE)
        )

        # Iterando sobre seu conteúdo
        if DESTINATION == 's3':
            rock.rock_data_to_s3(
                bucket=S3_BUCKET,
                prefix=S3_PREFIX,
                nested_json=rock_albuns,
                n_objs=N_OBJS
            )
        elif DESTINATION == 'sqs':
            rock.rock_data_to_sqs(
                queue=SQS_QUEUE,
                nested_json=rock_albuns,
                n_objs=N_OBJS,
                interval=SQS_INTERVAL
            )

    elif MODE == 'check':
        # Retornando itens inseridos no DynamoDB
        table_items = rock.count_dynamodb_items(
            table=DYNAMODB_TABLE
        )