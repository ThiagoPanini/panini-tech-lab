# Definindo variáveis de diretório local
DATA_PATH="/home/hadoop/panini-tech-lab/data/employee"
EMPLOYEE_LOCAL_PATH="${DATA_PATH}/general/employee.txt"
CONTRACT_LOCAL_PATH="${DATA_PATH}/contract/employee_contract.txt"

# Variáveis do HDFS
DATABASE_NAME="paninitechlab.db"
HDFS_DB_PATH="/user/hive/warehouse/${DATABASE_NAME}"

# Variáveis de tabelas do HDFS
EMPLOYEE_HDFS_PATH="${HDFS_DB_PATH}/employees"
CONTRACT_HDFS_PATH="${HDFS_DB_PATH}/employee_contract"

# Comando HDFS para mover arquivos para o sistema distribuído
hdfs dfs -put -f ${EMPLOYEE_LOCAL_PATH} ${EMPLOYEE_HDFS_PATH}
hdfs dfs -put -f ${CONTRACT_LOCAL_PATH} ${CONTRACT_HDFS_PATH}
