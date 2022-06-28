/* --------------------------------------------------
FILE: variables.tf @ root module

CONTEXT: Arquivo de especificação de variáveis a serem
utilizadas no módulo root desta especificação de infra

GOAL: O objetivo deste arquivo é centralizar a declaração
de variáveis importantes para o projeto, se tornando 
então uma foram de agilizar o desenvolvimento do código
através de um local organizado para uso das variáveis.
As variáveis alocadas neste arquivo são de uso 
exclusivo do arquivo main.tf no módulo root.
-------------------------------------------------- */

variable "aws_provider_config" {
  description = "Caminhos de configuração e credenciais do provedor AWS"
  type        = map(any)
  default = {
    "config"      = ["~/.aws/config"]
    "credentials" = ["~/.aws/credentials"]
  }
}

variable "enable_force_destroy" {
  description = "Habilita eliminação de objetos do bucket na aplicação do terraform destroy"
  type        = bool
  default     = false
}

variable "bucket_folders" {
  description = "Lista de folders a serem criados no bucket alvo para posterior recepção dos objetos"
  type        = list(string)
  default     = ["data/", "resources/lambda/", "resources/glue/"]
}

variable "local_upload_data_path" {
  description = "Caminho local de armazenamento das bases de dados que serão inseridos no s3"
  type        = string
  default     = "../../../../../../../data/"
}

variable "local_upload_lambda_path" {
  description = "Caminho local de armazenamento das funções lambda que serão inseridas no s3"
  type        = string
  default     = "../../../../core-services-lambda/"
}
