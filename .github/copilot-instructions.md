# Copilot Instructions — GymTrack

This project also has an `AGENTS.md` at the repository root — read it
first for full context (project description, tech stack, structure,
data model, and behavior rules). This file mirrors the key points so
inline suggestions stay consistent with it.

## Quick reference

- **Language/stack**: Python 3, standard library only. SQLite via
  `sqlite3`. Console app (`input()`/`print()`) — no web framework, no
  ORM, no third-party libraries unless explicitly approved.
- **Structure**: `src/main.py` (entry point/menu), `src/database.py`
  (DB connection & tables), `src/rutinas.py` (routine/exercise logic),
  `src/entrenamientos.py` (workout logging/history).
- **Code language**: all code (variables, functions, comments) in
  English. User-facing console text in Spanish.
- **Naming**: `snake_case`, per PEP 8.
- **Do not**: invent unrequested features, add dependencies without
  approval, or implement beyond the current requested step.
- **Always**: validate user input before saving it; handle invalid
  input without crashing.

For anything not covered here, defer to `AGENTS.md` and `SPEC.md`.
