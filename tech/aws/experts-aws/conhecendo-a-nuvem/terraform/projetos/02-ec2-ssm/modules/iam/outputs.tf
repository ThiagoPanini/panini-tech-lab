/* --------------------------------------------------
FILE: outputs.tf @ iam module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
policies e roles IAM aqui descritas.
-------------------------------------------------- */

output "instance_profile_name" {
  description = "Role iam com permissões para que instâncias ec2 "
  value       = aws_iam_instance_profile.ec2.name
}
