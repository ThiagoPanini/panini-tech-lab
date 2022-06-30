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

data "aws_iam_policy_document" "lambda-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}


/* --------------------------------------------------
------------------- IAM POLICIES --------------------
------- Políticas que irão integrar roles IAM -------
-------------------------------------------------- */

resource "aws_iam_policy" "lambda-logging" {
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
          "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/experts-aws-lambda-*:*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "s3-get-csv-data" {
  name        = "s3-get-csv-data"
  path        = "/"
  description = "Permite a coleta de objetos csv de bucket especifico"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "S3GetCSVObject",
        "Effect" : "Allow",
        "Action" : "s3:GetObject",
        "Resource" : "arn:aws:s3:::${var.bucket_name}/lambda/input/*.csv"
      }
    ]
  })
}

resource "aws_iam_policy" "s3-put-json-data" {
  name        = "s3-put-json-data"
  path        = "/"
  description = "Permite a escrita de objetos json em bucket especifico"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "S3PutJSONObject",
        "Effect" : "Allow",
        "Action" : "s3:PutObject",
        "Resource" : "arn:aws:s3:::${var.bucket_name}/lambda/output/*.json"
      }
    ]
  })
}

resource "aws_iam_policy" "ec2-start-stop-instance" {
  name        = "ec2-start-stop-instance"
  path        = "/"
  description = "Permite inicializar e interromper instancias ec2"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "ManageEC2Instances",
        "Effect" : "Allow",
        "Action" : [
          "ec2:DescribeInstances",
          "ec2:DescribeRegions",
          "ec2:StartInstances",
          "ec2:StopInstances"
        ],
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_policy" "ec2-delete-ebs-volumes" {
  name        = "ec2-delete-ebs-volumes"
  path        = "/"
  description = "Permite descrever e deletar volumes ebs"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "ManageEBSVolumes",
          "Effect" : "Allow",
          "Action" : [
            "ec2:DeleteVolume",
            "ec2:DescribeRegions",
            "ec2:DescribeVolumes"
          ],
          "Resource" : "*"
        }
      ]
    }
  )
}

resource "aws_iam_policy" "s3-json-to-dynamodb" {
  name        = "s3-json-to-dynamodb"
  path        = "/"
  description = "Permite coletar objetos json de bucket e escrever itens no dynamodb"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "S3GetJSONData",
          "Effect" : "Allow",
          "Action" : "s3:GetObject",
          "Resource" : "arn:aws:s3:::${var.bucket_name}/lambda/output/*.json"
        },
        {
          "Sid" : "DynamoDBManageTables",
          "Effect" : "Allow",
          "Action" : [
            "dynamodb:ListTables",
            "dynamodb:CreateTable",
            "dynamodb:DescribeTable"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "DynamoDBPutItem",
          "Effect" : "Allow",
          "Action" : "dynamodb:PutItem",
          "Resource" : "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/rock-albuns"
        }
      ]
    }
  )
}

resource "aws_iam_policy" "sqs-msgs-to-dynamodb" {
  name        = "sqs-msgs-to-dynamodb"
  path        = "/"
  description = "Permite receber e coletar mensagens do sqs e escrever itens no dynamodb"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "SQSGetMessages",
          "Effect" : "Allow",
          "Action" : [
            "sqs:Get*",
            "sqs:List*",
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage"
          ],
          "Resource" : "arn:aws:sqs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:rock-albuns-messages"
        },
        {
          "Sid" : "DynamoDBManageTables",
          "Effect" : "Allow",
          "Action" : [
            "dynamodb:ListTables",
            "dynamodb:CreateTable",
            "dynamodb:DescribeTable"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "DynamoDBPutItem",
          "Effect" : "Allow",
          "Action" : "dynamodb:PutItem",
          "Resource" : "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/rock-albuns"
        }
      ]
    }
  )
}


/* --------------------------------------------------
--------------------- IAM ROLES ---------------------
------- Roles IAM para utilização em serviços -------
-------------------------------------------------- */

# Role que comporta operações padrão de log para funções lambda
resource "aws_iam_role" "lambda-basic-role" {
  name                = "experts-aws-lambda-basic-role"
  assume_role_policy  = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [aws_iam_policy.lambda-logging.arn]
}

# Role para a função experts-aws-lambda-103
resource "aws_iam_role" "lambda-103" {
  name               = "experts-aws-lambda-role-103"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [
    aws_iam_policy.lambda-logging.arn,
    aws_iam_policy.s3-get-csv-data.arn
  ]
}

# Role para a função experts-aws-lambda-104
resource "aws_iam_role" "lambda-104" {
  name               = "experts-aws-lambda-role-104"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [
    aws_iam_policy.lambda-logging.arn,
    aws_iam_policy.s3-get-csv-data.arn,
    aws_iam_policy.s3-put-json-data.arn
  ]
}

# Role para a função experts-aws-lambda-105
resource "aws_iam_role" "lambda-105" {
  name               = "experts-aws-lambda-role-105"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [
    aws_iam_policy.lambda-logging.arn,
    aws_iam_policy.ec2-start-stop-instance.arn
  ]
}

# Role para a função experts-aws-lambda-106
resource "aws_iam_role" "lambda-106" {
  name               = "experts-aws-lambda-role-106"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [
    aws_iam_policy.lambda-logging.arn,
    aws_iam_policy.ec2-delete-ebs-volumes.arn
  ]
}

# Role para a função experts-aws-lambda-107
resource "aws_iam_role" "lambda-107" {
  name               = "experts-aws-lambda-role-107"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [
    aws_iam_policy.lambda-logging.arn,
    aws_iam_policy.s3-json-to-dynamodb.arn
  ]
}

# Role para a função experts-aws-lambda-108
resource "aws_iam_role" "lambda-108" {
  name               = "experts-aws-lambda-role-108"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
  managed_policy_arns = [
    aws_iam_policy.lambda-logging.arn,
    aws_iam_policy.sqs-msgs-to-dynamodb.arn
  ]
}
