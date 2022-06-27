/* --------------------------------------------------
FILE: variables.tf @ iam module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis cabíveis ao contexto de permissões na AWS
para que uma instância EC2 consiga se comunicar com
o serviço Systems Manager através do Session Manager.
-------------------------------------------------- */

# ARN da managed policy da AWS responsável por tais permissões
variable "ssm_policy_arn" {
  description = "ARN da política gerenciada pela AWS que permite conexões de uma EC2 via SSM"
  type        = string
}
