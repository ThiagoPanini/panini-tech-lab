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

> Dados extarídos a partir de interações com o Airbnb nos mais diferentes cenários envolvendo a utilização de seus serviços. A base de dados possui mais de 700 atributos a serem explorados para as mais variadas finalidades.

- 📌 **Acesso:** [data/airbnb](https://github.com/ThiagoPanini/panini-tech-lab/tree/main/data/airbnb)
- 🎲 **Formato dos dados:** CSV
- 📂 **Quantidade de arquivos:** 1
- 📦 **Volume total aproximado:** 32MB
- 🌎 **Origem:** [Repositório Github - Spark the Definitive Guide](https://github.com/databricks/Spark-The-Definitive-Guide)

| Coluna | Descrição | Tipo Primitivo | Exemplo |
| :---: | :---: | :---: | :---: |
| id | Teste | <class 'int'> | 958 |
| listing_url | Teste | <class 'str'> | https://www.airbnb.com/rooms/958 |
| scrape_id | Teste | <class 'int'> | 20190306152813 |
| last_scraped | Teste | <class 'str'> | 2019-03-06 |
| name | Teste | <class 'str'> | Bright, Modern Garden Unit - 1BR/1B |
| summary | Teste | <class 'str'> | New update: the house next door is under construction and there is the possibility of noise from 7am - 5pm. Our rates are discounted during this time period. Our bright garden unit overlooks a grassy backyard area with fruit trees and native plants. It is an oasis in a big city. The apartment comfortably fits a couple or small family. It is located on a cul de sac street that ends at lovely Duboce Park. |
| space | Teste | <class 'str'> | Newly remodeled, modern, and bright garden unit in historic Victorian home.  *New fixtures and finishes. *Organic cotton sheets and towels. *Zero VOC and non-toxic Yolo paint. *Organic and fair-trade teas, fresh local ground coffee. *Local art on walls. *Sofa bed and Queen bed are in the same room. More of a petite apartment with a separate room for dining and kitchen. |
| description | Teste | <class 'str'> | New update: the house next door is under construction and there is the possibility of noise from 7am - 5pm. Our rates are discounted during this time period. Our bright garden unit overlooks a grassy backyard area with fruit trees and native plants. It is an oasis in a big city. The apartment comfortably fits a couple or small family. It is located on a cul de sac street that ends at lovely Duboce Park. Newly remodeled, modern, and bright garden unit in historic Victorian home.  *New fixtures and finishes. *Organic cotton sheets and towels. *Zero VOC and non-toxic Yolo paint. *Organic and fair-trade teas, fresh local ground coffee. *Local art on walls. *Sofa bed and Queen bed are in the same room. More of a petite apartment with a separate room for dining and kitchen. *Full access to patio and backyard (shared with us and our dog who live upstairs) *Beautiful garden with fruit trees, native plants and lawn *Washer and dryer *Children's toys *Charcoal grill A family of 4 lives upstairs  |
| experiences_offered | Teste | <class 'str'> | none |
| neighborhood_overview | Teste | <class 'str'> | *Quiet cul de sac in friendly neighborhood *Steps away from grassy park with 2 playgrounds and Recreational Center *Very family-friendly neighborhood *Quaint shops, grocery stores and restaurants all within a 5-10 minute walk |
| notes | Teste | <class 'str'> | Due to the fact that we have children and a dog, we are up early 7-8am and their footsteps or paws can be heard from the apartment. Our place is ideal for early risers or hard sleepers who appreciate quiet evenings more than late mornings. |
| transit | Teste | <class 'str'> | *Public Transportation is 1/2 block away.  *Centrally located with easy access to major lines of public transportation (N-Judah, Haight #7, J-Church, Fillmore, and Bart) *No Parking is offered.  *Street parking is unmetered. From 9AM - 8PM restricted to two hours per space (this is the case for residential street parking city wide).  *Overnight and weekend parking on the street is unrestricted.  *Street cleaning happens at least 2 times a week on most streets. *Taxis suggested for Airport trips |
| access | Teste | <class 'str'> | *Full access to patio and backyard (shared with us and our dog who live upstairs) *Beautiful garden with fruit trees, native plants and lawn *Washer and dryer *Children's toys *Charcoal grill |
| interaction | Teste | <class 'str'> | A family of 4 lives upstairs with their dog. Normally we are able to meet guests, but we like to give people their privacy and mostly leave them alone. We are always available if anything is needed or questions need to be answered. |
| house_rules | Teste | <class 'str'> | * No Pets - even visiting guests for a short time period. * No Smokers allowed - even if smoking off premises. |
| thumbnail_url | Teste | <class 'float'> | nan |
| medium_url | Teste | <class 'float'> | nan |
| picture_url | Teste | <class 'str'> | https://a0.muscache.com/im/pictures/b7c2a199-4c17-4ba6-b81d-751719d2dac6.jpg?aki_policy=large |
| xl_picture_url | Teste | <class 'float'> | nan |
| host_id | Teste | <class 'int'> | 1169 |
| host_url | Teste | <class 'str'> | https://www.airbnb.com/users/show/1169 |
| host_name | Teste | <class 'str'> | Holly |
| host_since | Teste | <class 'str'> | 2008-07-31 |
| host_location | Teste | <class 'str'> | San Francisco, California, United States |
| host_about | Teste | <class 'str'> | We are a family with 2 boys born in 2009 and 2011.  We have a new puppy (Feb 2017) named Tucker who is part black lab and part border collie. |
| host_response_time | Teste | <class 'str'> | within an hour |
| host_response_rate | Teste | <class 'str'> | 100% |
| host_acceptance_rate | Teste | <class 'float'> | nan |
| host_is_superhost | Teste | <class 'str'> | t |
| host_thumbnail_url | Teste | <class 'str'> | https://a0.muscache.com/im/pictures/efdad96a-3efc-4bc2-bdc9-f69740a5a818.jpg?aki_policy=profile_small |
| host_picture_url | Teste | <class 'str'> | https://a0.muscache.com/im/pictures/efdad96a-3efc-4bc2-bdc9-f69740a5a818.jpg?aki_policy=profile_x_medium |
| host_neighbourhood | Teste | <class 'str'> | Duboce Triangle |
| host_listings_count | Teste | <class 'int'> | 1 |
| host_total_listings_count | Teste | <class 'int'> | 1 |
| host_verifications | Teste | <class 'str'> | ['email', 'phone', 'facebook', 'reviews', 'kba'] |
| host_has_profile_pic | Teste | <class 'str'> | t |
| host_identity_verified | Teste | <class 'str'> | t |
| street | Teste | <class 'str'> | San Francisco, CA, United States |
| neighbourhood | Teste | <class 'str'> | Duboce Triangle |
| neighbourhood_cleansed | Teste | <class 'str'> | Western Addition |
| neighbourhood_group_cleansed | Teste | <class 'float'> | nan |
| city | Teste | <class 'str'> | San Francisco |
| state | Teste | <class 'str'> | CA |
| zipcode | Teste | <class 'int'> | 94117 |
| market | Teste | <class 'str'> | San Francisco |
| smart_location | Teste | <class 'str'> | San Francisco, CA |
| country_code | Teste | <class 'str'> | US |
| country | Teste | <class 'str'> | United States |
| latitude | Teste | <class 'float'> | 37.76931 |
| longitude | Teste | <class 'float'> | -122.43386 |
| is_location_exact | Teste | <class 'str'> | t |
| property_type | Teste | <class 'str'> | Apartment |
| room_type | Teste | <class 'str'> | Entire home/apt |
| accommodates | Teste | <class 'int'> | 3 |
| bathrooms | Teste | <class 'float'> | 1.0 |
| bedrooms | Teste | <class 'int'> | 1 |
| beds | Teste | <class 'int'> | 2 |
| bed_type | Teste | <class 'str'> | Real Bed |
| amenities | Teste | <class 'str'> | {TV,"Cable TV",Internet,Wifi,Kitchen,"Pets live on this property",Dog(s),Heating,"Family/kid friendly",Washer,Dryer,"Smoke detector","Carbon monoxide detector","First aid kit",Essentials,Shampoo,"24-hour check-in",Hangers,"Hair dryer",Iron,"Laptop friendly workspace","Self check-in",Keypad,"Private entrance","Pack ’n Play/travel crib","Room-darkening shades"} |
| square_feet | Teste | <class 'float'> | nan |
| price | Teste | <class 'str'> | $170.00 |
| weekly_price | Teste | <class 'str'> | $1,120.00 |
| monthly_price | Teste | <class 'str'> | $4,200.00 |
| security_deposit | Teste | <class 'str'> | $100.00 |
| cleaning_fee | Teste | <class 'str'> | $100.00 |
| guests_included | Teste | <class 'int'> | 2 |
| extra_people | Teste | <class 'str'> | $25.00 |
| minimum_nights | Teste | <class 'int'> | 1 |
| maximum_nights | Teste | <class 'int'> | 30 |
| minimum_minimum_nights | Teste | <class 'int'> | 1 |
| maximum_minimum_nights | Teste | <class 'int'> | 1 |
| minimum_maximum_nights | Teste | <class 'int'> | 30 |
| maximum_maximum_nights | Teste | <class 'int'> | 30 |
| minimum_nights_avg_ntm | Teste | <class 'float'> | 1.0 |
| maximum_nights_avg_ntm | Teste | <class 'float'> | 30.0 |
| calendar_updated | Teste | <class 'str'> | today |
| has_availability | Teste | <class 'str'> | t |
| availability_30 | Teste | <class 'int'> | 1 |
| availability_60 | Teste | <class 'int'> | 1 |
| availability_90 | Teste | <class 'int'> | 2 |
| availability_365 | Teste | <class 'int'> | 64 |
| calendar_last_scraped | Teste | <class 'str'> | 2019-03-06 |
| number_of_reviews | Teste | <class 'int'> | 180 |
| number_of_reviews_ltm | Teste | <class 'int'> | 52 |
| first_review | Teste | <class 'str'> | 2009-07-23 |
| last_review | Teste | <class 'str'> | 2019-02-17 |
| review_scores_rating | Teste | <class 'int'> | 97 |
| review_scores_accuracy | Teste | <class 'int'> | 10 |
| review_scores_cleanliness | Teste | <class 'int'> | 10 |
| review_scores_checkin | Teste | <class 'int'> | 10 |
| review_scores_communication | Teste | <class 'int'> | 10 |
| review_scores_location | Teste | <class 'int'> | 10 |
| review_scores_value | Teste | <class 'int'> | 10 |
| requires_license | Teste | <class 'str'> | t |
| license | Teste | <class 'str'> | STR-0001256 |
| jurisdiction_names | Teste | <class 'str'> | {"SAN FRANCISCO"} |
| instant_bookable | Teste | <class 'str'> | t |
| is_business_travel_ready | Teste | <class 'str'> | f |
| cancellation_policy | Teste | <class 'str'> | moderate |
| require_guest_profile_picture | Teste | <class 'str'> | f |
| require_guest_phone_verification | Teste | <class 'str'> | f |
| calculated_host_listings_count | Teste | <class 'int'> | 1 |
| calculated_host_listings_count_entire_homes | Teste | <class 'int'> | 1 |
| calculated_host_listings_count_private_rooms | Teste | <class 'int'> | 0 |
| calculated_host_listings_count_shared_rooms | Teste | <class 'int'> | 0 |
| reviews_per_month | Teste | <class 'float'> | 1.54 |
