from __future__ import annotations

import os
import warnings
import xml.etree.ElementTree as ET
from typing import Any

import requests
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning


class BusinessObjectsClient:
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
        url = f"{self.base_url}/logon/long"

        payload = f"""
<attrs xmlns="http://www.sap.com/rws/bip">
  <attr name="userName" type="string">{self.user}</attr>
  <attr name="password" type="string">{self.password}</attr>
  <attr name="auth" type="string">{self.auth}</attr>
</attrs>
""".strip()

        response = self.session.post(
            url,
            headers={
                "Content-Type": "application/xml",
                "Accept": "application/xml",
            },
            data=payload.encode("utf-8"),
            verify=self.verify_ssl,
            timeout=30,
        )

        if response.status_code != 200:
            print("Erro no login.")
            print("Status:", response.status_code)
            print("Resposta:", response.text[:1000])
            response.raise_for_status()

        self.token = self._extract_logon_token(response.text)
        return self.token

    def get(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        if not self.token:
            self.login()

        url = f"{self.base_url}/{path.lstrip('/')}"

        response = self.session.get(
            url,
            headers={
                "Accept": "application/xml",
                "X-SAP-LogonToken": self.token or "",
            },
            params=params,
            verify=self.verify_ssl,
            timeout=30,
        )

        if response.status_code >= 400:
            print("Erro na requisição GET.")
            print("URL:", response.url)
            print("Status:", response.status_code)
            print("Resposta:", response.text[:1000])
            response.raise_for_status()

        return response

    def listar_objetos(self, top: int = 50) -> list[dict[str, Any]]:
        response = self.get("infostore", params={"top": top})
        return self._parse_infostore_entries(response.text)

    def consultar_infostore(self, query: str, top: int = 50) -> list[dict[str, Any]]:
        query = " ".join(query.split())

        response = self.get(
            "infostore",
            params={
                "query": query,
                "top": top,
            },
        )

        return self._parse_xml_seguro(response.text)

    def listar_pastas(self, top: int = 50) -> list[dict[str, Any]]:
        query = """
        SELECT SI_ID, SI_NAME, SI_KIND, SI_CUID
        FROM CI_INFOOBJECTS
        WHERE SI_KIND = 'Folder'
        """
        return self.consultar_infostore(query, top=top)

    def listar_relatorios_webi(self, top: int = 50) -> list[dict[str, Any]]:
        query = """
        SELECT SI_ID, SI_NAME, SI_KIND, SI_CUID
        FROM CI_INFOOBJECTS
        WHERE SI_KIND = 'Webi'
        """
        return self.consultar_infostore(query, top=top)

    def buscar_por_nome(self, termo: str, top: int = 50) -> list[dict[str, Any]]:
        query = f"""
        SELECT SI_ID, SI_NAME, SI_KIND, SI_CUID
        FROM CI_INFOOBJECTS
        WHERE SI_NAME LIKE '%{termo}%'
        """
        return self.consultar_infostore(query, top=top)

    def _extract_logon_token(self, xml_text: str) -> str:
        root = ET.fromstring(xml_text)

        namespaces = {
            "bip": "http://www.sap.com/rws/bip",
        }

        token_element = root.find(".//bip:attr[@name='logonToken']", namespaces)

        if token_element is None or not token_element.text:
            raise RuntimeError("Token de logon não encontrado na resposta do BO.")

        return token_element.text

    def _parse_xml_seguro(self, xml_text: str) -> list[dict[str, Any]]:
        try:
            return self._parse_infostore_entries(xml_text)
        except ET.ParseError:
            print("Resposta não era XML válido:")
            print(xml_text[:1000])
            raise

    def _parse_infostore_entries(self, xml_text: str) -> list[dict[str, Any]]:
        root = ET.fromstring(xml_text)

        namespaces = {
            "atom": "http://www.w3.org/2005/Atom",
            "bip": "http://www.sap.com/rws/bip",
        }

        objetos: list[dict[str, Any]] = []

        for entry in root.findall("atom:entry", namespaces):
            objeto: dict[str, Any] = {}

            title = entry.find("atom:title", namespaces)
            if title is not None:
                objeto["title"] = title.text

            for attr in entry.findall(".//bip:attr", namespaces):
                name = attr.attrib.get("name")
                value = attr.text

                if name:
                    objeto[name] = value

            objetos.append(objeto)

        return objetos

    def listar_filhos(self, object_id: int | str = 4, page_size: int = 50) -> list[dict[str, Any]]:
        response = self.get(
            f"infostore/{object_id}/children",
            params={
                "page": 1,
                "pageSize": page_size,
            },
        )
        return self._parse_xml_seguro(response.text)
