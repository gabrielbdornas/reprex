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

if __name__ == '__main__':
    id = 'cadastro-nacional-da-pessoa-juridica---cnpj'
    id_recurso = '02f4f963-751c-45d5-862c-4f01d53da45b'
    info = get_conjunto_dados_info(id)
    recurso = [recurso for recurso in info['recursos'] if recurso['id'] == id_recurso][0]
    print(recurso['link'])
