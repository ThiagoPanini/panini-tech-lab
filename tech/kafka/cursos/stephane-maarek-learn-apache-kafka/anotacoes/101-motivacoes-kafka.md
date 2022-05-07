# Kafka

___
**Curso:** Apache Kafka Series - Learn Apache Kafka for Beginners
**Autor:** Stephane Maarek
**Título:** Motivações para Implementação do Kafk
___

## Problema

- Em grandes sitemas, a existência de diversas origens e múltiplos destinos para os dados exigia um grande trabalho de configuração
- Nesse ceário, muitas rotas eram necessárias e o esforço operacional era imenso
- Como exemplo prático, um cenário com 4 fontes de origem e 6 destino exigiria 24 integrações
- Cada integração possui seus próprios desafios, como por exemplo:
  - Protocolo: é preciso definir como os dados serão transportados (TCP, HTTP, REST, FTP, JDBC, etc)
  - Formato: o formato dos dados é extremamente importante (binário, csv, json, avro, protobuf)
  - Schema: os dados irão suportar mudanças em seu esquema?
  - Requisições: os sistemas origem terão um grande aumento de carga devido às conexões e integrações com os destinos

___

## Solução

- O Apache Kafka surgiu para solucionar alguns problemas relacionados a integração dos dados de diferentes fontes e destinos
- Com o Kafka, este processo pode ser simplificado e melhor gerenciado em um esquema de produtores e consumidores
- A principal palavra associada é: decoupling
- Os sistemas origem irão produzir os dados para o Kafka
- Os sitemas destino irão consumir os dados do Kafka

___

## Benefícios

- O Kafka possui uma arquitetura distribuída, resiliente e tolerante à falhas
- Possui escalabilidade horizontal através da adição de brokers (servidores)
- Pode escalar para milhões de mensagens por segundo
- Possui alta performance
- Latência abaixo de 10ms (real time)

___

## Casos de Uso

- Sistemas de mensagens
- Monitorador de atividades
- Coleta de métricas de diferentes locais
- Coleta de logs de aplicações
- Processamento de streaming de dados
- Desacoplamento de dependências de sistemas
- Integração com tecnologias de Big Data (Hadoop, Spark, Flink, Storm)
- Arquiteturas de microsserviços no conceito pub/sub (publisher/subscriber)

___

## Detalhes Adicionais

- O Kafka foi criado pelo LinkedIn e hoje é um projeto Open Source suportado por grandes companhias, como por exemplo:
  - Confluent
  - IBM
  - Cloudera
- O Kafka é utilizado como mecanismo de transporte de dados (e não de armazenamento ou processamento!)
