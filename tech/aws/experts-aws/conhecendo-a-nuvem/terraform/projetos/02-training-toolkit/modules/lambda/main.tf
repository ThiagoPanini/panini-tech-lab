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



/* --------------------------------------------------
----------------- LAMBDA FUNCTIONS ------------------
------- Funções lambda da frente experts-aws --------
-------------------------------------------------- */

# Função experts-aws-lambda-101
resource "aws_lambda_function" "experts" {
  for_each      = var.lambda_config
  function_name = each.key
  runtime       = "python3.8"

  s3_bucket = var.bucket_name
  s3_key    = each.value["s3_key"]
  role      = aws_iam_role.pratica01.arn
  handler   = "lambda_function.py"
}
