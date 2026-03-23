import json
from app.api.v1.utils.constant_paths import tsunami_precautions_json_file
from app.api.v1.models.tsunami_precautions import (
    TsunamiPrecautions,
    TsunamiPrecautionsSection,
)


class TsunamiPrecautionsService:
    def __init__(self, lang: str) -> None:
        self.lang = lang

    def load(self) -> TsunamiPrecautions:
        default_lang_file = next(iter(tsunami_precautions_json_file.values()))

        with open(tsunami_precautions_json_file.get(self.lang, default_lang_file)) as f:
            data = json.load(f)

        sections = [
            TsunamiPrecautionsSection(
                id=section["id"],
                title=section["title"],
                content=section.get("content"),
                precautions=section.get("precautions"),
            )
            for section in data["sections"]
        ]

        return TsunamiPrecautions(
            id=data["id"],
            title=data["title"],
            sections=sections,
        )
