import re
import sqlite3
from datetime import date as date_type

from database import get_connection


def _validate_integer(value: int, field_name: str, minimum: int) -> None:
	if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
		raise ValueError(f"{field_name} must be an integer greater than or equal to {minimum}")


def _validate_date(value: str) -> str:
	if not isinstance(value, str):
		raise ValueError("Date must be text in YYYY-MM-DD format")

	normalized_date = value.strip()
	if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", normalized_date):
		raise ValueError("Date must use YYYY-MM-DD format")

	try:
		date_type.fromisoformat(normalized_date)
	except ValueError as error:
		raise ValueError("Date must be a valid calendar date") from error

	return normalized_date


def _validate_notes(notes: str | None) -> str | None:
	if notes is not None and not isinstance(notes, str):
		raise ValueError("Notes must be text or None")
	return notes


def _require_existing_entity(
	connection: sqlite3.Connection,
	table_name: str,
	entity_id: int,
	entity_name: str,
) -> None:
	entity = connection.execute(
		f"SELECT id FROM {table_name} WHERE id = ?",
		(entity_id,),
	).fetchone()
	if entity is None:
		raise LookupError(f"{entity_name} with ID {entity_id} does not exist")


def register_workout(
	routine_id: int,
	exercise_id: int,
	sets: int,
	reps: int,
	weight: int,
	date: str,
	notes: str | None = None,
) -> int:
	_validate_integer(routine_id, "Routine ID", 1)
	_validate_integer(exercise_id, "Exercise ID", 1)
	_validate_integer(sets, "Sets", 1)
	_validate_integer(reps, "Reps", 1)
	_validate_integer(weight, "Weight", 0)
	normalized_date = _validate_date(date)
	validated_notes = _validate_notes(notes)

	connection = get_connection()
	try:
		with connection:
			_require_existing_entity(connection, "routine", routine_id, "Routine")
			_require_existing_entity(connection, "exercise", exercise_id, "Exercise")

			cursor = connection.execute(
				"""
				INSERT INTO workout_log
					(routine_id, exercise_id, sets, reps, weight, date, notes)
				VALUES (?, ?, ?, ?, ?, ?, ?)
				""",
				(
					routine_id,
					exercise_id,
					sets,
					reps,
					weight,
					normalized_date,
					validated_notes,
				),
			)
			return cursor.lastrowid
	finally:
		connection.close()


def get_workout_history() -> list[sqlite3.Row]:
	connection = get_connection()
	try:
		rows = connection.execute(
			"""
			SELECT
				workout_log.id,
				workout_log.routine_id,
				routine.name AS routine_name,
				workout_log.exercise_id,
				exercise.name AS exercise_name,
				workout_log.sets,
				workout_log.reps,
				workout_log.weight,
				workout_log.date,
				workout_log.notes
			FROM workout_log
			JOIN routine ON routine.id = workout_log.routine_id
			JOIN exercise ON exercise.id = workout_log.exercise_id
			ORDER BY workout_log.date DESC, workout_log.id DESC
			"""
		).fetchall()
		return rows
	finally:
		connection.close()
