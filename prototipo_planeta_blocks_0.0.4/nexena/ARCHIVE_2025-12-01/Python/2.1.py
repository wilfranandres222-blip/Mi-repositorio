import os
import shutil
from pathlib import Path

# ====================================
#  FUNCIONES REUTILIZABLES (BACKEND)
# ====================================

def crear_carpeta_proyectos():
    """Crea la carpeta de proyectos si no existe."""
    ruta = Path("Proyectos")
    ruta.mkdir(exist_ok=True)
    return str(ruta)

def crear_carpeta_proyecto(nombre):
    """Crea la carpeta principal del proyecto."""
    crear_carpeta_proyectos()
    ruta = os.path.join("Proyectos", nombre)
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


# ====================================
#  MODO CONSOLA (TEMPORAL)
# ====================================

def crear_proyecto():
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


if __name__ == "__main__":
    crear_proyecto()
