# Variável com parâmetros de configuração
variable "aws_provider_config" {
    description = "Caminhos de configuração e credenciais do provedor AWS"
    type = map
    default = {
        "config" = ["~/.aws/config"]
        "credentials" = ["~/.aws/credentials"]
    }
}
