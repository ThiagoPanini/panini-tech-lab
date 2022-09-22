# Importando bibliotecas
from pyspark.sql import SparkSession

# Inicializando sessão
spark = SparkSession\
    .builder\
    .appName(__file__)\
    .master("local[*]")\
    .getOrCreate()

# Criando DataFrames
df1 = spark.range(0, 5)
df2 = spark.range(5, 10)
df = df1.union(df2)

# Mostrando e coletando dados no driver
df.show()
print(df.collect())

# Encerrando sessão
spark.stop()
