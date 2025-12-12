# API de Autenticación - `1.0.py`

## Descripción
API REST pura (solo JSON) sin HTML/CSS embebido **y sin base de datos**. 
- Usa **datos en memoria** (diccionarios Python)
- Todos los datos se pierden al reiniciar la app
- Ideal para prototipos, pruebas y desarrollo

## Instalación

```powershell
# Sitúate en la carpeta del script
cd 'c:\Users\USUARIO\OneDrive\Desktop\Nexena\nexena\ARCHIVE_2025-12-01\Python'

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app
py -3 1.0.py
```

## Endpoints

| Método | Ruta | Descripción | Auth | Body |
|--------|------|-------------|------|------|
| GET | `/api/health` | Health check | No | - |
| POST | `/api/auth/register` | Registrar usuario | No | `{username, email, password}` |
| POST | `/api/auth/login` | Iniciar sesión | No | `{username, password}` |
| POST | `/api/auth/logout` | Cerrar sesión | Sí | - |
| GET | `/api/auth/me` | Obtener usuario actual | Sí | - |
| POST | `/api/auth/forgot-username` | Recuperar usuario por email | No | `{email}` |
| POST | `/api/auth/forgot-password` | Generar token de reset | No | `{username}` |
| POST | `/api/auth/reset-password` | Restablecer contraseña | No | `{reset_token, new_password}` |
| POST | `/api/auth/change-password` | Cambiar contraseña (autenticado) | Sí | `{old_password, new_password}` |
| GET | `/api/users` | Listar usuarios (demo) | No | - |

## Ejemplo de Uso (PowerShell)

```powershell
# Health check
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/health" -Method Get
$response

# Login
$loginBody = @{username = "demo"; password = "Password123"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" -Method Post `
  -Body $loginBody -ContentType "application/json"
$response

# Registrar usuario
$registerBody = @{username = "newuser"; email = "new@example.com"; password = "Test1234"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method Post `
  -Body $registerBody -ContentType "application/json"
$response
```

## Usuario Demo
- **Username**: `demo`
- **Email**: `demo@example.com`
- **Password**: `Password123`

## Características
- ✅ Sin SQLite, sin base de datos (datos en memoria)
- ✅ Solo Python (Flask + Werkzeug)
- ✅ API REST JSON pura
- ✅ Validación de contraseñas hasheadas
- ✅ Gestión de sesiones
- ✅ Tokens para reset de contraseña
- ✅ Decorador `@require_login` para endpoints protegidos

## Notas
- Los datos se pierden al reiniciar la app.
- Ideal para demostración y prototipado rápido.
- Las contraseñas se hashean con `Werkzeug` para mayor seguridad.
- Ejecuta `test_api.ps1` para probar todos los endpoints automáticamente.

