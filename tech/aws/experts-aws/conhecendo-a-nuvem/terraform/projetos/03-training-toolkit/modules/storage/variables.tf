/* --------------------------------------------------
FILE: variables.tf @ storage module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para toda a construção do ambiente de
armazenamento dos dados e insumos no s3
-------------------------------------------------- */

variable "bucket_name" {
  description = "Nome do bucket s3 a ser criado para consolidação dos objetos do tookit de capacitação"
  type        = string
}

variable "enable_force_destroy" {
  description = "Habilita eliminação de objetos do bucket na aplicação do terraform destroy"
  type        = bool
}

variable "bucket_folders" {
  description = "Lista de folders a serem criados no bucket alvo para posterior recepção dos objetos"
  type        = list(string)
}

variable "local_upload_data_path" {
  description = "Caminho de armazenamento dos dados locais que serão inseridos no s3"
  type        = string
}

variable "flag_upload_data_files" {
  description = "Flag para realização do upload de bases de dados"
  type        = bool
  default     = true
}

variable "local_upload_lambda_path" {
  description = "Caminho local de armazenamento das funções lambda que serão inseridas no s3"
  type        = string
}

variable "flag_upload_lambda_packages" {
  description = "Flag para realização do upload de funções lambda"
  type        = bool
  default     = true
}
