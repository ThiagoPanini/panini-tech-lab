# Configurando providers
provider "aws" {
    shared_config_files = ["~/.aws/config"]
    shared_credentials_files = ["~/.aws/credentials"]
}

# Definindo recursos
resource "aws_instance" "tf-ec2" {
  ami = "ami-0cff7528ff583bf9a"
  instance_type = "t2.micro"
  availability_zone = "us-east-1a"
}