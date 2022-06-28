/* --------------------------------------------------
FILE: main.tf @ storage module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é consolidar a criação
de um bucket s3 alvo de todo o armazemaneto dos
objetos a serem utilizados no toolkit de capacitação
aqui proposto.

RESOURCES: Os recursos aqui implantados serão:
  - Bucket S3
-------------------------------------------------- */

# Definindo bucket s3
resource "aws_s3_bucket" "private_training_bucket" {
  bucket        = var.bucket_name
  force_destroy = var.enable_force_destroy
}

# Definindo bloqueio de acesso público ao bucket
resource "aws_s3_bucket_public_access_block" "all_private" {
  bucket = aws_s3_bucket.private_training_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Criptografando bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.private_training_bucket.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

# Criando diretórios para o bucket
resource "aws_s3_object" "bucket_folders" {
  for_each               = toset(var.bucket_folders)
  bucket                 = aws_s3_bucket.private_training_bucket.bucket
  key                    = each.key
  server_side_encryption = "aws:kms"
}

# Realizando o upload de bases de dados
resource "aws_s3_object" "bucket_data_sources" {
  for_each = var.flag_data_path ? fileset(var.local_upload_data_path, "**") : []
  bucket   = aws_s3_bucket.private_training_bucket.bucket
  key      = "data/${each.value}"
  source   = "${var.local_upload_data_path}${each.value}"
  #etag                   = filemd5("${var.local_upload_data_path}${each.value}")
  server_side_encryption = "aws:kms"
}

# Realizando o upload de funções lambda
resource "aws_s3_object" "bucket_lambda_functions" {
  for_each = var.flag_lambda_path ? fileset(var.local_upload_lambda_path, "**") : []
  bucket   = aws_s3_bucket.private_training_bucket.bucket
  key      = "resources/lambda/${each.value}"
  source   = "${var.local_upload_lambda_path}${each.value}"
  #etag                   = filemd5("${var.local_upload_lambda_path}${each.value}")
  server_side_encryption = "aws:kms"
}
