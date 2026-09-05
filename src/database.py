import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "gymtrack.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize_database():
    connection = get_connection()
    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS routine (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS exercise (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS routine_exercise (
                    routine_id INTEGER NOT NULL,
                    exercise_id INTEGER NOT NULL,
                    PRIMARY KEY (routine_id, exercise_id),
                    FOREIGN KEY (routine_id) REFERENCES routine(id) ON DELETE CASCADE,
                    FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS workout_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    routine_id INTEGER NOT NULL,
                    exercise_id INTEGER NOT NULL,
                    sets INTEGER NOT NULL CHECK (sets > 0),
                    reps INTEGER NOT NULL CHECK (reps > 0),
                    weight INTEGER NOT NULL CHECK (weight >= 0),
                    date TEXT NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (routine_id) REFERENCES routine(id) ON DELETE RESTRICT,
                    FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON DELETE RESTRICT
                )
                """
            )
    finally:
        connection.close()

    return DB_PATH
