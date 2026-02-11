import zipfile
import os
from dotenv import load_dotenv
import requests
from xml.etree import ElementTree as ET



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

def get_main_page():
    # See https://chatgpt.com/share/698cf7b1-5fd0-8003-8014-4ebe76f956b3
    url = "https://arquivos.receitafederal.gov.br/public.php/dav/files/YggdBLfdninEJX9/2025-11/"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Depth": "1",                     # list current directory
        "Content-Type": "application/xml"
    }

    # Empty body is usually enough for Nextcloud public shares
    response = requests.request(
        method="PROPFIND",
        url=url,
        headers=headers
    )

    response.raise_for_status()

    xml = ET.fromstring(response.content)
    ns = {"d": "DAV:"}

    files = []

    for resp in xml.findall("d:response", ns):
        href = resp.find("d:href", ns)
        if href is not None:
            files.append(href.text)

    zip_files = [
        f for f in files
        if f.lower().endswith(".zip")
    ]

    for f in zip_files:
        print("https://arquivos.receitafederal.gov.br" + f)



if __name__ == '__main__':
    # id = 'cadastro-nacional-da-pessoa-juridica---cnpj'
    # id_recurso = '02f4f963-751c-45d5-862c-4f01d53da45b'
    # info = get_conjunto_dados_info(id)
    # recurso = [recurso for recurso in info['recursos'] if recurso['id'] == id_recurso][0]
    # print(recurso['url'])
    get_main_page()
