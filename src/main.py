import sqlite3

from database import initialize_database
from entrenamientos import get_workout_history, register_workout
from rutinas import (
	add_exercise_to_routine,
	create_routine,
	list_exercises,
	list_routines,
)


def prompt_integer(
	prompt: str,
	minimum: int = 0,
	zero_is_cancel: bool = True,
) -> int | None:
	while True:
		cancel_hint = "0 para cancelar" if zero_is_cancel else "'cancelar' para cancelar"
		value = input(f"{prompt} ({cancel_hint}): ").strip()
		if value.casefold() == "cancelar" or (zero_is_cancel and value == "0"):
			return None

		try:
			number = int(value)
		except ValueError:
			print("Error: ingresá un número entero válido.")
			continue

		if number < minimum:
			print(f"Error: el valor debe ser mayor o igual que {minimum}.")
			continue

		return number


def prompt_required_text(prompt: str) -> str | None:
	value = input(f"{prompt} (vacío o 'cancelar' para cancelar): ").strip()
	if not value or value.casefold() == "cancelar":
		return None
	return value


def prompt_notes() -> tuple[bool, str | None]:
	value = input("Observaciones (opcional; 'cancelar' cancela): ").strip()
	if value.casefold() == "cancelar":
		return True, None
	return False, value or None


def show_routines() -> list[sqlite3.Row]:
	routines = list_routines()
	if not routines:
		print("No hay rutinas creadas.")
		return routines

	print("Rutinas disponibles:")
	for routine in routines:
		print(f"  {routine['id']}: {routine['name']}")
	return routines


def show_exercises() -> list[sqlite3.Row]:
	exercises = list_exercises()
	if not exercises:
		print("No hay ejercicios creados.")
		return exercises

	print("Ejercicios disponibles:")
	for exercise in exercises:
		print(f"  {exercise['id']}: {exercise['name']}")
	return exercises


def create_routine_menu() -> None:
	name = prompt_required_text("Nombre de la rutina")
	if name is None:
		print("Operación cancelada.")
		return

	try:
		routine_id = create_routine(name)
	except ValueError:
		print("Error: el nombre de la rutina no es válido.")
	except sqlite3.Error:
		print("Error: no se pudo guardar la rutina.")
	else:
		print(f"Rutina creada correctamente con ID {routine_id}.")


def add_exercise_menu() -> None:
	try:
		routines = show_routines()
	except sqlite3.Error:
		print("Error: no se pudieron consultar las rutinas.")
		return

	if not routines:
		return

	routine_id = prompt_integer("ID de la rutina", 1)
	if routine_id is None:
		print("Operación cancelada.")
		return
	if routine_id not in {routine["id"] for routine in routines}:
		print("Error: el ID de rutina no está entre las opciones mostradas.")
		return

	exercise_name = prompt_required_text("Nombre del ejercicio")
	if exercise_name is None:
		print("Operación cancelada.")
		return

	try:
		exercise_id = add_exercise_to_routine(routine_id, exercise_name)
	except ValueError:
		print("Error: los datos ingresados no son válidos.")
	except LookupError:
		print("Error: la rutina seleccionada no existe.")
	except sqlite3.Error:
		print("Error: no se pudo asociar el ejercicio a la rutina.")
	else:
		print(f"Ejercicio asociado correctamente con ID {exercise_id}.")


def register_workout_menu() -> None:
	try:
		routines = show_routines()
	except sqlite3.Error:
		print("Error: no se pudieron consultar las rutinas.")
		return

	if not routines:
		return

	routine_id = prompt_integer("ID de la rutina", 1)
	if routine_id is None:
		print("Operación cancelada.")
		return
	if routine_id not in {routine["id"] for routine in routines}:
		print("Error: el ID de rutina no está entre las opciones mostradas.")
		return

	try:
		exercises = show_exercises()
	except sqlite3.Error:
		print("Error: no se pudieron consultar los ejercicios.")
		return

	if not exercises:
		return

	exercise_id = prompt_integer("ID del ejercicio", 1)
	if exercise_id is None:
		print("Operación cancelada.")
		return
	if exercise_id not in {exercise["id"] for exercise in exercises}:
		print("Error: el ID de ejercicio no está entre las opciones mostradas.")
		return

	sets = prompt_integer("Cantidad de series", 1)
	if sets is None:
		print("Operación cancelada.")
		return
	reps = prompt_integer("Cantidad de repeticiones", 1)
	if reps is None:
		print("Operación cancelada.")
		return
	weight = prompt_integer("Peso utilizado", 0, zero_is_cancel=False)
	if weight is None:
		print("Operación cancelada.")
		return

	workout_date = prompt_required_text("Fecha (YYYY-MM-DD)")
	if workout_date is None:
		print("Operación cancelada.")
		return

	cancelled, notes = prompt_notes()
	if cancelled:
		print("Operación cancelada.")
		return

	try:
		workout_id = register_workout(
			routine_id,
			exercise_id,
			sets,
			reps,
			weight,
			workout_date,
			notes,
		)
	except ValueError:
		print("Error: los datos del entrenamiento no son válidos.")
	except LookupError:
		print("Error: la rutina o el ejercicio seleccionado no existe.")
	except sqlite3.Error:
		print("Error: no se pudo guardar el entrenamiento.")
	else:
		print(f"Entrenamiento registrado correctamente con ID {workout_id}.")


def show_workout_history() -> None:
	try:
		history = get_workout_history()
	except sqlite3.Error:
		print("Error: no se pudo consultar el historial.")
		return

	if not history:
		print("Todavía no hay entrenamientos registrados.")
		return

	print("Historial de entrenamientos:")
	for workout in history:
		notes = workout["notes"] or "Sin observaciones"
		print(
			f"ID {workout['id']} | Fecha: {workout['date']} | "
			f"Rutina {workout['routine_id']}: {workout['routine_name']} | "
			f"Ejercicio {workout['exercise_id']}: {workout['exercise_name']} | "
			f"Series: {workout['sets']} | Repeticiones: {workout['reps']} | "
			f"Peso: {workout['weight']} | Observaciones: {notes}"
		)


def print_menu() -> None:
	print("\n--- GymTrack ---")
	print("1. Crear una rutina")
	print("2. Agregar un ejercicio a una rutina")
	print("3. Registrar un entrenamiento")
	print("4. Ver el historial de entrenamientos")
	print("5. Salir")


def main() -> None:
	try:
		initialize_database()
	except sqlite3.Error:
		print("Error: no se pudo inicializar la base de datos.")
		return

	print("Bienvenido a GymTrack")
	while True:
		print_menu()
		option = input("Elegí una opción: ").strip()

		if option == "1":
			create_routine_menu()
		elif option == "2":
			add_exercise_menu()
		elif option == "3":
			register_workout_menu()
		elif option == "4":
			show_workout_history()
		elif option == "5":
			print("Hasta luego.")
			return
		else:
			print("Error: elegí una opción del 1 al 5.")


if __name__ == "__main__":
	main()
