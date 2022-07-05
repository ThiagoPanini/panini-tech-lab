/* --------------------------------------------------
FILE: outputs.tf @ security module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
chaves KMS implantadas no arquivo main
-------------------------------------------------- */

# Exportando id da chave
output "kms_key_id" {
  description = "Identificação da chave KMS criada"
  value       = aws_kms_key.main.key_id
}

# Exportando arn da chave
output "kms_key_arn" {
  description = "ARN da chave KMS criada"
  value       = aws_kms_key.main.arn
}
