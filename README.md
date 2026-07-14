# SIAFI — pipeline de dados e painel

Este repositório baixa o data package do SIAFI 2026 (execução orçamentária de
MG), gera tabelas fato por recurso mais uma "linktable" (tabela ponte) que
conecta os recursos entre si por dimensões em comum, e serve um painel em
[Observable Framework](https://observablehq.com/framework/) para explorar a
tabela `credito` filtrando por qualquer dimensão presente em qualquer um dos
outros recursos.

## Como funciona

1. **`data.toml`** descreve de onde baixar o data package (repositório
   `splor-mg/dados-armazem-siafi-2026`). O comando `dpm install` lê esse
   arquivo e baixa o pacote para `datapackages/siafi/`.

2. **`scripts/main.py`** processa cada *resource* do data package
   (`cota`, `execucao`, `credito`, `receita`, `alteracoes_orcamentarias`,
   `restos_pagar`, `restos_pagar_folha`, `execucao_alem_credito`):
   - separa as colunas de cada recurso em **dimensões** (tudo que não começa
     com `vlr_`) e **fatos** (colunas `vlr_*`, os valores monetários);
   - calcula uma **chave** por linha, concatenando os valores das dimensões
     desse recurso com `|`;
   - grava `datapackages/siafi/data/linktable/fact_<recurso>.csv.gz`: apenas
     a chave + as colunas de fato;
   - acumula as linhas de dimensão (sem os fatos, deduplicadas) de todos os
     recursos e as empilha em uma única tabela, adicionando uma coluna
     `key_<recurso>` para cada recurso — essa é a
     `datapackages/siafi/data/linktable/linktable.csv.gz`. Uma mesma linha da
     linktable pode ter `key_credito` preenchida e `key_execucao` vazia (ou
     vice-versa), dependendo de qual recurso originou aquela combinação de
     dimensões.

   Todos os campos de dimensão no `datapackage.json` precisam ser do tipo
   `"string"`. Se algum vier como `"integer"`/`"number"`, o pandas carrega a
   coluna em um dtype numérico *nullable*; ao empilhar recursos que não têm
   aquela coluna, o `pandas.concat` promove a coluna para `float64` e valores
   como `1231` viram `"1231.0"` na chave — quebrando o encontro com a chave
   já gravada (em texto puro) no `fact_<recurso>.csv.gz`.

3. **`docs/data/*.py`** são *data loaders* do Observable Framework, executados
   em tempo de build/preview (apenas biblioteca padrão do Python, sem
   depender do virtualenv do Poetry estar ativo):
   - `fact_credito.csv.py`: repassa `fact_credito.csv.gz` descompactado, sem
     alterações (3.130 linhas, todos os campos).
   - `credito-filters.json.py`: para cada `key_credito`, varre a linktable
     inteira e monta um índice compacto (`{columns, options, facets}`) com os
     valores de dimensão que aquela chave já assumiu em qualquer recurso.

     Esse índice existe porque `credito` tem só 11 dimensões, mais grosseiras
     que as ~30 de `execucao` (que inclui `num_empenho`, quase um id único de
     transação). Um `JOIN` direto entre `fact_credito` e a `linktable`
     produziria centenas de milhares de linhas — cada uma das 3.130 linhas de
     `credito` repetida dezenas ou centenas de vezes. O índice de facetas
     evita isso: o navegador nunca baixa a linktable inteira nem uma junção
     "explodida", só esse índice pequeno (poucos MB) usado para filtrar as
     3.130 linhas originais por pertencimento a um conjunto.

4. **`docs/index.md`** é o painel: um filtro (`select`) para cada coluna de
   dimensão presente na linktable, e uma tabela com todas as linhas/colunas
   de `fact_credito` que batem com os filtros ativos.

## Pré-requisitos

- Python + [Poetry](https://python-poetry.org/) (pipeline de dados)
- Node.js + npm (painel)
- Variável de ambiente `GH_TOKEN` (usada pelo `dpm` para baixar o data
  package — já configurada em `.env`)

## Rodando o pipeline de dados

```bash
poetry install
poetry run dpm install          # baixa/atualiza datapackages/siafi/ a partir de data.toml
poetry run python scripts/main.py   # gera datapackages/siafi/data/linktable/*.csv.gz
```

## Vendo o painel

```bash
npm install
npm run dev     # inicia o servidor de preview e mostra a URL local (ex: http://127.0.0.1:3000)
```

Para gerar o site estático (ex.: para publicar):

```bash
npm run build    # gera em dist/
```

## Estrutura

```
data.toml                          # de onde o dpm baixa o data package
scripts/main.py                    # ETL: gera fact_*.csv.gz e linktable.csv.gz
datapackages/siafi/                # data package baixado + dados gerados
  datapackage.json
  data/
    *.csv.gz                       # dados brutos baixados
    linktable/
      fact_<recurso>.csv.gz        # chave + colunas de fato, por recurso
      linktable.csv.gz             # dimensões empilhadas + uma key_<recurso> por recurso
docs/                              # site do Observable Framework
  index.md                         # o painel
  data/
    fact_credito.csv.py            # loader: repassa fact_credito.csv.gz
    credito-filters.json.py        # loader: monta o índice de facetas para os filtros
observablehq.config.js             # configuração do site (título etc.)
```
