# Kafka

___
**Curso:** Apache Kafka Series - Learn Apache Kafka for Beginners
**Autor:** Stephane Maarek
**Título:** Definição de Termos e Componentes do Kafka
___

## Objetivos

- Compreender os termos mais comuns relacionados ao Apache Kafka, como:
  - Tópicos
  - Partições
  - Offsets
  - Broker
  - Cluster
  - Producer
  - Consumer
  - Client

___

## Definições de Conceitos

### Tópicos

- Um tópico no Kafka é um stream particular de dados presentes no cluster Kafka
- Em outras palavras, um tópico é basicamente um "canal" de envio ou consumo de dados em um contexto estabelecido
- Exemplos de tópicos que podem estar em um cluster Kafka:
  - logs-applicacao
  - compras-setor-x
  - transacoes
  - localizacao-veiculos
- Em uma comparação, tópicos no Kafka são semelhantes a tabelas em um banco de dados (sem todas as contraints)
- É possível obter quantos tópicos foram desejados em um cluster
- Os tópicos são identificados pelo seu nome
- Tópicos são imutávels. Uma vez escritas, as mensagens não podem ser deletadas ou alteradas

___

### Mensagens

- Mensagens são os elementos enviados ao cluster Kafka a partir de tópicos
- Em um tópico, é possível enviar mensagens em qualquer tipo de formato, incluindo:
  - Arquivos txt
  - Arquivos json
  - Arquivos binário
  - Arquivos avro
  - Entre outros
- Uma sequência de mensagens em um tópico é chamada de data stream
- Mensagens em um tópico não podem ser "consultadas"
- Para enviar mensagens em tópicos, são utilizados os Kafka Producers
- Para ler mensagens em tópicos, são utilizados os Kafka Consumers
- Mensagens no Kafka são mantidas temporariamente
- Por padrão, mensagens são eliminadas após 7 dias
- A ordem das mensagens é garantida apenas dentro da partição
- **A anatomia de uma mensagem é formada por:**
  - Chave (binário - pode ser `null`)
  - Valor (binário - pode ser `null`)
  - Tipo de compressão (ex: nenhum, `gzip`, `snappy`, `lz4`, `zstd`)
  - Headers (opcional - formado por conjuntos de chave e valor)
  - Partição + Offset
  - Timestamp (do sistema ou configurado pelo usuário)

___

### Partições

- Como visto, os tópicos são genéricos e contemplam mensagens de um mesmo assunto
- Entretanto, é possível dividir os tópicos em partições
- Mensagens enviadas a um tópico serão posicionadas em uma das partições existentes
- Uma mensagem é aleatoriamente direcionada a uma partição, a não ser que esta seja identificada por uma CHAVE
- Em um tópico Kafka, é possível ter quantas partições forem desejadas

___

### Offsets

- Mensagens escritas em tópicos são colocadas em partições e recebem um ID numérico de 0 até a quantidade de mensagens
- Este ID recebe o nome de offsets
- Os offsets possuem significado apenas dentro da partição
- Isto significa que a mensagem de offset 4268 na partição 0 não tem o mesmo significado que a mensagem de offset 4268 na partição 1 em um mesmo tópico

___

### Producer

- Basicamente, os Producers escrevem dados nos tópicos
- Os Producers sabem por antecedência a partição exata a ser alvo da escrita dos dados
- Eles também sabem qual o Kafka Broker (servidor) possui o tópico/partição alvo
- Dessa forma, é incorreto pensar que o Kafka decide em qual partição a mensagem será escrita
- No fundo, o Producer é o responsável por tomar essa decisão e, de fato, escrever a mensagem na partição desejada
- Em caso de falhas do Broker, o Producer tem um mecanismo de auto recuperação

___

### Chaves de Mensagens

