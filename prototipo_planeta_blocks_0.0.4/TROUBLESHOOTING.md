# 🔧 Solución de Problemas - Los Papaspitufos

## Errores comunes y soluciones

### 1. Error: "ModuleNotFoundError: No module named 'flask'"

**Síntomas:**
```
ModuleNotFoundError: No module named 'flask'
```

**Causas:**
- Flask no está instalado
- Estás usando el entorno virtual incorrecto

**Soluciones:**

Opción A: Instalar Flask
```bash
pip install flask
```

Opción B: Instalar todas las dependencias
```bash
pip install -r requirements.txt
```

Opción C: Si usas entorno virtual, activarlo primero
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

### 2. Error: "Port 5000 already in use"

**Síntomas:**
```
OSError: [WinError 10048] Only one usage of each socket address
Address already in use
```

**Causas:**
- La aplicación ya está corriendo en ese puerto
- Otro programa usa el puerto 5000

**Soluciones:**

Opción A: Cambiar el puerto
Edita `run.py` (última línea):
```python
app.run(host='127.0.0.1', port=5001)  # Cambiar 5000 por otro número
```

Opción B: Terminar proceso en puerto 5000 (Windows)
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Opción C: Terminar proceso en puerto 5000 (macOS/Linux)
```bash
lsof -i :5000
kill -9 <PID>
```

---

### 3. Error: "Template not found"

**Síntomas:**
```
jinja2.exceptions.TemplateNotFoundError: index.html
```

**Causas:**
- Los archivos HTML no están en la carpeta `templates/`
- El nombre del archivo no coincide

**Soluciones:**

Verifica la estructura:
```
prototipo_planeta_blocks_0.0.3/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── ... (otros archivos HTML)
```

Si faltan archivos, cópialos a la carpeta correcta.

---

### 4. Error: "Database locked"

**Síntomas:**
```
sqlite3.OperationalError: database is locked
```

**Causas:**
- Múltiples instancias de la app accediendo a la BD
- Archivo de BD corrupto

**Soluciones:**

Opción A: Cerrar todas las instancias de la app (presiona Ctrl+C)

Opción B: Eliminar y recrear la base de datos
```bash
# Elimina el archivo
del database/prototipo.db

# Reinicia la app
python run.py
# Se recreará automáticamente
```

---

### 5. Error: "No such table: usuarios"

**Síntomas:**
```
sqlite3.OperationalError: no such table: usuarios
```

**Causas:**
- La tabla no se creó correctamente
- Base de datos corrompida

**Soluciones:**

Opción A: Reinicia la app
```bash
# Presiona Ctrl+C
python run.py
# Se recreará la tabla automáticamente
```

Opción B: Elimina y recrea la BD
```bash
del database/prototipo.db
python run.py
```

---

### 6. Error: "Form submission failed"

**Síntomas:**
- El formulario no envía datos
- Aparece error en consola

**Causas:**
- JavaScript no funciona correctamente
- Hay error en la validación

**Soluciones:**

Opción A: Abre la consola del navegador (F12)
```
- Busca errores en la pestaña "Console"
- Mira la pestaña "Network" para ver si llegan las peticiones
```

Opción B: Verifica que los IDs de elementos coincidan
```html
<!-- En el HTML -->
<input id="usuario" name="usuario">

<!-- En el JavaScript -->
document.getElementById('usuario')  // Debe existir
```

---

### 7. Error: "CSRF token missing"

**Síntomas:**
```
Error: CSRF token missing
```

**Causas:**
- No hay protección CSRF configurada (normal en desarrollo)

**Soluciones:**
No es un error crítico en desarrollo. Para producción, implementar:
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

---

### 8. Las contraseñas no coinciden en registro

**Síntomas:**
- El campo de confirmación de contraseña marca error
- Dice "Las contraseñas no coinciden"

**Causas:**
- Los valores de los dos campos de contraseña son diferentes
- Hay espacios extra

**Soluciones:**
- Verifica que escribas la contraseña exactamente igual en ambos campos
- No incluyas espacios al principio o final
- Asegúrate que Caps Lock no esté activado

---

### 9. No puedo iniciar sesión con la cuenta creada

**Síntomas:**
- Aparece "Usuario, documento o contraseña incorrectos"
- Aunque acabas de registrarte

**Causas:**
- La contraseña no se guardó correctamente
- Hay diferencia en mayúsculas/minúsculas en el usuario
- El documento no coincide

**Soluciones:**

Opción A: Crea una nueva cuenta
```bash
1. Ve a /register
2. Crea una cuenta con datos simples
3. Intenta iniciar sesión inmediatamente
```

Opción B: Verifica la base de datos
```bash
# Abre la BD con un gestor SQLite
# Verifica que el usuario está en la tabla usuarios
```

---

### 10. La página se ve deformada en móvil

**Síntomas:**
- El CSS no se ve correcto en teléfono
- Textos muy grandes o muy pequeños
- Elementos se salen de la pantalla

**Causas:**
- Navegador no cargó el CSS completamente
- Zoom del navegador

**Soluciones:**

Opción A: Actualizar página (Ctrl+Shift+R)
```
Ctrl+Shift+R (limpia caché y recarga)
```

Opción B: Verificar zoom
```
Ctrl+0 (resetea zoom a 100%)
```

Opción C: Abrir en navegador diferente
```
Prueba con Chrome, Firefox o Edge
```

---

## 🐛 Checklist de debugging

- [ ] ¿Está activo el entorno virtual?
- [ ] ¿Se instalaron las dependencias? (`pip install -r requirements.txt`)
- [ ] ¿Está corriendo el servidor? (`python run.py`)
- [ ] ¿Abriste la URL correcta? (`http://127.0.0.1:5000`)
- [ ] ¿Revisaste la consola del navegador? (F12)
- [ ] ¿Revisaste los logs del servidor?
- [ ] ¿Limpiaste caché del navegador?
- [ ] ¿Probaste en navegador diferente?

---

## 📋 Información útil

### Acceder a la consola de Python
```bash
python
>>> import sqlite3
>>> conn = sqlite3.connect('database/prototipo.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT * FROM usuarios")
>>> for row in cursor.fetchall():
...     print(row)
```

### Ver logs del servidor
Los logs aparecen automáticamente en la terminal cuando ejecutas:
```bash
python run.py
```

### Modo debug
Para ver más detalles en modo debug:
```python
# En app/__init__.py
app.run(debug=True)  # Ya está habilitado por defecto
```

---

## 💡 Tips útiles

1. **Mantén la consola del navegador abierta (F12)** - Te mostrará errores JavaScript
2. **Revisa los logs del servidor** - Te dirá qué está pasando en Python
3. **Usa validación en tiempo real** - Los campos cambiam de color si hay error
4. **Prueba con datos simples** - Usuarios sin caracteres especiales
5. **Reinicia el servidor** - A veces soluciona problemas extraños

---

## 🆘 Si nada funciona

1. Elimina la carpeta `database/` completamente
2. Elimina la carpeta `venv/` (entorno virtual)
3. Ejecuta:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python run.py
   ```
4. Si aún no funciona, verifica que Python 3.7+ esté instalado:
   ```bash
   python --version
   ```

---

**Última actualización:** Diciembre 2025  
**¿Problema no está aquí?** Revisa los logs y la consola del navegador.
