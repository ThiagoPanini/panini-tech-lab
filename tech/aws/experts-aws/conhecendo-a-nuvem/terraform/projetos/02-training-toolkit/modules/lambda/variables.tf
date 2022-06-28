/* --------------------------------------------------
FILE: variables.tf @ lambda module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis cabíveis ao contexto da instância EC2
a ser construída em subnet privada e conexão via SSM
-------------------------------------------------- */

variable "bucket_name" {
  description = "Nome do bucket s3 criado para consolidação dos objetos do tookit de capacitação"
  type        = string
}

variable "s3_functions_keys" {
  description = "Dicionário que referencia as chaves de cada função Lambda no bucket s3"
  type        = map(string)
}

variable "lambda_config" {
  type = map(any)
}
