#!/bin/sh

echo "Inicializando base de datos..."
python database/init_db.py
python database/inserciondatos.py
python database/insertar_partes.py
python database/insertar_usuarios.py

echo "Arrancando aplicación..."
python app.py