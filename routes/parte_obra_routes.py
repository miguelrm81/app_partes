from flask import Blueprint, render_template, request, redirect, url_for
from models.parte_obra_model import *

parte_bp = Blueprint('partes', __name__)

# Ruta para listar los partes
@parte_bp.route('/')
def index():
    parte_numero = request.args.get('parte_numero')
    fecha_parte = request.args.get('fecha_parte')
    estado_id = request.args.get('estado_id')
    responsable_id = request.args.get('responsable_id')
    pagina = request.args.get('pagina', 1, type=int)
    reg_x_pagina = 15
    total_partes = contar_partes(parte_numero, fecha_parte, estado_id, responsable_id)
    total_paginas = (total_partes + reg_x_pagina - 1) // reg_x_pagina
    partes = obtener_partes(parte_numero, fecha_parte, estado_id, responsable_id, pagina, reg_x_pagina)
    estados = get_estados()
    personal = get_personal_activo()
    return render_template("index.html", partes = partes, estados=estados, parte_numero=parte_numero, fecha_parte=fecha_parte, estado_id=estado_id, responsable_id=responsable_id, personal=personal, pagina=pagina, total_paginas=total_paginas)

#Ruta para el formulario de nuevo parte

@parte_bp.route("/partes/nuevo", methods=["GET"])
def nuevo_parte():
    tipos_terreno = get_tipo_terreno()
    secciones_tipo = get_seccion_tipo()
    estados = get_estados()
    motivos_exceso = get_motivo_exceso()
    personal = get_personal_activo()
    return render_template("nuevo.html", tipos_terreno=tipos_terreno, secciones_tipo=secciones_tipo, 
                           estados=estados, motivos_exceso=motivos_exceso, personal=personal)

# Ruta para guardar un nuevo parte

@parte_bp.route("/partes/nuevo", methods=["POST"])
def guardar_parte():
    form = request.form

    if comprobar_num_parte(form.get("parte_numero")):
        tipos_terreno  = get_tipo_terreno()
        secciones_tipo = get_seccion_tipo()
        estados        = get_estados()
        motivos_exceso = get_motivo_exceso()
        personal       = get_personal_activo()
        return render_template("nuevo.html",
            error="Numero de parte repetido.",
            tipos_terreno=tipos_terreno,
            secciones_tipo=secciones_tipo,
            estados=estados,
            motivos_exceso=motivos_exceso,
            personal=personal,
            form=form
        )
    
    datos = {
            "parte_numero": form.get("parte_numero"),
            "fecha_parte": form.get("fecha_parte"),
            "canal_codigo": form.get("canal_codigo") or None,
            "canal_nombre": form.get("canal_nombre") or None,
            "responsable_id": form.get("responsable_id"),
            "relevo_id": form.get("relevo_id") or None,
            "hora_inicio_relevo": form.get("hora_inicio_relevo") or None,
            "hora_fin_relevo": form.get("hora_fin_relevo") or None,
            "pk_inicio_km": form.get("pk_inicio_km") or None,
            "pk_inicio_m": form.get("pk_inicio_m") or None,
            "pk_fin_km": form.get("pk_fin_km") or None,
            "pk_fin_m": form.get("pk_fin_m") or None,
            "tipo_terreno_id": form.get("tipo_terreno_id") or None,
            "seccion_tipo_id": form.get("seccion_tipo_id") or None,
            "total_actividades_min": form.get("total_actividades_min") or None,
            "exceso_justificado": 1 if form.get("exceso_justificado") else 0,
            "motivo_exceso_id": form.get("motivo_exceso_id") or None,
            "justificacion_exceso": form.get("justificacion_exceso") or None,
            "hubo_averias": 1 if form.get("hubo_averias") else 0,
            "hubo_paradas": 1 if form.get("hubo_paradas") else 0,
            "observaciones": form.get("observaciones") or None,
            "estado_id": form.get("estado_id"),
        }
    insertar_parte(datos)
    return redirect(url_for("partes.index"))

# Ruta para mostrar el formulario de edicion
@parte_bp.route("/partes/editar/<int:parte_id>", methods=["GET"])
def editar_parte(parte_id):
    parte = obtener_parte_por_id(parte_id)
    if not parte:
        return "Parte no encontrado", 404
    tipos_terreno = get_tipo_terreno()
    secciones_tipo = get_seccion_tipo()
    estados = get_estados()
    motivos_exceso = get_motivo_exceso()
    personal = get_personal_activo()
    return render_template("editar.html", parte=parte, tipos_terreno = tipos_terreno, 
                           secciones_tipo = secciones_tipo, estados = estados, 
                           motivos_exceso = motivos_exceso, personal = personal)

# Ruta para guardar los cambios de un parte editado

@parte_bp.route("/partes/editar/<int:parte_id>", methods=["POST"])
def actualizar_parte_route(parte_id):
    form = request.form
    datos = {
        "parte_numero": form.get("parte_numero"),
        "fecha_parte": form.get("fecha_parte"),
        "canal_codigo": form.get("canal_codigo") or None,
        "canal_nombre": form.get("canal_nombre") or None,
        "responsable_id": form.get("responsable_id"),
        "relevo_id": form.get("relevo_id") or None,
        "hora_inicio_relevo": form.get("hora_inicio_relevo") or None,
        "hora_fin_relevo": form.get("hora_fin_relevo") or None,
        "pk_inicio_km": form.get("pk_inicio_km") or None,
        "pk_inicio_m": form.get("pk_inicio_m") or None,
        "pk_fin_km": form.get("pk_fin_km") or None,
        "pk_fin_m": form.get("pk_fin_m") or None,
        "tipo_terreno_id": form.get("tipo_terreno_id") or None,
        "seccion_tipo_id": form.get("seccion_tipo_id") or None,
        "total_actividades_min": form.get("total_actividades_min") or None,
        "exceso_justificado": 1 if form.get("exceso_justificado") else 0,
        "motivo_exceso_id": form.get("motivo_exceso_id") or None,
        "justificacion_exceso": form.get("justificacion_exceso") or None,
        "hubo_averias": 1 if form.get("hubo_averias") else 0,
        "hubo_paradas": 1 if form.get("hubo_paradas") else 0,
        "observaciones": form.get("observaciones") or None,
        "estado_id": form.get("estado_id"),
    }
    actualizar_parte(parte_id, datos)
    return redirect(url_for("partes.index"))

# Ruta para eliminar un parte

@parte_bp.route("/partes/eliminar/<int:parte_id>", methods=["POST"])
def borrar_parte_route(parte_id):
    borrar_parte(parte_id)
    return redirect(url_for("partes.index"))
