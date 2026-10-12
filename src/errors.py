"""Custom exceptions for parsing, generation and scoring errors."""


class PacmanError(Exception):
    """Base exception for all Pac-Man project errors."""


class ParsingError(PacmanError):
    """Raised when parsing a configuration file fails."""


class GenerationError(PacmanError):
    """Raised when a maze or asset generation step fails."""


class ScorerFileError(PacmanError):
    """Raised when the leaderboard file cannot be read or written."""
