/* ----------------------------------------
MÓDULO: network

Declaração e especificação de recursos aws
relacionados à infraestrutura de redes do
projeto. Os blocos aqui consolidados irão
definir a VPC do projeto e suas respectivas
subnets para implantação dos recursos
computacionais definidos no módulo "compute"
---------------------------------------- */

# Definindo a VPC do projeto
resource "aws_vpc" "tf-app-vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
}
