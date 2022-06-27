# Definindo VPC
resource "aws_vpc" "tf-vpc" {
  cidr_block           = var.network_config["vpc_cidr_block"]
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    "Name" = "tf-vpc"
  }
}

# Definindo subnet
resource "aws_subnet" "tf-pvt-sub-1a" {
  vpc_id            = aws_vpc.tf-vpc.id
  cidr_block        = var.network_config["subnet_cidr_block"]
  availability_zone = "us-east-1a"

  tags = {
    "Name" = "tf-pvt-sub-1a"
  }
}

# Definindo interface de rede
resource "aws_network_interface" "tf-eni" {
  subnet_id = aws_subnet.tf-pvt-sub-1a.id
}

# Definindo recursos
resource "aws_instance" "tf-ec2" {
  ami           = var.ec2_config["ami_id"]
  instance_type = var.ec2_config["instance_type"]

  network_interface {
    network_interface_id = aws_network_interface.tf-eni.id
    device_index         = 0
  }

  tags = {
    "Name" = "tf-ec2"
  }
}
