# Configurando provider AWS
provider "aws" {
  region = "us-east-1"
  access_key = ""
  secret_key = ""
}

# Criando instância EC2
resource "aws_instance" "terraform-ec2" {
  ami = "ami-0cff7528ff583bf9a"
  instance_type = "t2.micro"
}
