/* --------------------------------------------------
FILE: main.tf @ compute module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste módulo é consolidar a criação
dos elementos computacionais representados por 
instâncias ec2

RESOURCES: Os recursos aqui implantados serão:
  - EC2
-------------------------------------------------- */

# Coletando chave kms para volume ebs
data "aws_kms_key" "ebs" {
  key_id = "alias/aws/ebs"
}

# Inicializando instância EC2
resource "aws_instance" "tf-ec2" {
  ami                    = var.instance_ami
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]
  iam_instance_profile   = var.instance_profile

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 8
    delete_on_termination = true
    encrypted             = true
    #kms_key_id            = data.aws_kms_key.ebs.key_id
  }
}
