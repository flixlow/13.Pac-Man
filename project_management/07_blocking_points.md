# 07 – Blocking points and conflicts

| Issue | Impact | Resolution |
|---|---|---|
| Parallel work on Drawer and engine caused merge conflicts | Time lost on 09-14 and 09-25 | More frequent merges, clearer module boundaries |
| Latency and input bugs | Delayed gameplay polish | Velocity, direction queue, AI-assisted fix |
| Pathfinding needed the player position inside the ghost's sequence generator | Blocked on 09-20 | Ghosts now hold a `self.player` reference |
| Theme loader did not catch exceptions | Crash risk | JSONDecodeError and OSError handled, extended later |
| Timer "doesn't work for the moment" | Delayed timer feature | Rewritten as `GeneralTimer` |
| `highscores.json` committed by mistake | Repo noise | Removed from repo **[verify .gitignore]** |
| No activity 10-01 → 10-04 | Slower sprint 4 | **[verify cause]** |
| Last-minute README image error and bugs | Delivery risk | Fixed on 10-13 |

## Lessons learned
- Merge `main` daily.
- Define interfaces before splitting UI and engine work.
- Start docs and lint earlier.
- Keep a written plan so planned vs actual can be proven.