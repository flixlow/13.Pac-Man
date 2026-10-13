*This project has been created as part of the 42 curriculum by pdauga, flauweri.*

# Pac-Man

## Description

This repository contains a Pac-Man-style game implemented in Python with `pygame`, built around a generated maze, entity movement, score tracking, themes, and a persistent highscore file.

The project is built around a few core data structures and systems:

- `Config` in parsing.py validates the runtime configuration file and generates all mazes.
- `GameEngine` in game.py owns the lifecycle of the game, score, lives, level progression, and game-state transitions.
- `Level` in level.py creates the maze, player, ghosts, pacgums, and simulation state.
- `Maze` in maze.py stores the generated maze data and corner positions used for ghost spawn points and super-pellets.
- `MazeDrawer` and `PacManDrawer` render the maze, entities, and movement animation.
- `AssetLoader` loads the game resources from assets.
- `ThemeSelection` loads themed configuration and assets.
- `Scorer` manages the score and leaderboard persistence.

The project also includes a Makefile for installation, running, debugging, linting, and cleanup, and a local wheel dependency for `mazegenerator` declared in pyproject.toml.

## Installation and execution

The repository expects Python 3.13 and uses `uv` for dependency management and execution. The exact project metadata is declared in pyproject.toml:

- package name: `pac-man`
- version: `0.1.0`
- Python requirement: `>=3.13,<3.14`
- dependencies:
  - `mazegenerator`
  - `pydantic>=2.13.5`
  - `pygame>=2.6.1`
  - `flake8`
  - `mypy`

The wheel is referenced locally in pyproject.toml:

```toml
[tool.uv.sources]
mazegenerator = { path = "mazegenerator-2.1.0-py3-none-any.whl" }
```

Installation and execution are defined in Makefile:

```make
install: Makefile mazegenerator-2.1.0-py3-none-any.whl
        uv sync
        @echo "\033[0;32m\n[OK] installation completed ✔\n\033[0m"

run:
        @PYGAME_HIDE_SUPPORT_PROMPT=1 uv run -m src config.jsonc

debug:
        uv run -m pdb -m src config.jsonc
```

Use:

```bash
make install
make run
```

or launch directly with:

```bash
uv run -m src config.jsonc
```

The project also supports:

```bash
make debug
make lint
make lint-strict
make clean
```

## Linux package

Build a self-contained Linux archive from the repository root with
`bash package-linux.sh`. The script synchronizes the locked development
environment, builds the PyInstaller bundle from `Pac-Man.spec`, and writes
`dist/Pac-Man-linux-<architecture>.tar.gz`. Extract the archive and launch
`Pac-Man/Pac-Man`.

## Configuration

The runtime configuration is loaded from config.jsonc by `parsing()` in parsing.py. The parser strips comment lines beginning with `#` before `json.loads()`, validates the structure using Pydantic models, and raises `ParsingError` on malformed input.

The default configuration file present in the repository is:

```json
{
  "highscore_filename": "highscores.json",
  "levels": [
    { "width": 10, "height": 10 },
    { "width": 11, "height": 11 },
    { "width": 12, "height": 12 },
    { "width": 13, "height": 13 },
    { "width": 14, "height": 14 },
    { "width": 15, "height": 15 }
  ],
  "lives": 3,
  "points": {
    "per_pacgum": 10,
    "per_super_pacgum": 50,
    "per_ghost": 200
  },
  "seed": 42,
  "level_max_time": 90000
}
```

This is enforced by the `Config` model in parsing.py:

- `highscore_filename: str`
- `levels: list[LevelSize]`
- `lives: int` with `gt=0`
- `points: Points`
- `seed: int`
- `level_max_time: int` with `gt=0`

`LevelSize` also validates `width` and `height` with `gt=6`, so generated maze sizes are always greater than 6 in either axis. The default values in the shipped config.jsonc are therefore:

- `lives = 3`
- `seed = 42`
- `level_max_time = 90000`
- points:
  - pacgum: `10`
  - super pacgum: `50`
  - ghost: `200`
- level sizes: `10x10`, `11x11`, `12x12`, `13x13`, `14x14`, `15x15`

## Highscore system

The configuration defines `highscore_filename: "highscores.json"`, which means the leaderboard is stored in the project root as `highscores.json`, unless the config is changed. This is managed by the `Scorer` component and is used to store persistent rank information across game sessions.

The project includes a `Scorer` implementation in scorer.py with the purpose of recording score progression and leaderboard entries. The key design idea is that the game does not only keep a transient score in memory; it persists the leaderboard to a JSON file so the ranking is available across runs.

The repository also includes a todo file noting a highscore-related requirement:

