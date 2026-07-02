from pathlib import Path
import csv
import xml.etree.ElementTree as ET

from businessobjects import BOClient


DOCUMENT_ID = 41398836
OUTPUT_PATH = Path("restos_pagar_folha.csv")

client = BOClient()
client.login()

response = client.get(
    f"raylight/v1/documents/{DOCUMENT_ID}/dataproviders/DP0/flows/0"
)

root = ET.fromstring(response.content)

headers = [
    value.text
    for value in root.findall("./metadata/value")
]

rows = []
for row in root.findall("./row"):
    rows.append([
        value.text
        for value in row.findall("./value")
    ])

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"CSV salvo em: {OUTPUT_PATH.resolve()}")
print(f"Colunas: {len(headers)}")
print(f"Linhas: {len(rows)}")
