## Boas vindas e apresentação

Bem-vindos à série **Linux Básico** no blog `panini-tech-lab`! A grande motivação em criar um espaço reservado para abordar temas relacionados ao Linux tem raízes na curiosidade pessoal e na necessidade de um aprimoramento de conhecimento. Afinal, o sistema Linux e os tópicos que o cercam se fazem presentes em uma gama gigantesca de tecnologias que [utilizamos em nosso dia a dia](https://www.omgubuntu.co.uk/2016/08/25-awesome-unexpected-things-powered-linux), às vezes mesmo sem saber.

Movido por este anseio, decidi falar um pouco mais a respeito desta tecnologia e tentar quebrar um pouco do paradigma de complexidade que ronda o Linux. Não tenho como meta mergulhar a fundo e explorar detalhadamente cada conceito envolvendo a teoria de sistemas operacionais mas, por outro lado, imagino que interessante seria ganhar uma maior autonomia e segurança em encontrar, em cenários distintos, termos como Unix, GNU, Debian, Ubuntu e entender, mesmo que de forma simplista, seus respectivos contextos.

Para escrever e compartilhar conteúdos nesta série, certamente irei ler, pesquisar, assistir aulas e aprender muito sobre o Linux. Espero que seja uma jornada incrível e que você, caro leitor, consiga alcançar seus objetivos neste caminho de aprendizagem.

![p01i01-boas-vindas.PNG](https://cdn.hashnode.com/res/hashnode/image/upload/v1648648676077/3OMU4yOxX.PNG)

___

## O que é o Linux?

Ao pesquisar em uma vasta quantidade de fontes, verifiquei que a grande maioria dos blogs, fóruns e sites técnicos define o Linux como um sistema operacional tal qual o Windows ou o MacOS. De fato, sob uma ótica simplista, esta definição atende usuários que estão interessados em conhecer o assunto de forma panorâmica, sem se importar com detalhes de implementação ou do funcionamento das engrenagens que fazem tudo acontecer.

Porém, sob um viés mais técnico, dizer que o Linux é apenas um sistema operacional deixa tudo muito superficial. De acordo com a [Wikipedia](), Linux é um termo popularmente empregado para se referir a sistemas operacionais que utilizam o **kernel Linux**. Neste contexto, o conceito de *kernel* pode ser entendido como o **núcleo** de um sistema, sendo definido em um artigo postado na página [linuxdescomplicado](https://www.linuxdescomplicado.com.br/2016/09/muito-alem-do-kernel-conheca-todos-os-elementos-que-formam-a-estrutura-do-sistema-linux.html) da seguinte forma:

> O *kernel* de um sistema é o componente central que serve para dar vida ao *hardware*. É a camada responsável por garantir que todos os programas e processos tenham acesso aos recursos da máquina de que necessitam (memória RAM, acesso ao disco e controle da CPU, por exemplo) simultaneamente, fazendo com que haja um compartilhamento concorrente desses. A grosso modo, é o “cérebro” do sistema operacional; o responsável por coordenar o acesso ao hardware e dados entre os diferentes componentes do sistema.

Ao longo dos anos, diversos colaboradores contribuíram e continuam contribuindo substancialmente para o aprimoramento do Linux e sua difusão, proporcionando adaptações, versões, distribuições e ferramentas substanciais para o avanço deste sistema. Por mais que tenhamos, agora, uma noção mais técnica sobre o *kernel* Linux, conhecer um pouco mais da história de seu surgimento poderá enriquecer, ainda mais, nosso conhecimento.

### Um pouco sobre a história do Linux

Em um dos vídeos da série [Curso de Linux - Primeiros Passos](https://www.youtube.com/watch?v=qs_NZXmVUr0&list=PLHz_AreHm4dlIXleu20uwPWFOSswqLYbV&index=3) do professor Gustavo Guanabra em parceria com o professor Ricardo Pinheiro (canal [Curso em Vídeo](https://www.youtube.com/channel/UCrWvhVmt0Qac3HgsjQK62FQ) no Youtube), a história do surgimento do Linux é contada em detalhes. O vídeo possui 41 minutos e pode ser visualizado abaixo.

%[https://www.youtube.com/watch?v=qs_NZXmVUr0&list=PLHz_AreHm4dlIXleu20uwPWFOSswqLYbV&index=3]

Em resumo, por mais complexo que possa parecer, é possível afirmar que as coisas surgiram "umas das outras" até que Linus Torvalds, em 25 de agosto de 1991, enviasse a seguinte mensagem na *Usenet* (uma espécie de antecessora da internet baseada em troca de mensagens):

> Assunto: O que você gostaria de ver no Minix?

> Summary: Pequena pesquisa para o meu novo sistema operacional

> Olá a todos que usam o Minix -

> Estou fazendo um sistema operacional (livre - apenas como um hobby,
não será algo grande e profissional como o GNU) para
máquinas AT 386 (486). Ele tem sido trabalhado desde abril, e
está começando a ficar pronto. Eu gostaria de
opiniões sobre coisas que as pessoas gostam/não gostam no
Minix, já que o meu SO lembra um pouco ele (mesmo layout
físico do sistema de arquivos (por motivos práticos),
entre outros).

> Eu já portei o bash (1.08) e o gcc (1.40) e as coisas parecem
funcionar. Isso indica que conseguirei alguma coisa prática
dentro de alguns meses, e gostaria de saber quais recursos as pessoas
mais gostaria de ter. Todas as sugestões serão
bem-vindas, mas não prometo implementá-las :-)

> Linus (torvalds@kruuna.helsinki.fi)

> PS. Sim - ele está livre de qualquer código do Minix, e
tem sistema de arquivos com multi-threading. Ele NÃO é
portável (usa 386, chaveamento de tarefas, etc) e provavelmente
nunca suportará qualquer coisa além de discos
rígidos AT, pois é tudo o que eu tenho :-(.

E assim, o Linux dava seus primeiros passos até chegar neste verdadeiro conglomerado de opções e funcionalidades presentes nos dias atuais. Até que isso fosse possível, uma série de eventos históricos aconteceram e uma vasta imensidão de sistemas surgiram e foram utilizados como base. Na própria mensagem de Linus Torvalds é possível identificar algumas palavras especiais que são de suma importância para o entendimento histórico deste feito. 

Para garantir um esclarecimento resumido de tudo isso, o glossário abaixo poderá ser utilizado em complemento ao [vídeo acima](https://www.youtube.com/watch?v=qs_NZXmVUr0&list=PLHz_AreHm4dlIXleu20uwPWFOSswqLYbV&index=3) e ao [excelente artigo](https://www.infowester.com/historia_linux.php) da infowester sobre a história do Linux:

| Termo              |  Definição      |
| :-------------: | :------------: |
| Multics          | Sistema criado pela Bell Labs, AT&T e o governo americano na década de 60 |
| Unix               | Sistema criado em 1969 pela Bell Labs e um cojunto de pesquisadores e programadores devido a dificuldades encontradas no processo de criação do Multics |
| GNU               | Acrônimo de *GNU is not Unix*, é um sistema baseado em Unix criado em 1983 para ser totalmente livre e garantir que a briga judicial da Bell Labs não prejudicasse a continuidade de utilização do Unix pela comunidade |
| Hurd               | Kernel inicial do sistema GNU |
| FSF                 | Fundada pelo criador do GNU, a *Free Software Foundation* é onde pode-se encontrar o projeto GNU hoje em dia |
| Minix              | Sistema baseado em Unix criado em 1987 para servir de auxílio educacional nas universidades |
| Linux              | Sistema criado em 1991 a partir da exploração e modificação do Minix em conjunto com o software GNU |

Além dos termos importantes, também é extremamente fundamental conhecer alguns nomes envolvidos em todos estes eventos históricos.

| Nome ou Empresa | Descrição |
| :-----------------: | :---------- |
| Bell Labs | Empresa criadora do Multics e, posteriormente, do Unix |
| Ken Thompson e Dennis Ritchie | Programadores fundamentais para a criação do Unix e da linguagem C |
| Richard Stallman | Criador do projeto GNU e da FSF |
| Andrew Tanenbaum | Renomado professor de computação criador do Minix e publicador de diversos livros sobre sistemas operacionais |
| Linus Torvalds | Criador do kernel Linux |

### Distribuições Linux

Uma vez entendido o contexto de toda a criação e surgimento do Linux, fica mais claro definir que o GNU/Linux é um núcleo de sistema operacional de código aberto baseado em Unix e, sendo dessa forma, programadores com os mais variados propósitos podem ter acesso ao código fonte e modificar conforme suas necessidades, gerando assim o que conhecemos hoje como distribuições Linux.

A partir deste ponto, um imenso ecossistema começou a ser criado em torno do Linux e milhares de colaboradores e empresas continuam atuando tempestivamente para a criação das mais variadas distribuições, como Debian, Ubuntu, Fedora, Mint, Arch, entre outras.

![p01i01-linux-distros.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1648655001919/5Ba0DTsrH.png)

Neste contexto, existem três principais distribuições que serem como base para as demais: Slackware, Debian e RedHat. Para entender este conceito, o Ubuntu pode ser definido como uma distribuição Linux baseada no Debian. Algumas outras distribuições, como o Arch Linux, possuem raízes diretamente no Linux.

### Onde o Linux é utilizado?

Até aqui, uma série de conceitos técnicos foram empregados para definir o Linux como um todo e todos os eventos históricos que culminaram em sua criação. A primeira vista, parece tudo distante da nossa realidade cotidiana, mesmo em cenários de tecnologia, certo? Felizmente, não! O Linux está mais próximo do que imaginamos e, só pra te dar um gostinho especial, abaixo seguem algumas [aplicações do Linux](https://www.omgubuntu.co.uk/2016/08/25-awesome-unexpected-things-powered-linux) amplamente conhecidas:

- Servidores e super computadores
- Smart TVs
- Smartwatches
- Robôs espaciais
- Consoles de vídeo games
- Carros autônomos

É notável, apenas com este simples trecho presente em um simples blog, que o Linux é uma ferramenta extraordinária e que merece, no mínimo, um pouco de sua atenção, caro leitor! 🐧
___

## Considerações Finais

Este é literalmente o primeiro post da primeira série do meu primeiro blog! Espero que ele tenha auxiliado você, caro leitor, no propósito de entender um pouco mais o que é o Linux e como podemos facilmente dar os primeiros passos nesta que é uma tecnologia essencial dentro da jornada de aprendizado no mundo de tecnologia.

Aguardo ansiosamente pelo seu feedback e fique ligado para a continuidade desta série!

___

## Referências

- https://pt.wikipedia.org/wiki/Linux
- https://www.youtube.com/watch?v=K05CssAbQgo
- https://www.omgubuntu.co.uk/2016/08/25-awesome-unexpected-things-powered-linux
- https://en.wikipedia.org/wiki/Linux_distribution
- https://ubuntu.com/download/desktop
- https://www.youtube.com/watch?v=qs_NZXmVUr0&list=PLHz_AreHm4dlIXleu20uwPWFOSswqLYbV&index=3
- https://www.linuxdescomplicado.com.br/2016/03/1-historia-do-linux-5-minutos.html
- https://www.infowester.com/historia_linux.php


