### 1. Introdução

A ideia de um supermercado completamente automatizado sem filas ou funcionários pa-
rece tão distante quanto atrativa para a maioria das pessoas, porém o uso desse tipo de

tecnologia é uma realidade que vem crescendo bastante nos últimos anos, afinal os custos
e o acesso a esse tipo de tecnologia tem se tornado cada vez mais prático e acessível.
Sem atendentes ou seguranças, os produtos são escaneados automaticamente ao
serem removidos da prateleira ou ao passarem pelo caixa e o valor é transferido da conta
do cliente, sem espaço para fraudes ou furtos. Em muitos desses casos é feito o uso da
Internet das Coisas (IoT) ou da Identificação por Radiofrequência (RFID) que permite a
leitura simultânea de múltiplas etiquetas.
Visando otimizar seu supermercado reduzindo o número de filas e o tempo levado

para fazer uma compra, uma empresa desse ramo em Feira de Santana decidiu imple-
mentar um sistema de caixas com leitores RFID. Esse sistema deve funcionar automatica-
mente quando o cliente se aproxima do sensor com as compras que então calcula o preço

total dos produtos e executa a atualização dos itens automaticamente no estoque assim
facilitando e acelerando o processo.
### 2. Fundamentação Teórica
Para solucionar o problema foi implementado um sistema de redes cliente-servidor através

da linguagem de programação Python no qual um servidor abriga as informações referen-
tes aos produtos disponíveis e as compras realizadas que são solicitadas pelos múltiplos

clientes que funcionam como caixas. O gerenciamento dos clientes é feito através do uso
de multithreading.
Para o envio de dados entre o servidor e os clientes foi utilizado um protocolo
semelhante ao sistema de API REST. Para a leitura das etiquetas com o código de cada
produto foi usado um módulo de leitura RFID simultânea M6E Nano da SparkFun que
se conecta ao cliente também em um modelo cliente-servidor. Adicionalmente, foi usado
um conjunto de tags RFID UHF, um módulo de interface serial mini USB (CH340G) da
SparkFun com cabo serial mini USB e um Raspberry Pi Zero W.

### 3. Metodologia, Implementação e Testes
Almejando solucionar o problema, o grupo decidiu que o cliente deveria poder executar
as operaçöes principais de uma API REST (GET, PUT, POST e DELETE) através de uma
conexão com o servidor. Essa conexão seria feita através de sockets (pontos de conexão)
e seguiria o protocolo TCP/IP de conexão, pois assim ambos poderiam receber e enviar
dados de forma assíncrona.
Uma interface do administrador também foi entendida como necessária, através
dela, o administrador consegue ver o histórico de compras, bloquear determinado caixa,

além de poder executar cada uma das operações principais no estoque de produtos atra-
vés do protocolo no modelo de API REST. O uso de multithreading também foi visto

como necessário para implementação correta do problema, visto que a intenção era que o
servidor atendesse a múltiplos clientes simultaneamente.

<img width = '50' height = '50'src="/figura1.png" />

Várias implementações corretas são possíveis para a resolução do problema, po-
rém optei em fazer da seguinte forma: a thread principal apenas aguarda por novas co-
nexões e quando um cliente novo se conecta ao servidor, é criada uma thread secundária

que atende a todas as requisições do cliente e no fim encerra a conexão. A conexão entre
o leitor RFID e os clientes para transmissão do código de cada etiqueta detectada foi feito
de forma semelhante, também com multithreading.
O processo de execução do sistema se faz da seguinte forma: o cliente se conecta
ao leitor RFID que então envia o código de cada tag lida e encerra a conexão. O cliente

então se conecta ao servidor principal e faz chamadas GET com os códigos de identifi-
cação adquiridos, recebendo agora as informações dos produtos identificados. Então, o

sistema exibe na tela a listagem dos produtos e caso o operador assim escolha, a compra
é efetuada.
Para reduzir os itens no estoque, o cliente envia chamadas PUT para o servidor,
editando apenas o número de itens no estoque. Por fim, a compra é registrada na memória
através de uma conexão POST com o servidor que envia os itens comprados e a data da
compra.
### 4. Resultados e Discussões
O desenvolvimento do sistema foi feito seguindo a metodologia descrita na Seção 3 e
apresenta êxito em todas as suas funcionalidades conforme foi testado. Desde o início do
desenvolvimento, realizei testes no sistema, inicialmente em uma máquina e depois em
duas, simulando melhor a dinâmica entre os caixas e o servidor. Executei testes também
com o programa armazenado em um docker, e também foram bem-sucedidos.

O sistema funciona perfeitamente para a proposta do problema, de forma que to-
dos os seus atores conseguem se comunicar e transmitir as informações de forma correta,

além de tratar corretamente a concorrência entre diferentes máquinas através do multith-
reading e atender a todas as metas e requisitos propostos.

### 5. Conclusão

O solucionamento do problema correu bem e os resultados esperados foram atingidos, evi-
denciando a viabilidade de um sistema de supermercado automatizado e sua eficiência em

facilitar e otimizar o processo de compra. Além disso, a metodologia usada envolvendo a

arquitetura cliente-servidor se mostrou eficaz no armazenamento e gestão de estoque e o
uso de multithreading para o uso de múltiplos caixas também funcionou bem.Em suma,
este projeto demonstrou com sucesso a implementação de um sistema de supermercado
automatizado eficiente e integrado com as tecnologias de RFID e IoT.
Referências