- `"highscore can take only alphanumeric"`
- `"leaderboard qui se rescale pour afficher plus de noms"`
- `"10 max pour le leaderboard"`
- `"clear leaderboard"`

This indicates that the score system is intentionally constrained to alphanumeric names and capped leaderboard length, and the saved data is expected to be human-readable JSON. The project also has logic to handle missing highscore files gracefully, as the todo file mentions a fix for the case where the highscore file is missing.

## Maze generation

The maze system is implemented in parsing.py and relies on the external library `mazegenerator`, imported as:

```python
from mazegenerator import MazeGenerator
```

The `Config.generate_all_maze()` method loops through every configured level and does the following:

```python
g = MazeGenerator(size=(lvl.width, lvl.height), seed=seed)
maze = Maze(
    maze_map=g.maze,
    seed=seed,
    w=lvl.width,
    h=lvl.height,
    corners=self._get_corners(lvl.width - 1, lvl.height - 1)
)
```

This means:

- each level is generated with a size based on config.jsonc
- a deterministic seed is used for the generation
- a new `Maze` object is created for each level
- the generator uses a hashed seed progression for subsequent levels:
  - `seed = self.seed`
  - then `seed = self._get_new_seed(seed)` after each level

The `Config._get_new_seed()` method computes a new seed using `hashlib.sha256`:

```python
digest = sha256(str(seed).encode()).digest()
return int.from_bytes(digest, byteorder="big")
```

This ensures that the maze generation is reproducible and each subsequent level gets a derived random seed.

The `Maze` class wraps the raw maze map and stores metadata such as the map dimensions, the generated grid, and the corner positions used to place special entities and super-pellets.

## Implementation details

### Startup and runtime

__main__.py validates the command line arguments and invokes the monitor:

```python
def main() -> None:
    if len(argv) != 2:
        raise ParsingError(
            "It must take exactly one argument: a configuration file."
        )
    try:
        Monitor(argv[1]).main_loop()
    except FileNotFoundError:
        print("Theme not found !")
```

It also catches known runtime issues:

```python
except (PacmanError, ValidationError, KeyboardInterrupt) as e:
    print(f"[ERROR]: {e}")
```

### `GameEngine`

`GameEngine` in game.py is the top-level coordinator of the game loop. It:

- stores the active configuration and list of generated mazes
- manages score (`self.score`)
- manages lives (`self.lives`)
- transitions between game states (`START_NEW_GAME`, `IN_GAME`, `HAS_COMPLETED_LEVEL`, `HAS_LOSE_A_LIFE`, `GAME_OVER`, etc.)
- advances to the next level
- applies cheat mode toggles
- checks win/loss conditions

Important logic includes:

- `next_level()` loads the next `Level` instance
- `bank_score()` uses the score table from `config.points` and accumulates delivery values
- `update_game_state()` checks timer expiry, completion, entity death, and game-over conditions
- `running()` updates the active level when the state is `IN_GAME`

### `Level`

`Level` in level.py constructs a playable scene for a single maze. It initializes:

- the maze object
- the timer
- `eaten` counters for scoreable items
- completion and cheat flags
- player and ghosts
- pacgum and super-pacgum positions

The method `_init_pacgums()` scans the grid and marks all traversable tiles; super-pellets are placed on the maze corners:

```python
if (x, y) in self.maze.corners:
    self.super_pacgums.add((x, y))
self.pacgums.add((x, y))
```

`_init_ghosts()` shuffles ghost classes and randomly chooses whether one of them is the secret ghost. The ghost instances are created from classes such as `Blue`, `Red`, `Pink`, `Orange`, and `Secret`, using coordinates from `self.maze.corners`.

### `Maze`

`Maze` in maze.py stores the generated map as a grid and the structural metadata needed for gameplay. It is also responsible for the corners used in the level layout and for ghost spawning or special-object placement. The project passes `corners=self._get_corners(lvl.width - 1, lvl.height - 1)` when generating each maze.

### Drawing

The rendering pipeline is split into specific drawer classes:

- `PacManDrawer` in pacman_drawer.py is responsible for drawing Pac-Man and animation states.
- `MazeDrawer` in maze_drawer.py draws the maze itself, including the walls and collectible points.
- `AssetLoader` in assetloader.py loads sprite resources from assets.
- `ThemeSelection` in theme_selection.py selects and validates a theme file, as well as related visual configuration.

The game clearly supports thematic styling by JSON-based theme definitions and multiple assets directories such as:

- button
- default_themes
- font
- fruit
- ghosts
- icon
- pacman

The theme files include:

- black_and_white.json
- blue_ocean.json
- green_jungle.json
- red_blaze.json
- yellow_thunder.json

