# Definindo variáveis
SET hivevar:database=paninitechlab;
SET hivevar:table=employees;

# Criando tabela
CREATE TABLE IF NOT EXISTS ${database}.${table} (
    name STRING,
    work_place ARRAY<STRING>,
    gender_age STRUCT<gender:STRING, age:INT>,
    skills_score MAP<STRING, INT>,
    depart_title MAP<STRING, ARRAY<STRING>>
)
ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;