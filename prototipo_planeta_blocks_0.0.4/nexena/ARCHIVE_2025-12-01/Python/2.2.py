import os
import shutil
from pathlib import Path

RUTA_PROYECTOS = "Proyectos"

def crear_carpeta_proyectos():
    """Crea la carpeta de proyectos si no existe."""
    ruta = Path(RUTA_PROYECTOS)
    ruta.mkdir(exist_ok=True)
    return str(ruta)

# =====================================================
#  FUNCIÓN: LISTAR PROYECTOS
# =====================================================
def ver_proyectos():
    print("\n📁 LISTA DE PROYECTOS:\n")
    
    crear_carpeta_proyectos()

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


# =====================================================
#  FUNCIÓN: EDITAR NOMBRE DE UN PROYECTO
# =====================================================
def editar_proyecto():
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


# =====================================================
#  FUNCIÓN: DESCARGAR PROYECTO (COPIARLO)
# =====================================================
def descargar_proyecto():
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


# =====================================================
#  MENÚ PRINCIPAL
# =====================================================
def menu():
    while True:
        print("\n📂 GESTOR DE PROYECTOS")
        print("1. Ver proyectos")
        print("2. Editar proyecto")
        print("3. Descargar proyecto")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_proyectos()
        elif opcion == "2":
            editar_proyecto()
        elif opcion == "3":
            descargar_proyecto()
        elif opcion == "4":
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    menu()
