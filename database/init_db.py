import sqlite3
from datetime import datetime

conn = sqlite3.connect("database/teciman.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

#Tablas maestras para campos fijos

# Tabla Personal
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Personal(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               activo INTEGER NOT NULL DEFAULT 1)
               """)

# Tabla Tipo de Terreno
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TipoTerreno(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               descripcion TEXT NOT NULL)
               """)

# Tabla de Tipo de sección
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SeccionTipo(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               descripcion TEXT NOT NULL)
               """)

# Tabla de Motivo de Exceso de horas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS MotivoExcesoHoras(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               descripcion TEXT NOT NULL)
               """)

# Tabla Estado de los partes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS EstadoParte(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               descripcion TEXT NOT NULL)
                """)

# Tabla principal Parte de Obra
cursor.execute("""
               CREATE TABLE IF NOT EXISTS ParteObra(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               parte_numero TEXT NOT NULL UNIQUE,
               fecha_parte DATE NOT NULL,
               fecha_registro_utc DATETIME NOT NULL DEFAULT (datetime('now')),
               canal_codigo TEXT,
               canal_nombre TEXT,
               responsable_id INTEGER,
               relevo_id INTEGER,
               hora_inicio_relevo TEXT,
               hora_fin_relevo TEXT,
               pk_inicio_km INTEGER,
               pk_inicio_m INTEGER,
               pk_fin_km INTEGER,
               pk_fin_m INTEGER,
               tipo_terreno_id INTEGER,
               seccion_tipo_id INTEGER,
               total_actividades_min INTEGER,
               exceso_justificado INTEGER NOT NULL DEFAULT 0,
               motivo_exceso_id INTEGER,
               justificacion_exceso TEXT,
               hubo_averias INTEGER NOT NULL DEFAULT 0,
               hubo_paradas INTEGER NOT NULL DEFAULT 0,
               observaciones TEXT,
               estado_id INTEGER NOT NULL,

                FOREIGN KEY (responsable_id) REFERENCES Personal(id),
                FOREIGN KEY (relevo_id) REFERENCES Personal(id),
                FOREIGN KEY (tipo_terreno_id) REFERENCES TipoTerreno(id),
                FOREIGN KEY (seccion_tipo_id) REFERENCES SeccionTipo(id),
                FOREIGN KEY (motivo_exceso_id) REFERENCES MotivoExcesoHoras(id),
                FOREIGN KEY (estado_id) REFERENCES EstadoParte(id)

               )""")

# Tabla Actividades
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Actividad (
        actividadid INTEGER PRIMARY KEY,
        parteid INTEGER NOT NULL,
        descripcion TEXT,
        duracion_min INTEGER,
        FOREIGN KEY (parteid) REFERENCES ParteObra(id) ON DELETE CASCADE
        )""")

#Tabla de Adjuntos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Adjunto (
        adjunto_id INTEGER PRIMARY KEY,
        parteid INTEGER NOT NULL,
        nombre_archivo TEXT,
        FOREIGN KEY (parteid) REFERENCES ParteObra(id) ON DELETE CASCADE
    )""")

#Tabla Maquinaria
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Maquinaria (
        maquinaria_id INTEGER PRIMARY KEY,
        parteid INTEGER NOT NULL,
        nombre TEXT,
        FOREIGN KEY (parteid) REFERENCES ParteObra(id) ON DELETE CASCADE
    )""")

#Tabla Materiales
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Material (
        material_id INTEGER PRIMARY KEY,
        parteid INTEGER NOT NULL,
        nombre TEXT,
        cantidad INTEGER,
        unidad TEXT,
        FOREIGN KEY (parteid) REFERENCES ParteObra(id) ON DELETE CASCADE
    )""")

conn.commit()
conn.close()

print("Base de datos creada correctamente.")