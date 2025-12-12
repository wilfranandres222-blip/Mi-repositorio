import sqlite3
import subprocess

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

def cargar_usuarios_db():
    crear_tabla_usuarios()
    try:
        conn = sqlite3.connect('prototipo1.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, documento, clave FROM usuarios")
        usuarios = {(row[0].strip().lower(), row[1].strip(), row[2]) for row in cursor.fetchall()}
        conn.close()
        return usuarios
    except sqlite3.Error as e:
        print(f"❌ Error al acceder a la base de datos: {e}")
        return set()

def registrar_usuario(nombre, documento, correo):
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, documento, correo) VALUES (?, ?, ?)", (nombre, documento, correo))
    conn.commit()
    conn.close()

def iniciar_sesion():
    crear_tabla_usuarios()
    usuarios = cargar_usuarios_db()
    usuario = input("Ingrese su nombre de usuario: ").strip().lower()
    documento = input("Ingrese su documento: ").strip()
    clave = input("Ingrese su contraseña: ").strip()

    encontrado = False
    for u, d, c in usuarios:
        if (usuario, documento) == (u, d) and clave == c:
            encontrado = True
            break
    if encontrado:
        print(f"Bienvenido, {usuario}")
        subprocess.run(["python", "Python/2.0.py"], check=False)
    else:
        print("Usuario, documento o clave incorrectos.")
        opcion = input("¿Desea registrar este usuario? (s/n): ").strip().lower()
        if opcion == 's':
            subprocess.run(["python", "Python/1.2.py"], check=False)

if __name__ == '__main__':
    iniciar_sesion()