/* --------------------------------------------------
FILE: outputs.tf @ iam module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
policies e roles IAM aqui descritas.
-------------------------------------------------- */

output "role_lambda_101" {
  description = "Role iam para função experts-aws-lambda-role-101"
  value       = aws_iam_role.lambda-101.arn
}
