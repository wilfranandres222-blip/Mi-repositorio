import sqlite3
import shutil
from pathlib import Path

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

def eliminar_usuario():
    try:
        conn = sqlite3.connect('prototipo1.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, documento FROM usuarios")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("❌ No hay usuarios registrados.")
            conn.close()
            return

        print("\n📋 Lista de usuarios registrados:")
        for i, (uid, nombre, documento) in enumerate(usuarios, start=1):
            print(f"{i}. {nombre} - Documento: {documento}")

        opcion = input("\nSeleccione el número del usuario que desea eliminar: ").strip()
        try:
            opcion = int(opcion)
            if opcion < 1 or opcion > len(usuarios):
                raise ValueError
        except ValueError:
            print("❌ Opción inválida.")
            conn.close()
            return

        uid, nombre, documento = usuarios[opcion-1]
        clave_a_eliminar = input(f"🔑 Ingrese la clave de la cuenta de '{nombre}': ").strip()

        cursor.execute("SELECT id FROM usuarios WHERE id=? AND clave=?", (uid, clave_a_eliminar))
        resultado = cursor.fetchone()
        
        if not resultado:
            print("❌ Clave incorrecta.")
            conn.close()
            return

        # Eliminar aprendices asociados a este usuario
        cursor.execute("DELETE FROM aprendices WHERE usuario_id=?", (uid,))
        # Eliminar usuario
        cursor.execute("DELETE FROM usuarios WHERE id=?", (uid,))
        conn.commit()
        conn.close()
        
        print(f"✅ Usuario '{nombre}' y todos sus datos asociados eliminados del sistema.")

        # Eliminar la carpeta del usuario y todo su contenido
        ruta_carpeta_usuario = Path("Usuarios") / nombre
        if ruta_carpeta_usuario.exists() and ruta_carpeta_usuario.is_dir():
            shutil.rmtree(ruta_carpeta_usuario)
            print(f"🗑️ Carpeta del usuario '{nombre}' eliminada correctamente.")
        else:
            print("⚠️ No se encontró carpeta personal del usuario.")

        # Eliminar la carpeta de platos si existe
        ruta_platos = Path("Usuarios") / nombre / "Platos"
        if ruta_platos.exists() and ruta_platos.is_dir():
            shutil.rmtree(ruta_platos)
            print(f"🗑️ Carpeta de platos de '{nombre}' eliminada correctamente.")
    except sqlite3.Error as e:
        print(f"❌ Error al acceder a la base de datos: {e}")

if __name__ == "__main__":
    crear_tabla_usuarios()
    eliminar_usuario()
