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

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = data.aws_vpc.default.id
}

/* --------------------------------------------------
[LAMBDA ROLES] Definição de roles para funções Lambda

1. Definição de políticas a serem anexadas às roles
-------------------------------------------------- */
resource "aws_iam_policy" "lambda_logging" {
  name        = "cloudwatch-lambda-logging"
  path        = "/"
  description = "Politica que permite escrita de logs no CloudWatch"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "logs:CreateLogGroup",
        "Resource" : "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : [
          "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/experts-aws-lambda-101:*"
        ]
      }
    ]
  })
}

/* --------------------------------------------------
[LAMBDA ROLES] Definição de roles para funções Lambda

1. Definição de roles com políticas anexadas
-------------------------------------------------- */

resource "aws_iam_role" "pratica01" {
  name = "experts-aws-lambda-role-101"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Effect" : "Allow",
        "Sid" : ""
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "pratica01" {
  role       = aws_iam_role.pratica01.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}


/* --------------------------------------------------
[PRÁTICA 01] Primeira função Lambda
-------------------------------------------------- */
#resource "aws_lambda_function" "pratica01" {
#  function_name = "experts-aws-lambda-101"
#  runtime       = "python3.8"
#  s3_bucket     = var.bucket_name
#  s3_key        = var.s3_functions_keys["pratica01"]
#  role          = aws_iam_role.pratica01.arn
#  handler       = "lambda_function.py"
#}

resource "aws_lambda_function" "experts" {
  for_each      = var.lambda_config
  function_name = each.key
  runtime       = "python3.8"

  s3_bucket = var.bucket_name
  s3_key    = each.value["s3_key"]
  role      = aws_iam_role.pratica01.arn
  handler   = "lambda_function.py"

  vpc_config {
    subnet_ids         = data.aws_subnet_ids.all.ids
    security_group_ids = ["sg-0cbc8010789658c80"]
  }

}
