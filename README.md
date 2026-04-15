# APP_PARTESDEOBRA

Aplicacion web en Flask para gestionar partes de obra: crear, editar, ver en modo lectura, borrar, listar y administrar datos maestros.

## Funcionalidades actuales

- Login en la pagina principal
- Listado de partes con filtros y paginacion
- Alta de partes
- Edicion de partes
- Vista de detalle de parte sin posibilidad de edicion
- Borrado de partes
- Panel de administracion para datos maestros
- Registro de fecha de creacion y fecha de ultima edicion en UTC

## Requisitos

```text
Python 3.10 o superior
pip
```

## Instalacion rapida (Windows PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en la raiz del proyecto con:

```env
SECRET_KEY=tu_clave_secreta
```

## Inicializar base de datos y datos iniciales

Ejecuta estos scripts en orden:

```bash
python database/init_db.py
python database/inserciondatos.py
python database/insertar_usuarios.py
```
El script de datos crea datos de ejemplo en tablas maestras.
El script de usuarios crea usuarios de ejemplo para pruebas.

## Ejecutar la app

```bash
python app.py
```

Abrir en el navegador:

`http://127.0.0.1:5000`

## Flujo de acceso

1. La ruta principal muestra la pantalla de login.
2. Al iniciar sesion, se accede al listado de partes.
3. Los usuarios con rol admin pueden entrar en administracion de maestros.

## Estructura del proyecto

```text
APP_PARTESDEOBRA/
|-- app.py
|-- README.md
|-- requirements.txt
|-- database/
|   |-- db.py
|   |-- init_db.py
|   |-- inserciondatos.py
|   |-- insertar_usuarios.py
|   `-- teciman.db
|-- models/
|   |-- admin_model.py
|   `-- parte_obra_model.py
|-- routes/
|   |-- admin_routes.py
|   `-- parte_obra_routes.py
|-- static/
|       |--imagen/
           `-- logotipo.png
|   `-- styles.css
`-- templates/
    |-- admin.html
    |-- editar.html
    |-- index.html
    |-- login.html
    |-- nuevo.html
    `-- ver.html
```

## Mejoras implementadas

- Validacion de datos en frontend y backend
- Funcion centralizada de validacion para partes
- Limpieza de datos antes de guardar
- Filtros de busqueda y paginacion en listado
- Autenticacion con hash de contraseña (`werkzeug.security`)
- Control de rol para acceso a panel de administracion
- Campo `fecha_edicion_utc` para registro de ultima modificacion
- Vista de detalle de parte en modo solo lectura

## Proximos cambios (version 2.0)

- [ ] Mejora visual de plantillas con estilo mas moderno
- [ ] Insercion de archivos y manejo de rutas en base de datos
- [ ] Uso de la tabla Maquinaria dentro de formularios
- [ ] Uso de la tabla Material dentro de formularios
- [x] Exportacion de partes a PDF o Excel

## Notas

- Si cambias los usuarios de ejemplo, recuerda usar hash de contrasena.
- Si borras la base de datos, vuelve a ejecutar los scripts de inicializacion.
