from werkzeug.security import generate_password_hash
from db import get_connection

def crear_usuario(usuario, password, rol):
    conn = get_connection()
    cursor = conn.cursor()
    hash = generate_password_hash(password)
    cursor.execute("INSERT INTO Usuario (usuario, password, rol) VALUES (?, ?, ?)", (usuario, hash, rol))
    conn.commit()
    conn.close()

crear_usuario("admin", "Teciman", "admin")
crear_usuario("user1", "1234", "usuario")
crear_usuario("user2", "4321", "usuario")