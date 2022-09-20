"""
SCRIPT: brazilian-ecommerce.py

CONTEXTO:
---------
Script criado para servir como um exemplo prático, eficiente
e completo dentro da jornada de aprendizado em Apache Spark
com pyspark em termos de submissão de aplicações para
um cluster de computadores (ou para o driver, em caso de
utilização do modo local do Spark).

OBJETIVO:
---------
Consolidar múltiplas fontes externas de dados contendo
informações sobre compras e atividades no cenário do
e-commerce brasileiro registrado pela empresa Olist,
permitindo assim a construção de um dataset completo,
não normalizado e com atributos suficientemente ricos
de modo a garantir análises eficientes em outras etapas
do fluxo analítico.

TABLE OF CONTENTS:
------------------
1. Preparação inicial do script
    1.1 Importação das bibliotecas
    1.2 Configuração do objeto logger
    1.3 Coleta e validação dos argumentos
2. Programa principal
    2.1 Criando e configurando SparkSession
    2.2 Lendo objetos do s3 em DataFrames Spark
    2.3 Cruzando e preparando dados
    2.4 Criando coluna de partição da tabela
    2.5 Escrevendo tabela final em bucket no s3

------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando bibliotecas
import sys
import argparse
import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import boto3
from warnings import filterwarnings
filterwarnings("ignore")


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.2 Configuração do objeto logger
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
        1.3 Definição e coleta dos argumentos
---------------------------------------------------"""

# Criando objeto para parse dos argumentos
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    usage="spark-submit spec-brazilian-ecommerce.py <bucket_name>",
    description="Script responsável por realizar a " +
                "leitura de dados contendo informações sobre o " +
                "e-commerce brasileiro para a criação de um " +
                "dataset escalável utilizando a API estruturada " +
                "de DataFrames do Spark via pyspark"
)

# Adicionando argumento: --version
parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"{os.path.splitext(parser.prog)[0]} 0.1"
)

# Adicionando argumento: --bucket
parser.add_argument(
    "-b", "--bucket",
    dest="bucket",
    type=str,
    help="Nome do bucket alvo do processo de leitura e escrita",
    required=True
)

# Adicionando argumento: --input-prefix
parser.add_argument(
    "-in", "--input-prefix",
    dest="input_prefix",
    type=str,
    default="brazilian-ecommerce",
    help="Prefixo de folder no s3 para leitura dos arquivos",
    required=False
)

# Adicionando argumento: --output-prefix
parser.add_argument(
    "-out", "--output-prefix",
    dest="output_prefix",
    type=str,
    default="output",
    help="Prefixo de folder no s3 para escrita dos arquivos",
    required=False
)

# Adicionando argumento: --format
parser.add_argument(
    "-f", "--format",
    dest="format",
    type=str,
    default="parquet",
    help="Formato do arquivo final a ser armazenado no s3",
    required=False
)

# Adicionando argumento: --table-name
parser.add_argument(
    "-t", "--table-name",
    dest="table_name",
    type=str,
    default="tbl_spec_brazilian_ecommerce",
    help="Nome da 'tabela' final a ser armazenada no s3",
    required=False
)

# Coletando argumentos do script
args = parser.parse_args()


