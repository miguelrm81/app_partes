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

