# ⚡ Guía Rápida - Los Papaspitufos

## Inicio rápido en 3 pasos

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar la aplicación
```bash
python run.py
```

### 3️⃣ Abrir en navegador
```
http://127.0.0.1:5000
```

---

## 🎯 Flujos principales

### Crear una cuenta
1. Haz clic en "Registrarse"
2. Completa: nombre, documento, correo, contraseña
3. Haz clic en "Crear Cuenta"
4. Inicia sesión con tus credenciales

### Iniciar sesión
1. Haz clic en "Iniciar Sesión"
2. Ingresa: nombre de usuario, documento, contraseña
3. Haz clic en "Entrar"

### Recuperar contraseña
1. En la página de login, haz clic en "¿Olvidaste tu contraseña?"
2. Ingresa: nombre de usuario, documento, correo
3. Ingresa tu nueva contraseña
4. Haz clic en "Recuperar Acceso"

### Cambiar contraseña (desde perfil)
1. Inicia sesión
2. Ve a "Perfil"
3. En "Cambiar Contraseña", ingresa tu contraseña actual
4. Ingresa tu nueva contraseña (2 veces)
5. Haz clic en "Actualizar Contraseña"

### Eliminar cuenta
1. Inicia sesión
2. Ve a "Perfil"
3. Haz clic en "Eliminar mi cuenta"
4. Confirma con tu contraseña
5. Escribe "ELIMINAR" para confirmar
6. Haz clic en "Sí, eliminar mi cuenta permanentemente"

---

## 📂 Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `run.py` | Ejecutar la aplicación |
| `app/__init__.py` | Aplicación Flask principal |
| `app/database.py` | Manejo de base de datos |
| `templates/*.html` | Páginas HTML |
| `static/css/*.css` | Estilos CSS |
| `static/js/*.js` | Scripts JavaScript |
| `requirements.txt` | Dependencias Python |

---

## 🔧 Troubleshooting

**Error: puerto en uso**
```bash
# Cambiar puerto en run.py (línea final):
app.run(host='127.0.0.1', port=5001)  # Usar otro puerto
```

**Error: módulo no encontrado**
```bash
pip install flask werkzeug jinja2
```

**Limpiar base de datos**
```bash
# Elimina database/prototipo.db y se recreará
```

---

## 📊 Estructura simplificada

```
prototipo/
├── app/           → Código Python
├── static/        → CSS, JS
├── templates/     → HTML
├── database/      → Base de datos
├── run.py         → Ejecutar aquí
└── README.md      → Documentación completa
```

---

## ✅ Checklist de prueba

- [ ] Crear usuario nuevo
- [ ] Iniciar sesión
- [ ] Ver dashboard
- [ ] Ver perfil
- [ ] Cambiar contraseña
- [ ] Recuperar contraseña
- [ ] Cerrar sesión
- [ ] Eliminar cuenta

---

**Documentación completa:** Ver `README.md`
