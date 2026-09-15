import json
from pathlib import Path

from .utils import PlayerState
from .errors import ScorerFileError


class Scorer:
    def __init__(self, highscore_filename: str) -> None:
        self.file: str = highscore_filename
        self.highscore: dict[str, int] = self._load()

    def _load(self) -> dict[str, int]:
        try:
            if not Path(self.file).exists():
                return {}
            with open(self.file, encoding="utf-8") as f:
                return dict(json.loads(f.read()))  # not sure about that cast
        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")
        except json.JSONDecodeError as e:
            raise ScorerFileError(
                f"Error occurs while reading {self.file}."
                f"(line {e.lineno})."
            )

    def save(self, player_state: PlayerState) -> None:
        self.highscore[player_state.name] = player_state.score

        self.highscore = dict(sorted(
            self.highscore.items(), key=lambda x: [1], reverse=True)[:10])

        try:
            with open(self.file, 'w') as f:
                f.write(json.dumps(self.highscore, indent=4))
        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")
