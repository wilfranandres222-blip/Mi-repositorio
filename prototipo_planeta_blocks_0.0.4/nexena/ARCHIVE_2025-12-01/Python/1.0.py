import subprocess
import sys
from pathlib import Path

def mostrar_menu():
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Recuperar contraseña")
        print("4. Eliminar cuenta")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        base_path = Path(__file__).parent
        
        try:
            if opcion == '1':
                subprocess.run([sys.executable, str(base_path / "1.1.py")], check=True)
            elif opcion == '2':
                subprocess.run([sys.executable, str(base_path / "1.2.py")], check=True)
            elif opcion == '3':
                subprocess.run([sys.executable, str(base_path / "1.3.py")], check=True)
            elif opcion == '4':
                subprocess.run([sys.executable, str(base_path / "1.4.py")], check=True)
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
