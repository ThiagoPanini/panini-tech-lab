/* --------------------------------------------------
FILE: variables.tf @ root module

CONTEXT: Arquivo de especificação de variáveis a serem
utilizadas no módulo root desta especificação de infra

GOAL: O objetivo deste arquivo é centralizar a declaração
de variáveis importantes para o projeto, se tornando 
então uma foram de agilizar o desenvolvimento do código
através de um local organizado para uso das variáveis.
As variáveis alocadas neste arquivo são de uso 
exclusivo do arquivo main.tf no módulo root.
-------------------------------------------------- */

# Variável utilizada para autenticação e configuração do provedor AWS
variable "aws_provider_config" {
  description = "Caminhos de configuração e credenciais do provedor AWS"
  type        = map(any)
  default = {
    "config"      = ["~/.aws/config"]
    "credentials" = ["~/.aws/credentials"]
  }
}

# Definição de bloco CIDR a ser utilizado na criação da VPC
variable "vpc_cidr_block" {
  description = "Bloco cidr que define o intervalo de endereços de ip da vpc"
  type        = string
  default     = "172.11.0.0/16"
}

# ARN da managed policy da AWS responsável por tais permissões
variable "ssm_policy_arn" {
  description = "ARN da política gerenciada pela AWS que permite conexões de uma EC2 via SSM"
  type        = string
  default     = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Definindo ami da instância
variable "instance_ami" {
  description = "Identificação da AMI utilizada para a instância EC2"
  type        = string
  default     = "ami-0cff7528ff583bf9a"
}

# Tipo da instância
variable "instance_type" {
  description = "Tipo da instância a ser construída e implantada"
  type        = string
  default     = "t2.micro"
}
