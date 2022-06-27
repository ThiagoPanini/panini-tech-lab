/* --------------------------------------------------
FILE: main.tf @ iam module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste módulo é consolidar a criação
de elementos do iam (policies e roles) responsáveis
por permitir acesso à instância ec2 ao session manager.

RESOURCES: Os recursos aqui implantados serão:
  - Role IAM com Managed Policy
-------------------------------------------------- */

# Declarando forma de assumir a role para a ec2
data "aws_iam_policy_document" "instance-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# Definindo role para acesso de ec2 via ssm
resource "aws_iam_role" "tf-ec2-ssm-role" {
  name = "tf-ec2-ssm-role"
  managed_policy_arns = [
    var.ssm_policy_arn
  ]
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.instance-assume-role-policy.json
}

# Criando instance profile
resource "aws_iam_instance_profile" "tf-ec2-ssm-instance-profile" {
  name = "tf-ec2-ssm-instance-profile"
  role = aws_iam_role.tf-ec2-ssm-role.name
}
