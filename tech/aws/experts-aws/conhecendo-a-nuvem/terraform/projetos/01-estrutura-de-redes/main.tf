/* --------------------------------------------------
FILE: main.tf @ root module

CONTEXT: Arquivo principal de construção da infra que,
através das informações contidas nos outros arquivos
.tf e nos módulos especificados em ./modules, realiza
a especificação dos elementos a serme implantados
nos providers declarados.

GOAL: O objetivo deste arquivo é consolidar e detalhar
os elementos para a criação de uma infraestrutura
completa de redes na AWS, incluindo recursos como VPC,
Subnets, Route Tables, NACL, Security Group, role IAM
e, por fim, uma instância EC2 que será utilizada para
validar uma conexão via SSM.

MODULES: A organização da infra comporta os módulos:
  - ./modules/network
  - ./modules/firewall
  . ./modules/iam
  - ./modules/compute
Especificações e detalhes sobre o conteúdo de cada
módulo poderá ser encontrado em seus respectivos
arquivos main.tf
-------------------------------------------------- */

# Chamada do módulo ./modules/network
module "network" {
  source = "./modules/network"

  vpc_cidr_block = var.vpc_cidr_block
}

# Chamada do módulo ./modules/firewall
module "firewall" {
  source = "./modules/firewall"

  vpc_id         = module.network.vpc_id
  vpc_cidr_block = module.network.vpc_cidr_block
  subnet_ids     = module.network.subnet_ids
}

# Chamada do módulo ./modules/iam
module "iam" {
  source = "./modules/iam"

  ssm_policy_arn = var.ssm_policy_arn
}

# Chamada do módulo ./modules/compute
module "compute" {
  source = "./modules/compute"

  instance_ami      = var.instance_ami
  instance_type     = var.instance_type
  subnet_ids        = module.network.subnet_ids
  security_group_id = module.firewall.https_security_group_id
  instance_profile  = module.iam.ssm_ec2_instance_profile
}
