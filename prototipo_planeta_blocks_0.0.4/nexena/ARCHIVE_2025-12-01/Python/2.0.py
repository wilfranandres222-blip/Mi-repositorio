import subprocess
import sys
from pathlib import Path

def mostrar_menu():
    while True:
        print("\n📁 MENÚ DE PROYECTOS")
        print("1. Nuevo proyecto")
        print("2. Ver proyecto")
        print("3. Editar proyecto")
        print("4. Eliminar proyecto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        base_path = Path(__file__).parent
        
        try:
            if opcion == '1':
                subprocess.run([sys.executable, str(base_path / "2.1.py")], check=True)
            elif opcion == '2':
                subprocess.run([sys.executable, str(base_path / "2.2.py")], check=True)
            elif opcion == '3':
                subprocess.run([sys.executable, str(base_path / "2.2.py")], check=True)
            elif opcion == '4':
                subprocess.run([sys.executable, str(base_path / "2.3.py")], check=True)
            elif opcion == '5':
                print("👋 Hasta luego.")
                raise SystemExit
            else:
                print("❌ Opción inválida")
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo del módulo.")
        except subprocess.CalledProcessError:
            print("⚠️ El proceso anterior fue cancelado o generó un error.")

if __name__ == "__main__":
    mostrar_menu()
