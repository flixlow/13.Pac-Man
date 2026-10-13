# 04 – Risk analysis

| # | Risk | Prob. | Impact | Mitigation | Outcome |
|---|---|---|---|---|---|
| R1 | Merge conflicts between two parallel workstreams | High | Med | Feature branches, small PRs, frequent `merge main` | Occurred (`c00d028`), resolved |
| R2 | Display/engine coupling blocks UI work | Med | High | Early refactors (Drawer, monitor, Screen) | Mitigated |
| R3 | Input latency and movement bugs | High | Med | Velocity, direction queue, hitbox rework | Resolved by 09-16 |
| R4 | Pathfinding complexity | Med | Med | Staged: random → pathfinding → secret | Delivered 09-21 |
| R5 | Corrupt or missing config, themes, highscores | Med | High | Fallback config, JSONDecodeError/OSError handling, scorer error catching | Mitigated 10-12 |
| R6 | Norm and lint failures at evaluation | Med | High | `make lint-strict` run regularly | One `type: ignore` left |
| R7 | Scope creep (themes, cheats) | Med | Med | Core features first, extras after 09-23 | Controlled |
| R8 | Late regressions (last level, respawn, crazy mode persisting) | High | Med | Fix commits per bug, manual replays | Found and fixed |
| R9 | Single-person dependency (engine vs UI) | Med | Med | Cross-review of PRs | Partially mitigated |
| R10 | Deadline pressure (commits still on 10-13) | High | Med | Docs and packaging tracked from 10-11 | Tight but met |