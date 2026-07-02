from businessobjects import BOClient, InfoStore
import os
from dotenv import load_dotenv


load_dotenv()

client = BOClient()
client.login()

infostore = InfoStore(client)

USER_FOLDERS_ID = 18
USER_LOGIN = os.getenv("BO_USER").upper()
# breakpoint()  # Adicione um breakpoint aqui para depuração
PASTA_ALVO = "AID/SPLOR"


usuarios = infostore.listar_todos_filhos(
    USER_FOLDERS_ID,
    page_size=100,
    max_pages=500,
)

usuario = next((obj for obj in usuarios if obj.name == USER_LOGIN), None)

if not usuario:
    raise RuntimeError(f"Usuário {USER_LOGIN} não encontrado.")


pastas_usuario = infostore.listar_todos_filhos(
    usuario.id,
    page_size=100,
    max_pages=100,
)

aid_splor = next((obj for obj in pastas_usuario if obj.name == PASTA_ALVO), None)

if not aid_splor:
    raise RuntimeError(f"Pasta {PASTA_ALVO} não encontrada.")


print(f"Pasta encontrada: {aid_splor.id} - {aid_splor.name}")


print("\nRelatórios WebI diretamente em AID/SPLOR:")
for relatorio in infostore.listar_webi(aid_splor.id):
    print(relatorio.id, relatorio.name)


print("\nBuscando pastas chamadas dados_siafi dentro de AID/SPLOR:")

pastas_dados_siafi = infostore.buscar_recursivo(
    aid_splor.id,
    "dados_siafi",
    exact=True,
    max_depth=5,
)

if not pastas_dados_siafi:
    print("Nenhuma pasta dados_siafi encontrada.")
    raise SystemExit


for pasta in pastas_dados_siafi:
    print(pasta.id, pasta.name, pasta.type)


dados_siafi = pastas_dados_siafi[0]

print(f"\nRelatórios WebI diretamente em {dados_siafi.name}:")
for relatorio in infostore.listar_webi(dados_siafi.id):
    print(relatorio.id, relatorio.name)
