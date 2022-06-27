/* --------------------------------------------------
FILE: variables.tf @ compute module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis cabíveis ao contexto da instância EC2
a ser construída em subnet privada e conexão via SSM
-------------------------------------------------- */

# Definindo ami da instância
variable "instance_ami" {
  description = "Identificação da AMI utilizada para a instância EC2"
  type        = string
}

# Tipo da instância
variable "instance_type" {
  description = "Tipo da instância a ser construída e implantada"
  type        = string
}

# Subnets para implantação das instâncias
variable "subnet_id" {
  description = "Ids de subnet privada utilizada no projeto"
  type        = string
}

# Grupos de segurança
variable "security_group_id" {
  description = "Id do security group para implantação da instância"
  type        = string
}

# Instance profile
variable "instance_profile" {
  description = "Instance profile para conexão da EC2 via Session Manager"
  type        = string
}
