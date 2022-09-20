# Importando bibliotecas
import sys
import argparse

# Criando objeto para obtenção dos argumentos
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    usage="python script-teste.py <range>",
    description="Imprime um intervalo sequencial de inteiros"
)

# Adicionando argumento: --range
parser.add_argument(
    "-r", "--range",
    dest="range",
    type=int,
    help="Número do limiar superior do intervalo a ser impresso",
    required=True
)

# Coletando argumento
args = parser.parse_args()

# Criando programa principal
if __name__ == "__main__":
    for i in range(args.range + 1):
        print(i)
