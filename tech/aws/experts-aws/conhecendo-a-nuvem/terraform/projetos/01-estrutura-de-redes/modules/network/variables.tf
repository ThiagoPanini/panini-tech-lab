/* --------------------------------------------------
FILE: variables.tf @ network module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis cabíveis ao contexto de redes para os
recursos implantados no módulo main.tf. Entre as
variáveis consideradas, será possível encontrar
blocos CIDR para facilitar a definição do intervalo
de endereços de uma VPC e de suas respectivas subnets.
-------------------------------------------------- */

variable "vpc_cidr_block" {
  description = "Bloco cidr que define o intervalo de endereços de ip da vpc"
  type        = string
}

variable "security_group_id" {
  description = "Id do security group a ser associado aos endpoints de vpc"
  type        = string
}
