import os
from flask import Blueprint, render_template, request, redirect, session, url_for, make_response
from models.parte_obra_model import *
from xhtml2pdf import pisa
from io import BytesIO


parte_bp = Blueprint('partes', __name__)

# Funcion de validacion de partes para evitar errores
def validar_parte(form):
    errores = {}

    if form.get("relevo_id") and not form.get("hora_inicio_relevo"):
        errores['hora_inicio_relevo'] = "Campo obligatorio"

    if form.get("relevo_id") and not form.get("hora_fin_relevo"):
        errores['hora_fin_relevo'] = "Campo obligatorio"

    if form.get("exceso_justificado") and not form.get("motivo_exceso_id"):
        errores['motivo_exceso_id'] = "Seleccione motivo"
    
    if form.get("exceso_justificado") and not form.get("justificacion_exceso"):
        errores['justificacion_exceso'] = "Justifique el exceso"

    if form.get("relevo_id") and form.get("responsable_id") == form.get("relevo_id"):
        errores['relevo_id'] = "El relevo y responsable no pueden ser iguales."

    pk_inicio_km = form.get("pk_inicio_km")
    pk_inicio_m = form.get("pk_inicio_m")
    pk_fin_km = form.get("pk_fin_km")
    pk_fin_m = form.get("pk_fin_m")

    if pk_inicio_km and pk_fin_km:
        inicio= int(pk_inicio_km) * 1000 + int(pk_inicio_m or 0)
        fin = int(pk_fin_km) * 1000 + int(pk_fin_m or 0)
        if inicio >= fin:
            errores['pk_fin_km'] = "El PK final debe ser mayor que el PK inicial"
    
    hora_inicio = form.get("hora_inicio_relevo")
    hora_fin = form.get("hora_fin_relevo")
    if hora_inicio and hora_fin:
        if hora_inicio >= hora_fin:
            errores['hora_fin_relevo'] = "La hora de fin debe ser mayor que la inicial"
    
    return errores

# Funcion para limpiar los datos de espacios en blanco al principio y al final del texto
def limpiar_datos(datos):
    for clave, valor in datos.items():
        if isinstance(valor, str):
            datos[clave] = valor.strip()
    return datos

# funcion para cargar los datos de las tablas maestras en los formularios
def cargar_maestras():
    return {
        "tipos_terreno":  get_tipo_terreno(),
        "secciones_tipo": get_seccion_tipo(),
        "estados":        get_estados(),
        "motivos_exceso": get_motivo_exceso(),
        "personal":       get_personal_activo(),
    }

# ruta de login para acceder a la aplicacion
@parte_bp.route("/", methods=["GET", "POST"])   
def login():
    return render_template("login.html")


# Ruta para listar los partes
@parte_bp.route('/partes')
def index():
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    parte_numero = request.args.get('parte_numero')
    fecha_parte = request.args.get('fecha_parte')
    estado_id = request.args.get('estado_id')
    responsable_id = request.args.get('responsable_id')
    pagina = request.args.get('pagina', 1, type=int)
    reg_x_pagina = 12
    total_partes = contar_partes(parte_numero, fecha_parte, estado_id, responsable_id)
    total_paginas = (total_partes + reg_x_pagina - 1) // reg_x_pagina
    partes = obtener_partes(parte_numero, fecha_parte, estado_id, responsable_id, pagina, reg_x_pagina)
    estados = get_estados()
    personal = get_personal_activo()
    return render_template("index.html", partes = partes, estados=estados, parte_numero=parte_numero, fecha_parte=fecha_parte, 
                           estado_id=estado_id, responsable_id=responsable_id, personal=personal, pagina=pagina, total_paginas=total_paginas)

#Ruta para el formulario de nuevo parte

@parte_bp.route("/partes/nuevo", methods=["GET"])
def nuevo_parte():
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    maestras = cargar_maestras()
    return render_template("nuevo.html", **maestras)
   

# Ruta para guardar un nuevo parte

@parte_bp.route("/partes/nuevo", methods=["POST"])
def guardar_parte():
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    form = request.form
    errores = validar_parte(form)

    if comprobar_num_parte(form.get("parte_numero")):
        errores['parte_numero'] = "Numero de parte repetido."

    if errores:
        maestras = cargar_maestras()
        return render_template("nuevo.html", errores=errores, form=form, **maestras)
       
    
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
    datos = limpiar_datos(datos)
    insertar_parte(datos)
    return redirect(url_for("partes.index"))

# Ruta para mostrar el formulario de edicion
@parte_bp.route("/partes/editar/<int:parte_id>", methods=["GET"])
def editar_parte(parte_id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    parte = obtener_parte_por_id(parte_id)
    if not parte:
        return "Parte no encontrado", 404
    maestras = cargar_maestras()
    return render_template("editar.html", parte=parte, **maestras)

# Ruta para ver partes sin editar

@parte_bp.route("/partes/ver/<int:parte_id>", methods=["GET"])
def ver_parte(parte_id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    parte = obtener_parte_ver(parte_id)
    
    if not parte:
        return "Parte no encontrado", 404
    
    return render_template("ver.html", parte=parte)


# Ruta para guardar los cambios de un parte editado

@parte_bp.route("/partes/editar/<int:parte_id>", methods=["POST"])
def actualizar_parte_route(parte_id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    form = request.form
    errores = validar_parte(form)

    if errores:
        parte = obtener_parte_por_id(parte_id)
        maestras = cargar_maestras()
        return render_template("editar.html", parte=parte, errores=errores, form=form, **maestras)
    
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
    datos = limpiar_datos(datos)
    actualizar_parte(parte_id, datos)
    return redirect(url_for("partes.index"))

# Ruta para eliminar un parte

@parte_bp.route("/partes/eliminar/<int:parte_id>", methods=["POST"])
def borrar_parte_route(parte_id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    borrar_parte(parte_id)
    return redirect(url_for("partes.index"))

# Ruta para descargar parte en pdf

@parte_bp.route("/partes/pdf/<int:parte_id>", methods=["GET"])
def descargar_pdf(parte_id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    parte = obtener_parte_ver(parte_id)
    if not parte:
        return "Parte no encontrado", 404
    
    ruta_logo = os.path.join(os.path.abspath('static'), 'imagen', 'logotipo.png')
    html = render_template("parte_pdf.html", parte=parte, ruta_logo=ruta_logo)

    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=parte_{parte["parte_numero"]}.pdf'

    return response
