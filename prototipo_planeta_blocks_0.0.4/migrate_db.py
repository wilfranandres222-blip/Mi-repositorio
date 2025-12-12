"""
Script para migrar la base de datos existente
Añade las nuevas columnas usuario_id y foto_perfil
"""

import sqlite3
import os
import random
from datetime import datetime
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'prototipo.db')

def migrate_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar si la columna usuario_id ya existe
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Agregar columnas si no existen (sin UNIQUE constraint al inicio)
        if 'usuario_id' not in columns:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN usuario_id TEXT")
            print("✅ Columna usuario_id añadida")
        
        if 'foto_perfil' not in columns:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN foto_perfil TEXT")
            print("✅ Columna foto_perfil añadida")
        
        # Generar usuario_id para usuarios existentes que no lo tengan
        cursor.execute("SELECT id FROM usuarios WHERE usuario_id IS NULL")
        usuarios_sin_id = cursor.fetchall()
        
        for usuario in usuarios_sin_id:
            usuario_id = f"{random.randint(100000, 999999)}{int(datetime.now().timestamp() * 100) % 10000:04d}"
            cursor.execute("UPDATE usuarios SET usuario_id=? WHERE id=?", (usuario_id, usuario[0]))
            print(f"✅ Usuario ID generado: {usuario_id}")
        
        # Crear tabla de blogs si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                categoria TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        print("✅ Tabla blogs creada/verificada")
        
        conn.commit()
        conn.close()
        print("✅ Migración completada exitosamente")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error durante la migración: {e}")
        return False

if __name__ == '__main__':
    migrate_db()
