from pathlib import Path
import os
import requests
from requests.auth import HTTPBasicAuth

URL = os.environ["VPN_URL"]
OUTPUT = Path("Standard-Configurations-Archive.zip")

USERNAME = os.environ["PRODEMGE_USER"]
PASSWORD = os.environ["PRODEMGE_PASSWORD"]


def download_file():
    with requests.get(
        URL,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        stream=True,
        timeout=60,
        headers={
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "Chrome/136.0.0.0 Safari/537.36"
        )
    },
    ) as response:
        response.raise_for_status()

        with open(OUTPUT, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    print(f"Download concluído: {OUTPUT.resolve()}")


if __name__ == "__main__":
    download_file()
