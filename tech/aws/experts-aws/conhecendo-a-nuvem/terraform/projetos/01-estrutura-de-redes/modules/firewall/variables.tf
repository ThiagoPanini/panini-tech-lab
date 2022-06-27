/* --------------------------------------------------
FILE: variables.tf @ firewall module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis cabíveis ao contexto de firewalls a nível
de instância (security groups) e a nível de subnets
(networl acl).
-------------------------------------------------- */

variable "vpc_id" {
  description = "Id da vpc criada para implantação dos recursos do projeto"
  type        = string
}

variable "vpc_cidr_block" {
  description = "Bloco cidr da vpc criada para implantação dos recursos do projeto"
  type        = string
}

variable "subnet_ids" {
  description = "Ids de cada subnet declarada no projeto"
  type        = map(string)
}
