/* --------------------------------------------------
FILE: main.tf @ network module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é consolidar a criação
dos elementos de rede do projeto para utilização dos
recursos em um ambiente totalmente privado na aws e
sem conexão com a internet pública.

RESOURCES: Os recursos aqui implantados serão:
  - VPC
  - Subnet
  - Route Table
  - Security Group
  - S3 Gateway Endpoint
  - DynamoDB Gateway Endpoint
-------------------------------------------------- */

# Definindo data sources para globalização do código
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}

# Definindo a VPC do projeto
resource "aws_vpc" "project" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    "Name" = "ttkit-vpc"
  }
}

# Definindo as Subnets do projeto
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.project.id
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block        = cidrsubnet(aws_vpc.project.cidr_block, 8, 0)

  tags = {
    "Name" = "ttkit-pvt-sub-1a"
  }
}

# Definindo a tabela de rotas da estrutura de redes
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.project.id

  tags = {
    "Name" = "ttkit-pvt-rt"
  }
}

# Criando associações das subnets à tabela de rotas
resource "aws_route_table_association" "private" {
  route_table_id = aws_route_table.private.id
  subnet_id      = aws_subnet.private.id
}
# TODO: associar rota aos gateway endpoints (levar esse bloco de cima pro final, após a criação dos endpoints)

# Criando security group restrito
resource "aws_security_group" "restricted" {
  name        = "ttkit-lambda-sg"
  description = "Permite trafego inbound e outbound de todos os enderecos provenientes de recursos no proprio security group"
  vpc_id      = aws_vpc.project.id
}

resource "aws_security_group_rule" "sg-inbound-all" {
  security_group_id        = aws_security_group.restricted.id
  type                     = "ingress"
  protocol                 = "-1"
  from_port                = 0
  to_port                  = 0
  source_security_group_id = aws_security_group.restricted.id
  description              = "Permite todo trafego de entrada para requisicoes vindas do proprio sg"
}

resource "aws_security_group_rule" "sg-outbound-https" {
  security_group_id = aws_security_group.restricted.id
  type              = "egress"
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_blocks       = ["0.0.0.0/0"]
  description       = "Permite saida para qualquer endereco sob o protocolo https na porta 443"
}


resource "aws_security_group_rule" "sg-outbound-all" {
  security_group_id        = aws_security_group.restricted.id
  type                     = "egress"
  protocol                 = "-1"
  from_port                = 0
  to_port                  = 0
  source_security_group_id = aws_security_group.restricted.id
  description              = "Permite todo o trafego de saida para recursos do proprio sg"
}
