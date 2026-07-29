# Upload em lote para YouTube

#### IMPORTANTE

**Olhar `*.json` pc CAMG**.

Script em Python para enviar videos de uma pasta para o YouTube em ordem natural de numeracao, por exemplo `1.1.mp4`, `1.2.mp4`, `1.10.mp4`.

## O que ele configura

- Privacidade como `private`.
- `selfDeclaredMadeForKids=false`, ou seja, nao feito para criancas.
- Adiciona cada video na playlist `Leilões`, ou na playlist indicada por ID.
- Define `defaultLanguage=pt-BR` para ajudar o YouTube a tratar os metadados como portugues.
- Gera `youtube_uploads.csv` com link do video e emails informados.
- Encurta automaticamente titulos acima de 100 caracteres, limite aceito pelo YouTube.

Limites da API: a YouTube Data API permite upload e playlist, mas nao expõe um campo para convidar emails para assistir videos privados. Esse convite precisa ser feito manualmente no YouTube Studio. As legendas/transcricoes automaticas tambem nao podem ser forcadas via API; o YouTube publica automaticamente quando o video for elegivel e o processamento terminar.

## Preparacao

1. No Google Cloud Console, crie ou escolha um projeto.
2. Ative a **YouTube Data API v3**.
3. Crie um OAuth Client ID do tipo **Desktop app**.
4. Baixe o JSON e salve como `client_secrets.json` na raiz deste projeto.
5. Instale as dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

Primeiro confira a ordem sem enviar nada:

```bash
python3 youtube_bulk_upload.py /caminho/para/videos --dry-run
```

Depois envie:

```bash
python3 youtube_bulk_upload.py /caminho/para/videos \
  --playlist-name "Leilões" \
  --share-email primeiro@gmail.com \
  --share-email segundo@gmail.com
```

Por padrao, o titulo do video vem do nome do arquivo sem a extensao. Se quiser usar outro limite:

```bash
python3 youtube_bulk_upload.py /caminho/para/videos --title-max-length 90
```

Se voce ja souber o ID da playlist, prefira:

```bash
python3 youtube_bulk_upload.py /caminho/para/videos --playlist-id PLxxxxxxxxxxxxxxxx
```

No primeiro uso, o navegador vai abrir para autorizar a conta do YouTube. O token fica salvo em `token.json`.
