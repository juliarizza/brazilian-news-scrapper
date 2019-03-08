# UOL (desde 2009)
A página de notícias do site [uol.com.br](http://uol.com.br) possui um histórico de notícias acessível que exibe a página inicial do site para cada dia desde o início de 2009. Dessa forma, devemos acessar o conteúdo de cada uma dessas páginas iniciais e realizar o web scraping.

## Explorando o Histórico

### Versões
É possível encontrar pelo menos 3 versões da página inicial do site de notícias UOL.
* **Versão 2009-2011:** versão funcional e simples, de acordo com o padrão da época.
* **Versão 2012:** erro de carregamento no layout, é possível ver apenas os links para as notícias e outras páginas.
* **Versão 2013:** versão intermediária com carregamento funcional.
* **Versão 2014:** versão intermediária com carregamento funcional.
* **Versão 2015 - 2019:** versão atual com carregamento funcional, exceto pelo ano de 2016 que possui algumas falhas de carregamento do layout.

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


