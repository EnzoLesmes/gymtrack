import sqlite3

from database import get_connection


def _validate_name(name: str) -> str:
	if not isinstance(name, str):
		raise ValueError("Name must be text")

	normalized_name = name.strip()
	if not normalized_name:
		raise ValueError("Name cannot be empty")

	return normalized_name


def _validate_routine_id(routine_id: int) -> None:
	if not isinstance(routine_id, int) or isinstance(routine_id, bool) or routine_id <= 0:
		raise ValueError("Routine ID must be a positive integer")


def create_routine(name: str) -> int:
	normalized_name = _validate_name(name)
	connection = get_connection()

	try:
		with connection:
			cursor = connection.execute(
				"INSERT INTO routine (name) VALUES (?)",
				(normalized_name,),
			)
			return cursor.lastrowid
	finally:
		connection.close()


def _get_or_create_exercise(connection: sqlite3.Connection, name: str) -> int:
	normalized_name = _validate_name(name)
	exercise = connection.execute(
		"""
		SELECT id
		FROM exercise
		WHERE TRIM(name) COLLATE NOCASE = ?
		LIMIT 1
		""",
		(normalized_name,),
	).fetchone()

	if exercise is not None:
		return exercise["id"]

	cursor = connection.execute(
		"INSERT INTO exercise (name) VALUES (?)",
		(normalized_name,),
	)
	return cursor.lastrowid


def get_or_create_exercise(name: str) -> int:
	connection = get_connection()

	try:
		with connection:
			return _get_or_create_exercise(connection, name)
	finally:
		connection.close()


def add_exercise_to_routine(routine_id: int, exercise_name: str) -> int:
	_validate_routine_id(routine_id)
	normalized_name = _validate_name(exercise_name)
	connection = get_connection()

	try:
		with connection:
			routine = connection.execute(
				"SELECT id FROM routine WHERE id = ?",
				(routine_id,),
			).fetchone()
			if routine is None:
				raise LookupError(f"Routine with ID {routine_id} does not exist")

			exercise_id = _get_or_create_exercise(connection, normalized_name)
			connection.execute(
				"""
				INSERT OR IGNORE INTO routine_exercise (routine_id, exercise_id)
				VALUES (?, ?)
				""",
				(routine_id, exercise_id),
			)
			return exercise_id
	finally:
		connection.close()
