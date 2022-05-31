# Importando biblioteca de log
import logging

# Definindo constantes do módulo
LOG_FORMAT = '%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s'

# Definindo função para configuração de objeto logger
def log_config(logger, level=logging.DEBUG, log_format=LOG_FORMAT):

    # Configurando level e formatação do objeto
    logger.setLevel(level)
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    return logger
