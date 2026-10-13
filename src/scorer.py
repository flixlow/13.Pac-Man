"""Leaderboard persistence logic.

This module stores and loads leaderboard entries as JSON.
"""

from json import JSONDecodeError, load, dump

from .errors import ScorerFileError


class Scorer:
    """Load, sort and persist a leaderboard stored in a JSON file.

    Args:
        score_filename: Path to the leaderboard file.
    """

    def __init__(self, score_filename: str) -> None:
        """Initialize the scorer and load the current high scores.

        Args:
            score_filename: Path to the JSON leaderboard file.
        """
        self.file: str = score_filename
        self.scores: dict[str, int] = {}
        try:
            self._load()
        except (Exception) as e:
            print(f"[WARNING]: can't load from highscore file: {e}")
        else:
            if (
                not isinstance(self.scores, dict)
                or not all(
                    isinstance(k, str) and isinstance(v, int)
                    for k, v in self.scores.items())
            ):
                print("[WARNING] ValueError in the highscore file")
                self.scores = dict()
        self._sort()

    def _sort(self) -> None:
        """Sort the scores by descending value."""
        self.scores = dict(
            sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        )

    def _load(self) -> None:
        """Read the leaderboard file from disk.

        Returns:
            Loaded score dictionary.

        Raises:
            ScorerFileError: If the file does not exist, cannot be read or
                contains invalid JSON.
        """
        try:
            with open(self.file, encoding="utf-8") as f:
                self.scores = load(f)
                return

        except OSError as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")
        except JSONDecodeError as e:
            raise ScorerFileError(
                f"Error occurs while reading {self.file}."
                f"(line {e.lineno})."
            )
        self.scores = {}

    def save(self, name: str, score: int) -> None:
        """Save a player's result in the leaderboard.

        Args:
            name: Player name entered by the user.
            score: Score reached by the player.
        """
        entered_name = name.strip()

        last = self.scores.get(entered_name, -1)

        self.scores[entered_name] = max(score, last)

        self._sort()

        try:
            with open(self.file, 'w') as f:
                dump(self.scores, f, indent=4)
        except (OSError, UnicodeEncodeError) as e:
            raise ScorerFileError(f"{self.file}: {e.__class__.__name__}")

    def clear(self) -> None:
        """Remove all entries from the leaderboard and file."""
        self.scores = {}
        try:
            with open(self.file, "w") as f:
                dump(self.scores, f, indent=4)
        except (JSONDecodeError, OSError):
            raise ScorerFileError("Can't clear leaderboard.")
