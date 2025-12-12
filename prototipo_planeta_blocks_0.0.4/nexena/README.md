Planeta de Blocs

Proyecto mínimo con Flask que expone una API y una página principal.

Instalación (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ejecutar la app:

```powershell
python app.py
```

Rutas útiles:
- `/` : Interfaz principal (servida desde `templates/index.html`).
- `/api/planet` : Devuelve JSON con la información del planeta.

Notas:
- `app.py` inicializa `database.db` si está vacío y crea una fila de ejemplo.
- Puedes reemplazar `templates/index.html` y `static/style.css` con tu propio diseño.
