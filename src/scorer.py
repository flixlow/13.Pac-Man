
from pathlib import Path
import json

from .utils import PlayerState
from .errors import ScorerFileError


class Scorer:
    def __init__(self, score_filename: str) -> None:
        self.file: str = score_filename
        self.scores: dict[str, int] = self._load()

    def sort(self) -> None:
        self.scores = dict(
            sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        )

    def _load(self) -> dict[str, int]:
        try:
            if not Path(self.file).exists():
                self.scores = {}
            with open(self.file, encoding="utf-8") as f:
                return json.load(f)

        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")
        except json.JSONDecodeError as e:
            raise ScorerFileError(
                f"Error occurs while reading {self.file}."
                f"(line {e.lineno})."
            )

    def save(self, player_state: PlayerState, score: int) -> None:
        entered_name = player_state.name.strip()
        last = self.scores.get(player_state.name, -1)

        self.scores[entered_name] = max(score, last)

        self.sort()

        try:
            with open(self.file, 'w') as f:
                json.dump(self.scores, f, indent=4)
        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")

    def clear(self) -> bool:
        try:
            with open(self.file, "w") as f:
                json.dump({}, f, indent=4)
        except (json.JSONDecodeError, OSError):
            print("Warning: json clear is not possible")
            return False
        else:
            return True
