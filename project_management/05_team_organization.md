# 05 – Team organization

| Member | Main areas (from commits) |
|---|---|
| Felix Lauwerie (flixlow / flauweri) | Config and parsing, maze generator, entities, ghost AI, crazy mode, timer, cheats, Screen refactor, lint and typing, docstrings, packaging |
| Pablo Dauga | Drawer and rescaling, assets and sprites, animations, menu, buttons, leaderboard, name screen, theme system, README, project management |

**[verify]** Other names in the log (`scoobydoobydoo`, `flixlow`, `Pablo`) are probably alternate git identities of the same two people. The branch `lgirard` / "spawn bug with lgirard" suggests a third contributor or tester: name them here if relevant.

## Workflow
- Personal branches (`felix`, `flauweri`, `pdauga`, `pablo`, `lgirard`) merged into `main` through PRs (#1 → #47).
- Topic branches: `feature/crazy_mode`, `feat/health_system`, `fix/respawn_period`, `doc/docstrings`.
- Cross-review: UI changes checked by Pablo, engine changes by Felix.
- Commit prefixes: `fix:`, `add:`, `refactor:`, `norm:`, `style:`.

## Decision making **[verify]**
Decisions discussed orally or by chat, then recorded in commit and PR messages. Disagreements settled by who owns the module.

## Issue handling
Bugs reported by whoever found them, fixed on a `fix/` branch, merged by PR.