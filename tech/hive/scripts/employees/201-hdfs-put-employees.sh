# Definindo variáveis
EMPLOYEE_PATH="/home/hadoop/panini-tech-lab/data/employee/general/employee.txt"
DATABASE_NAME="paninitechlab.db"
TABLE_NAME="employees"
HDFS_PATH="/user/hive/warehouse/${DATABASE_NAME}/${TABLE_NAME}"

# Comando HDFS para mover arquivos para o sistema distribuído
hdfs dfs -put ${EMPLOYEE_PATH} ${HDFS_PATH}