Additionally, the project contains:

- neon_arcade.json
- place_your_theme_here.txt

## Architecture

The project is organized as follows:

- src: engine, rendering, assets, parsing, menus, score, and game state logic.
  - __main__.py: entry point
  - parsing.py: config parsing and maze generation
  - engine: game, level, and maze logic
  - drawing: rendering layer for maze and player
  - assetloader.py: resource loading
  - scorer.py: leaderboard and score management
  - theme_selection.py: theme selection and validation
  - menu.py, screens.py, monitor.py, button.py: UI and game flow
- assets: artist and game resources: pacman sprites, ghosts, fruit, icons, fonts, buttons, and default themes
- themes: user theme definitions and sample theme files
- config.jsonc: runtime configuration
- Makefile: developer automation
- pyproject.toml: dependency and project metadata
- todo: project task log and historical implementation notes

In practice, the architecture is a typical game loop structure:

1. `__main__` reads config and starts `Monitor`.
2. `Monitor` runs the main loop.
3. `Config` parses and validates the JSON.
4. `MazeGenerator` produces the maze layout.
5. `GameEngine` manages the game progression.
6. `Level` creates entities and collectibles.
7. `PacManDrawer` and `MazeDrawer` render the game.
8. `Scorer` persists the leaderboard and score data.

## Usage examples and useful commands

Common commands from the project:

```bash
make install
make run
make debug
make lint
make lint-strict
make clean
```

Direct execution:

```bash
uv run -m src config.jsonc
```

or, if the user wants to run the entry point directly with standard Python:

```bash
python -m src config.jsonc
```

The repository already ships the config file:

```bash
python -m src config.jsonc
```

This is consistent with the Makefile target:

```make
run:
        @PYGAME_HIDE_SUPPORT_PROMPT=1 uv run -m src config.jsonc
```

## Project management

The todo file is effectively a historical implementation log. It includes milestones like:

- movement and inertia handling
- main menu
- lives and pacgum/super-pacgum support
- ghost movement and pathfinding
- score display and timer
- highscore and leaderboard work
- asset loading
- theme handling
- bug fixes for level changes, game-over edge cases, and missing highscore file
- integration of external references such as Chebyshev and taxicab geometry

It also includes a list of remaining or deferred tasks such as:

- `Readme`
- `docstring`
- `config par default si jamais la config est eronée`
- `implementer une statemachine`
- `Mieux gerer les collisions`

This means the project is not purely a final artifact; it was developed iteratively and the todo file documents the implementation history and remaining improvements.

## Resources

The project includes references that are useful for the game logic and movement model. In the todo file, the following external links appear:

- `https://en.wikipedia.org/wiki/Chebyshev_distance`
- `https://en.wikipedia.org/wiki/Taxicab_geometry`

These are relevant to ghost movement and path evaluation because the game uses tile-based movement and entity navigation across a maze grid.

The project also includes a note in todo about `Forbidden Behavior from pygame`, including rules such as:

- no `pygame.time.Clock.tick(60)` as a gameplay restriction
- no scaling/rotation of images
- no direct custom font manipulation
- no custom draw rectangle exceptions

This means the project is intentionally constrained in how it renders and updates artifacts.

As for AI usage: there is no built-in AI module in the game itself. The repository’s planning notes imply that AI or coding assistants should be used as a supplemental development tool, for example to help with refactoring, boilerplate, or understanding movement/geometry, but not as a substitute for project rules or gameplay logic. The project does not ship any in-game AI system beyond the game logic defined in the engine and entities.

## Notes and inferred details

Some information is inferred from code, not explicitly stated in a dedicated documentation file:

- the startup loop runs through `Monitor` and starts the game from the config file (__main__.py)
- `Config` performs JSON validation and strict checks on level sizes and score values (parsing.py)
- the game stores leaderboard data under `highscores.json` because config.jsonc sets that value and the `Scorer` subsystem is the logical persistence point for this file
- the structure of files and directories (assets, themes, src) comes directly from the repository state

This README has been written to match only the behaviors and defaults visible in the repository itself, without adding assumptions beyond the code and project metadata.

## Summary

This project is a complete Pac-Man-inspired game built with Python and `pygame`, configured via a JSON file, generated with `mazegenerator`, rendered with dedicated drawing modules, and designed around a persistent leaderboard and theme-based visual assets. It is a strong example of a small but complete game project with a clear separation between:

- configuration
- maze generation
- game logic
- rendering
- assets
- scoring
- helper tooling

It is ready to run with the provided Makefile and config, and it follows a clean project layout suitable for teaching, extension, and further feature work.