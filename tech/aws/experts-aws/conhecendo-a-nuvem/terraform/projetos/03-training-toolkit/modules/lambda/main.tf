/* --------------------------------------------------
FILE: main.tf @ lambda module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é realizar a implantação
das funções Lambda e seus respectivos recursos dentro
do ambiente prático utilizado para experimentação
e aprendizado AWS

RESOURCES: Os recursos aqui implantados serão:
  - Funções Lambda
  - Policies e Roles IAM
  - Regras do EventBridge
  - Fila do SQS
  - Tabela do DynamoDB
-------------------------------------------------- */

/* --------------------------------------------------
--------------- ADDITIONAL RESOURCES ----------------
-- Serviços adicionais para composição das funções --
-------------------------------------------------- */

# Tabela no DynamoDB
resource "aws_dynamodb_table" "rock-albuns" {
  name           = "rock-albuns"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "banda"
  range_key      = "album"

  attribute {
    name = "banda"
    type = "S"
  }

  attribute {
    name = "album"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }
}

# Fila no SQS
resource "aws_sqs_queue" "rock-albuns-messages" {
  name              = "rock-albuns-messages"
  kms_master_key_id = "alias/aws/sqs"
}


/* --------------------------------------------------
----------------- LAMBDA FUNCTIONS ------------------
------- Funções lambda da frente experts-aws --------
-------------------------------------------------- */

# Função experts-aws-lambda-101
resource "aws_lambda_function" "experts" {
  for_each      = var.lambda_configs
  function_name = each.key
  runtime       = var.runtime
  role          = each.value.iam_role

  s3_bucket = var.bucket_name
  s3_key    = each.value.s3_zip_key
  handler   = "lambda_function.py"
}
