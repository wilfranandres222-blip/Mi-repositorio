"""
SISTEMA CONSOLIDADO DE GESTIÓN DE PROYECTOS Y USUARIOS
Archivo que integra todos los módulos Python del proyecto
sin modificar funcionalidad ni punto de inicio de cada código.
Versión mejorada con manejo robusto de errores y rutas absolutas.
"""

import os
import shutil
import sqlite3
import re
from pathlib import Path


# ==============================================================================
#  MÓDULO 1.0: AUTENTICACIÓN (INICIO DE SESIÓN)
# ==============================================================================

def crear_tabla_usuarios():
    """Crea la tabla de usuarios si no existe."""
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
    """Carga todos los usuarios desde la base de datos."""
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


def registrar_usuario_db(nombre, documento, correo):
    """Registra un nuevo usuario en la base de datos."""
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, documento, correo) VALUES (?, ?, ?)", 
                   (nombre, documento, correo))
    conn.commit()
    conn.close()


def iniciar_sesion():
    """Inicia sesión validando credenciales del usuario."""
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
        # Descomentar para ejecutar menú de proyectos
        # mostrar_menu()
        return usuario
    else:
        print("Usuario, documento o clave incorrectos.")
        opcion = input("¿Desea registrar este usuario? (s/n): ").strip().lower()
        if opcion == 's':
            registrar_usuario_interfaz()
        return None


# ==============================================================================
#  MÓDULO 1.2: REGISTRO DE USUARIO
# ==============================================================================

def validar_correo(correo):
    """Valida el formato de un correo electrónico."""
    patron = r'^\S+@\S+\.\S+$'
    return re.match(patron, correo)


def usuario_existente(usuario, documento):
    """Verifica si un usuario ya existe en la base de datos."""
    crear_tabla_usuarios()
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nombre=? AND documento=?", (usuario, documento))
    existe = cursor.fetchone()
    conn.close()
    return bool(existe)


def guardar_usuario(usuario, correo, documento, clave):
    """Guarda un nuevo usuario en la base de datos."""
    crear_tabla_usuarios()
    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, documento, correo, clave) VALUES (?, ?, ?, ?)", 
                   (usuario, documento, correo, clave))
    conn.commit()
    conn.close()


def registrar_usuario_interfaz():
    """Interfaz de registro de usuario."""
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


# ==============================================================================
#  MÓDULO 1.3: RECUPERACIÓN DE CONTRASEÑA
# ==============================================================================

def recuperar_contraseña():
    """Permite al usuario recuperar su contraseña."""
    nombre_usuario = input("Ingresa tu nombre de usuario: ").strip().lower()
    correo = input("Ingresa tu correo electrónico: ").strip()
    documento = input("Ingresa tu documento: ").strip().lower()

    conn = sqlite3.connect('prototipo1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE LOWER(nombre)=? AND LOWER(documento)=? AND correo=?", 
                   (nombre_usuario, documento, correo))
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


# ==============================================================================
#  MÓDULO 1.4: ELIMINACIÓN DE USUARIO
# ==============================================================================

def eliminar_usuario():
    """Permite eliminar un usuario y todos sus datos asociados."""
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


# ==============================================================================
#  MÓDULO 2.0: MENÚ PRINCIPAL DE PROYECTOS
# ==============================================================================

