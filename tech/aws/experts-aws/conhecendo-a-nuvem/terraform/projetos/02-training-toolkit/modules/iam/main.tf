/* --------------------------------------------------
FILE: main.tf @ iam module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é centralizar a criação
de policies e roles do IAM a serem utilizadas pelos
demais recursos e serviços deste projeto de infra

RESOURCES: Os recursos aqui implantados serão:
  - IAM Policies
  - IAM Roles
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}


/* --------------------------------------------------
------------------- IAM POLICIES --------------------
------- Políticas que irão integrar roles IAM -------
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
--------------------- IAM ROLES ---------------------
------- Roles IAM para utilização em serviços -------
-------------------------------------------------- */

# Role para a função experts-aws-lambda-101
resource "aws_iam_role" "lambda-101" {
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

resource "aws_iam_role_policy_attachment" "lambda-101" {
  role       = aws_iam_role.lambda-101.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}