- Os Producers podem escolher enviar uma **chave** na mensagem
- A chave pode possuir diferentes formatos, como string, inteiro, binário, etc.
- Se `key-null`, as mensagens são enviadas para as partições utilizando a estratégia *round robin*
  - Esta estratégia indica uma tentativa de preencher as partições de forma equalitária
  - Neste caso, a primeira mensagem é escrita na partição 0, a segunda na partição 1, a próxima na partição 2, e assim por diante
  - [Link para maiores detalhes](https://kafka.apache.org/24/javadoc/org/apache/kafka/clients/producer/RoundRobinPartitioner.html#:~:text=The%20%22Round%2DRobin%22%20partitioner,regardless%20of%20record%20key%20hash.)
- Se a chave possuir algum valor (`key != null`), o Kafka possuirá um comportamento específico:
  - Todas as mensagens com a mesma chave sempre estarão na mesma partição (*hashing*)
  - Diferentes chaves podem estar em uma mesma partição, mas é garantido que uma mesma chave estará sempre na mesma partição
- O Kafka usa o algoritmo `murmur2` para o *hashing* das chaves das mensagens e decidir qual partição será o alvo. Sua fórmula é:
  - `targetPartition = Math.abs(Utils.murmur2(keyBytes)) % (numPartitions - 1)`

___

## Serialização e Desserialização

- O Kafka aceita apenas `bytes` como *input* dos Producers e envia `bytes` como *output* para os Consumers
- Para isso, são utilizados **serializers** (processo de transformação de objetos/dados em bytes)
- Existem diferentes **motores de serialização** de acordo com o tipo primitivo das chaves e dos dados enviados nas mensagens
- Os **Consumers** então utilizam diferentes **motores de desserialização** para transformar os `bytes` em objetos
- Este conceito é importante pois, como os processos de serialização e desserialização dependem do formato dos dados (diferentes classes são executadas para transformar os objetos), os tipos dos dados nas mensagems **não podem sofrer alterações** durante o tempo de vida do tópico
- Se houver a necessidade de enviar um "mesmo dado" com alterações nos tipos primitivos, é preciso criar um novo tópico

___

### Consumers

- Os Consumers no Kafka atuam no modelo `pull` de mensagens
- Eles solicitam mensagens aos Brokers (servidores do Kafka) e obtém uma resposta
- Isso é importante para evitar erros de conceito sobre os Brokers enviando dados aos Consumers. São os Consumers quem requisitam
- Um Consumer pode ler mensagens de mais de uma partição em um mesmo tópico
- Consumer automaticamente sabem o Broker exato onde as mensagens estão armazenadas
- Em caso de falha no Broker, os Consumers possuem auto recuperação
- As mensagens são lidas **em ordem**, do offset mais baixo para o mais alto **em cada partição**
  - É importante reforçar que os offsets possuem significado apenas em uma mesma partição
  - O processamento ordenado ocorre considerando uma mesma partição
  - Em outras palavras, após a leitura da mensagem 0 da partição 0, o Consumer **NÃO** lerá a mensagem 0 da partição 1, pois elas não tem relação alguma em termos de ordenação. Neste caso, a próxima leitura será da mensagem 1 da partição 0.

#### Consumer Group

- Consumers podem ser alocados em **grupos**
- Os Consumers dentro de um mesmo grupo apenas poderão ler mensagens de **partições distintas**
- Em outras palavras, Consumers de um mesmo grupo não poderão ler mensagens de uma mesma partição
- É possível ter múltiplos grupos lendo mensagens de um mesmo tópico e de múltiplas partições
- Neste caso, mensagens de uma mesma partição serão lidas por múltiplos Consumers, porém sempre relacionados a **grupos distintos**
- Um bom exemplo para justificar a existência de múltiplos grupos é a existência de múltiplos serviços consumindo as mesmas mensagens
  - Ex: mensagens de localização de veículos sendo consumidas pelos serviços de **notificação** e **visualização**
- Para criar grupos de Consumers, utiliza-se a propriedade `group.id`

#### Consumer Offsets

- Os Consumer Offsets são informações relacionadas a leitura dos Consumers de um determinado grupo
- Cada vez que um Consumer de um grupo processar uma mensagem, ele fornece a informação do offset (id da mensagem) obtida
- Assim, isso permite que os Consumers deste mesmo grupo coletem mensagens daquele offset em diante
- Além disso, isso permite que os Consumers retomem de um ponto definido em caso de falhas, garantindo que os dados não serão perdidos
- A este processo, dá-se o nome de `commit offset`
- Existem três formas de commitar os offsets adotadas pelos Consumers:
  - **At least once:** informação de offsets é enviada assim que as mensagens são **processadas**, garantindo que o offset só será estabelecido quando o Consumer processar a mensagem
  - **At most once:** informação de offsets é enviada assim que as mensagens são **recebidas**
  - **Exactly once**

___

### Kafka Brokers

- Um Broker é basicamente um servidor do Kafka
- Um cluster Kafka é composto por múltiplos Brokers
- Cada Broker é identificado com um ID numérico
- Cada Broker contém certas partições de tópicos
- O conceito de *bootstrap broker* está associado a um Broker coringa alvo da conexão pelo *client* Kafka
- No conceito de *bootstrap broker*, o *client* conecta com qualquer Broker do cluster
