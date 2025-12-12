import sqlite3

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

def recuperar_contraseña():
    nombre_usuario = input("Ingresa tu nombre de usuario: ").strip().lower()
    correo = input("Ingresa tu correo electrónico: ").strip()
    documento = input("Ingresa tu documento: ").strip().lower()

    try:
        conn = sqlite3.connect('prototipo1.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE LOWER(nombre)=? AND LOWER(documento)=? AND correo=?", (nombre_usuario, documento, correo))
        resultado = cursor.fetchone()

        if resultado:
            print("✅ Usuario encontrado.")
            nueva_contraseña = input("Ingresa tu nueva contraseña (mínimo 6 caracteres): ").strip()
            if len(nueva_contraseña) < 6:
                print("❌ La contraseña debe tener al menos 6 caracteres.")
                conn.close()
                return
            cursor.execute("UPDATE usuarios SET clave=? WHERE id=?", (nueva_contraseña, resultado[0]))
            conn.commit()
            print("🔐 Contraseña actualizada correctamente.")
        else:
            print("❌ Usuario, documento o correo incorrecto.")
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Error al acceder a la base de datos: {e}")

if __name__ == '__main__':
    crear_tabla_usuarios()
    recuperar_contraseña()
