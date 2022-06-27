/* ----------------------------------------
MÓDULO: root

Declaração dos módulos presentes no projeto
para implantação da infraestrutura de redes
e elementos computacionais a serem implantados
nesta configuração. Os módulos utilizados são:

- ./modules/network
- ./modules/compute
---------------------------------------- */

# Módulo network
module "network" {
  source = "./modules/network"

}
