# APP_PARTESDEOBRA
Aplicación web en Flask para gestionar partes de obra (crear, editar, borrar, listar y administrar datos maestros).

## Requisitos
```text
Python 3.10 o superior
pip
```

## Instalación rápida (Windows PowerShell)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo .env en la raíz del proyecto con:

```env
SECRET_KEY=tu_clave_secreta
ADMIN_USER=admin
ADMIN_PASSWORD=tu_password
```

## Inicializar base de datos

```bash
python database/init_db.py
python database/inserciondatos.py
```

## Ejecutar la app

```bash
python app.py
```

Abrir en el navegador:

http://127.0.0.1:5000

## Estructura

```text
APP_PARTESDEOBRA/
├── app.py
├── README.md
├── requirements.txt
├── database/
│   ├── db.py
│   ├── init_db.py
│   └── inserciondatos.py
├── models/
│   ├── admin_model.py
│   └── parte_obra_model.py
├── routes/
│   ├── admin_routes.py
│   └── parte_obra_routes.py
├── static/
│   └── styles.css
└── templates/
    ├── admin.html
    ├── editar.html
    ├── index.html
    ├── login.html
    └── nuevo.html
```

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

## Proximos cambios version 2.0

- Crear sistema de usuarios y autenticacion completa en la app mediante werkzeug.security
- Mejora visual de las plantillas actualizando bordeados y con un estilo mas moderno
- Insercion de archivos y manejo de rutas en la base de datos
- Uso de la tabla maquinaria dentro de los formularios
- Exportacion de partes a PDF o Excel
