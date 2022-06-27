/* --------------------------------------------------
FILE: outputs.tf @ iam module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é expor algumas variáveis,
atributos ou elementos para relacionamento das permissões
(roles e políticas IAM) em instâncias EC2
-------------------------------------------------- */

# Instance profile
output "ssm_ec2_instance_profile" {
  description = "Instance profile para conexão da EC2 via Session Manager"
  value       = aws_iam_instance_profile.tf-ec2-ssm-instance-profile.name
}