def mostrar_menu():
    """Menú principal del sistema de proyectos."""
    while True:
        print("\n📁 MENÚ DE PROYECTOS")
        print("1. Nuevo proyecto")
        print("2. Ver proyectos")
        print("3. Editar proyecto")
        print("4. Eliminar proyecto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            crear_proyecto_interfaz()
        elif opcion == '2':
            ver_proyectos()
        elif opcion == '3':
            editar_proyecto()
        elif opcion == '4':
            eliminar_proyecto_interfaz()
        elif opcion == '5':
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción inválida")


# ==============================================================================
#  MÓDULO 2.1: CREACIÓN DE PROYECTOS
# ==============================================================================

RUTA_PROYECTOS = "Proyectos"


def crear_carpeta_proyecto(nombre):
    """Crea la carpeta principal del proyecto."""
    ruta = os.path.join(RUTA_PROYECTOS, nombre)
    if os.path.exists(ruta):
        return None  # Indica que ya existe
    os.makedirs(ruta)
    return ruta


def guardar_archivo_o_carpeta(ruta_origen, ruta_destino):
    """Guarda un archivo o carpeta completa dentro del proyecto."""
    if not os.path.exists(ruta_origen):
        return False, "Ruta no encontrada"

    nombre = os.path.basename(ruta_origen.rstrip("/\\"))
    destino = os.path.join(ruta_destino, nombre)

    try:
        if os.path.isdir(ruta_origen):
            shutil.copytree(ruta_origen, destino)
            return True, f"📂 Carpeta añadida: {nombre}"
        else:
            shutil.copy(ruta_origen, ruta_destino)
            return True, f"📄 Archivo añadido: {nombre}"
    except FileExistsError:
        return False, f"Error: {nombre} ya existe en el destino."
    except shutil.Error as e:
        return False, f"Error copiando elemento: {e}"
    except OSError as e:
        return False, f"Error del sistema: {e}"


def crear_proyecto_interfaz():
    """Interfaz de creación de nuevo proyecto."""
    print("\n📁 CREACIÓN DE NUEVO PROYECTO\n")

    nombre = input("Ingrese el nombre del proyecto: ").strip()

    ruta_proyecto = crear_carpeta_proyecto(nombre)

    if ruta_proyecto is None:
        print("⚠ Ya existe un proyecto con ese nombre.")
        return

    print(f"✔ Proyecto '{nombre}' creado.\n")

    print("📤 Pegue rutas de archivos o carpetas. Escriba 'fin' para terminar.\n")

    while True:
        ruta = input("Ruta del archivo/carpeta: ").strip()

        if ruta.lower() == "fin":
            break

        _, msg = guardar_archivo_o_carpeta(ruta, ruta_proyecto)
        print(msg)

    print("\n🎉 Proyecto creado con éxito.")


# ==============================================================================
#  MÓDULO 2.2: VISUALIZACIÓN Y EDICIÓN DE PROYECTOS
# ==============================================================================

def ver_proyectos():
    """Lista todos los proyectos disponibles."""
    print("\n📁 LISTA DE PROYECTOS:\n")

    if not os.path.exists(RUTA_PROYECTOS):
        print("⚠ No existe la carpeta de proyectos.")
        return

    proyectos = os.listdir(RUTA_PROYECTOS)

    if not proyectos:
        print("⚠ No hay proyectos disponibles.")
        return

    for idx, proyecto in enumerate(proyectos, start=1):
        ruta = os.path.join(RUTA_PROYECTOS, proyecto)
        archivos = os.listdir(ruta)
        print(f"{idx}. {proyecto} ({len(archivos)} elementos)")

    print()


def editar_proyecto():
    """Edita el nombre de un proyecto."""
    ver_proyectos()

    nombre = input("Ingrese el nombre del proyecto a editar: ").strip()
    ruta_actual = os.path.join(RUTA_PROYECTOS, nombre)

    if not os.path.exists(ruta_actual):
        print("❌ Ese proyecto no existe.")
        return

    nuevo_nombre = input("Ingrese el nuevo nombre del proyecto: ").strip()
    ruta_nueva = os.path.join(RUTA_PROYECTOS, nuevo_nombre)

    if os.path.exists(ruta_nueva):
        print("⚠ Ya existe otro proyecto con ese nombre.")
        return

    os.rename(ruta_actual, ruta_nueva)
    print(f"✔ Proyecto renombrado a: {nuevo_nombre}")


def descargar_proyecto():
    """Descarga (copia) un proyecto a una ruta destino."""
    ver_proyectos()

    nombre = input("Ingrese el nombre del proyecto a descargar: ").strip()
    ruta_proyecto = os.path.join(RUTA_PROYECTOS, nombre)

    if not os.path.exists(ruta_proyecto):
        print("❌ Ese proyecto no existe.")
        return

    destino = input("Ingrese la ruta donde desea copiar el proyecto: ").strip()

    if not os.path.exists(destino):
        print("❌ El destino no existe.")
        return

    destino_final = os.path.join(destino, nombre)

    try:
        shutil.copytree(ruta_proyecto, destino_final)
        print(f"📥 Proyecto descargado en: {destino_final}")
    except FileExistsError:
        print("❌ Error: Ya existe un proyecto con ese nombre en el destino.")
    except shutil.Error as e:
        print(f"❌ Error al copiar archivos: {e}")
    except OSError as e:
        print(f"❌ Error del sistema: {e}")


# ==============================================================================
#  MÓDULO 2.3: ELIMINACIÓN DE PROYECTOS
# ==============================================================================

def ver_proyectos_para_eliminar():
    """Lista proyectos para seleccionar cuál eliminar."""
    print("\n📁 PROYECTOS DISPONIBLES:\n")

    if not os.path.exists(RUTA_PROYECTOS):
        print("⚠ No existe la carpeta de proyectos.")
        return []

    proyectos = os.listdir(RUTA_PROYECTOS)

    if not proyectos:
        print("⚠ No hay proyectos para eliminar.")
        return []

    for idx, proyecto in enumerate(proyectos, start=1):
        print(f"{idx}. {proyecto}")

    print()
    return proyectos


def eliminar_proyecto_interfaz():
    """Interfaz para eliminar un proyecto."""
    proyectos = ver_proyectos_para_eliminar()

    if not proyectos:
        return

    nombre = input("Ingrese el nombre del proyecto que desea eliminar: ").strip()
    ruta = os.path.join(RUTA_PROYECTOS, nombre)

    if not os.path.exists(ruta):
        print("❌ Ese proyecto no existe.")
        return

    confirmacion = input(f"⚠ Está seguro de eliminar '{nombre}'? (s/n): ").lower()

    if confirmacion == "s":
        try:
            shutil.rmtree(ruta)
            print(f"🗑 Proyecto '{nombre}' eliminado exitosamente.")
        except OSError as e:
            print(f"❌ Error eliminando el proyecto: {e}")
    else:
        print("❌ Eliminación cancelada.")


# ==============================================================================
#  PUNTO DE ENTRADA PRINCIPAL
# ==============================================================================

def main():
    """Función principal que gestiona el flujo del programa."""
    print("=" * 50)
    print("   SISTEMA CONSOLIDADO DE GESTIÓN")
    print("=" * 50)
    
    while True:
        print("\n📌 MENÚ PRINCIPAL")
        print("1. Iniciar sesión")
        print("2. Registrar usuario")
        print("3. Recuperar contraseña")
        print("4. Eliminar usuario")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            usuario = iniciar_sesion()
            if usuario:
                mostrar_menu()
        elif opcion == '2':
            registrar_usuario_interfaz()
        elif opcion == '3':
            recuperar_contraseña()
        elif opcion == '4':
            eliminar_usuario()
        elif opcion == '5':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    main()
