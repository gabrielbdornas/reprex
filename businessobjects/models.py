from dataclasses import dataclass


@dataclass
class BOObject:
    id: int
    name: str
    type: str
    cuid: str | None = None
    description: str | None = None

    @property
    def is_folder(self) -> bool:
        return self.type.endswith("Folder")

    @property
    def is_webi(self) -> bool:
        return self.type == "Webi"
