/* --------------------------------------------------
FILE: main.tf @ iam module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é centralizar a criação
de policies e roles do IAM a serem utilizadas pelos
demais recursos e serviços deste projeto de infra

RESOURCES: Os recursos aqui implantados serão:
  - IAM Policies
  - IAM Roles
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "ec2-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}


/* --------------------------------------------------
--------------------- IAM ROLES ---------------------
------- Roles IAM para utilização em serviços -------
-------------------------------------------------- */

# Role que comporta operações padrão de log para funções lambda
resource "aws_iam_role" "ssm" {
  name                = "tf-ec2-ssm-role"
  assume_role_policy  = data.aws_iam_policy_document.ec2-assume-role-policy.json
  managed_policy_arns = [var.ssm_policy_arn]
}

resource "aws_iam_instance_profile" "ec2" {
  name = "tf-ec2-ssm-instance-profile"
  role = aws_iam_role.ssm.name
}
