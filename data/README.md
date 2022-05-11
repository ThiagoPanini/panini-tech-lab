<logo>

___

## Dados para Exploração

Em meio a jornada de aprendizado no universo de tecnologia, nada mais gratificante que ter em mãos bases de dados nos mais variados formatos e contextos prontas para serem utilizadas, exploradas, enriquecidas e analisadas.

Neste cenário, este diretório tem como objetivo alocar conjuntos de dados retirados de fontes públicas disponíveis em repositórios conhecidos da internet, livros, páginas do github e outras referências tecnicamente confiáveis para serem alvos das soluções e produtos de dados construídos e documentados neste repositório.

Em complemento, este documento servirá como um grande guia para o detalhamento do conteúdo de cada uma das bases de dados obtidas, garantindo aos usuários um conhecimento prévio e completo de tudo o que poderá ser usado deste ponto em diante em tarefas *hands on*.

___

### Activity Data

> Base de dados criada a partir da coleta de leituras de sensores de smartphones e smartwatchs enquanto seus usuários realivam algum tipo de atividade física, como bicicleta, caminhada, corrida, entre outras. Ao todo, 9 usuários foram alvo da coleta de dados e uma série de dispositivos distintos foram utilizados com sensores focados em acelerômetro e giroscópio. Esta base de dados também é conhecida como Heterogeneity Human Activity Recognition Dataset.

- 📌 **Acesso:** [data/activity-data](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/activity-data)
- 🎲 **Formato dos dados:** JSON
- 📂 **Quantidade de arquivos:** 80
- 📦 **Volume total aproximado:** 1,1GB
- 🌎 **Origem:** [Repositório Github - Spark the Definitive Guide](https://github.com/databricks/Spark-The-Definitive-Guide)

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| Arrival_Time | Tempo de chegada do usuário | <class 'int'> | 1424686735175 |
| Creation_Time | Tempo de criação da medição sensorial | <class 'int'> | 1424686733176178965 |
| Device | Identificação do dispositivo de medição | <class 'str'> | nexus4_1 |
| Index | Índice do dispositivo de medição | <class 'int'> | 35 |
| Model | Modelo do dispositivo de medição | <class 'str'> | nexus4 |
| User | Identificação do usuário | <class 'str'> | g |
| gt | Categoria | <class 'str'> | stand |
| x | Coordenada x da medição do usuário | <class 'float'> | 0.0014038086 |
| y | Coordenada y da medição do usuário | <class 'float'> | 0.00050354 |
| z | Coordenada z da medição do usuário | <class 'float'> | -0.0124053955 |

___

### Airbnb

> 