#!/usr/bin/env python3
"""
RUN.PY - Planeta de Blogs
Archivo principal para ejecutar la aplicación Flask
Uso: python run.py
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║           🪐 PLANETA DE BLOGS 🪐                    ║
    ║                                                        ║
    ║  Iniciando servidor Flask...                          ║
    ║  🌐 http://127.0.0.1:5000                            ║
    ║  📊 Debug: True                                       ║
    ║                                                        ║
    ║  Presiona CTRL+C para detener el servidor             ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Crear base de datos si no existe
    from app.database import crear_tabla_usuarios
    crear_tabla_usuarios()
    
    # Ejecutar la aplicación
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )
