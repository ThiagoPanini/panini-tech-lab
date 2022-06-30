/* --------------------------------------------------
FILE: outputs.tf @ storage module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é expor algumas variáveis,
atributos ou elementos criados no contexto de armazenamento
dos insumos do toolkit de capacitação para serem utilizados
em módulos posteriores deste projeto de implantação
de infraestrutura.
-------------------------------------------------- */

# Retornando informações do bucket criado
output "bucket_name" {
  value = aws_s3_bucket.private_training_bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.private_training_bucket.arn
}
