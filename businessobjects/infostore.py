from __future__ import annotations

import xml.etree.ElementTree as ET

from businessobjects.client import BOClient
from businessobjects.models import BOObject


class InfoStore:
    def __init__(self, client: BOClient) -> None:
        self.client = client

    def listar_filhos(
        self,
        object_id: int | str,
        page: int = 1,
        page_size: int = 50,
    ) -> list[BOObject]:
        response = self.client.get(
            f"infostore/{object_id}/children",
            params={
                "page": page,
                "pageSize": page_size,
            },
        )
        return self._parse_objects(response.text)

    def listar_todos_filhos(
        self,
        object_id: int | str,
        page_size: int = 50,
        max_pages: int = 20,
    ) -> list[BOObject]:
        objetos: list[BOObject] = []

        for page in range(1, max_pages + 1):
            pagina = self.listar_filhos(object_id, page=page, page_size=page_size)

            if not pagina:
                break

            objetos.extend(pagina)

            if len(pagina) < page_size:
                break

        return objetos

    def buscar_filho_por_nome(
        self,
        parent_id: int | str,
        nome: str,
        exact: bool = True,
    ) -> BOObject | None:
        objetos = self.listar_todos_filhos(parent_id)

        for obj in objetos:
            if exact and obj.name == nome:
                return obj

            if not exact and nome.lower() in obj.name.lower():
                return obj

        return None

    def buscar_caminho(
        self,
        root_id: int | str,
        caminho: str,
    ) -> BOObject | None:
        atual_id = root_id
        atual_obj: BOObject | None = None

        partes = [parte for parte in caminho.split("/") if parte]

        for parte in partes:
            atual_obj = self.buscar_filho_por_nome(atual_id, parte)

            if atual_obj is None:
                return None

            atual_id = atual_obj.id

        return atual_obj

    def listar_webi(self, folder_id: int | str) -> list[BOObject]:
        return [
            obj
            for obj in self.listar_todos_filhos(folder_id)
            if obj.is_webi
        ]

    def imprimir_arvore(
        self,
        root_id: int | str,
        depth: int = 2,
        indent: int = 0,
    ) -> None:
        if depth < 0:
            return

        for obj in self.listar_todos_filhos(root_id):
            print("  " * indent + f"{obj.id} {obj.name} ({obj.type})")

            if obj.is_folder:
                self.imprimir_arvore(obj.id, depth=depth - 1, indent=indent + 1)

    def _parse_objects(self, xml_text: str) -> list[BOObject]:
        root = ET.fromstring(xml_text)

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "bip": "http://www.sap.com/rws/bip",
        }

        objetos: list[BOObject] = []

        for entry in root.findall("atom:entry", ns):
            attrs: dict[str, str | None] = {}

            for attr in entry.findall(".//bip:attr", ns):
                name = attr.attrib.get("name")
                if name:
                    attrs[name] = attr.text

            if "id" not in attrs or "name" not in attrs or "type" not in attrs:
                continue

            objetos.append(
                BOObject(
                    id=int(attrs["id"]),
                    name=attrs["name"] or "",
                    type=attrs["type"] or "",
                    cuid=attrs.get("cuid"),
                    description=attrs.get("description"),
                )
            )

        return objetos

    def buscar_recursivo(
        self,
        root_id: int | str,
        nome: str,
        exact: bool = True,
        max_depth: int = 5,
    ) -> list[BOObject]:
        encontrados: list[BOObject] = []

        def visitar(folder_id: int | str, depth: int) -> None:
            if depth > max_depth:
                return

            for obj in self.listar_todos_filhos(folder_id):
                match = obj.name == nome if exact else nome.lower() in obj.name.lower()

                if match:
                    encontrados.append(obj)

                if obj.is_folder:
                    visitar(obj.id, depth + 1)

        visitar(root_id, 0)
        return encontrados
