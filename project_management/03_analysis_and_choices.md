# 03 – Project analysis and choices

| Decision | Choice | Rationale / evidence |
|---|---|---|
| Tooling | `uv`, Makefile (`run`, `lint`, `lint-strict`, `clean`) | First commits; reproducible setup |
| Language and quality | Python, pygame, flake8, mypy strict typing | Norm enforced (`0527acf`) |
| Config | `config.json` parsed into a BaseModel, comments stripped, `default_config` fallback | Fail-safe (`c37a08a`) |
| Maze | Generator yielding `list[list[int]]`, binary wall encoding per cell | `32edcac`, `b715ff0` |
| Architecture | `engine/` (entities, level, maze), `utils/`, drawer and screens; polymorphism (`can_it_move`, `level.update`) | Refactors on 09-12, 09-20, 09-23 |
| Ghost AI | One subclass per colour: Red pathfinding, Blue random, Secret teleport and random spawn | Commits 09-13 → 09-22 |
| Movement | Velocity + `next_direction` queue | Fixed input latency (`bbe1e09`) |
| Time | Dedicated `Timer` class, then its own file | `dd0508b`, `e30b71c` |
| Themes | User-editable JSON in `assets/theme/` | `859933a`; extensible without code changes |
| UI flow | `Screen` class handling input and display, with callbacks | Replaced `check_user_events` (`bfef858`) |
| Persistence | `highscores.json`, max 10 entries, not versioned | `87c9b32` |
| AI assistance | Used and labelled in commits ("ai refactor", "ai_fix") | Transparency **[verify school policy]** |