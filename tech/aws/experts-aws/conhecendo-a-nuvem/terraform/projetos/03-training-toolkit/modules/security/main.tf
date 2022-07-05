/* --------------------------------------------------
FILE: main.tf @ security module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é implantar recursos
relacionados à segurança da aplicação/projeto, como
chaves KMS, segredos no Secrets Manager, entre outros

RESOURCES: Os recursos aqui implantados serão:
  - KMS
  - Secrets Manager
-------------------------------------------------- */

# Criando chave KMS
resource "aws_kms_key" "main" {
  description = "Chave KMS utilizada para criptografia nos recursos implantados"
}

resource "aws_kms_alias" "main" {
  name          = "alias/ttkit"
  target_key_id = aws_kms_key.main.key_id
}
