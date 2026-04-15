from routes.parte_obra_routes import parte_bp
from routes.admin_routes import admin_bp
from flask import Flask
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(parte_bp)
app.register_blueprint(admin_bp)

def convertir_metros(valor):
    if valor is None:
        return '000'
    return str(valor).zfill(3)

def formatear_fecha(fecha):
    if not fecha:
        return '-'
    if len(fecha) > 10:
        fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        return fecha.strftime("%d-%m-%Y %H:%M")
    else:
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        return fecha.strftime("%d-%m-%Y")

app.jinja_env.filters['metros'] = convertir_metros
app.jinja_env.filters['fecha'] = formatear_fecha


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
