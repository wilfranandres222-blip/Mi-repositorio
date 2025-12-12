"""
Módulo de manejo de base de datos SQLite
Gestiona todas las operaciones de usuarios y autenticación
"""

import sqlite3
import re
import os
from datetime import datetime

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'prototipo.db')


def get_db_connection():
    """Obtiene una conexión a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tabla_usuarios():
    """Crea la tabla de usuarios si no existe."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                documento TEXT UNIQUE NOT NULL,
                correo TEXT UNIQUE,
                clave TEXT NOT NULL,
                foto_perfil TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"❌ Error al crear tabla de usuarios: {e}")
        return False


def crear_tabla_blogs():
    """Crea la tabla de blogs si no existe."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                categoria TEXT,
                completado INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"❌ Error al crear tabla de blogs: {e}")
        return False


def validar_correo(correo):
    """Valida el formato de un correo electrónico."""
    patron = r'^\S+@\S+\.\S+$'
    return re.match(patron, correo) is not None


def usuario_existente(usuario=None, documento=None, correo=None):
    """Verifica si un usuario ya existe en la base de datos."""
    crear_tabla_usuarios()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if usuario and documento:
            cursor.execute(
                "SELECT id FROM usuarios WHERE LOWER(nombre)=? AND documento=?",
                (usuario.lower(), documento)
            )
        elif documento:
            cursor.execute(
                "SELECT id FROM usuarios WHERE documento=?",
                (documento,)
            )
        elif correo:
            cursor.execute(
                "SELECT id FROM usuarios WHERE LOWER(correo)=?",
                (correo.lower(),)
            )
        else:
            conn.close()
            return False
            
        existe = cursor.fetchone()
        conn.close()
        return bool(existe)
    except sqlite3.Error as e:
        print(f"❌ Error al verificar usuario: {e}")
        return False


def guardar_usuario(usuario, correo, documento, clave):
    """Guarda un nuevo usuario en la base de datos."""
    crear_tabla_usuarios()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generar usuario_id único numérico (usando timestamp + random)
        import random
        usuario_id = f"{random.randint(100000, 999999)}{int(datetime.now().timestamp() * 100) % 10000:04d}"
        
        cursor.execute(
            "INSERT INTO usuarios (usuario_id, nombre, documento, correo, clave) VALUES (?, ?, ?, ?, ?)",
            (usuario_id, usuario, documento, correo, clave)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, "✅ Usuario registrado con éxito.", usuario_id, usuario_id
    except sqlite3.IntegrityError as e:
        if 'documento' in str(e).lower():
            return False, "❌ Error: El documento ya existe en la base de datos.", None, None
        elif 'correo' in str(e).lower():
            return False, "❌ Error: El correo ya existe en la base de datos.", None, None
        else:
            return False, f"❌ Error de integridad: {e}", None, None
    except sqlite3.Error as e:
        return False, f"❌ Error al guardar el usuario: {e}", None, None


def verificar_credenciales(usuario, documento, clave):
    """Verifica si las credenciales de un usuario son correctas."""
    crear_tabla_usuarios()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre FROM usuarios WHERE LOWER(nombre)=? AND documento=? AND clave=?",
            (usuario.lower(), documento, clave)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None, resultado
    except sqlite3.Error as e:
        print(f"❌ Error al verificar credenciales: {e}")
        return False, None


def obtener_usuario_por_id(user_id):
    """Obtiene los datos de un usuario por su ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario_id, nombre, documento, correo, foto_perfil FROM usuarios WHERE id=?", (user_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"❌ Error al obtener usuario: {e}")
        return None


def obtener_usuario_por_usuario_id(usuario_id):
    """Obtiene los datos de un usuario por su usuario_id único."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario_id, nombre, documento, correo, foto_perfil FROM usuarios WHERE usuario_id=?", (usuario_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except sqlite3.Error as e:
        print(f"❌ Error al obtener usuario: {e}")
        return None


def actualizar_contraseña(usuario, documento, correo, nueva_clave):
    """Actualiza la contraseña de un usuario."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE LOWER(nombre)=? AND documento=? AND LOWER(correo)=?",
            (usuario.lower(), documento, correo.lower())
        )
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "❌ Usuario, documento o correo incorrecto."
        
        user_id = resultado[0]
        cursor.execute("UPDATE usuarios SET clave=? WHERE id=?", (nueva_clave, user_id))
        conn.commit()
        conn.close()
        return True, "🔐 Contraseña actualizada correctamente."
    except sqlite3.Error as e:
        return False, f"❌ Error al actualizar contraseña: {e}"


