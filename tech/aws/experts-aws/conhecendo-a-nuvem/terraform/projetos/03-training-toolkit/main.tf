/* --------------------------------------------------
FILE: main.tf @ root module

CONTEXT: Arquivo principal de construção da infra que,
através das informações contidas nos outros arquivos
.tf e nos módulos especificados em ./modules, realiza
a especificação dos elementos a serme implantados
nos providers declarados.

GOAL: O objetivo deste arquivo é definir toda a infra
necessária para o projeto "AWS Training Toolkit" onde
uma série de elementos de capacitação são disponibili-
zados aos usuários para que estes possam consultar
fontes práticas para aprimorar os conhecimentos nos
mais variados pilares da AWS.

MODULES: A organização da infra comporta os módulos:
  - ./modules/storage
  - ./modules/lambda
Especificações e detalhes sobre o conteúdo de cada
módulo poderá ser encontrado em seus respectivos
arquivos main.tf
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

/* --------------------------------------------------
----------------- MÓDULO: SECURITY ------------------
------- Criando chaves e segredos do projeto --------
-------------------------------------------------- */
module "security" {
  source = "./modules/security"

}


/* --------------------------------------------------
------------------ MÓDULO: STORAGE ------------------
-------- Consolidando o armazenamento no s3 ---------
-------------------------------------------------- */
module "storage" {
  source = "./modules/storage"

  bucket_name              = "aws-training-toolkit-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  enable_force_destroy     = var.enable_force_destroy
  bucket_folders           = var.bucket_folders
  local_upload_data_path   = var.local_upload_data_path
  local_upload_lambda_path = var.local_upload_lambda_path

  flag_upload_data_files      = true
  flag_upload_lambda_packages = false
}


/* --------------------------------------------------
-------------------- MÓDULO: IAM --------------------
-------- Políticas e roles para os recursos ---------
-------------------------------------------------- */
module "iam" {
  source = "./modules/iam"

  bucket_name = module.storage.bucket_name
}


/* --------------------------------------------------
------------------ MÓDULO: NETWORK ------------------
----------- Estrutura de redes do projeto -----------
-------------------------------------------------- */
module "network" {
  source = "./modules/network"

  vpc_cidr_block = var.vpc_cidr_block
}


/* --------------------------------------------------
------------------ MÓDULO: LAMBDA -------------------
---------- Funções lambda para exploração -----------
-------------------------------------------------- */
locals {
  lambda_configs = {
    "experts-aws-lambda-101" : {
      "s3_zip_key" = "services/lambda/pratica01-primeira-funcao/experts-aws-lambda-101.zip"
      "iam_role"   = module.iam.lambda-basic-role
    }
    "experts-aws-lambda-102" : {
      "s3_zip_key" = "services/lambda/pratica02-modulos-adicionais/experts-aws-lambda-102.zip"
      "iam_role"   = module.iam.lambda-basic-role
    }
    "experts-aws-lambda-103" : {
      "s3_zip_key" = "services/lambda/pratica03-integracao-s3/experts-aws-lambda-103.zip"
      "iam_role"   = module.iam.lambda-103
    }
    "experts-aws-lambda-104" : {
      "s3_zip_key" = "services/lambda/pratica04-gatilho-s3/experts-aws-lambda-104.zip"
      "iam_role"   = module.iam.lambda-104
    }
    "experts-aws-lambda-105" : {
      "s3_zip_key" = "services/lambda/pratica05-desliga-ec2/experts-aws-lambda-105.zip"
      "iam_role"   = module.iam.lambda-105
    }
    "experts-aws-lambda-106" : {
      "s3_zip_key" = "services/lambda/pratica06-elimina-ebs/experts-aws-lambda-106.zip"
      "iam_role"   = module.iam.lambda-106
    }
    "experts-aws-lambda-107" : {
      "s3_zip_key" = "services/lambda/pratica07-s3-to-dynamodb/experts-aws-lambda-107.zip"
      "iam_role"   = module.iam.lambda-107
    }
    "experts-aws-lambda-108" : {
      "s3_zip_key" = "services/lambda/pratica08-gatilho-sqs/experts-aws-lambda-108.zip"
      "iam_role"   = module.iam.lambda-108
    }
  }
}

# Chamada do módulo ./modules/lambda
module "lambda" {
  source = "./modules/lambda"

  lambda_configs = local.lambda_configs
  runtime        = var.lambda_runtime
  bucket_name    = module.storage.bucket_name
}

