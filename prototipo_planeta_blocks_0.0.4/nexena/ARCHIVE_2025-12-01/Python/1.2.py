import sqlite3
import re

def crear_tabla_usuarios():
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT UNIQUE NOT NULL,
            correo TEXT,
            clave TEXT
        )
    ''')
    conn.commit()
    conn.close()

def validar_correo(correo):
    patron = r'^\S+@\S+\.\S+$'
    return re.match(patron, correo)

def usuario_existente(usuario, documento):
    crear_tabla_usuarios()
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nombre=? AND documento=?", (usuario, documento))
    existe = cursor.fetchone()
    conn.close()
    return bool(existe)

def guardar_usuario(usuario, correo, documento, clave):
    crear_tabla_usuarios()
    try:
        conn = sqlite3.connect('prototipo1.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, documento, correo, clave) VALUES (?, ?, ?, ?)", (usuario, documento, correo, clave))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        print("❌ Error: El documento ya existe en la base de datos.")
    except sqlite3.Error as e:
        print(f"❌ Error al guardar el usuario: {e}")

def registrar_usuario():
    crear_tabla_usuarios()
    print("=== Registro de Usuario ===")
    usuario = input("Nombre de usuario: ").strip()
    correo = input("Ingrese su correo electrónico: ").strip()
    documento = input("Documento de identidad: ").strip()
    contraseña = input("Contraseña: ").strip()
    confirmar = input("Confirmar contraseña: ").strip()

    if contraseña != confirmar:
        print("❌ Las contraseñas no coinciden.")
        return
    
    if usuario_existente(usuario, documento):
        print("⚠️ El usuario y documento ya existen. Intenta otro.")
        return
    
    guardar_usuario(usuario, correo, documento, contraseña)
    print("✅ Usuario registrado con éxito.")

if __name__ == "__main__":
    registrar_usuario()
