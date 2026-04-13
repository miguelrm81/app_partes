# APP_PARTESDEOBRA
Aplicación web en Flask para gestionar partes de obra (crear, editar, borrar, listar y administrar datos maestros).

Requisitos
Python 3.10 o superior
pip

## Instalación rápida (Windows PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Variables de entorno

Crea un archivo .env en la raíz del proyecto con:

SECRET_KEY=tu_clave_secreta
ADMIN_USER=admin
ADMIN_PASSWORD=tu_password

## Inicializar base de datos

python database/init_db.py
python database/inserciondatos.py

## Ejecutar la app

python app.py

Abrir en el navegador:

http://127.0.0.1:5000

## Estructura

app.py
database/
models/
routes/
templates/
static/

## Mejoras con la version anterior
- Validacion de datos en el front y en el back
- Panel de admin para gestion de personal y datos maestros
- Limpieza de datos antes de guardar en la base de datos
- Ampliacion de datos para la tabla de personal
- Autenticacion básica de Admin para modificacion de datos maestros
- Añadidos filtros de busqueda en Tabla de Index
- Paginacion en las tablas para mejora en la visualización
- Añadido el campo fecha_edicion_utc para tener un registro de modificaciones en los partes
- Mejoras visuales en creación y edición de partes