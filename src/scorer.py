
from pathlib import Path
import json

from .utils import PlayerState
from .errors import ScorerFileError


class Scorer:
    def __init__(self, score_filename: str) -> None:
        self.file: str = score_filename
        self.scores: dict[str, int] = self.load()

    def sort(self, content: dict[str, int]) -> dict[str, int]:
        return dict(sorted(content.items(), key=lambda x: x[1], reverse=True))

    def load(self) -> dict[str, int]:
        try:
            if not Path(self.file).exists():
                return {}
            with open(self.file, encoding="utf-8") as f:
                content: dict[str, int] = json.load(f)
                return self.sort(content)

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
