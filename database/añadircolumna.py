from db import get_connection

conn = get_connection()
cursor = conn.cursor()  
cursor.execute("ALTER TABLE ParteObra ADD COLUMN fecha_edicion_utc DATETIME")
conn.commit()
conn.close()