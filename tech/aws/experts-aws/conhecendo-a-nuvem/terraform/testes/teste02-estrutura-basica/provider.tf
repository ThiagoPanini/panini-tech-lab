# Definindo provedores do projeto
provider "aws" {
  shared_config_files      = var.aws_provider_config["config"]
  shared_credentials_files = var.aws_provider_config["credentials"]
}