def eliminar_usuario(usuario_id, clave_confirmacion):
    """Elimina un usuario de la base de datos."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM usuarios WHERE id=? AND clave=?", (usuario_id, clave_confirmacion))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "❌ Clave incorrecta."
        
        usuario_nombre = resultado[1]
        cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
        conn.commit()
        conn.close()
        return True, f"✅ Usuario '{usuario_nombre}' eliminado correctamente."
    except sqlite3.Error as e:
        return False, f"❌ Error al eliminar usuario: {e}"


def obtener_todos_usuarios():
    """Obtiene la lista de todos los usuarios."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario_id, nombre, documento, correo FROM usuarios ORDER BY nombre")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    except sqlite3.Error as e:
        print(f"❌ Error al obtener usuarios: {e}")
        return []


# ============================================================================
# FUNCIONES DE BLOGS
# ============================================================================

def crear_blog(usuario_id, titulo, contenido, categoria=None):
    """Crea un nuevo blog para un usuario."""
    crear_tabla_blogs()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO blogs (usuario_id, titulo, contenido, categoria) VALUES (?, ?, ?, ?)",
            (usuario_id, titulo, contenido, categoria)
        )
        conn.commit()
        blog_id = cursor.lastrowid
        conn.close()
        return True, "✅ Blog creado correctamente.", blog_id
    except sqlite3.Error as e:
        return False, f"❌ Error al crear blog: {e}", None


def obtener_blogs_usuario(usuario_id):
    """Obtiene todos los blogs de un usuario."""
    crear_tabla_blogs()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, titulo, contenido, categoria, fecha_creacion, completado FROM blogs WHERE usuario_id=? ORDER BY fecha_creacion DESC",
            (usuario_id,)
        )
        blogs = cursor.fetchall()
        conn.close()
        return blogs
    except sqlite3.Error as e:
        print(f"❌ Error al obtener blogs: {e}")
        return []


def obtener_blog_por_id(blog_id):
    """Obtiene un blog específico por su ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, usuario_id, titulo, contenido, categoria, fecha_creacion, fecha_actualizacion, completado FROM blogs WHERE id=?",
            (blog_id,)
        )
        blog = cursor.fetchone()
        conn.close()
        return blog
    except sqlite3.Error as e:
        print(f"❌ Error al obtener blog: {e}")
        return None


def actualizar_blog(blog_id, titulo, contenido, categoria=None):
    """Actualiza un blog existente."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE blogs SET titulo=?, contenido=?, categoria=?, fecha_actualizacion=CURRENT_TIMESTAMP WHERE id=?",
            (titulo, contenido, categoria, blog_id)
        )
        conn.commit()
        conn.close()
        return True, "✅ Blog actualizado correctamente."
    except sqlite3.Error as e:
        return False, f"❌ Error al actualizar blog: {e}"


def eliminar_blog(blog_id):
    """Elimina un blog."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blogs WHERE id=?", (blog_id,))
        conn.commit()
        conn.close()
        return True, "✅ Blog eliminado correctamente."
    except sqlite3.Error as e:
        return False, f"❌ Error al eliminar blog: {e}"


def obtener_blogs_por_categoria(categoria):
    """Obtiene todos los blogs de una categoría específica."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, usuario_id, titulo, contenido, categoria, fecha_creacion, completado FROM blogs WHERE categoria=? ORDER BY fecha_creacion DESC",
            (categoria,)
        )
        blogs = cursor.fetchall()
        conn.close()
        return blogs
    except sqlite3.Error as e:
        print(f"❌ Error al obtener blogs: {e}")
        return []


def actualizar_foto_perfil(usuario_id, ruta_foto):
    """Actualiza la foto de perfil de un usuario."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET foto_perfil=? WHERE id=?", (ruta_foto, usuario_id))
        conn.commit()
        conn.close()
        return True, "✅ Foto de perfil actualizada."
    except sqlite3.Error as e:
        return False, f"❌ Error al actualizar foto: {e}"


# Inicializar base de datos al importar el módulo
crear_tabla_usuarios()
crear_tabla_blogs()


def marcar_completado(blog_id, valor=1):
    """Marca o desmarca un blog como completado (1/0)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE blogs SET completado=? WHERE id=?", (1 if valor else 0, blog_id))
        conn.commit()
        conn.close()
        return True, "✅ Estado de completado actualizado."
    except sqlite3.Error as e:
        return False, f"❌ Error al actualizar completado: {e}"


def obtener_todos_blogs():
    """Obtiene todos los blogs (público)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario_id, titulo, contenido, categoria, fecha_creacion, completado FROM blogs ORDER BY fecha_creacion DESC LIMIT 200")
        blogs = cursor.fetchall()
        conn.close()
        return blogs
    except sqlite3.Error as e:
        print(f"❌ Error al obtener todos los blogs: {e}")
        return []
