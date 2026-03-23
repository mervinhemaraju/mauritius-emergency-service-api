import json
from app.api.v1.utils.constant_paths import tsunami_warnings_json_file
from app.api.v1.models.tsunami_warnings import (
    TsunamiWarnings,
    TsunamiWarningsSection,
    TsunamiWarningsStage,
)


class TsunamiWarningsService:
    def __init__(self, lang: str) -> None:
        self.lang = lang

    def load(self) -> TsunamiWarnings:
        default_lang_file = next(iter(tsunami_warnings_json_file.values()))

        with open(tsunami_warnings_json_file.get(self.lang, default_lang_file)) as f:
            data = json.load(f)

        sections = [
            TsunamiWarningsSection(
                id=section["id"],
                title=section["title"],
                content=section.get("content"),
                stages=[
                    TsunamiWarningsStage(
                        id=stage["id"],
                        level=stage["level"],
                        title=stage["title"],
                        content=stage.get("content"),
                        instructions=stage.get("instructions"),
                    )
                    for stage in section.get("stages", [])
                ]
                or None,
            )
            for section in data["sections"]
        ]

        return TsunamiWarnings(
            id=data["id"],
            title=data["title"],
            sections=sections,
        )
