import sqlite3

conn = sqlite3.connect("database/teciman.db")
cursor = conn.cursor()
if cursor.execute("SELECT COUNT(*) FROM Personal").fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO Personal (nombre, apellido1, apellido2, telefono, email, activo) VALUES (?, ?, ?, ?, ?, ?)", [
        ("Juan", "Pérez", "Gómez", "123456789", "juan@example.com", 1),
        ("Marta", "López", "Martínez", "987654321", "marta@example.com", 1),
        ("Miguel", "Sánchez", "Rodríguez", "456789123", "miguel@example.com", 1),
        ("Eusebio", "García", "Fernández", "789123456", "eusebio@example.com", 1),
        ])

if cursor.execute("SELECT COUNT(*) FROM TipoTerreno").fetchone()[0] == 0:
    cursor.executemany("INSERT INTO TipoTerreno (descripcion) VALUES (?)", [
        ("Arcilloso",),
        ("Hormigón",),
        ("Arena",),
    ])  

if cursor.execute("SELECT COUNT(*) FROM SeccionTipo").fetchone()[0] == 0:
    cursor.executemany("INSERT INTO SeccionTipo (descripcion) VALUES (?)", [
        ("Seccion A",),
        ("Seccion B",),
        ("Seccion C",),
    ])

if cursor.execute("SELECT COUNT(*) FROM MotivoExcesoHoras").fetchone()[0] == 0:
    cursor.executemany("INSERT INTO MotivoExcesoHoras (descripcion) VALUES (?)", [
        ("Avería",),
        ("Mal tiempo",),
        ("Tráfico",),
    ])

if cursor.execute("SELECT COUNT(*) FROM EstadoParte").fetchone()[0] == 0:
    cursor.executemany("INSERT INTO EstadoParte (descripcion) VALUES (?)", [
        ("Activo",),
        ("Cerrado",),
        ("En curso",),
    ])

conn.commit()
conn.close()
print("Datos de ejemplo insertados correctamente.")
