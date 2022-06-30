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

variable "ssm_policy_arn" {
  description = "ARN da role que permite conexão à uma ec2 via ssm"
  type        = string
}
