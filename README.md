# fakenews-api-py

## Descrição

Todo o código aqui apresentado serviu como parte integrante de um projeto final de curso ***Botcamp*** da [LetsBot](https://www.letsbot.com.br/). 

O tema do projeto consiste na criação de um chatbot de auxilio no combate às Fakenews, por forma a contribuir para esta causa.

Um dos muitos temas que o chatbot vai responder é a capacidade de avaliar se uma notícia é verdadeira ou falsa, recorrendo à Inteligência Artifical. É neste ponto que entra esta API realizada em Python.

O projeto vai ser criado em Dialogflow, que irá usar o webhook para detetar fakenews de forma inteligente, e é aqui que entra a API. 

## Objetivo

O desafio foi criar uma API que fosse chamada pelo chatbot para detectar se uma determinada notícia, dada por um URL, é verdadeira ou não.
um segundo desafio era fazer o código e disponibilizar na cloud ser qualquer custo, até porque é um projeto académico. Para tal foram apenas usadas ferramentas open source, como será descrito mais à frente.

## Grupo de trabalho

O projeto é composto por 6 elementos

[Carolina Santos](https://www.linkedin.com/in/mariacarolinademelosantos/) PO / UX Writer /Curadoria <br>
[Adriana Melo](https://www.linkedin.com/in/adriana-poletimelo/) UX Writer <br>
[Andréa Araújo](www.linkedin.com/in/andrea-araujo-749b1960/) UX Research / UX Writer <br>
[Domingos Lemos](www.linkedin.com/in/domingos-lemos-51b71970/) Scrum Master / Desenvolvedor <br>
[Marconne Resende](www.linkedin.com/in/marconnebiblio/) UX Research <br>
[Pedro Edgar](https://www.linkedin.com/in/pedro-edgar-240780205/) Desenvolvedor / Curadoria <br>

E a nossa mentora de projeto: [Ariana de Souza](https://www.linkedin.com/in/arianesouza/) <br>


## Pressupostos/limitações

Esta API tem as seguintes limitações:
* Apenas responde à língua pt-br
* O dataset usado para o modelo incluí duas categorias: política e saúde
* Só aceita URL de sites de notícias em formato texto. (imagens, som e vídeos não estão contemplados)
* O Dialogflow como canal não permite entrada pelo user maior que 256 caracteres, por isso a única forma de validar uma notícia é por ULR
* O tempo de espera de resposta de uma chamada a API pelo Dialogflow é de 5 segundos. Para ler a notícia de um site é necessário aceder ao mesmo e verificámos que alguns tiveram uma resposta superior a 5 segundos. Neste caso, apesar a API responder, o DF não tem em conta essa resposta.

Alguns pressupostos a considerar:
* Se o site não for de uma notícia o mais certo é que o resultado seja inconclusivo
* Valida-se sempre qualquer link que seja colocado pelo user, mesmo que não sejam das catergorias mensionadas nas limitações. Espera-se que os users façam bom uso com as indicações que lhe serão prestadas. 

## Ferramentas usadas

A lista de ferramentas usadas, para a construção desta API, são todas open source. Este foi um ponto assente na nossa escolha.

* Github e Github Desktop: para gestão do código
* Jupyter Notebook: para exploração preparação do dataset e construção e validação do modelo. Também foi usado na preparação do scraping.
* Visual Studio IDE: uma ferramenta da Microsoft que ajuda muito na construção do código.
* Heroku: plataforma para deploy do projeto na nuvem
* Dialogflow essencial: para testar a chamada da API em ambiente chatbot
* Python: linguagem de programação usada

## Roadmap

Aumentar as categorias treinadas<br>
Passar a aceitar mensagens de voz <br>

## Estrutura/setup do projecto

Um projeto desta complexidade e envolvendo tanta tecnologia, foi essencial recorrer à documentação de cada ferramenta. <br>
O código usado em todo o processo é todo em python. 
Os próximos capítulos vão ajudar a compreender melhor o que está feito, não tendo como objetivo entrar em grande profundidade.

### Setup

Para ver os notebooks que auxiliaram na preparação do código final, será necessário instalá-lo. Caso já o tenha, não será necessário fazer nada. <br> 
Pode recorrer a duas fontes: <br>
* Instalar apenas o jupyter notebook clássico (https://jupyter.org/) 
* Instalar através do Anaconda, que é muito usado pelos Data Science (https://www.anaconda.com/)

Como editor de código, eu usei o [Visual Studio IDE](https://visualstudio.microsoft.com/), que já vem linkado com o Github Desktop. Mas pode usar qualquer outro IDE ou até um simples editor de texto.

Vai ser necessário ter o [Python](https://www.python.org/) instalado no PC. Caso tenha instalado o Anaconda, já tem o python instalado assim como as principais bibliotecas. 

Será necessário criar uma conta no [Github](https://github.com/), para poder clonar o código do projeto para o seu PC.

Terá que criar uma conta no [Heroku](https://www.heroku.com/) para fazer o deploy do código na web. Pode arranjar outras soluções como virtualização na cloud dos grandes players, mas no Heroku pode fazer deploy de até 5 projetos de forma gratuíta.

A criação de conta no [Dialogflow Essentials](https://dialogflow.cloud.google.com/) não será obrigatório, mas simplifica muito na experimentação da api já na vertente do chatbot. Foi por essa razão que usei, mas pode sempre usar outras ferramentas como o Postman ou o SoapUI.

### API do webhook

Para criar um webhook para usar no chatbot, recorri ao Heroku (https://www.heroku.com/). Se não conhece, este site permite fazer deploy de web ou a exposição de API de forma gratuita (com limitação até 5 projetos).

Não é o meu propósito explicar os passos necessários para a criação das APIs, uma vez que há muitos videos na web a ensinar. Caso pretenda experimentar, pode usar a minha API criada para este projeto e que se encontra no código fonte.

### Estrutura do projeto

O projeto está dividido em dois grandes blocos de código, uma para fazer scraping às páginas das notícias e o outro para treinar o modelo na deteção de fakes.

| Ficheiro | Descrição |
| -------- | --------- |
| app.py | ficheiro principal que recebe as chamadas externas e procede de acordo com o pedido |
| predict.py | Lê os dados, prepara-os e constroi o modelo. Tem também as funções necessárias para analizar o conteúdo da notícia |
| scraping_noticia.py | Serve para interpretar e recolher algum conteúdo de uma página web, tal como o título, a notíca, o autor e a data da notícia | 
| FakeRecogna.xlsx | Ficheiro disponibilizado na web (ver em referências o link) com o dataset classificativo de ~12k notícias | 
| Prepare_data_and_model.ipynb | Ficheiro com o código de preparação do modelo. Não é ficheiro de texto standard e deve ser aberto pelo Jupyter Notebook |
| GetBodyURL.ipynb | Mais um ficheiro de auxilio na parte de scraping |

### Módulos

Estou a considerar um módulo cada ficheiro python com um conjunto de código e funções.<br>
Vou explicar alguns pontos do código, embora os mesmos estejam bem documentados com comentários ao longo do código.

#### Módulo Principal (app.py)

Para o python funcionar com web usei a library "flask".<br>
Apenas tem duas rotas desenvolvidas, a route (/) e a fakenews (/fakenews)

> @app.route("/", methods=["GET"])

Que serve apenas para informar que o serviço está ativo.

> @app.route('/fakenews', methods=['POST'])

Este bloco é o detector de fakes (action == 'predict")<br>
A primeira etapa é validar que o URL foi passado. Depois valida o mesmo com uma pequena base de conhecimento de sites confiáveis/fakes e se for encontrado na bd responde de acordo com a informação que tem.<br>
Por último, faz a interpretação do site e leitura dos campos necessários que são passados à função centrar da previsão (predict.valid_url)<br>

#### Módulo Predict (predict.py)

Começa por ler o dataset para um dataframe, prepara e treina o modelo (usado  modelo PassiveAggressive do sklearn).<br>
A função central para validar uma notícia é o "valid_url". Dentro deste tem todas as regras de validação e é de onde saí o resultado para trás.<br>
Regras:<br>
* valida se o autor é confiável.
* se não for, valida o ano da notícia >= 2019
* se for >= 2019 vai validar a notícia
* se não foi conclusívo, vai validar o titulo
     
O processo de validação pode terminar em qualquer ponto, caso a regra seja cumprida. <br>
Pontos a reter:<br>
* os títulos so são considerados se o comprimento > 50 caracteres
* só considera a data se no mesmo existir um número com 4 digitos (correspondente ao Ano)


#### Módulo Scraping (scraping_noticia.py)

Este modulo extrai o conteúdo de um link web (URL). Começa por abrir a página, procura os campos com base numas referências e por fim fecha a página para libertar memória.<br>
Os campos lidos são:
| campo | descrição | regra |
| ----- | --------- | ----- |
| titulo | o título | devolve o valor da tag "title" |
| autor | o autor | procura a palavra "uthor" dentro do vlor do atributo "class" de qualquer tag |
| dt | data da notícia (texto) | Muitas vezes a data vem no texto do autor. É usado regular expression para capturar a data, apesar de que apenas é pretendido o ano | 
| body | corpo da notícia | procura os primeiros 3 tag "p" (de parágrafo) com comprimento > 150 caracteres | 


### Executar o projeto:

Não há uma solução única de fazer upload do código no com o Github ou Heroku, ou testar o bot dentro do Dialogflow ou numa página web. Por isso, irei mostrar a minha forma de preparar e executar o projeto.

#### Github e Github Desktop

Começo por criar o projeto em Github e depois 
## Bibliografia



