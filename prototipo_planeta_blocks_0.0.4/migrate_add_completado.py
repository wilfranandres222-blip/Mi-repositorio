import sqlite3
import os
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'prototipo.db')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if column exists
cur.execute("PRAGMA table_info(blogs);")
cols = [r[1] for r in cur.fetchall()]

if 'completado' in cols:
    print('La columna completado ya existe. No se requiere migración.')
else:
    try:
        cur.execute("ALTER TABLE blogs ADD COLUMN completado INTEGER DEFAULT 0;")
        conn.commit()
        print('Columna completado añadida con éxito.')
    except Exception as e:
        print('Error al añadir la columna completado:', e)

conn.close()
