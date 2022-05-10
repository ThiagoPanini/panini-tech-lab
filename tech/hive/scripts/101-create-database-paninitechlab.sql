# Definindo variáveis
SET hivevar:database=paninitechlab;

# Dropando banco de dados se existente
DROP DATABASE IF EXISTS ${database};

# Criando banco de dados
CREATE DATABASE IF NOT EXISTS ${database}
    COMMENT 'Banco de dados para exploração panini-tech-lab'
    LOCATION '/user/hive/warehouse/paninitechlab.db'
    WITH DBPROPERTIES ('creator'='paninit', 'date'='2022-05-09');