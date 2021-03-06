# Definindo variáveis de diretório local
DATA_PATH="/home/hadoop/panini-tech-lab/data/employee"
EMPLOYEE_LOCAL_PATH="${DATA_PATH}/general/employee.txt"

# Variáveis do HDFS
DATABASE_NAME="paninitechlab.db"
HDFS_DB_PATH="/user/hive/warehouse/${DATABASE_NAME}"

# Variáveis de tabelas do HDFS
EMPOLOYEE_HDFS_PATH="${HDFS_DB_PATH}/employees"

# Comando HDFS para mover arquivos para o sistema distribuído
hdfs dfs -put ${EMPLOYEE_LOCAL_PATH} ${EMPLOYEE_HDFS_PATH}