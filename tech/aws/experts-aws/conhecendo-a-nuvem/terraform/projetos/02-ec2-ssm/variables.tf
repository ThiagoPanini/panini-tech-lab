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

variable "aws_provider_config" {
  description = "Caminhos de configuração e credenciais do provedor AWS"
  type        = map(any)
  default = {
    "config"      = ["~/.aws/config"]
    "credentials" = ["~/.aws/credentials"]
  }
}

variable "vpc_cidr_block" {
  description = "Bloco CIDR que define o intervalo de endereços possíveis dentro de uma VPC"
  type        = string
  default     = "172.11.0.0/16"
}

variable "ssm_policy_arn" {
  description = "ARN da role que permite conexão à uma ec2 via ssm"
  type        = string
  default     = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

variable "ami_mapping" {
  description = "Identificação da AMI utilizada para a instância EC2"
  type        = map(any)
  default = {
    "sa-east-1" : "ami-037c192f0fa52a358"
    "us-east-1" : "ami-0cff7528ff583bf9a"
  }
}

variable "instance_type" {
  description = "Tipo da instância a ser construída e implantada"
  type        = string
  default     = "t2.micro"
}
