from flask import Blueprint, render_template, request, redirect, url_for, session
from models.admin_model import *

import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin", methods=["GET"])
def carga_admin():

    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    tipos_terreno = get_tipo_terreno()
    secciones_tipo = get_seccion_tipo()
    estados = get_estados()
    motivos_exceso = get_motivo_exceso()
    personal = get_personal()
    return render_template("admin.html", tipos_terreno=tipos_terreno, secciones_tipo=secciones_tipo, 
                           estados=estados, motivos_exceso=motivos_exceso, personal=personal)

@admin_bp.route("/admin/insertar/<maestro>", methods=["POST"])
def insertar_maestro(maestro):
    
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
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
        apellido1 = request.form.get("apellido1")
        apellido2 = request.form.get("apellido2")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        insertar_personal(nombre, apellido1, apellido2, telefono, email)
    return redirect(url_for("admin.carga_admin"))

@admin_bp.route("/admin/eliminar/<maestro>/<int:id>", methods=["POST"])
def eliminar_maestro(maestro,id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    borrar_maestro(maestro, id)
    return redirect(url_for("admin.carga_admin"))

@admin_bp.route("/admin/activar_personal/<int:id>", methods=["POST"])
def activar_personal_route(id):
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    persona = obtener_personal_por_id(id)
    nuevo_activo = 0 if persona['activo'] == 1 else 1
    activar_personal(id, nuevo_activo)
    return redirect(url_for("admin.carga_admin"))

@admin_bp.route("/admin/login", methods=["GET"])
def login_admin():
    return render_template("login.html")

@admin_bp.route("/admin/login", methods=["POST"])
def login_admin_post():
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD")
    
    if username_input == username and password_input == password:
        session['autenticado'] = True
        return redirect(url_for("admin.carga_admin"))
    else:
        return render_template("login.html", error="Credenciales incorrectas")
    
@admin_bp.route("/admin/logout", methods=["GET"])
def logout_admin():
    session.clear()
    return redirect(url_for("admin.login_admin"))