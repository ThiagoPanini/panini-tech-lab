/* --------------------------------------------------
FILE: main.tf @ network module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é consolidar a criação
dos elementos de rede do projeto, incluindo uma VPC
e duas Subnets (uma em cada AZ) na AWS. As variáveis
necessárias para parametrização dos recursos poderão
ser encontradas no arquivo variables.tf neste mesmo
módulo.

RESOURCES: Os recursos aqui implantados serão:
  - VPC
  - Subnets
  - Route Table
  - VPC Endpoints
-------------------------------------------------- */

# Definindo data sources para globalização do código
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}

# Definindo a VPC do projeto
resource "aws_vpc" "tf-vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    "Name" = "tf-vpc"
  }
}

# Definindo as Subnets do projeto
resource "aws_subnet" "tf-pvt-sub-1a" {
  vpc_id            = aws_vpc.tf-vpc.id
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block        = cidrsubnet(aws_vpc.tf-vpc.cidr_block, 8, 0)

  tags = {
    "Name" = "tf-pvt-sub-1a"
  }
}

# Definindo a tabela de rotas da estrutura de redes
resource "aws_route_table" "tf-pvt-rt" {
  vpc_id = aws_vpc.tf-vpc.id

  tags = {
    "Name" = "tf-pvt-rt"
  }
}

# Criando associações das subnets à tabela de rotas
resource "aws_route_table_association" "tf-pvt-sub-a" {
  route_table_id = aws_route_table.tf-pvt-rt.id
  subnet_id      = aws_subnet.tf-pvt-sub-1a.id
}

# Criando endpoints para conexão de EC2 via SSM
resource "aws_vpc_endpoint" "ssm" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ssm"
  vpc_id              = aws_vpc.tf-vpc.id
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.tf-pvt-sub-1a.id
  ]

  security_group_ids = [
    var.security_group_id
  ]
}

resource "aws_vpc_endpoint" "ssmmessages" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ssmmessages"
  vpc_id              = aws_vpc.tf-vpc.id
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.tf-pvt-sub-1a.id
  ]

  security_group_ids = [
    var.security_group_id
  ]
}

resource "aws_vpc_endpoint" "ec2messages" {
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ec2messages"
  vpc_id              = aws_vpc.tf-vpc.id
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.tf-pvt-sub-1a.id
  ]

  security_group_ids = [
    var.security_group_id
  ]
}
