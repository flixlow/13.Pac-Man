
from pathlib import Path
from json import load, JSONDecodeError, dumps

from .utils import PlayerState
from .errors import ScorerFileError


class Scorer:
    def __init__(self, score_filename: str) -> None:
        self.file: str = score_filename
        self.scores: dict[str, int] = self._load()

    @staticmethod
    def _sort(scores: dict[str, int]) -> dict[str, int]:
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    def _load(self) -> dict[str, int]:
        try:
            if not Path(self.file).exists():
                return {}
            with open(self.file, encoding="utf-8") as f:
                return self._sort(load(f))
        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")
        except JSONDecodeError as e:
            raise ScorerFileError(
                f"Error occurs while reading {self.file}."
                f"(line {e.lineno})."
            )

    def save(self, player_state: PlayerState) -> None:
        last = self.scores.get(player_state.name, -1)

        self.scores[player_state.name] = max(player_state.score, last)

        try:
            with open(self.file, 'w') as f:
                f.write(dumps(self.scores, indent=4))
        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")

        self.scores = self._sort(self.scores)
