# 01 – Timeline

```mermaid
gantt
    title 13.Pac-Man - Actual timeline
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    section Setup
    Repo, uv, Makefile, lint rules      :done, s1, 2026-09-07, 2d
    Config parsing and scorer           :done, s2, 2026-09-07, 2d
    Maze generator                      :done, s3, 2026-09-08, 2d
    section Core engine
    Player movement, walls, velocity    :done, c1, 2026-09-09, 4d
    Ghost classes, pacgums              :done, c2, 2026-09-08, 6d
    Lives, hitbox, score, next level    :done, c3, 2026-09-14, 3d
    Ghost AI (random, pathfinding, secret) :done, c4, 2026-09-13, 9d
    Crazy mode (super pacgum)           :done, c5, 2026-09-22, 2d
    section UI and assets
    Drawer, rescale, assets             :done, u1, 2026-09-08, 3d
    Header, menu, leaderboard, buttons  :done, u2, 2026-09-14, 9d
    Animations and sprites              :done, u3, 2026-09-22, 5d
    Name entry screen                   :done, u4, 2026-09-25, 1d
    Theme system (JSON)                 :done, u5, 2026-09-24, 22d
    section Extras
    Timer / GeneralTimer                :done, e1, 2026-09-23, 8d
    Cheat modes (F1-F4, godmode, noclip):done, e2, 2026-10-08, 5d
    Screen refactor, custom levels      :done, e3, 2026-10-11, 3d
    section Quality and delivery
    Lint, typing, flake8, mypy          :done, q1, 2026-09-14, 25d
    Docstrings                          :done, q2, 2026-10-11, 2d
    README, packaging, bug fixes        :done, q3, 2026-10-12, 2d
```

## Milestones

| Date | Milestone |
|---|---|
| 09-09 | First playable: maze drawn, player moves |
| 09-16 | Score, lives, leaderboard, direction queue |
| 09-23 | Crazy mode, all ghost types, animations |
| 09-25 | Integration of both workstreams (`make run`) |
| 09-30 | JSON theme system |
| 10-09 | Cheat modes, lint clean |
| 10-12 | Docstrings, robustness (config fallback, scorer errors) |
| 10-13 | Packaging, README, final bug fixes |