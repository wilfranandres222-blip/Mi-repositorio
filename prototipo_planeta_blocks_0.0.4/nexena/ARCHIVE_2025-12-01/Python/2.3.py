import os
import shutil
from pathlib import Path

RUTA_PROYECTOS = "Proyectos"

def crear_carpeta_proyectos():
    """Crea la carpeta de proyectos si no existe."""
    ruta = Path(RUTA_PROYECTOS)
    ruta.mkdir(exist_ok=True)
    return str(ruta)

def ver_proyectos():
    print("\n📁 PROYECTOS DISPONIBLES:\n")
    
    crear_carpeta_proyectos()

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


def eliminar_proyecto():
    proyectos = ver_proyectos()

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


if __name__ == "__main__":
    eliminar_proyecto()
