/* --------------------------------------------------
FILE: outputs.tf @ firewall module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é expor algumas variáveis,
atributos ou elementos criados neste módulo de firewall
para serem utilizadas na implantação dos recursos
computacionais no módulo compute.
-------------------------------------------------- */

# Exportando id do security group criado para a ec2
output "https_security_group_id" {
  description = "Identificação do security group que habilita a porta 443 para o intervalo da vpc"
  value       = aws_security_group.tf-https-vpc-sg.id
}
