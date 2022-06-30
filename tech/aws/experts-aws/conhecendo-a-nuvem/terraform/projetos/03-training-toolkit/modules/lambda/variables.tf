/* --------------------------------------------------
FILE: variables.tf @ lambda module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis cabíveis ao contexto da instância EC2
a ser construída em subnet privada e conexão via SSM
-------------------------------------------------- */

variable "runtime" {
  description = "Linguagem de programação das funções lambda criadas"
  type        = string
}

variable "bucket_name" {
  description = "Nome do bucket s3 criado para consolidação dos objetos do tookit de capacitação"
  type        = string
}

variable "lambda_configs" {
  type = map(any)
}
