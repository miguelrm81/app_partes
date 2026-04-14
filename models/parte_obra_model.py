from database.db import get_connection

# Funciones para rellenar los desplegables de las tablas maestras

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
    rows = conn.execute("SELECT id, nombre, apellido1 FROM Personal WHERE activo = 1 ORDER BY nombre").fetchall()
    conn.close()
    return rows

# Funcion para crear un nuevo parte

def insertar_parte(datos):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO ParteObra (
            parte_numero,
            fecha_parte,
            canal_codigo,
            canal_nombre,
            responsable_id,
            relevo_id,
            hora_inicio_relevo,
            hora_fin_relevo,
            pk_inicio_km,
            pk_inicio_m,
            pk_fin_km,
            pk_fin_m,
            tipo_terreno_id,
            seccion_tipo_id,
            total_actividades_min,
            exceso_justificado,
            motivo_exceso_id,
            justificacion_exceso,
            hubo_averias,
            hubo_paradas,
            observaciones,
            estado_id
        ) VALUES (
            :parte_numero,
            :fecha_parte,
            :canal_codigo,
            :canal_nombre,
            :responsable_id,
            :relevo_id,
            :hora_inicio_relevo,
            :hora_fin_relevo,
            :pk_inicio_km,
            :pk_inicio_m,
            :pk_fin_km,
            :pk_fin_m,
            :tipo_terreno_id,
            :seccion_tipo_id,
            :total_actividades_min,
            :exceso_justificado,
            :motivo_exceso_id,
            :justificacion_exceso,
            :hubo_averias,
            :hubo_paradas,
            :observaciones,
            :estado_id
        )""", datos)
    conn.commit()
    conn.close()

#funcion para obtener todos los partes

def obtener_partes(parte_numero=None, fecha_parte=None, estado_id=None, responsable_id=None, pagina=1, por_pagina=15):
    conn = get_connection()
    query = """ SELECT
                        p.id, p.parte_numero, p.fecha_parte,p.fecha_registro_utc, p.canal_nombre,
                        p.total_actividades_min, p.hubo_averias, p.hubo_paradas, 
                        per.nombre AS responsable, 
                        rel.nombre AS relevo,
                        tt.descripcion AS tipo_terreno, 
                        st.descripcion AS seccion_tipo,
                        e.descripcion AS estado
                        FROM parteobra p
                        LEFT JOIN personal per ON p.responsable_id = per.id
                        LEFT JOIN personal rel ON p.relevo_id = rel.id
                        LEFT JOIN tipoterreno tt ON p.tipo_terreno_id = tt.id
                        LEFT JOIN secciontipo st ON p.seccion_tipo_id = st.id
                        LEFT JOIN estadoparte e ON p.estado_id = e.id
                        WHERE 1=1 """
    
    params = []
    
    if parte_numero:
        query += " AND p.parte_numero LIKE ?"
        params.append(f"%{parte_numero}%")

    if fecha_parte:
        query += " AND p.fecha_parte = ?"
        params.append(fecha_parte)

    if estado_id:
        query += " AND p.estado_id = ?"
        params.append(estado_id)

    if responsable_id:
        query += " AND p.responsable_id = ?"
        params.append(responsable_id)

    offset = (pagina - 1) * por_pagina
    query += " ORDER BY p.fecha_registro_utc DESC LIMIT ? OFFSET ?"
    params.append(por_pagina)
    params.append(offset)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows

#Funcion para buscar un parte por ID

def obtener_parte_por_id(parte_id):
    conn = get_connection()
    parte = conn.execute("SELECT * FROM ParteObra WHERE id = ?", (parte_id,)).fetchone()
    conn.close()
    return parte

# Funcion para actualizar un parte existente

def actualizar_parte(parte_id, datos):
    conn = get_connection()
    conn.execute(""" UPDATE ParteObra SET
                        parte_numero = :parte_numero,
                        fecha_parte = :fecha_parte,
                        canal_codigo = :canal_codigo,
                        canal_nombre = :canal_nombre,
                        responsable_id = :responsable_id,
                        relevo_id = :relevo_id,
                        hora_inicio_relevo = :hora_inicio_relevo,
                        hora_fin_relevo = :hora_fin_relevo,
                        pk_inicio_km = :pk_inicio_km,
                        pk_inicio_m = :pk_inicio_m,
                        pk_fin_km = :pk_fin_km,
                        pk_fin_m = :pk_fin_m,
                        tipo_terreno_id = :tipo_terreno_id,
                        seccion_tipo_id = :seccion_tipo_id,
                        total_actividades_min = :total_actividades_min,
                        exceso_justificado = :exceso_justificado,
                        motivo_exceso_id = :motivo_exceso_id,
                        justificacion_exceso = :justificacion_exceso,
                        hubo_averias = :hubo_averias,
                        hubo_paradas = :hubo_paradas,
                        observaciones = :observaciones,
                        estado_id = :estado_id,
                        fecha_edicion_utc = datetime('now', 'localtime')
                    WHERE id = :id""", 
                    {**datos, "id": parte_id,})
    conn.commit()
    conn.close()

# Funcion para eliminar un parte existente

def borrar_parte(parte_id):
    conn = get_connection()
    conn.execute("DELETE FROM ParteObra WHERE id = ?", (parte_id,))
    conn.commit()
    conn.close()

# Funcion para validar si existe un parte con el mismo numero para evitar duplicados

def comprobar_num_parte(parte_numero):
    conn = get_connection()
    row = conn.execute("SELECT id FROM parteObra WHERE parte_numero = ?", (parte_numero,)).fetchone()
    conn.close()
    return row is not None

# Funcion para contar cantidad de partes para hacer la paginacion del index.html

def contar_partes(parte_numero=None, fecha_parte=None, estado_id=None, responsable_id=None):
    conn = get_connection()
    query = "SELECT COUNT(*) FROM parteObra WHERE 1=1"
    params = []

    if parte_numero:
        query += " AND parte_numero LIKE ?"
        params.append(f"%{parte_numero}%")

    if fecha_parte:
        query += " AND fecha_parte = ?"
        params.append(fecha_parte)
    
    if estado_id:    
        query += " AND estado_id = ?"
        params.append(estado_id)

    if responsable_id:
        query += " AND responsable_id = ?"
        params.append(responsable_id)
    
    total = conn.execute(query, params).fetchone()[0]
    conn.close()
    return total

def obtener_parte_ver(parte_id):
    conn = get_connection()
    row = conn.execute("""
        SELECT
            p.*,
            per.nombre              AS responsable_nombre,
            per.apellido1           AS responsable_apellido1,
            rel.nombre              AS relevo_nombre,
            rel.apellido1           AS relevo_apellido1,
            tt.descripcion          AS tipo_terreno,
            st.descripcion          AS seccion_tipo,
            e.descripcion           AS estado,
            m.descripcion           AS motivo_exceso
        FROM ParteObra p
        LEFT JOIN Personal          per ON p.responsable_id  = per.id
        LEFT JOIN Personal          rel ON p.relevo_id        = rel.id
        LEFT JOIN TipoTerreno       tt  ON p.tipo_terreno_id  = tt.id
        LEFT JOIN SeccionTipo       st  ON p.seccion_tipo_id  = st.id
        LEFT JOIN EstadoParte       e   ON p.estado_id        = e.id
        LEFT JOIN MotivoExcesoHoras m   ON p.motivo_exceso_id = m.id
        WHERE p.id = ?
    """, (parte_id,)).fetchone()
    conn.close()
    return row