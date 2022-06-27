/* ----------------------------------------
MODULES: modules/network
FILE: variables.tf

Declaração de variáveis relacionadas a recursos
de redes a serem implantados na infraestrutura
---------------------------------------- */

variable "vpc_cidr_block" {
  description = "Bloco cidr que define o intervalo de endereços de ip da vpc"
  type        = string
  default     = "172.11.0.0/16"
}

variable "subnet_config" {
  description = "Configurações de blocos cidr para cada subnet em cada zona de disponibilidade"
  type        = map(any)
  default = {
    "us-east-1a" = {
      "private" = "172.11.0.0/24"
    },
    "us-east-1b" = {
      "private" = "172.11.1.0/24"
    }
  }
}
