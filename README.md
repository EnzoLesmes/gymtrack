# GymTrack

Aplicación de consola en Python para organizar rutinas de entrenamiento y registrar el progreso de los usuarios.

## Funcionalidades

- Crear una rutina de entrenamiento.
- Agregar ejercicios a una rutina (reutilizables entre rutinas).
- Registrar un entrenamiento (series, repeticiones, peso, fecha, observaciones).
- Ver el historial de entrenamientos, ordenado por fecha.

## Cómo ejecutar

Requisitos: Python 3 (sin dependencias externas, todo con la librería estándar).

Desde la raíz del proyecto:

```
python src/main.py
```

La primera ejecución crea automáticamente el archivo `gymtrack.db` (SQLite) con las tablas necesarias.

## Estructura del proyecto

- `src/main.py`: punto de entrada, menú de consola.
- `src/database.py`: conexión y esquema de la base de datos SQLite.
- `src/rutinas.py`: lógica de rutinas y ejercicios.
- `src/entrenamientos.py`: registro de entrenamientos e historial.

## Documentación del proyecto

- [`SPEC.md`](./SPEC.md): especificación funcional del producto.
- [`AGENTS.md`](./AGENTS.md): reglas de comportamiento y convenciones para el desarrollo asistido por IA.

## Requisitos

- Python 3
- SQLite incluido en la librería estándar de Python