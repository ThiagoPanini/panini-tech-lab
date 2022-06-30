/* --------------------------------------------------
FILE: variables.tf @ iam module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para a criação de políticas e roles iam
responsáveis por permitir acessos aos recursos 
utilizados neste projeto
-------------------------------------------------- */

variable "bucket_name" {
  description = "Nome do bucket s3 criado para alocação dos recursos do toolkit de capacitação"
  type        = string
}
