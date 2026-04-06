from flask import Blueprint, render_template, request, redirect, url_for
from models.admin_model import *

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin", methods=["GET"])
def carga_admin():
    tipos_terreno = get_tipo_terreno()
    secciones_tipo = get_seccion_tipo()
    estados = get_estados()
    motivos_exceso = get_motivo_exceso()
    personal = get_personal_activo()
    return render_template("admin.html", tipos_terreno=tipos_terreno, secciones_tipo=secciones_tipo, 
                           estados=estados, motivos_exceso=motivos_exceso, personal=personal)

@admin_bp.route("/admin/insertar/<maestro>", methods=["POST"])
def insertar_maestro(maestro):
    
    if maestro == "tipo_terreno":
        descripcion = request.form.get("descripcion")
        insertar_tipo_terreno(descripcion)
    elif maestro == "seccion_tipo":
        descripcion = request.form.get("descripcion")
        insertar_seccion_tipo(descripcion)
    elif maestro == "estado_parte":
        descripcion = request.form.get("descripcion")
        insertar_estado_parte(descripcion)
    elif maestro == "motivo_exceso":
        descripcion = request.form.get("descripcion")
        insertar_motivo_exceso(descripcion)
    elif maestro == "personal":
        nombre = request.form.get("nombre")
        insertar_personal(nombre)
    return redirect(url_for("admin.carga_admin"))

@admin_bp.route("/admin/eliminar/<maestro>/<int:id>", methods=["POST"])
def eliminar_maestro(maestro,id):
    borrar_maestro(maestro, id)
    return redirect(url_for("admin.carga_admin"))