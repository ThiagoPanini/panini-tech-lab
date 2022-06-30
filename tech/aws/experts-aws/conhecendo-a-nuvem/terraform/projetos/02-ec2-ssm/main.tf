/* --------------------------------------------------
FILE: main.tf @ root module

CONTEXT: Arquivo principal de construção da infra que,
através das informações contidas nos outros arquivos
.tf e nos módulos especificados em ./modules, realiza
a especificação dos elementos a serme implantados
nos providers declarados.

GOAL: O objetivo deste arquivo é definir toda a infra
necessária para a implantação de uma instância ec2
em um ambiente totalmente privado na aws, contemplando
uma conexão via ssm.

MODULES: A organização da infra comporta os módulos:
  - ./modules/network
  - ./modules/iam
  - ./modules/compute
Especificações e detalhes sobre o conteúdo de cada
módulo poderá ser encontrado em seus respectivos
arquivos main.tf
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# Chamando módulo network
module "network" {
  source = "./modules/network"

  vpc_cidr_block = var.vpc_cidr_block
}


# Chamando módulo iam
module "iam" {
  source = "./modules/iam"

  ssm_policy_arn = var.ssm_policy_arn
}

# Chamando módulo compute
module "compute" {
  source = "./modules/compute"

  instance_ami      = var.ami_mapping[data.aws_region.current.name]
  instance_type     = var.instance_type
  subnet_id         = module.network.subnet_id
  security_group_id = module.network.security_group_id
  instance_profile  = module.iam.instance_profile_name
}
