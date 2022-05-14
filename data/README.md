
## Table of Contents

- [Table of Contents](#table-of-contents)
- [Dados para Exploração](#dados-para-exploração)
  - [Activity Data](#activity-data)
  - [Airbnb](#airbnb)
  - [Bike Data](#bike-data)
    - [Station](#station)
    - [Trip](#trip)
  - [Blogs](#blogs)
  - [Employee](#employee)
    - [General/Id](#generalid)
    - [Contract](#contract)
    - [Hr](#hr)
  - [Flights Data](#flights-data)
    - [Airport Codes NA](#airport-codes-na)
    - [Departure Delays](#departure-delays)
- [IOT Devices](#iot-devices)

___

## Dados para Exploração

Em meio a jornada de aprendizado no universo de tecnologia, nada mais gratificante que ter em mãos bases de dados nos mais variados formatos e contextos prontas para serem utilizadas, exploradas, enriquecidas e analisadas.

Neste cenário, este diretório tem como objetivo alocar conjuntos de dados retirados de fontes públicas disponíveis em repositórios conhecidos da internet, livros, páginas do github e outras referências tecnicamente confiáveis para serem alvos das soluções e produtos de dados construídos e documentados neste repositório.

Em complemento, este documento servirá como um grande guia para o detalhamento do conteúdo de cada uma das bases de dados obtidas, garantindo aos usuários um conhecimento prévio e completo de tudo o que poderá ser usado deste ponto em diante em tarefas *hands on*.

| Base de Dados | Formato dos Dados | Quantidade de Arquivos | Volume Total |
| :---: | :---: | :---: | :---: |
| [Activity Data](#activity-data) | JSON | 80 | 1,1 GB |
| [Airbnb](#airbnb) | CSV | 1 | 32MB |

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

> Dados extarídos a partir de interações com o Airbnb nos mais diferentes cenários envolvendo a utilização de seus serviços. A base de dados possui mais de 700 atributos a serem explorados para as mais variadas finalidades.

- 📌 **Acesso:** [data/airbnb](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/airbnb)
- 🎲 **Formato dos dados:** CSV
- 📂 **Quantidade de arquivos:** 1
- 📦 **Volume total aproximado:** 32MB
- 🌎 **Origem:** [Repositório Github - Spark the Definitive Guide](https://github.com/databricks/Spark-The-Definitive-Guide)

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| id | A definir | <class 'int'> | 958 |
| listing_url | A definir | <class 'str'> | https://www.airbnb.com/rooms/958 |
| scrape_id | A definir | <class 'int'> | 20190306152813 |
| last_scraped | A definir | <class 'str'> | 2019-03-06 |
| name | A definir | <class 'str'> | Bright, Modern Garden Unit - 1BR/1B |
| summary | A definir | <class 'str'> | New update: the house next door is under construction and there is the possibility of noise from 7am - 5pm. Our rates are discounted during this time period. Our bright garden unit overlooks a grassy backyard area with fruit trees and native plants. It is an oasis in a big city. The apartment comfortably fits a couple or small family. It is located on a cul de sac street that ends at lovely Duboce Park. |
| space | A definir | <class 'str'> | Newly remodeled, modern, and bright garden unit in historic Victorian home.  *New fixtures and finishes. *Organic cotton sheets and towels. *Zero VOC and non-toxic Yolo paint. *Organic and fair-trade teas, fresh local ground coffee. *Local art on walls. *Sofa bed and Queen bed are in the same room. More of a petite apartment with a separate room for dining and kitchen. |
| description | A definir | <class 'str'> | New update: the house next door is under construction and there is the possibility of noise from 7am - 5pm. Our rates are discounted during this time period. Our bright garden unit overlooks a grassy backyard area with fruit trees and native plants. It is an oasis in a big city. The apartment comfortably fits a couple or small family. It is located on a cul de sac street that ends at lovely Duboce Park. Newly remodeled, modern, and bright garden unit in historic Victorian home.  *New fixtures and finishes. *Organic cotton sheets and towels. *Zero VOC and non-toxic Yolo paint. *Organic and fair-trade teas, fresh local ground coffee. *Local art on walls. *Sofa bed and Queen bed are in the same room. More of a petite apartment with a separate room for dining and kitchen. *Full access to patio and backyard (shared with us and our dog who live upstairs) *Beautiful garden with fruit trees, native plants and lawn *Washer and dryer *Children's toys *Charcoal grill A family of 4 lives upstairs  |
| experiences_offered | A definir | <class 'str'> | none |
| neighborhood_overview | A definir | <class 'str'> | *Quiet cul de sac in friendly neighborhood *Steps away from grassy park with 2 playgrounds and Recreational Center *Very family-friendly neighborhood *Quaint shops, grocery stores and restaurants all within a 5-10 minute walk |
| notes | A definir | <class 'str'> | Due to the fact that we have children and a dog, we are up early 7-8am and their footsteps or paws can be heard from the apartment. Our place is ideal for early risers or hard sleepers who appreciate quiet evenings more than late mornings. |
| transit | A definir | <class 'str'> | *Public Transportation is 1/2 block away.  *Centrally located with easy access to major lines of public transportation (N-Judah, Haight #7, J-Church, Fillmore, and Bart) *No Parking is offered.  *Street parking is unmetered. From 9AM - 8PM restricted to two hours per space (this is the case for residential street parking city wide).  *Overnight and weekend parking on the street is unrestricted.  *Street cleaning happens at least 2 times a week on most streets. *Taxis suggested for Airport trips |
| access | A definir | <class 'str'> | *Full access to patio and backyard (shared with us and our dog who live upstairs) *Beautiful garden with fruit trees, native plants and lawn *Washer and dryer *Children's toys *Charcoal grill |
| interaction | A definir | <class 'str'> | A family of 4 lives upstairs with their dog. Normally we are able to meet guests, but we like to give people their privacy and mostly leave them alone. We are always available if anything is needed or questions need to be answered. |
| house_rules | A definir | <class 'str'> | * No Pets - even visiting guests for a short time period. * No Smokers allowed - even if smoking off premises. |
| thumbnail_url | A definir | <class 'float'> | nan |
| medium_url | A definir | <class 'float'> | nan |
| picture_url | A definir | <class 'str'> | https://a0.muscache.com/im/pictures/b7c2a199-4c17-4ba6-b81d-751719d2dac6.jpg?aki_policy=large |
| xl_picture_url | A definir | <class 'float'> | nan |
| host_id | A definir | <class 'int'> | 1169 |
| host_url | A definir | <class 'str'> | https://www.airbnb.com/users/show/1169 |
| host_name | A definir | <class 'str'> | Holly |
| host_since | A definir | <class 'str'> | 2008-07-31 |
| host_location | A definir | <class 'str'> | San Francisco, California, United States |
| host_about | A definir | <class 'str'> | We are a family with 2 boys born in 2009 and 2011.  We have a new puppy (Feb 2017) named Tucker who is part black lab and part border collie. |
| host_response_time | A definir | <class 'str'> | within an hour |
| host_response_rate | A definir | <class 'str'> | 100% |
| host_acceptance_rate | A definir | <class 'float'> | nan |
| host_is_superhost | A definir | <class 'str'> | t |
| host_thumbnail_url | A definir | <class 'str'> | https://a0.muscache.com/im/pictures/efdad96a-3efc-4bc2-bdc9-f69740a5a818.jpg?aki_policy=profile_small |
| host_picture_url | A definir | <class 'str'> | https://a0.muscache.com/im/pictures/efdad96a-3efc-4bc2-bdc9-f69740a5a818.jpg?aki_policy=profile_x_medium |
| host_neighbourhood | A definir | <class 'str'> | Duboce Triangle |
| host_listings_count | A definir | <class 'int'> | 1 |
| host_total_listings_count | A definir | <class 'int'> | 1 |
| host_verifications | A definir | <class 'str'> | ['email', 'phone', 'facebook', 'reviews', 'kba'] |
| host_has_profile_pic | A definir | <class 'str'> | t |
| host_identity_verified | A definir | <class 'str'> | t |
| street | A definir | <class 'str'> | San Francisco, CA, United States |
| neighbourhood | A definir | <class 'str'> | Duboce Triangle |
| neighbourhood_cleansed | A definir | <class 'str'> | Western Addition |
| neighbourhood_group_cleansed | A definir | <class 'float'> | nan |
| city | A definir | <class 'str'> | San Francisco |
| state | A definir | <class 'str'> | CA |
| zipcode | A definir | <class 'int'> | 94117 |
| market | A definir | <class 'str'> | San Francisco |
| smart_location | A definir | <class 'str'> | San Francisco, CA |
| country_code | A definir | <class 'str'> | US |
| country | A definir | <class 'str'> | United States |
| latitude | A definir | <class 'float'> | 37.76931 |
| longitude | A definir | <class 'float'> | -122.43386 |
| is_location_exact | A definir | <class 'str'> | t |
| property_type | A definir | <class 'str'> | Apartment |
| room_type | A definir | <class 'str'> | Entire home/apt |
| accommodates | A definir | <class 'int'> | 3 |
| bathrooms | A definir | <class 'float'> | 1.0 |
| bedrooms | A definir | <class 'int'> | 1 |
| beds | A definir | <class 'int'> | 2 |
| bed_type | A definir | <class 'str'> | Real Bed |
| amenities | A definir | <class 'str'> | {TV,"Cable TV",Internet,Wifi,Kitchen,"Pets live on this property",Dog(s),Heating,"Family/kid friendly",Washer,Dryer,"Smoke detector","Carbon monoxide detector","First aid kit",Essentials,Shampoo,"24-hour check-in",Hangers,"Hair dryer",Iron,"Laptop friendly workspace","Self check-in",Keypad,"Private entrance","Pack ’n Play/travel crib","Room-darkening shades"} |
| square_feet | A definir | <class 'float'> | nan |
| price | A definir | <class 'str'> | $170.00 |
| weekly_price | A definir | <class 'str'> | $1,120.00 |
| monthly_price | A definir | <class 'str'> | $4,200.00 |
| security_deposit | A definir | <class 'str'> | $100.00 |
| cleaning_fee | A definir | <class 'str'> | $100.00 |
| guests_included | A definir | <class 'int'> | 2 |
| extra_people | A definir | <class 'str'> | $25.00 |
| minimum_nights | A definir | <class 'int'> | 1 |
| maximum_nights | A definir | <class 'int'> | 30 |
| minimum_minimum_nights | A definir | <class 'int'> | 1 |
| maximum_minimum_nights | A definir | <class 'int'> | 1 |
| minimum_maximum_nights | A definir | <class 'int'> | 30 |
| maximum_maximum_nights | A definir | <class 'int'> | 30 |
| minimum_nights_avg_ntm | A definir | <class 'float'> | 1.0 |
| maximum_nights_avg_ntm | A definir | <class 'float'> | 30.0 |
| calendar_updated | A definir | <class 'str'> | today |
| has_availability | A definir | <class 'str'> | t |
| availability_30 | A definir | <class 'int'> | 1 |
| availability_60 | A definir | <class 'int'> | 1 |
| availability_90 | A definir | <class 'int'> | 2 |
| availability_365 | A definir | <class 'int'> | 64 |
| calendar_last_scraped | A definir | <class 'str'> | 2019-03-06 |
| number_of_reviews | A definir | <class 'int'> | 180 |
| number_of_reviews_ltm | A definir | <class 'int'> | 52 |
| first_review | A definir | <class 'str'> | 2009-07-23 |
| last_review | A definir | <class 'str'> | 2019-02-17 |
| review_scores_rating | A definir | <class 'int'> | 97 |
| review_scores_accuracy | A definir | <class 'int'> | 10 |
| review_scores_cleanliness | A definir | <class 'int'> | 10 |
| review_scores_checkin | A definir | <class 'int'> | 10 |
| review_scores_communication | A definir | <class 'int'> | 10 |
| review_scores_location | A definir | <class 'int'> | 10 |
| review_scores_value | A definir | <class 'int'> | 10 |
| requires_license | A definir | <class 'str'> | t |
| license | A definir | <class 'str'> | STR-0001256 |
| jurisdiction_names | A definir | <class 'str'> | {"SAN FRANCISCO"} |
| instant_bookable | A definir | <class 'str'> | t |
| is_business_travel_ready | A definir | <class 'str'> | f |
| cancellation_policy | A definir | <class 'str'> | moderate |
| require_guest_profile_picture | A definir | <class 'str'> | f |
| require_guest_phone_verification | A definir | <class 'str'> | f |
| calculated_host_listings_count | A definir | <class 'int'> | 1 |
| calculated_host_listings_count_entire_homes | A definir | <class 'int'> | 1 |
| calculated_host_listings_count_private_rooms | A definir | <class 'int'> | 0 |
| calculated_host_listings_count_shared_rooms | A definir | <class 'int'> | 0 |
| reviews_per_month | A definir | <class 'float'> | 1.54 |

___

### Bike Data

> Dados públicos de usuários de serviços de empréstimos de bicicleta de São Francisco. A base disponível foi anonimizada e contém registros de viagens de bicicletas realizadas entre Agosto de 2013 e Agosto de 2015. Seu conteúdo está dividido em dois sub-diretórios:
>
> - `/station`: contém dados que representam a estação (metrô) onde usuários podem coletar e devolver bicicletas
> - `/trip`: contém dados de viagens individuais de usuários
>

- 📌 **Acesso:**
  - [data/bike-data/station](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/bike-data/station)
  - [data/bike-data/trip](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/bike-data/trip)
- 🎲 **Formato dos dados:** CSV
- 📂 **Quantidade de arquivos:** 2
- 📦 **Volume total aproximado:** 41MB
- 🌎 **Origem:** [Repositório Github - Spark the Definitive Guide](https://github.com/databricks/Spark-The-Definitive-Guide)

#### Station

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| station_id | ID da estação onde foi realizada a coleta da bicicleta | <class 'int'> | 2 |
| name | Nome da estação onde foi realizada a coleta da bicicleta | <class 'str'> | San Jose Diridon Caltrain Station |
| lat | Latitude do local de coleta da bicicleta | <class 'float'> | 37.329732 |
| long | Longitude do local de coleta da bicicleta | <class 'float'> | -121.901782 |
| dockcount | A definir | <class 'int'> | 27 |
| landmark | Cidade do local de coleta da bicicleta | <class 'str'> | San Jose |
| installation | Data da coleta da bicicleta | <class 'str'> | 8/6/2013 |

#### Trip

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| Trip ID | ID da viagem realizada | <class 'int'> | 913460 |
| Duration | Duração da viagem de bicicleta | <class 'int'> | 765 |
| Start Date | Data de início da viagem | <class 'str'> | 8/31/2015 23:26 |
| Start Station | Estação de início da viagem (coleta da bicicleta) | <class 'str'> | Harry Bridges Plaza (Ferry Building) |
| Start Terminal | Terminal de início da viagem (coleta da bicicleta) | <class 'int'> | 50 |
| End Date | Data de finalização da viagem | <class 'str'> | 8/31/2015 23:39 |
| End Station | Estação de finalização da viagem (entrega da bicicleta) | <class 'str'> | San Francisco Caltrain (Townsend at 4th) |
| End Terminal | Terminal de finalização da viagem (entrega da bicicleta) | <class 'int'> | 70 |
| Bike # | Identificador da bicicleta utilizada na viagem | <class 'int'> | 288 |
| Subscriber Type | Tipo de inscrição do usuário | <class 'str'> | Subscriber |
| Zip Code | CEP | <class 'int'> | 2139 |

___

### Blogs

> Base de dados contendo informações sobre blogs publicados na internet. Em um caráter totalmente exploratório e fictício, esta base possui apenas alguns elementos que podem ser utilizados para testes dentro do contexto de características de blogs geradas manualmente.

- 📌 **Acesso:** [data/blogs](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/blogs)
- 🎲 **Formato dos dados:** JSON
- 📂 **Quantidade de arquivos:** 1
- 📦 **Volume total aproximado:** 1KB
- 🌎 **Origem:** [Repositório Github - Spark the Definitive Guide](https://github.com/databricks/Spark-The-Definitive-Guide)

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| Id | ID do blog | <class 'int'> | 1 |
| First | Primeiro nome do autor do blog | <class 'str'> | Jules |
| Last | Sobrenome do autor do blog | <class 'str'> | Damji |
| Url | Link para acesso ao blog | <class 'str'> | https://tinyurl.1 |
| Published | Data de publicação do blog | <class 'str'> | 1/4/2016 |
| Hits | Quantidade de acessos do blog | <class 'int'> | 4535 |
| Campaigns | Locais onde o blog foi compartilhado | <class 'str'> | [twitter, LinkedIn] |

___

### Employee

> Esta base de dados possui um contexto relacionado a funcionários de uma determinada companhia e seu conteúdo foi gerado manualmente para fins exploratórios. O conjunto está dividido em 4 sub-diretórios, sendo eles:

> - `contract`: dados relacionados ao contrato de trabalho de cada funcionário
> - `general/id`: dados cadastrais dos funcionários
> - `hr`: dados relacionados ao horário de serviço de cada funcionário
> 
> A grande vantagem na utilização destes conjuntos de dados está atrelada às suas respectivas variedades. Extraídos de um livro específico de Apache Hive, o conteúdo de cada arquivo possui diferentes cenários de delimitação e tipos primitivos complexos, permitindo uma exploração variada de tópicos específicos.

- 📌 **Acesso:**
  - [data/employee/contract](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/employee/contract)
  - [data/employee/general](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/employee/general)
  - [data/employee/hr](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/employee/hr)
  - [data/employee/id](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/employee/id)
- 🎲 **Formato dos dados:** TXT
- 📂 **Quantidade de arquivos:** 4
- 📦 **Volume total aproximado:** 2KB
- 🌎 **Origem:** [Repositório Github - Apache Hive Essentials](https://github.com/PacktPublishing/Apache-Hive-Essentials-Second-Edition)

#### General/Id

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| name | Nome do funcionário | STRING | Michael |
| work_place | Campo com informações de local de trabalho (campo complexo) | ARRAY | Montreal,Toronto |
| gender_age | Gênero e idade do funcionário (campo complexo) | STRUCT | Male,30 |
| skills_score | Habilidades e proficiência do funcionário em data habilidade (campo complexo) | MAP | DB:80 |
| depart_title | Departamento e cargo do funcionário (campo complexo) | MAP | Developer:Lead |

#### Contract

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| name | Nome do funcionário | STRING | Michael |
| dept_num | Número do departamento do funcionário | INT | 1000 |
| employee_id | Identificador únido do funcionário | INT | 100 |
| salary | Salário do funcionário | INT | 5000 |
| type | Tipo de jornada do funcionário | STRING | full |
| start_date | Data de início do contrato de trabalho do funcionário | DATE | 2014-01-29 |

#### Hr

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| name | Nome do funcionário | STRING | Michael |
| employee_id | Identificador únido do funcionário | INT | 100 |
| sin_number | A definir | STRING | 547-968-091 |
| start_date | Data de início do contrato de trabalho do funcionário | DATE | 2014-01-29 |

___

### Flights Data

> Conjunto de dados formato por 2 principais subdiretórios contendo dados relacionados a viagens de avião realizadas nos Estados Unidos. A principal riqueza neste conjunto se dá pela existência de um subdiretório adicional contendo dados sumarizados nos mais variados formatos, incluindo avro, csv, json, orc e parquet. Com isso, os usuários podem realizar simulações em fluxos de análise de dados considernado cenários distintos.

> `airport-codes-na`: Tabela auxiliar com o código e descrição de aeroportos na América do Norte.
> `departure-delays`: Dados de viagens realizadas em diferentes datas, origens e destinos.

- 📌 **Acesso:**
  - [data/flights-data/airport-codes-na](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/flights-data/airport-codes-na)
  - [data/flights-data/departure-delays](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/flights-data/departure-delays)
  - [data/flights-data/summary-data](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/flights-data/summary-data)
- 🎲 **Formato dos dados:** Diversos
- 📂 **Quantidade de arquivos:** 4
- 📦 **Volume total aproximado:** 33MB
- 🌎 **Origem:** [Repositório Github - Apache Hive Essentials](https://github.com/PacktPublishing/Apache-Hive-Essentials-Second-Edition)

#### Airport Codes NA

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| City | Cidade de localização do aeroporto | <class 'str'> | Abbotsford |
| State | Estado de localização do aeroporto | <class 'str'> | BC |
| Country | País de localização do aeroporto | <class 'str'> | Canada |
| IATA | Código de identificação do aeroporto | <class 'str'> | YXX |

#### Departure Delays

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| date | Data da viagem aérea realizada | <class 'int'> | 1011245 |
| delay | Tempo total de duração da viagem aérea | <class 'int'> | 6 |
| distance | Distância total da viagem aérea | <class 'int'> | 602 |
| origin | Código do aeroporto de origem da viagem | <class 'str'> | ABE |
| destination | Código do aeroporto de destino da viagem | <class 'str'> | ATL |

___

## IOT Devices

- 📌 **Acesso:** [data/flights-data/airport-codes-na](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/flights-data/airport-codes-na)
  - [data/flights-data/departure-delays](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/flights-data/departure-delays)
  - [data/flights-data/summary-data](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/flights-data/summary-data)
- 🎲 **Formato dos dados:** Diversos
- 📂 **Quantidade de arquivos:** 4
- 📦 **Volume total aproximado:** 33MB
- 🌎 **Origem:** [Repositório Github - Apache Hive Essentials](https://github.com/PacktPublishing/Apache-Hive-Essentials-Second-Edition)

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| device_id | A definir | <class 'int'> | 1 |
| device_name | A definir | <class 'str'> | meter-gauge-1xbYRYcj |
| ip | A definir | <class 'str'> | 68.161.225.1 |
| cca2 | A definir | <class 'str'> | US |
| cca3 | A definir | <class 'str'> | USA |
| cn | A definir | <class 'str'> | United States |
| latitude | A definir | <class 'float'> | 38.0 |
| longitude | A definir | <class 'float'> | -97.0 |
| scale | A definir | <class 'str'> | Celsius |
| temp | A definir | <class 'int'> | 34 |
| humidity | A definir | <class 'int'> | 51 |
| battery_level | A definir | <class 'int'> | 8 |
| c02_level | A definir | <class 'int'> | 868 |
| lcd | A definir | <class 'str'> | green |
| timestamp | A definir | <class 'int'> | 1458444054093 |
