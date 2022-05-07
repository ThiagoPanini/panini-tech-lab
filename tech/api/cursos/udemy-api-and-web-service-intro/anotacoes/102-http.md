# O Protocolo HTTP

___
**Curso:** API and Web Service Introduction
**Autor:** Nate Ross
**Título:** Detalhamento sobre o protocolo HTTP
___

## O que é HTTP?

- Acrônimo para *Hypertext Transfer Protocol*
- Protocolo para transferência de dados através da internet
- Protocolo comumente utilizado por APIs em requisições e respostas através da internet

___

## Componentes do Protocolo HTTP

- Uma chamada HTTP é composta de 4 elementos:
  - **Start Line**
    - Nome
    - Versão HTTP (ex: `HTTP/1.1`)
    - Método (ex: `GET`, `POST`, `PUT`, `DELETE`, etc)
    - Diretório da URL (ex: `/search`)
    - Parâmetros (ex: `?q=termo`)
    - Status Code (ex: `200` - apenas na resposta)
  - **Headers**
    - Cabeçalho com informações sobre a requisição e a resposta. Existem diferentes tipos para requisição e resposta.
    - `Authorizator`
    - `Cache-Control`
    - `Content-Type` (ex: `application/json` ou `application/xml`)
    - `Host`
    - Entre vários outros...
  - **Blank Line**
    - Serve para separar o *header* do *body*
  - **Body**
    - Conteúdo da requisição/resposta
    - Considera o `Content-Type` do *header* para informar o tipo de conteúdo

___

### Start Line

Quando se fala em APIs, a *start line* é a primeira linha tanto na **requisição** quando na **resposta**. Como visto nos tópicos acima, o conteúdo da *start line* possui informações fundamentais da chamada.

A tabela abaixo detalha seu conteúdo tanto para requisições como também para respostas:

| Elemento | Requisição | Resposta |
| :---: | :---: | :---: |
| Versão HTTP | HTTP/1.1 | HTTP/1.1 |
| [Método](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) | GET, POST, PUT, DELETE, etc | Não se aplica |
| Diretório de localização da API | Sim (ex: `/search`) | Não se aplica |
| Parâmetros | Sim (ex: `?q=tuna`) | Não se aplica
| [Status Code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | Não se aplica | Sim (ex: `200`) |

O formato da *start line* em uma **requisição** HTTP é:

- `<método> <API program folder> <parameters> <http version>`
- *Exemplo:* `GET search?q=nba HTTP/1.1`

**Observação:** a informação do *host* (ex: www.google.com) é colocada no *header* dentro do elemento `Host`.

Já quanto a **resposta**, o formato é dado por:

- `<http version> <status code>`
- *Exemplo:* `HTTP/1.1 200`

Um conceito fundamental em relação aos **métodos** HTTP é o de **idempotência**. Basicamente, este termo significa poder executar uma determinada ação múltiplas vezes e obter o mesmo resultado. Em outras palavras, é poder repetir ações de forma segura sem o risco de obter consequências indesejadas. A tabela abaixo detalha os principais métodos HTTP dentro deste contexto.

| Método | Descrição | Paralelo CRUD | Idempotente? |
| :---: | :---: | :---: | :---: |
| `GET` | Coleta dados | (R) Read | Sim |
| `POST` | Escreve dados | (C) Create | Não |
| `PUT` | Atualiza dados | (U) Update | Sim |
| `DELETE` | Elimina dados | (D) Delete | Sim |

___

### Header

Assim como na *start line*, o *header* em uma chamada HTTP tem características distintas tanto para **requisições** como também para **respostas**.

O conceito de *header* está baseado na inserção de alguns elementos específicos no cabeçalho de requisições e respostas para, de alguma forma, "configurar" ou fornecer detalhes adicionais relacionados a chamada de API.

Na [página do wikipedia](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields) sobre headers, é possível observar uma lista completa de possibilidades. Exemplos são:

- `Accept-Language`: determina o idioma aceito nas chamadas
- `Authorization`: especifica o modo de autorização de chamadas (token, usuário/senha)
- `Content-Type`: especifica o tipo de conteúdo informado ao programa na chamada (ex: `application/json`, `image/png`, entre vários outros)
- `Date`: data e hora de criação da mensagem
- `Host`: nome do servidor ou do endereço da chamada. Este é um elemento muito importante pois, se na *start line* vimos que a construção é baseada em `<método> <diretório> <parâmetros> <versão http>`, o *header* Host é responsável por identificar o site/servidor da chamada (ex: `www.google.com`), completando assim todas as informações necessárias para a requisição.

Muitos elementos são comuns entre requisições e respostas, entretanto alguns são específicos para cada cenário ou possuem comportamentos particulares de acordo com o contexto (requisição ou resposta).

___

### Body

Da forma mais direta possível, o *body* de uma chamada HTTP é o local que contém o conteúdo, seja uma imagem, uma página HTML, vídeo ou simplesmente dados.

No contexto da **requisição** o *body* irá armazenar qualquer conteúdo necessário para que o programa realize as operações solicitadas. Já no contexto da **resposta**, o *body* trará o conteúdo enviado pelo programa como retorno à requisição realizada.

Unindo os pontos, o "conteúdo" aqui referido estará detalhado em uma chamada HTTP através do header `Content-Type`. As opções possíveis podem ser visualizadas na seguinte [página da wikipedia](https://en.wikipedia.org/wiki/Media_type)

Como destaque, vale citar que os dois tipos mais comuns utilizados para enviar ou receber dados de APIs são `json` e `xml`.
