from __future__ import annotations

import os
import warnings
import xml.etree.ElementTree as ET

import requests
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning


class BOClient:
    def __init__(self) -> None:
        load_dotenv()

        self.base_url = os.getenv("BO_BASE_URL", "").rstrip("/")
        self.user = os.getenv("BO_USER")
        self.password = os.getenv("BO_PASSWORD")
        self.auth = os.getenv("BO_AUTH", "secEnterprise")
        self.verify_ssl = os.getenv("BO_VERIFY_SSL", "true").lower() == "true"

        if not self.base_url:
            raise ValueError("BO_BASE_URL não definido no .env")
        if not self.user or not self.password:
            raise ValueError("BO_USER e BO_PASSWORD devem estar definidos no .env")

        if not self.verify_ssl:
            warnings.simplefilter("ignore", InsecureRequestWarning)

        self.session = requests.Session()
        self.token: str | None = None

    def login(self) -> str:
        response = self.session.post(
            f"{self.base_url}/logon/long",
            headers={
                "Content-Type": "application/xml",
                "Accept": "application/xml",
            },
            data=self._login_payload().encode("utf-8"),
            verify=self.verify_ssl,
            timeout=30,
        )

        if response.status_code != 200:
            print(response.text[:1000])
            response.raise_for_status()

        self.token = self._extract_token(response.text)
        return self.token

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        if not self.token:
            self.login()

        response = self.session.get(
            f"{self.base_url}/{path.lstrip('/')}",
            headers={
                "Accept": "application/xml",
                "X-SAP-LogonToken": self.token or "",
            },
            params=params,
            verify=self.verify_ssl,
            timeout=30,
        )

        if response.status_code >= 400:
            print("URL:", response.url)
            print(response.text[:1000])
            response.raise_for_status()

        return response

    def _login_payload(self) -> str:
        return f"""
<attrs xmlns="http://www.sap.com/rws/bip">
  <attr name="userName" type="string">{self.user}</attr>
  <attr name="password" type="string">{self.password}</attr>
  <attr name="auth" type="string">{self.auth}</attr>
</attrs>
""".strip()

    def _extract_token(self, xml_text: str) -> str:
        root = ET.fromstring(xml_text)
        ns = {"bip": "http://www.sap.com/rws/bip"}

        token = root.find(".//bip:attr[@name='logonToken']", ns)

        if token is None or not token.text:
            raise RuntimeError("Token de logon não encontrado.")

        return token.text
