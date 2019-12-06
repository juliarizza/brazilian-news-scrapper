# UOL (desde 2009)

A página de notícias do site [uol.com.br](http://uol.com.br) possui um histórico de notícias acessível que exibe a página inicial do site para cada dia desde o início de 2009. Dessa forma, devemos acessar o conteúdo de cada uma dessas páginas iniciais e realizar o web scrapping.

## TODO

- [ ] Identificar os diversos tipos de notícias
- [x] Filtrar as notícias que serão coletadas (remover horóscopos, clima, etc)
- [ ] Coletar informações de tipos de mídia diferentes (fotos, vídeos, etc)
- [x] Iterar ao longo dos dias
- [x] Mudar o tipo do arquivo CSV para _append_
- [ ] Extrair a quantidade de comentários (lazyload via JavaScript)
- [x] Tratar redirecionamento para `/#404` _(tratado automaticamente pelo Scrapy)_
- [x] Habilitar pausa e continuação do processo de crawl
- [ ] Configurar _bypass_ da Paywall da Folha de São Paulo

## Explorando o Histórico

### Versões

É possível encontrar pelo menos 3 versões da página inicial do site de notícias UOL.

- **Versão 2009-2011:** versão funcional e simples, de acordo com o padrão da época.
- **Versão 2012:** erro de carregamento no layout, é possível ver apenas os links para as notícias e outras páginas.
- **Versão 2013:** versão intermediária com carregamento funcional.
- **Versão 2014:** versão intermediária com carregamento funcional.
- **Versão 2015 - 2019:** versão atual com carregamento funcional, exceto pelo ano de 2016 que possui algumas falhas de carregamento do layout.

### Código Fonte

Acessando a página de [arquivo de notícias da UOL](), podemos analisar seu código fonte.

O carregamento das páginas antigas está contido em uma `div` de id `conteudo`. Dentro dessa `div` é utilizado um `iframe` que carrega cada página antiga. O seguinte link é utilizado no iframe para a data de 01/01/2009:

```
https://noticias.uol.com.br/arquivohome/20090101home_23.jhtm
```

Assim, percebemos que a data 01/01/2009 é convertida em `20090101` para o link. Além disso, o valor `23` indica que queremos uma análise de 23 horas desse dia, isto é, o dia todo de notícias. Por isso, o caminho final para a página inicial do dia 01/01/2009 é `20090101home_23`. Portanto, sempre que quisermos realizar o web scraping de uma data diferente, basta utilizar este caminho alterando a data.

```
https://noticias.uol.com.br/arquivohome/{%Y%m%d}home_23.jhtm
```

### Versão 2009-2011

Explorando o código fonte da versão 2009-2011, conseguimos ver que existem duas áreas na página: uma `div id=menu` e outra `div id=conteudo`. Como queremos as notícias, estamos interessados no que existe dentro de `conteudo`. Deste ponto em diante, queremos todos os links contidos em tags `<a>`.

Algumas notícias já não estão mais disponíveis, por isso é importante tratar a abertura desses links para resultados `404`. As notícias que ainda se encontram disponíveis podem ser redirecionadas para diferentes formatos de exibição dependendo do seu domínio. Por exemplo, notícias de [folha.uol.com.br](http://folha.uol.com.br) serão exibidas no formato atual da Folha de São Paulo; notícias de [esporte.uol.com.br](http://esporte.uol.com.br) serão exibidas no formato atual da página de esportes da UOL; e assim por diante.

### Versão 2012

Nesta versão, todas as notícias se encontram dentro de uma `div id=corpoEsquerda` e em seguida uma `div id=corpoEsquerdaPrincipal`. Nesta div, conseguimos separar o menu da `div id=modulos`, que contem as notícias. Portanto, deste ponto em diante podemos capturar todos os links.

Novamente, algumas notícias não existem mais e outras são redirecionadas para a versão atual de seus provedores. No entanto, também é possível encontrar notícias no modelo de layout antigo.

### Versão 2013

A organização da página nesta versão é exatamente a mesma da versão de 2012, onde o conteúdo de notícias fica na `div` de id `modulos`, dentro de `corpoEsquerdaPrincipal`. Isto leva a crer que esta versão e a de 2012 são, na verdade, a mesma. No entanto, a versão de 2012 encontra-se com o link com a folha de estilos desconfigurado.

### Versão 2014

Nesta versão a organização também segue a mesma estrutura de markup, porém com uma nova folha de estilos. Dessa forma, a aparência muda mas o conteúdo segue disponível pelo mesmo processo.

### Versão 2015-2019

Nesta versão, a organização da página é modificada. Agora, as notícias de maior destaque estão separadas em uma `div id=horizontalEspeciais`. O restante das notícias está armazenado em uma `div id=corpoEsquerdaPrincipal`.

Esta é a versão utilizada até os dias de hoje, portanto todas as notícias ainda estão disponíveis e são acessíveis pelos formatos de página atuais.

## Explorando as notícias

Onde estão os principais dados de cada notícia? Como podem ser acessados? Quais as diferenças de uma versão para outra?

### Folha de São Paulo

As notícias que redirecionam para a página da Folha de São Paulo estão no domínio [www1.folha.uol.com.br](https://www1.folha.uol.com.br). É possível identificar os seguintes dados destas notícias:

- **Categoria** - armazenada dentro do elemento `h1` em uma `div class=section-masthead`.
- **Título** - o título da notícia é acessível pelo elemento `<h1 itemprop="headline">`, dentro do `header` do `article id=news`.
- **Autor** - o autor é acessível pelo primeiro elemento `<b>` dentro de `<div class="author" itemprop="author">`.
- **Data e Hora** - acessível pelo elemento `<time>` logo após o autor, também dentro do `header` do `article id=news`.
- **Quantidade de Comentários** - acessível pelo elemento `<a class="more">` dentro do `header` de uma `<div id="article-comments">`.
- **URL**
- **Fonte** - Folha de São Paulo

**Observação:** A folha possui um mecanismo de limitação da leitura por assinatura, portanto múltiplas requisições podem ser um problema.

### UOL - Versão Antiga

Refere-se a qualquer subdomínio comum da UOL, como UOL Notícias e UOL Esportes. É possível identificar os seguintes dados destas notícias:

- **Categoria** - encontrada no hyperlink de classe `canal` dentro da `div id=barra-estacao`.
- **Título** - o título da notícia é acessível pelo `h1` dentro da `div` de classe `conteudo` que pertence à `div id=titulo`.
- **Autor** - o autor é acessível pelo primeiro elemento da `div id=credito-texto`, dentro da `div` de classe `conteudo` que pertence à `div id=titulo`.
- **Data e Hora** - acessível pelo elemento `<h2>` dentro da `div` de classe `conteudo` que pertence à `div id=titulo`.
- **Local** - acessível pelo segundo elemento da `div id=credito-texto`, dentro da `div` de classe `conteudo` que pertence à `div id=titulo`.
- **URL**
- **Fonte** - UOL Notícias, UOL Esportes, etc.

### UOL - Versão Atualizada I

Refere-se a qualquer subdomínio comum da UOL, como UOL Notícias e UOL Esportes. É possível identificar os seguintes dados destas notícias:

- **Categoria** - encontrada no elemento `h4` de classe `title-name`, dentro da `div` de classe `title`.
- **Título** - o título da notícia é acessível pelo elemento `h1` dentro do `header` do `article`.
- **Autor** - o autor é acessível pelo elemento `p` de classe `p-author`.
- **Data e Hora** - acessível pelo elemento `p` que contém ambas as classes `p-author time`.
- **Local** - acessível pelo elemento `p` que contém ambas a classe `p-author-local`.
- **Quantidade de Comentários** - acessível pelo elemento `<strong>` dentro do `<h4>` de uma `<div class="comments-total">`.
- **URL**
- **Fonte** - UOL Notícias, UOL Esportes, etc.

### UOL - Versão Atualizada II

Refere-se a qualquer subdomínio comum da UOL, como UOL Notícias e UOL Esportes. É possível identificar os seguintes dados destas notícias:

- **Categoria** - encontrada no hyperlink de classe `estacao`, dentro da `div id=titulo-uol`.
- **Título** - o título da notícia é acessível pelo elemento `h1` dentro do `header` do `article id=conteudo-principal`.
- **Autor** - o autor é acessível pelo elemento `span` de classe `com-autor` dentro do header.
- **Data e Hora** - acessível pelo elemento `time` dentro do header.
- **Quantidade de Comentários** - acessível pelo elemento `<strong>` dentro do `<h4>` de uma `<div class="comments-total">`.
- **URL**
- **Fonte** - UOL Notícias, UOL Esportes, etc.

### UOL - Versão Atualizada III

Refere-se a qualquer subdomínio comum da UOL, como UOL Notícias e UOL Esportes. É possível identificar os seguintes dados destas notícias:

- **Categoria** - encontrada no hyperlink de classe `estacao`, dentro da `div id=titulo-uol`.
- **Título** - o título da notícia é acessível pelo elemento `h1` dentro da `div id=texto`.
- **Autor** - o autor é acessível pelo primeiro elemento do `span` de classe `autor` dentro da `div id=texto`.
- **Data e Hora** - acessível pelo elemento `em` de classe `dataAtualizacao` dentro da `div id=texto`.
- **Local** - acessível pelo segundo elemento do `span` de classe `autor` dentro da `div id=texto`.
- **Quantidade de Comentários** - acessível pelo elemento `<strong>` dentro do `<h4>` de uma `<div class="comments-total">`.
- **URL**
- **Fonte** - UOL Notícias, UOL Esportes, etc.

### Páginas Não Relacionadas

Algumas notícias da página principal da UOL, principalmente em suas versões antigas, não são de fato notícias. Geralmente são galerias de fotos, jogos, horóscopo, entre outros tipos de páginas não relevantes para essa busca. Por isso, é importante tratar uma página para ser ignorada quando não forem encontrados os elementos básicos de uma notícia.

### Páginas Não Encontradas

Quando uma notícia não é encontrada, somos redirecionados para a página inicial da UOL com um pós-fixo `/#404` na URL. A página é carregada normalmente com um modal informando o erro, portanto a página em si não retorna um `404`. Por isso, é importante tratar esse caso especial em que o resultado da requisição é `200` mas na verdade temos um erro.
