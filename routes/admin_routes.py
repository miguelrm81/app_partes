from flask import Blueprint, render_template, request, redirect, url_for, session
from models.admin_model import *
import os

admin_bp = Blueprint('admin', __name__)

def limpiar_datos(texto):
    if not texto:
        return texto
    return texto.strip().title()

def limpiar_personal(datos):
    datos['nombre']    = datos['nombre'].strip().title()
    datos['apellido1'] = datos['apellido1'].strip().title()
    datos['apellido2'] = datos['apellido2'].strip().title()
    datos['email']     = datos['email'].strip().lower()
    datos['telefono']  = datos['telefono'].strip()
    return datos

@admin_bp.route("/admin", methods=["GET"])
def carga_admin():

    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    maestras = cargar_maestras_admin()
    return render_template("admin.html", **maestras)
                           

@admin_bp.route("/admin/insertar/<maestro>", methods=["POST"])
def insertar_maestro(maestro):
    
    if not session.get('autenticado'):
        return redirect(url_for("admin.login_admin"))
    
    errores = {}
    
    if maestro == "personal":
        datos = {
            "nombre": request.form.get("nombre"),
            "apellido1": request.form.get("apellido1"),
            "apellido2": request.form.get("apellido2"),
            "telefono": request.form.get("telefono"),
            "email": request.form.get("email")
        }
        datos = limpiar_personal(datos)

        if not all(datos.values()):
            errores['todos'] = "Todos los campos son obligatorios."   
        elif not datos['telefono'].isdigit() or len(datos['telefono']) != 9:
            errores['telefono'] = "El teléfono tiene que tener 9 digitos" 
        if errores:
            maestras = cargar_maestras_admin()
            return render_template("admin.html", errores=errores, **maestras)
        
        if validar_personal(datos['nombre'], datos['apellido1'], datos['apellido2']):
            errores['personal'] = "Ya existe una persona con ese nombre y apellidos"
        elif validar_email(datos['email']):
            errores['email'] = "Ya existe un personal con ese email"
        elif validar_telefono(datos['telefono']):
            errores['telefono'] = "Ya existe un personal con ese teléfono"
        
        if not errores:
            insertar_personal(datos['nombre'], datos['apellido1'], datos['apellido2'], datos['telefono'], datos['email'])
    
    else:
        descripcion = limpiar_datos(request.form.get("descripcion"))

        if validar_descripcion(maestro, descripcion):
            errores[maestro] = "Ya existe ese valor"
        else:
            funciones = {
                "tipo_terreno": insertar_tipo_terreno,
                "seccion_tipo": insertar_seccion_tipo,
                "estado_parte": insertar_estado_parte,
                "motivo_exceso": insertar_motivo_exceso
            }
            funcion_error = funciones.get(maestro)
            if funcion_error:
                funcion_error(descripcion)

    if errores:
        maestras = cargar_maestras_admin()
        return render_template("admin.html", errores=errores, **maestras)
    
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