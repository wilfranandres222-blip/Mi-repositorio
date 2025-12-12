# 🪐 Los Papaspitufos - Planeta de Blogs

Una aplicación web moderna y completamente integrada para compartir blogs y contenido.

## 📋 Características

✅ **Autenticación completa**
- Login con usuario/documento/contraseña
- Registro de nuevos usuarios
- Recuperación de contraseña
- Eliminación de cuenta

✅ **Dashboard personal**
- Panel de control para usuarios autenticados
- Crear y publicar blogs
- Gestionar contenido personal

✅ **Perfil de usuario**
- Ver información personal
- Cambiar contraseña
- Configuración de cuenta

✅ **Diseño responsivo**
- Compatible con dispositivos móviles, tablets y desktop
- Interfaz moderna y amigable
- Animaciones y transiciones suaves

✅ **Seguridad**
- Base de datos SQLite integrada
- Validación de entrada en cliente y servidor
- Sesiones seguras
- Protección contra XSS

## 🚀 Instalación y Configuración

### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd prototipo_planeta_blocks_0.0.3
   ```

2. **Crear un entorno virtual (recomendado)**
   
   En Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   En macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

5. **Acceder a la aplicación**
   - Abre tu navegador web
   - Ve a: `http://127.0.0.1:5000`

## 📁 Estructura del Proyecto

```
prototipo_planeta_blocks_0.0.3/
├── app/
│   ├── __init__.py              # Aplicación Flask principal
│   └── database.py              # Módulo de base de datos
├── static/
│   ├── css/
│   │   ├── styles.css           # Estilos globales
│   │   ├── auth.css             # Estilos de autenticación
│   │   ├── dashboard.css        # Estilos del dashboard
│   │   ├── perfil.css           # Estilos del perfil
│   │   ├── index.css            # Estilos de página de inicio
│   │   └── error.css            # Estilos de páginas de error
│   └── js/
│       ├── main.js              # Scripts de página de inicio
│       ├── auth.js              # Scripts de autenticación
│       ├── dashboard.js         # Scripts del dashboard
│       └── perfil.js            # Scripts del perfil
├── templates/
│   ├── index.html               # Página de inicio
│   ├── login.html               # Página de login
│   ├── register.html            # Página de registro
│   ├── recuperar_contraseña.html # Recuperación de contraseña
│   ├── dashboard.html           # Dashboard
│   ├── perfil.html              # Perfil de usuario
│   └── error.html               # Página de errores
├── database/
│   └── prototipo.db             # Base de datos SQLite (creada automáticamente)
├── run.py                       # Archivo para ejecutar la app
├── requirements.txt             # Dependencias Python
└── README.md                    # Este archivo
```

## 🔐 Credenciales de Prueba

Por ahora, debes crear una nueva cuenta. El sistema de prueba se habilitará próximamente.

### Crear una cuenta de prueba:

1. Haz clic en "Registrarse" en la página de inicio
2. Completa el formulario:
   - **Nombre de usuario:** tuusuario
   - **Documento:** 123456789
   - **Correo:** tu@email.com
   - **Contraseña:** 123456

3. Inicia sesión con tus credenciales

## 🗂️ Rutas Disponibles

### Páginas públicas
- `/` - Página de inicio
- `/login` - Iniciar sesión
- `/register` - Crear cuenta
- `/recuperar-contraseña` - Recuperar acceso

### Páginas protegidas (requieren login)
- `/dashboard` - Panel principal
- `/perfil` - Perfil de usuario
- `/logout` - Cerrar sesión

### API endpoints
- `GET /api/usuarios` - Lista de usuarios
- `GET /api/usuario/<id>` - Datos de usuario específico
- `POST /api/validar-correo` - Validar disponibilidad de correo
- `POST /api/validar-documento` - Validar disponibilidad de documento

## 🎨 Colores y Diseño

**Colores principales:**
- Azul primario: #0d47a1
- Azul secundario: #9bc9ff
- Verde (éxito): #27ae60
- Rojo (error): #e74c3c
- Oscuro: #022b59
- Claro: #e9f3ff

## 🔧 Configuración

### Cambiar puerto
Edita `run.py` y modifica el puerto en la última línea:
```python
app.run(host='127.0.0.1', port=5000)  # Cambiar 5000 por otro puerto
```

### Cambiar clave de sesión
En `app/__init__.py`, cambia:
```python
app.secret_key = 'tu_clave_secreta_segura_aqui_2025'
```

## 📚 Módulos Python Integradores

La aplicación integra las siguientes funcionalidades de los módulos originales:

- **Autenticación (1.1.py):** Login con validación de credenciales
- **Registro (1.2.py):** Registro de nuevos usuarios con validación
- **Recuperación (1.3.py):** Cambio de contraseña con verificación
- **Eliminación (1.4.py):** Eliminación segura de cuenta
- **Menú (1.0.py):** Interfaz integrada en web

## ⚠️ Notas Importantes

1. **Base de datos:** La base de datos SQLite se crea automáticamente en `database/prototipo.db`
2. **Sesiones:** Las sesiones duran 24 horas
3. **Contraseñas:** Se guardan en texto plano (para demo). En producción, usar hash bcrypt
4. **HTTPS:** Usar en producción con protocolo HTTPS seguro

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Port 5000 already in use"
**Solución:** Cambia el puerto en `run.py` o detén el proceso en puerto 5000

### Error: "Base de datos bloqueada"
**Solución:** Cierra todas las instancias de la app y elimina el archivo `.db`

## 📞 Soporte

Para reportar bugs o sugerencias, por favor contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto es de código cerrado. Todos los derechos reservados.

---

**Versión:** 0.0.3  
**Última actualización:** Diciembre 2025  
**Estado:** En desarrollo 🚧
