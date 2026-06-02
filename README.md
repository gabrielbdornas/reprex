# Reprex MarkItDown

Este repositório é um exemplo mínimo para converter arquivos em Markdown usando
o [MarkItDown](https://github.com/microsoft/markitdown), biblioteca da Microsoft
para extrair conteúdo de documentos e representá-lo em Markdown.

O caso de uso principal aqui é converter arquivos como PDF para `.md`, mantendo
texto, tabelas e alguma estrutura do documento em um formato mais fácil de ler,
versionar e enviar para fluxos com LLMs.

## Sobre o MarkItDown

Sim, conheço a biblioteca. O MarkItDown é um pacote Python e uma ferramenta de
linha de comando para converter diversos formatos para Markdown, incluindo:

- PDF
- DOCX
- PPTX
- XLSX
- HTML
- CSV, JSON e XML
- imagens, áudio, EPUB, ZIP e outros formatos, dependendo das dependências
  instaladas

Neste projeto, o `pyproject.toml` usa uma cópia local do MarkItDown:

```toml
markitdown[all] @ file:///home/gabrielbdornas/code/gabrielbdornas/reprex/markitdown/packages/markitdown
```

Ou seja, os comandos rodam contra a versão local disponível em `markitdown/`.

## Instalação

Instale as dependências com Poetry:

```bash
poetry install
```

Confira se o comando está disponível:

```bash
poetry run markitdown --version
```

## Como converter arquivos para Markdown

A sintaxe desta versão local é:

```bash
poetry run markitdown caminho/do/arquivo.pdf -o caminho/do/arquivo.md
```

Também é possível redirecionar a saída:

```bash
poetry run markitdown caminho/do/arquivo.pdf > caminho/do/arquivo.md
```

Exemplo com o arquivo deste repositório:

```bash
poetry run markitdown itau_proposta.pdf -o itau_proposta.md
```

## Observação sobre `markitdown convert`

Nesta versão instalada no projeto (`markitdown 0.1.6`), o CLI não usa o
subcomando `convert`. O próprio comando `markitdown` já executa a conversão:

```bash
poetry run markitdown itau_proposta.pdf -o itau_proposta.md
```

Se você viu algum exemplo com `markitdown convert`, ele provavelmente pertence a
outra versão, wrapper ou integração. Para confirmar a sintaxe da versão atual do
projeto, rode:

```bash
poetry run markitdown --help
```

## Uso via Python

Também dá para usar a biblioteca diretamente em Python:

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("itau_proposta.pdf")

print(result.text_content)
```

## Arquivos principais

- `itau_proposta.pdf`: arquivo de entrada usado no exemplo.
- `itau_proposta.md`: Markdown gerado a partir do PDF.
- `pyproject.toml`: configuração do projeto e dependência local do MarkItDown.
- `markitdown/`: cópia local do projeto MarkItDown.

## Limitações

A saída em Markdown é pensada principalmente para análise textual, indexação e
uso com LLMs. Em PDFs com tabelas complexas, colunas, textos duplicados ou layout
visual muito carregado, a conversão pode exigir revisão manual.
