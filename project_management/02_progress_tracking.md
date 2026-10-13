# 02 – Progress tracking (planned vs actual)

The "Planned" column is reconstructed **[verify: replace with the original plan if you have it]**.

| Sprint | Planned | Delivered (from git log) | Status |
|---|---|---|---|
| S1 (09-07 → 09-13) | Setup, parsing, maze, movement | All, plus drawer rescale and velocity | On time |
| S2 (09-14 → 09-20) | Lives, menu, leaderboard | Plus start of ghost AI, next_direction queue | On time |
| S3 (09-21 → 09-27) | Ghost AI, crazy mode | Pathfinding, secret ghost, crazy mode, Timer, name screen | Ahead |
| S4 (09-28 → 10-04) | UI polish | Timer, score display, JSON themes | Slowed: no commits 10-01 to 10-04 **[verify reason]** |
| S5 (10-05 → 10-11) | Cheats, refactor | Cheats, godmode, noclip, Screen class | On time |
| S6 (10-12 → 10-13) | Docs, delivery | Docstrings, README, packaging | Done, with last-day bug fixes |

## Velocity
About 40 commits per week on average. Peaks of 60+ commits on 09-09 and 09-21 to 09-23, when assets and gameplay features landed together.

## Scope changes
Extras added beyond the base subject: themes, cheat modes, custom levels (width, height, theme), 90 s level timer.