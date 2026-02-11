import zipfile
import os
from dotenv import load_dotenv
from requests import get


def get_conjunto_dados_info(id):
    load_dotenv()
    url = f'https://dados.gov.br/dados/api/publico/conjuntos-dados/{id}'
    token = os.getenv('DADOS_GOV_BR_TOKEN')
    headers = {
        'Accept': 'application/json',
        'chave-api-dados-abertos': token,
    }
    response = get(url, headers=headers)
    return response.json()

def download_recurso():
    url = "https://arquivos.receitafederal.gov.br/public.php/dav/files/YggdBLfdninEJX9/2023-05/Cnaes.zip"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    with get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open("Cnaes.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile("Cnaes.zip") as z:
        z.extractall("cnaes_extracted")

if __name__ == '__main__':
    id = 'cadastro-nacional-da-pessoa-juridica---cnpj'
    id_recurso = '02f4f963-751c-45d5-862c-4f01d53da45b'
    info = get_conjunto_dados_info(id)
    recurso = [recurso for recurso in info['recursos'] if recurso['id'] == id_recurso][0]
    print(recurso['url'])
