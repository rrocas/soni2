import json
from pathlib import Path

class Config:
    def __init__(self, path=None):
        path = Path(path or (Path(__file__).resolve().parent / "../config.json")).resolve()

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        self._data = data

    @property
    def files_path(self):
        return self._data.get("files_path", "./")