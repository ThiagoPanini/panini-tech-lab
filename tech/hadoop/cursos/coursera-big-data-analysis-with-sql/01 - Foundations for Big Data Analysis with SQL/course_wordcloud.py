"""
    Script desenvolvido para criar uma WordCloud baseada em todo o conteúdo agrupado (transcrições em txt) do
    curso em questão.
"""

"""
------------------------------------------------------------------------------------------------
-------------------------------- IMPORTANDO BIBLIOTECAS ----------------------------------------
------------------------------------------------------------------------------------------------
"""
import os
import sys
import re
import shutil
import matplotlib.pyplot as plt
try:
    from wordcloud import WordCloud, STOPWORDS
except:
    print('Biblioteca wordcloud inexistente. Realizando download via pip\n')
    try:
        os.system('pip install wordcloud')
        from wordcloud import WordCloud, STOPWORDS
        print('Download realizado com sucesso.\n')
    except:
        print(f'Não foi possível realizar o download via pip. Encerrando script.')
        sys.exit()

"""
------------------------------------------------------------------------------------------------
---------------------------------- DEFININDO CLASSES -------------------------------------------
------------------------------------------------------------------------------------------------
"""


class CloudGenerator:

    def __init__(self, raw_path, transcriptions_path):
        self.raw_path = raw_path
        self.transcriptions_path = transcriptions_path

    def collect_transcriptions(self):
        """
        Função responsável por navegar entre o diretório fornecido e retornar apenas arquivos referentes as
        transcrições de áudio em formato txt

        :return dict_transcriptions: dicionário contendo as transcrições (valores) por semana (chaves)
        """

        os.chdir(self.raw_path)
        transcriptions = []
        for dir_path, dirs, files in os.walk(self.raw_path):
            temp_transcript = [f for f in files if 'Transcriptions' in f]
            transcriptions += temp_transcript

        return transcriptions


    def generate_wordcloud(self):
        """
        Função responsável por ler o conteúdo das transcrições, consolidá-lo por semana e gerar uma wordCloud
        pra todos os arquivos lidos dentro daquela respectiva semana

        :param transcriptions: lista com nome de arquivos contendo transcrições de áudio
        :return: imagens png salvas no mesmo diretório dos arquivos lidos
        """
        words = ''
        for file_name in os.listdir(path=self.transcriptions_path):
            # Definindo caminho
            file_path = self.transcriptions_path + f'\{file_name}'

            # Adicionando todas as transcrições da semana em uma string única
            with open(file_path, 'r') as f:
                content = ' '.join(f.readlines())
                words += content

        # Preparando string (removendo urls)
        words = re.sub('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?',
                       'link', words)

        # Removendo números
        words = re.sub('\d+(?:\.\d*(?:[eE]\d+))?', 'number', words)

        # Caracteres especiais
        words = re.sub(r'\W', ' ', words)

        # Espaços em branco
        words = re.sub(r'\s+', ' ', words)

        # Lower case
        words = words.lower()

        # WordCloud
        stopwords = set(list(STOPWORDS) + ['data', 'll'])
        wordcloud = WordCloud(stopwords=stopwords, background_color="white", collocations=False).generate(words)

        plt.figure(figsize=(15, 15))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title('WordCloud 02 - Analyzing Big Data with SQL', size=30, pad=20)
        word_cloud_figname = self.raw_path + r'\Course02_WordCloud.png'
        plt.savefig(word_cloud_figname, format='png', dpi=300)


"""
------------------------------------------------------------------------------------------------
--------------------------------- PROGRAMA PRINCIPAL -------------------------------------------
------------------------------------------------------------------------------------------------
"""


def main():

    # Definindo variáveis
    study_path = r'D:\Users\thiagoPanini\github_files\programming_languages\sql\coursera-Modern_BigData_Analysis_with_SQL'
    course_path = study_path + r'\02 - Analyzing Big Data with SQL'
    transcriptions_path  = course_path + r'\course02_transcriptions'
    wc_generator = CloudGenerator(raw_path=course_path, transcriptions_path=transcriptions_path)

    # Coletando transcrições de cada semana e movendo para diretório destino
    #course_transcriptions = wc_generator.collect_transcriptions()

    # Gerando WordClouds
    wc_generator.generate_wordcloud()


if __name__ == '__main__':
    main()