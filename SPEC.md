--- SPEC ---
[# GymTrack

## Objetivo
Crear una aplicación de consola que permita organizar rutinas de 
entrenamiento y registrar el progreso de los usuarios a lo largo del tiempo.

## Problema
Las personas que entrenan (en gimnasio o en casa) no tienen una forma 
simple de planificar sus rutinas y llevar un registro de lo que realmente 
hicieron en cada sesión, lo que dificulta ver su progreso.

## Usuario
Personas que realizan actividad física y quieren llevar un control 
ordenado de sus rutinas y entrenamientos.

## Entidades y datos

### Rutina
- Nombre de la rutina
- Lista de ejercicios que la componen

### Ejercicio
- Nombre del ejercicio

### Registro de entrenamiento
- Rutina asociada
- Ejercicio realizado
- Cantidad de series
- Cantidad de repeticiones
- Peso utilizado
- Fecha
- Observaciones

## Funcionalidades (MVP - primera versión)
1. Crear una rutina.
2. Agregar ejercicios a una rutina.
3. Registrar un entrenamiento (series, repeticiones, peso, fecha, observaciones).
4. Ver el historial de entrenamientos.

## Funcionalidades futuras (no incluir todavía)
- Buscar ejercicios por nombre.
- Estadísticas o gráficos de progreso.
- Edición/eliminación de rutinas y registros.

## Restricciones
- La aplicación debe ser fácil de usar, con un menú de consola claro.
- Los datos deben guardarse correctamente y persistir entre ejecuciones (SQLite).
- El código debe ser simple, legible y sin abstracciones innecesarias.
- Debe haber manejo de errores ante datos ingresados incorrectamente 
  (por ejemplo, texto donde se espera un número).

## Stack técnico
- Python (librería estándar).
- SQLite (módulo `sqlite3`), sin frameworks externos.
- Interfaz por consola (sin frontend web).

## Criterios de validación
- Todas las funciones del MVP funcionan correctamente.
- Los datos ingresados se guardan y se recuperan bien de la base SQLite.
- La app es fácil de navegar por consola.
- El código está organizado por archivo según responsabilidad (rutinas, 
  entrenamientos, base de datos, main).
- Los errores de entrada del usuario no rompen la aplicación.]
