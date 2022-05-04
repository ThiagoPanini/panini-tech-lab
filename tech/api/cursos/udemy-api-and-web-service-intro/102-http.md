# API

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

- Uma requisição HTTP é composta de 4 elementos:
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
    - Serve para separar os *headers* do *body*
  - **Body**
    - Conteúdo da requisição/resposta
    - Considera o `Content-Type` do *header* para informar o tipo de conteúdo

- O formato da **start line** em uma API é:
  - *Requisição*: `<método> <API program folder> <parameters> <http version>` (ex: `GET /search?q=nba HTTP/1.1`)

- Já o **header** comporta 