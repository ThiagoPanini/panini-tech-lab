# Definindo variáveis
SET hivevar:database=paninitechlab;
SET hivevar:tbl_employees=employees;

# Criando tabela
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