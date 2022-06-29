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

# Chamada do módulo ./modules/storage
module "storage" {
  source = "./modules/storage"

  bucket_name              = "aws-training-toolkit-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  enable_force_destroy     = var.enable_force_destroy
  bucket_folders           = var.bucket_folders
  local_upload_data_path   = var.local_upload_data_path
  local_upload_lambda_path = var.local_upload_lambda_path

  flag_data_path   = false
  flag_lambda_path = true
}

# Chamada do módulo ./modules/iam
module "iam" {
  source = "./modules/iam"
}

# Definição de elemento para facilitar a criação das funções
locals {
  lambda_configs = {
    "experts-aws-lambda-101" : {
      "s3_zip_key" = "resources/lambda/pratica01-primeira-funcao/experts-aws-lambda-101.zip"
      "iam_role"   = module.iam.role_lambda_101
    }
  }
}

# Chamada do módulo ./modules/lambda
/* module "lambda" {
  source = "./modules/lambda"

  lambda_configs = local.lambda_configs
  runtime        = var.lambda_runtime
  bucket_name    = module.storage.bucket_name
}
*/