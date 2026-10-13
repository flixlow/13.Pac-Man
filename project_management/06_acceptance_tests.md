# 06 – Acceptance test plan

| ID | Feature | Test | Expected | Result |
|---|---|---|---|---|
| T1 | Config | Missing or invalid `config.json` | Default config loads | Pass |
| T2 | Maze | Generate several levels | Valid, connected maze | Pass |
| T3 | Movement | Arrows against walls, rapid turns | No wall crossing, queued turns work | Pass (after fixes) |
| T4 | Ghosts | Observe each colour | Red chases, Blue random, Secret teleports | Pass |
| T5 | Collisions | Player vs ghost | Life lost, clean respawn | Pass |
| T6 | Crazy mode | Eat a super pacgum | Ghosts flee, edible, respawn on timer, score added | Pass |
| T7 | Score and lives | Play several games | Score resets between games | Pass |
| T8 | Levels | Clear all levels | Next level loads, end screen shown | Pass |
| T9 | Timer | 90 s level limit | Game over at timeout | Pass |
| T10 | Leaderboard | Finish games, clear it | Max 10, sorted, no empty names | Pass |
| T11 | Menu and name screen | Escape, Enter, pause | No crash, correct return to menu | Pass |
| T12 | Themes | Press T, add custom JSON | Theme switches, resets on new game | Pass |
| T13 | Cheats | F1 to F4, godmode, noclip | Visible indicators, F4 skips level | Pass |
| T14 | Corrupt save | Broken `highscores.json` | No crash | Pass |
| T15 | Lint | `make lint-strict` | Clean except one `type: ignore` | Pass |

**[verify]** Results are inferred from the fix history. Re-run each test and update the column.

## Bugs found and fixed (selected)

| Date | Bug | Fix commit |
|---|---|---|
| 09-09 | Player movement and wall errors | `dda612f`, `b715ff0` |
| 09-15 | Hitbox with ghosts | `3f040e1` |
| 09-16 | Direction priority in `can_it_move` | `c32637a` |
| 09-20 | Pathfinding errors (`is` vs `!=`) | `64c09ce` |
| 09-22 | 42-logo secret teleport; passing through ghosts | `2053bf6`, `9f794c3` |
| 09-30 | Very high scores; empty name saved | `4f5328a`, `2e6d2f4` |
| 10-08 | New game loads last map; GameState duplicates | `cad8c26`, `92462f6` |
| 10-09 | Respawn teleport; crazy mode persisting; theme change during name entry | `4156d0a`, `af0b4dd` |
| 10-12 | Last-level bug; scorer load errors | `d68b244`, `a9dc966` |
| 10-13 | Menu pause on restart prompt; destroyable reflect; spawn bug | `7de2961`, `105f0b9`, `c4c24ad` |