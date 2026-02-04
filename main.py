import requests
from bs4 import BeautifulSoup

URL = "https://ppggoc.eci.ufmg.br/matricula/"
TARGET_PREFIX = "* Disciplinas com vagas para isolada"

response = requests.get(URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

matches = []

for p in soup.find_all("a"):
    text = p.get_text(strip=False)  # keep original spacing
    if not text:
        continue

    # print(text)
    # breakpoint()
    left_trimmed = text.lstrip()


    if left_trimmed.startswith(TARGET_PREFIX):
        matches.append(left_trimmed)

# Output results
if matches:
    print("Matches found:\n")
    for m in matches:
        print("-", m)
else:
    print("No matching span found.")