if __name__ == "__main__":

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
          2.1 Criando e configurando SparkSession
    -----------------------------------------------"""
    logger.debug("Criando objeto de sessão spark")
    try:
        spark = SparkSession\
            .builder\
            .appName(__file__)\
            .getOrCreate()
    except Exception as e:
        logger.error("Erro ao criar objeto de sessão spark")
        raise e

    # Criando sessão do boto3 para coleta das credenciais
    session = boto3.Session()
    credentials = session.get_credentials()
    frozen_credentials = credentials.get_frozen_credentials()
    access_key = frozen_credentials.access_key
    secret_key = frozen_credentials.secret_key

    # Configurando contexto para integração com AWS
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.amazonaws.com")

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
        2.2 Lendo objetos do s3 em DataFrames Spark
    -----------------------------------------------"""

    # Corrigindo prefixo de entrada, se necessário
    if args.input_prefix != "":
        input_prefix = args.input_prefix + "/" \
            if args.input_prefix[-1] != "/" \
            else args.input_prefix

    # Corrigindo prefixo de saída, se necessário
    if args.output_prefix != "":
        output_prefix = args.output_prefix + "/" \
            if args.output_prefix[-1] != "/" \
            else args.output_prefix

    # Definindo caminhos de entrada e saída no s3
    s3_input_path = f"s3a://{args.bucket}/{input_prefix}"
    s3_output_path = f"s3a://{args.bucket}/{output_prefix}/{args.table_name}"

    # Criando dicionário de caminhos a partir de entrada no s3
    s3_key_dict = {
        "customers": "olist_customers_dataset/olist_customers_dataset.csv",
        "items": "olist_order_items_dataset/olist_order_items_dataset.csv",
        "pay": "olist_order_payments_dataset/olist_order_payments_dataset.csv",
        "orders": "olist_orders_dataset/olist_orders_dataset.csv",
        "products": "olist_products_dataset/olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset/olist_sellers_dataset.csv"
    }

    # Inserindo informação de protocolo e bucket de entrada
    s3_input_list = [s3_input_path] * len(s3_key_dict)
    s3_input_zip = zip(s3_key_dict.keys(), s3_key_dict.values(), s3_input_list)
    s3_input_dict = {k: p + v for k, v, p in s3_input_zip}

    # Lendo DataFrame: customers
    try:
        logger.debug("Realizando a leitura de DataFrame: customers")
        df_customers = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load(s3_input_dict["customers"])
    except Exception as e:
        logger.error("Erro ao realizar a leitura do DataFrame: customers")
        raise e

    # Lendo DataFrame: customers
    try:
        logger.debug("Realizando a leitura de DataFrame: items")
        df_order_items = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load(s3_input_dict["items"])
    except Exception as e:
        logger.error("erro ao realizar a leitura do DataFrame: items")
        raise e

    # Lendo DataFrame: payments
    try:
        logger.debug("Realizando a leitura de DataFrame: payments")
        df_order_payments = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load(s3_input_dict["pay"])
    except Exception as e:
        logger.error("Erro ao realizar a leitura do DataFrame: payments")
        raise e

    # Lendo DataFrame: orders
    try:
        logger.debug("Realizando a leitura de DataFrame: orders")
        df_orders = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load(s3_input_dict["orders"])
    except Exception as e:
        logger.error("Erro ao realizar a leitura do DataFrame: orders")
        raise e

    # Lendo DataFrame: products
    try:
        logger.debug("Realizando a leitura de DataFrame: products")
        df_products = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load(s3_input_dict["products"])
    except Exception as e:
        logger.error("Erro ao realizar a leitura do DataFrame: products")
        raise e

    # Lendo DataFrame: sellers
    try:
        logger.debug("Realizando a leitura de DataFrame: sellers")
        df_sellers = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load(s3_input_dict["sellers"])
    except Exception as e:
        logger.error("Erro ao realizar a leitura do DataFrame: sellers")
        raise e

    logger.info(f"Todos os {len(s3_input_dict)} objetos foram lidos com " +
                f"sucesso do bucket {args.bucket}")

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
            2.3 Cruzando e preparando dados
    -----------------------------------------------"""
    logger.debug("Aplicando cruzamento dos dados para geração de tabela única")

    # Cruzando dados: pedidos e pagamentos
    df_ord_pay = df_orders.join(
        other=df_order_payments,
        how="left",
        on=[df_orders.order_id == df_order_payments.order_id]
    ).drop(df_order_payments.order_id)

    # Cruzando dados: pedidos, pagamentos e clientes
    df_ord_pay_cust = df_ord_pay.join(
        other=df_customers,
        how="left",
        on=[df_ord_pay.customer_id == df_customers.customer_id]
    ).drop(df_customers.customer_id)

    # Cruzando dados: pedidos, pagamentos, clientes e itens
    df_ord_pay_cust_items = df_ord_pay_cust.join(
        other=df_order_items,
        how="left",
        on=[df_ord_pay_cust.order_id == df_order_items.order_id]
    ).drop(df_order_items.order_id)

    # Cruzando dados: pedidos, pagamentos, clientes, itens e produtos
    df_ord_pay_cust_items_prod = df_ord_pay_cust_items.join(
        other=df_products,
        how="left",
        on=[df_ord_pay_cust_items.product_id == df_products.product_id]
    ).drop(df_products.product_id)

    # Cruzando dados: pedidos, pgtos, clientes, itens, produtos e vendedores
    df_ecommerce_join = df_ord_pay_cust_items_prod.join(
        other=df_sellers,
        how="left",
        on=[df_ord_pay_cust_items_prod.seller_id == df_sellers.seller_id]
    ).drop(df_sellers.seller_id)

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
        2.4 Criando coluna de partição da tabela
    -----------------------------------------------"""
    logger.debug("Adicionando coluna de partição como a data do pedido")

    # Adicionando coluna de partição
    partition_expr = "date_format(order_purchase_timestamp, 'yyyyMM')"
    df_ecommerce_spec = df_ecommerce_join.selectExpr(
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state"
    ).withColumn("order_purchase_date", expr(partition_expr))

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
       2.5 Escrevendo tabela final em bucket no s3
    -----------------------------------------------"""
    logger.debug(f"Salvando dados em bucket {args.bucket}")

    # Executando comando
    df_ecommerce_spec.write.format(args.format)\
        .partitionBy("order_purchase_date")\
        .save(s3_output_path)

    # Encerrando sessão
    spark.stop()
