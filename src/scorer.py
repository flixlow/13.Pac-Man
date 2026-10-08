
from typing import Any
from pathlib import Path
from json import JSONDecodeError, load, dump

from .errors import ScorerFileError


class Scorer:
    def __init__(self, score_filename: str) -> None:
        self.file: str = score_filename
        self.scores: dict[str, int] = self._load()

    def sort(self) -> None:
        self.scores = dict(
            sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        )

    def _load(self) -> Any:
        try:
            if not Path(self.file).exists():
                self.scores = {}
            with open(self.file, encoding="utf-8") as f:
                return load(f)

        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")
        except JSONDecodeError as e:
            raise ScorerFileError(
                f"Error occurs while reading {self.file}."
                f"(line {e.lineno})."
            )

    def save(self, name: str, score: int) -> None:
        entered_name = name.strip()

        last = self.scores.get(entered_name, -1)

        self.scores[entered_name] = max(score, last)

        self.sort()

        try:
            with open(self.file, 'w') as f:
                dump(self.scores, f, indent=4)
        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")

    def clear(self) -> None:
        self.scores = {}
        try:
            with open(self.file, "w") as f:
                dump(self.scores, f, indent=4)
        except (JSONDecodeError, OSError):
            raise ScorerFileError("Can't clear leaderboard.")
