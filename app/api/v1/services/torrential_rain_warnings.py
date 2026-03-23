import json
from app.api.v1.utils.constant_paths import torrential_rain_warnings_json_file
from app.api.v1.models.torrential_rain_warnings import (
    TorrentialRainWarnings,
    TorrentialRainWarningsSection,
)


class TorrentialRainWarningsService:
    def __init__(self, lang: str) -> None:
        self.lang = lang

    def load(self) -> TorrentialRainWarnings:
        default_lang_file = next(iter(torrential_rain_warnings_json_file.values()))

        with open(
            torrential_rain_warnings_json_file.get(self.lang, default_lang_file)
        ) as f:
            data = json.load(f)

        sections = [
            TorrentialRainWarningsSection(
                id=section["id"],
                title=section["title"],
                content=section.get("content"),
                stakeholders=section.get("stakeholders"),
            )
            for section in data["sections"]
        ]

        return TorrentialRainWarnings(
            id=data["id"],
            title=data["title"],
            sections=sections,
        )
