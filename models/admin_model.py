from database.db import get_connection

#funciones para rellenar las tablas maestras en Admin

def get_tipo_terreno():
    conn = get_connection()
    rows = conn.execute("SELECT id, descripcion FROM TipoTerreno ORDER BY descripcion").fetchall()
    conn.close()
    return rows

def get_seccion_tipo():
    conn = get_connection()
    rows = conn.execute("SELECT id, descripcion FROM SeccionTipo ORDER BY descripcion").fetchall()
    conn.close()
    return rows

def get_estados():
    conn = get_connection()
    rows = conn.execute("SELECT id, descripcion FROM EstadoParte ORDER BY id").fetchall()
    conn.close()
    return rows

def get_motivo_exceso():
    conn = get_connection()
    rows = conn.execute("SELECT id, descripcion FROM MotivoExcesoHoras ORDER BY descripcion").fetchall()
    conn.close()
    return rows

def get_personal_activo():
    conn = get_connection()
    rows = conn.execute("SELECT id, nombre FROM Personal WHERE activo = 1 ORDER BY nombre").fetchall()
    conn.close()
    return rows

# Funciones para insertar datos nuevos en las tablas maestras

def insertar_tipo_terreno(descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TipoTerreno (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()

def insertar_seccion_tipo(descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SeccionTipo (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()

def insertar_estado_parte(descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO EstadoParte (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()

def insertar_motivo_exceso(descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO MotivoExcesoHoras (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()

def insertar_personal(nombre):      
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Personal (nombre, activo) VALUES (?, ?)", (nombre, 1))
    conn.commit()
    conn.close()

# Funcion para activar/desactivar personas

def activar_personal(id, activo):
    conn = get_connection()
    conn.execute("UPDATE Personal SET activo = ? WHERE id = ?", (activo, id))
    conn.commit()
    conn.close()

