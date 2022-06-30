/* --------------------------------------------------
FILE: outputs.tf @ network module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é expor algumas variáveis,
atributos ou elementos criados neste módulo de redes
para serem utilizados em outros módulos ou mesmo na 
especificação da infraestrutura no arquivo de
configuração root. De maneira prática, o ID da VPC ou
bloco cidr podem ser informações úteis a serem utilizados
em uma série de outros recursos declarados no projeto.
-------------------------------------------------- */

# Exportando id da vpc como saída
output "vpc_id" {
  value       = aws_vpc.project.id
  description = "Id da vpc criada no módulo network"
}

# Exportando cidr block da vpc
output "vpc_cidr_block" {
  value       = aws_vpc.project.cidr_block
  description = "Id da vpc criada no módulo network"
}

# Exportando informações das subnets
output "subnet_id" {
  value       = aws_subnet.private.id
  description = "Id de subnet privada para definição de regras em outros módulos"
}

# Explorando id do security group criado
output "security_group_id" {
  value       = aws_security_group.restricted.id
  description = "Id do security group criado para a instância ec2"
}
