# Definindo variáveis
SET hivevar:database=paninitechlab;
SET hivevar:tbl_contract=employee_contract;

# Definindo script de criação de tabela
CREATE TABLE IF NOT EXISTS ${database}.${tbl_contract} (
    name STRING COMMENT "Nome do funcionário",
    dept_num INT COMMENT "Número do departamento do funcionário",
    employee_id INT COMMENT "Identificador do funcionário",
    salary INT COMMENT "Salário do funcionário",
    type INT COMMENT "Tipo de jornada do funcionário",
    start_date DATE COMMENT "Data de início do contrato"
)
ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;