class PacmanError(Exception):
    pass


class ParsingError(PacmanError):
    pass


class GenerationError(PacmanError):
    pass


class ScorerFileError(PacmanError):
    pass
