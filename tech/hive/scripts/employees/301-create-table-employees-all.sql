# Definindo variáveis
SET hivevar:database=paninitechlab;
SET hivevar:tbl_employees=employees;
SET hivevar:tbl_contract=employee_contract;

# Dropando tabelas caso existentes
DROP TABLE IF EXISTS ${database}.${tbl_employees};
DROP TABLE IF EXISTS ${database}.${tbl_contract};

# Criando tabela de funcionários
CREATE TABLE IF NOT EXISTS ${database}.${tbl_employees} (
    name STRING COMMENT "Nome do funcionário",
    work_place ARRAY<STRING> COMMENT "Campo com informações de local de trabalho",
    gender_age STRUCT<gender:STRING, age:INT> COMMENT "Gênero e idade do funcionário",
    skills_score MAP<STRING, INT> COMMENT "Habilidades e proficiência do funcionário em data habilidade",
    depart_title MAP<STRING, ARRAY<STRING>> COMMENT "Departamento e cargo do funcionário"
)
ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;

# Criando tabela de contratos de trabalho
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
