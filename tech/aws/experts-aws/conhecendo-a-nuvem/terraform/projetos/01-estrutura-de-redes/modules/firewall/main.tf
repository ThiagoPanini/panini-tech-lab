/* --------------------------------------------------
FILE: main.tf @ firewall module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é consolidar a criação
dos elementos de segurança e firewalls do projeto a
nível de instância e a nível de subnet.

RESOURCES: Os recursos aqui implantados serão:
  - Nework Access Control List (NACL)
  - Security Group
-------------------------------------------------- */

# Definindo nacl do projeto e associando subnets
resource "aws_network_acl" "tf-pvt-nacl" {
  vpc_id = var.vpc_id

  ingress {
    rule_no    = 100
    protocol   = "tcp"
    from_port  = 443
    to_port    = 443
    cidr_block = var.vpc_cidr_block
    action     = "allow"
  }

  egress {
    rule_no    = 100
    protocol   = "tcp"
    from_port  = 1024
    to_port    = 65535
    cidr_block = "0.0.0.0/0"
    action     = "allow"
  }

  tags = {
    "Name" = "tf-pvt-nacl"
  }
}

resource "aws_network_acl_association" "tf-nacl-association-a" {
  network_acl_id = aws_network_acl.tf-pvt-nacl.id
  subnet_id      = var.subnet_ids["az-a"]
}

resource "aws_network_acl_association" "tf-nacl-association-b" {
  network_acl_id = aws_network_acl.tf-pvt-nacl.id
  subnet_id      = var.subnet_ids["az-b"]
}

# Definindo security group para instância ec2
resource "aws_security_group" "tf-https-vpc-sg" {
  name        = "tf-https-vpc-sg"
  description = "Permite trafego https do cidr block da vpc"
  vpc_id      = var.vpc_id

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = [var.vpc_cidr_block]
    description = "Porta 443 do intervalo da vpc"
  }

  tags = {
    "Name" = "tf-https-vpc-sg"
  }
}
