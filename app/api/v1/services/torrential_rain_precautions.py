import json
from app.api.v1.utils.constant_paths import torrential_rain_precautions_json_file
from app.api.v1.models.torrential_rain_precautions import (
    TorrentialRainPrecautions,
    TorrentialRainPrecautionsSection,
)


class TorrentialRainPrecautionsService:
    def __init__(self, lang: str) -> None:
        self.lang = lang

    def load(self) -> TorrentialRainPrecautions:
        default_lang_file = next(iter(torrential_rain_precautions_json_file.values()))

        with open(
            torrential_rain_precautions_json_file.get(self.lang, default_lang_file)
        ) as f:
            data = json.load(f)

        sections = [
            TorrentialRainPrecautionsSection(
                id=section["id"],
                title=section["title"],
                content=section.get("content"),
                precautions=section.get("precautions"),
            )
            for section in data["sections"]
        ]

        return TorrentialRainPrecautions(
            id=data["id"],
            title=data["title"],
            sections=sections,
        )
