# AGENTS.md — GymTrack

## Project context

GymTrack is a console application that helps users organize workout
routines and track their training progress over time. It is a learning
project for a full-stack (AI-first) programming course. See `SPEC.md`
for the full product specification.

## Tech stack and constraints

- **Language**: Python 3, standard library only.
- **Persistence**: SQLite via the built-in `sqlite3` module.
- **Interface**: command-line only (`input()` / `print()`). No web
  frontend, no GUI framework.
- **Do NOT** add web frameworks (Flask, FastAPI, Django), ORMs
  (SQLAlchemy), or any third-party library unless explicitly requested.
  `requirements.txt` should stay empty unless a dependency is approved.

## Project structure

```
gymtrack/
├── src/
│   ├── main.py           # entry point, console menu, program loop
│   ├── database.py       # DB connection, table creation, raw queries
│   ├── rutinas.py         # routine & exercise logic
│   └── entrenamientos.py  # workout logging & history logic
├── SPEC.md
├── README.md
├── AGENTS.md
├── .gitignore
└── requirements.txt
```

Each file owns one responsibility. New functions go in the file that
matches their responsibility — don't create new files or folders
without asking first.

## Agent behavior rules

- Do not invent features that were not requested.
- Do not add libraries or dependencies without explicit approval.
- Do not make architectural decisions silently — ask before assuming.
- Keep the code simple and readable; avoid unnecessary abstractions,
  design patterns, or premature optimization.
- Only implement what is asked for the current stage/step. Do not get
  ahead of the requested scope.
- If a request conflicts with this file or with `SPEC.md`, point out
  the conflict instead of silently resolving it.

## Data model (reference)

**Rutina (Routine)**
- name
- list of exercises that make it up

**Ejercicio (Exercise)**
- name

**Registro de entrenamiento (Workout log entry)**
- associated rutina
- ejercicio performed
- sets (series)
- reps (repeticiones)
- weight used (peso)
- date (fecha)
- notes (observaciones)

Note: a *rutina* (the plan) and a *registro de entrenamiento* (what was
actually done on a given day) are different entities — do not merge them.

## Code conventions

- All code — variable names, function names, comments — in **English**.
- User-facing text (console menus, prompts, messages) in **Spanish**,
  since the end user speaks Spanish.
- Naming style: `snake_case` for variables and functions, per standard
  Python convention (PEP 8).
- Every function that takes user input must validate it (e.g. confirm
  a number was entered where a number is expected) before saving.
- Prefer plain functions over classes unless there's a clear reason to
  use a class.

## Definition of done (per stage)

A stage is complete when:
- All functions for that stage work as intended.
- Data entered by the user is saved and retrieved correctly from SQLite.
- The console flow is clear and easy to navigate.
- Code is organized in the correct file per its responsibility.
- Invalid user input (wrong type, empty value, etc.) does not crash
  the app — it shows a clear message and lets the user retry.
