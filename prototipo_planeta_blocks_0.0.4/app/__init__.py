"""
APLICACIÓN FLASK INTEGRADA - Planeta de Blogs
Integra autenticación, registro, y gestión de usuarios
Versión mejorada y completamente funcional
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from datetime import datetime, timedelta
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from app.database import (
    crear_tabla_usuarios,
    validar_correo,
    usuario_existente,
    guardar_usuario,
    verificar_credenciales,
    obtener_usuario_por_id,
    obtener_usuario_por_usuario_id,
    actualizar_contraseña,
    eliminar_usuario,
    obtener_todos_usuarios,
    crear_blog,
    obtener_blogs_usuario,
    obtener_blog_por_id,
    actualizar_blog,
    obtener_blogs_por_categoria,
    marcar_completado,
    obtener_todos_blogs,
    actualizar_foto_perfil
)
from app.database import eliminar_blog

# Configuración de Flask
# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).parent.parent
app = Flask(__name__, 
            static_folder=str(BASE_DIR / 'static'), 
            template_folder=str(BASE_DIR / 'templates'))
app.secret_key = 'tu_clave_secreta_segura_aqui_2025'  # Cambiar en producción
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Decorador para requerir login
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            # Si la petición es AJAX/JSON, devolver 401 JSON en lugar de redirigir
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'mensaje': 'Autenticación requerida.'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================================

@app.route('/')
def index():
    """Página de inicio."""
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión."""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        usuario = data.get('usuario', '').strip()
        documento = data.get('documento', '').strip()
        clave = data.get('clave', '').strip()
        
        if not all([usuario, documento, clave]):
            return jsonify({'success': False, 'mensaje': '❌ Complete todos los campos.'}), 400
        
        existe, usuario_data = verificar_credenciales(usuario, documento, clave)
        
        if existe:
            session.permanent = True
            session['usuario_id'] = usuario_data['id']
            session['usuario_nombre'] = usuario_data['nombre']
            
            if request.is_json:
                return jsonify({'success': True, 'mensaje': '✅ Sesión iniciada correctamente.'})
            return redirect(url_for('dashboard'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'mensaje': '❌ Usuario, documento o contraseña incorrectos.'}), 401
            return render_template('login.html', error='Usuario, documento o contraseña incorrectos.')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuario."""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        usuario = data.get('nombre', '').strip()
        correo = data.get('correo', '').strip()
        documento = data.get('documento', '').strip()
        clave = data.get('clave', '').strip()
        confirmar_clave = data.get('confirmar_clave', '').strip()
        
        # Validaciones
        if not all([usuario, correo, documento, clave]):
            mensaje = '❌ Complete todos los campos.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
        
        if clave != confirmar_clave:
            mensaje = '❌ Las contraseñas no coinciden.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
        
        if len(clave) < 6:
            mensaje = '❌ La contraseña debe tener al menos 6 caracteres.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
        
        if not validar_correo(correo):
            mensaje = '❌ Correo electrónico inválido.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
        
        if usuario_existente(usuario=usuario, documento=documento):
            mensaje = '⚠️ El usuario y documento ya existen. Intenta otro.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
        
        if usuario_existente(correo=correo):
            mensaje = '⚠️ El correo ya está registrado.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
        
        # Guardar usuario
        exito, mensaje, _usuario_id, user_id_str = guardar_usuario(usuario, correo, documento, clave)
        if exito:
            if request.is_json:
                return jsonify({'success': True, 'mensaje': mensaje, 'usuario_id': user_id_str})
            return render_template('login.html', exito='Usuario registrado. Inicia sesión.')
        else:
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('register.html', error=mensaje)
    
    return render_template('register.html')


@app.route('/recuperar-contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    """Página para recuperar contraseña."""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        usuario = data.get('usuario', '').strip()
        documento = data.get('documento', '').strip()
        correo = data.get('correo', '').strip()
        nueva_clave = data.get('nueva_clave', '').strip()
        confirmar_clave = data.get('confirmar_clave', '').strip()
        
        if not all([usuario, documento, correo, nueva_clave]):
            mensaje = '❌ Complete todos los campos.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('recuperar_contraseña.html', error=mensaje)
        
        if nueva_clave != confirmar_clave:
            mensaje = '❌ Las contraseñas no coinciden.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('recuperar_contraseña.html', error=mensaje)
        
        if len(nueva_clave) < 6:
            mensaje = '❌ La contraseña debe tener al menos 6 caracteres.'
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('recuperar_contraseña.html', error=mensaje)
        
        exito, mensaje = actualizar_contraseña(usuario, documento, correo, nueva_clave)
        if exito:
            if request.is_json:
                return jsonify({'success': True, 'mensaje': mensaje})
            return render_template('login.html', exito='Contraseña actualizada. Inicia sesión.')
        else:
            if request.is_json:
                return jsonify({'success': False, 'mensaje': mensaje}), 400
            return render_template('recuperar_contraseña.html', error=mensaje)
    
    return render_template('recuperar_contraseña.html')


@app.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    session.clear()
    return redirect(url_for('index'))


# ============================================================================
# RUTAS DE DASHBOARD Y USUARIO
# ============================================================================

@app.route('/dashboard')
@login_requerido
def dashboard():
    """Panel principal del usuario autenticado."""
    usuario = obtener_usuario_por_id(session['usuario_id'])
    return render_template('dashboard.html', usuario=usuario)


@app.route('/perfil')
@login_requerido
def perfil():
    """Página de perfil de usuario."""
    usuario = obtener_usuario_por_id(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)


@app.route('/eliminar-cuenta', methods=['POST'])
@login_requerido
def eliminar_cuenta():
    """Elimina la cuenta del usuario autenticado."""
    data = request.get_json() if request.is_json else request.form
    clave = data.get('clave', '').strip()
    
    if not clave:
        return jsonify({'success': False, 'mensaje': '❌ Ingrese su contraseña.'}), 400
    
    exito, mensaje = eliminar_usuario(session['usuario_id'], clave)
    if exito:
        session.clear()
        return jsonify({'success': True, 'mensaje': mensaje, 'redirect': url_for('index')})
    else:
        return jsonify({'success': False, 'mensaje': mensaje}), 400


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/usuarios', methods=['GET'])
def api_usuarios():
    """Obtiene la lista de todos los usuarios (solo para desarrolladores)."""
    usuarios = obtener_todos_usuarios()
    return jsonify([dict(u) for u in usuarios])


@app.route('/api/usuario/<int:user_id>', methods=['GET'])
@login_requerido
def api_usuario(user_id):
    """Obtiene los datos de un usuario específico."""
    if session['usuario_id'] != user_id:
        return jsonify({'error': 'No tienes permiso para acceder a este usuario.'}), 403
    
    usuario = obtener_usuario_por_id(user_id)
    if usuario:
        return jsonify(dict(usuario))
    else:
        return jsonify({'error': 'Usuario no encontrado.'}), 404


@app.route('/api/validar-correo', methods=['POST'])
def api_validar_correo():
    """Valida si un correo está disponible."""
    data = request.get_json()
    correo = data.get('correo', '').strip()
    
    if not correo:
        return jsonify({'valido': False, 'disponible': False})
    
    if not validar_correo(correo):
        return jsonify({'valido': False, 'disponible': False})
    
    disponible = not usuario_existente(correo=correo)
    return jsonify({'valido': True, 'disponible': disponible})


@app.route('/api/validar-documento', methods=['POST'])
def api_validar_documento():
    """Valida si un documento está disponible."""
    data = request.get_json()
    documento = data.get('documento', '').strip()
    
    disponible = not usuario_existente(documento=documento)
    return jsonify({'disponible': disponible})


# ============================================================================
# RUTAS DE BLOGS
# ============================================================================

@app.route('/crear_blog', methods=['POST'])
@login_requerido
def crear_nuevo_blog():
    """Crea un nuevo blog."""
    # Aceptar JSON o form-encoded
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    titulo = (data.get('titulo') or '').strip()
    contenido = (data.get('contenido') or '').strip()
    categoria = (data.get('categoria') or '').strip()
    
    if not titulo or not contenido:
        return jsonify({'success': False, 'mensaje': '❌ Complete todos los campos.'}), 400
    
    usuario_id = session.get('usuario_id')
    exito, mensaje, blog_id = crear_blog(usuario_id, titulo, contenido, categoria if categoria else None)
    
    if exito:
        return jsonify({'success': True, 'mensaje': mensaje, 'blog_id': blog_id}), 201
    return jsonify({'success': False, 'mensaje': mensaje}), 400


@app.route('/crear_blog_form', methods=['POST'])
@login_requerido
def crear_blog_form():
    """Permite crear un blog desde un formulario (POST estándar).
    Redirige al dashboard después de crear.
    """
    titulo = request.form.get('titulo', '').strip()
    contenido = request.form.get('contenido', '').strip()
    categoria = request.form.get('categoria', '').strip() or None

    if not titulo or not contenido:
        # Volver al dashboard con mensaje simple (se puede mejorar con flash)
        return redirect(url_for('dashboard'))

    usuario_id = session.get('usuario_id')
    _exito, _mensaje, _blog_id = crear_blog(usuario_id, titulo, contenido, categoria)
    # Simple redirección; el dashboard carga blogs vía AJAX
    return redirect(url_for('dashboard'))


@app.route('/obtener_blogs')
@login_requerido
def obtener_mis_blogs():
    """Obtiene los blogs del usuario actual."""
    usuario_id = session.get('usuario_id')
    blogs = obtener_blogs_usuario(usuario_id)
    
    blogs_lista = []
    for blog in blogs:
        blogs_lista.append({
            'id': blog[0],
            'titulo': blog[1],
            'contenido': blog[2][:100] + '...' if len(blog[2]) > 100 else blog[2],
            'categoria': blog[3],
            'fecha': str(blog[4])
        })
    
    return jsonify({'blogs': blogs_lista})


@app.route('/obtener_blogs_categoria/<categoria>')
def obtener_blogs_cat(categoria):
    """Obtiene blogs de una categoría específica."""
    blogs = obtener_blogs_por_categoria(categoria)
    
    blogs_lista = []
    for blog in blogs:
        usuario = obtener_usuario_por_id(blog[1])
        blogs_lista.append({
            'id': blog[0],
            'usuario': usuario[2] if usuario else 'Desconocido',
            'usuario_id': usuario[4] if usuario else '',
            'titulo': blog[2],
            'contenido': blog[3][:100] + '...' if len(blog[3]) > 100 else blog[3],
            'categoria': blog[4],
            'fecha': str(blog[5])
        })
    
    return jsonify({'blogs': blogs_lista})


@app.route('/public/obtener_blogs')
def public_obtener_blogs():
    """Endpoint público que devuelve los blogs recientes."""
    blogs = obtener_todos_blogs()
    blogs_lista = []
    for blog in blogs:
        # blog: id, usuario_id, titulo, contenido, categoria, fecha_creacion, completado
        usuario = obtener_usuario_por_id(blog[1])
        blogs_lista.append({
            'id': blog[0],
            'usuario_id': usuario[1] if usuario else '',
            'usuario_nombre': usuario[2] if usuario else 'Desconocido',
            'titulo': blog[2],
            'contenido': blog[3][:200] + '...' if len(blog[3]) > 200 else blog[3],
            'categoria': blog[4],
            'fecha': str(blog[5]),
            'completado': bool(blog[6])
        })
    return jsonify({'blogs': blogs_lista})


@app.route('/debug/db_blogs')
def debug_db_blogs():
    """Endpoint de depuración: devuelve todos los blogs y, si hay sesión, los del usuario actual."""
    try:
        todos = obtener_todos_blogs()
        todos_list = [dict(id=b[0], usuario_id=b[1], titulo=b[2], contenido=b[3], categoria=b[4], fecha=str(b[5]), completado=bool(b[6])) for b in todos]
    except Exception as e:
        app.logger.exception('Error obteniendo todos los blogs: %s', e)
        todos_list = []

    user_blogs = []
    if 'usuario_id' in session:
        try:
            ub = obtener_blogs_usuario(session['usuario_id'])
            for b in ub:
                # b: id, titulo, contenido, categoria, fecha_creacion, completado
                user_blogs.append(dict(id=b[0], titulo=b[1], contenido=b[2], categoria=b[3], fecha=str(b[4]), completado=bool(b[5])))
        except Exception as e:
            app.logger.exception('Error obteniendo blogs del usuario: %s', e)
            user_blogs = []

    return jsonify({'todos': todos_list, 'mis_blogs': user_blogs, 'session': {'usuario_id': session.get('usuario_id'), 'usuario_nombre': session.get('usuario_nombre')}})


@app.route('/api/blog/<int:blog_id>')
def api_obtener_blog(blog_id):
    """Devuelve los datos de un blog (público)."""
    blog = obtener_blog_por_id(blog_id)
    if not blog:
        return jsonify({'success': False, 'mensaje': 'Blog no encontrado.'}), 404
    usuario = obtener_usuario_por_id(blog[1])
    return jsonify({
        'id': blog[0],
        'usuario_id': usuario[1] if usuario else '',
        'usuario_nombre': usuario[2] if usuario else 'Desconocido',
        'titulo': blog[2],
        'contenido': blog[3],
        'categoria': blog[4],
        'fecha': str(blog[5]),
        'completado': bool(blog[7])
    })


@app.route('/api/notes', methods=['GET', 'POST'])
def api_notes():
    """API simple para listar notas (GET) y crear nota (POST JSON).
    GET: devuelve formato compatible con `nexena-notes-orbit.html` JS (id,title,content,type,completed,date,color,icon)
    POST: requiere sesión; crea nota y devuelve {success,id}.
    """
    if request.method == 'GET':
        blogs = obtener_todos_blogs()
        notes = []
        # mapear categoría -> color (clases Tailwind usadas en HTML)
        color_map = {
            'vida-diaria': 'from-indigo-500 to-blue-500',
            'cocina': 'from-orange-500 to-amber-500',
            'viajes': 'from-cyan-500 to-sky-500',
            'tecnologia': 'from-fuchsia-500 to-pink-500',
            'curiosidades': 'from-emerald-500 to-green-500'
        }
        for b in blogs:
            # b: id, usuario_id, titulo, contenido, categoria, fecha_creacion, completado
            cat = b[4] or 'blog'
            # incluir nombre de usuario para mostrar en UI
            usuario = obtener_usuario_por_id(b[1])
            usuario_nombre = usuario[2] if usuario else ''
            notes.append({
                'id': b[0],
                'title': b[2],
                'content': b[3],
                'type': cat,
                'usuario_id': b[1],
                'usuario_nombre': usuario_nombre,
                'completed': bool(b[6]) if len(b) > 6 else False,
                'date': str(b[5]),
                'color': color_map.get(cat, 'from-indigo-500 to-blue-500'),
                'icon': ''
            })
        return jsonify({'notes': notes})

    # POST -> crear
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'mensaje': 'Autenticación requerida.'}), 401
    data = request.get_json() or {}
    titulo = data.get('titulo', '').strip()
    contenido = data.get('contenido', '').strip()
    categoria = data.get('categoria', '').strip() or None
    if not titulo or not contenido:
        return jsonify({'success': False, 'mensaje': 'Título y contenido requeridos.'}), 400

    usuario_id = session.get('usuario_id')
    exito, mensaje, blog_id = crear_blog(usuario_id, titulo, contenido, categoria)
    if exito:
        return jsonify({'success': True, 'id': blog_id}), 201
    return jsonify({'success': False, 'mensaje': mensaje}), 500


@app.route('/api/notes/<int:note_id>/toggle', methods=['POST'])
@login_requerido
def api_notes_toggle(note_id):
    data = request.get_json() or {}
    valor = data.get('valor', None)
    blog = obtener_blog_por_id(note_id)
    if not blog:
        return jsonify({'success': False, 'mensaje': 'Nota no encontrada.'}), 404
    if blog[1] != session.get('usuario_id'):
        return jsonify({'success': False, 'mensaje': 'No tienes permiso.'}), 403
    # si valor es None -> alternar
    if valor is None:
        nuevo = 0 if bool(blog[7]) else 1
    else:
        nuevo = 1 if int(valor) else 0

    exito, msg = marcar_completado(note_id, nuevo)
    if exito:
        return jsonify({'success': True, 'mensaje': msg})
    return jsonify({'success': False, 'mensaje': msg}), 500


@app.route('/api/notes/<int:note_id>/delete', methods=['POST', 'DELETE'])
@login_requerido
def api_notes_delete(note_id):
    """Elimina un blog/nota si el usuario es propietario."""
    blog = obtener_blog_por_id(note_id)
    if not blog:
        return jsonify({'success': False, 'mensaje': 'Nota no encontrada.'}), 404
    if blog[1] != session.get('usuario_id'):
        return jsonify({'success': False, 'mensaje': 'No tienes permiso.'}), 403

    exito, msg = eliminar_blog(note_id)
    if exito:
        return jsonify({'success': True, 'mensaje': msg})
    return jsonify({'success': False, 'mensaje': msg}), 500


@app.route('/actualizar_blog', methods=['POST'])
@login_requerido
def api_actualizar_blog():
    data = request.get_json() or request.form
    blog_id = data.get('blog_id')
    titulo = data.get('titulo', '').strip()
    contenido = data.get('contenido', '').strip()
    categoria = data.get('categoria', '').strip()

    if not blog_id or not titulo or not contenido:
        return jsonify({'success': False, 'mensaje': 'Parámetros incompletos.'}), 400

    # verificar propietario
    blog = obtener_blog_por_id(blog_id)
    if not blog:
        return jsonify({'success': False, 'mensaje': 'Blog no encontrado.'}), 404
    if blog[1] != session.get('usuario_id'):
        return jsonify({'success': False, 'mensaje': 'No tienes permiso para editar este blog.'}), 403

    exito, msg = actualizar_blog(blog_id, titulo, contenido, categoria if categoria else None)
    if exito:
        return jsonify({'success': True, 'mensaje': msg})
    return jsonify({'success': False, 'mensaje': msg}), 500


@app.route('/toggle_completado', methods=['POST'])
@login_requerido
def api_toggle_completado():
    data = request.get_json() or request.form
    blog_id = data.get('blog_id')
    valor = data.get('valor', 1)
    if not blog_id:
        return jsonify({'success': False, 'mensaje': 'blog_id requerido.'}), 400

    blog = obtener_blog_por_id(blog_id)
    if not blog:
        return jsonify({'success': False, 'mensaje': 'Blog no encontrado.'}), 404
    if blog[1] != session.get('usuario_id'):
        return jsonify({'success': False, 'mensaje': 'No tienes permiso.'}), 403

    exito, msg = marcar_completado(blog_id, 1 if int(valor) else 0)
    if exito:
        return jsonify({'success': True, 'mensaje': msg})
    return jsonify({'success': False, 'mensaje': msg}), 500


@app.route('/perfil_publico/<usuario_id_str>')
def perfil_publico(usuario_id_str):
    """Muestra el perfil público de un usuario y sus blogs."""
    usuario = obtener_usuario_por_usuario_id(usuario_id_str)
    
    if not usuario:
        return render_template('error.html', codigo=404, mensaje='Usuario no encontrado'), 404
    
    blogs = obtener_blogs_usuario(usuario[0])
    
    return render_template('perfil_publico.html', usuario=usuario, blogs=blogs)


@app.route('/api/buscar_usuario')
def api_buscar_usuario():
    """Busca un usuario por `usuario_id` o por nombre (q).
    Devuelve {'success': True, 'usuario_id': '...'} si lo encuentra.
    """
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'success': False, 'mensaje': 'Parámetro q vacío.'}), 400

    # Intentar buscar por usuario_id exacto
    usuario = obtener_usuario_por_usuario_id(q)
    if usuario:
        return jsonify({'success': True, 'usuario_id': usuario[1]})

    # Buscar por nombre (case-insensitive)
    usuarios = obtener_todos_usuarios()
    for u in usuarios:
        try:
            nombre = u[2]
            uid = u[1]
        except Exception as e:
            app.logger.exception('Error parseando usuario en busqueda de nombre: %s', e)
            continue
        if nombre and nombre.lower() == q.lower():
            return jsonify({'success': True, 'usuario_id': uid})

    return jsonify({'success': False, 'mensaje': 'Usuario no encontrado.'}), 404


@app.route('/nexena-notes-orbit')
def nexena_notes_orbit():
    """Página orbital de notas (vista estática / demo)."""
    categoria = request.args.get('categoria')
    blog_id = request.args.get('blog_id')
    current_user_id = session.get('usuario_id')
    return render_template('nexena-notes-orbit.html', categoria=categoria, blog_id=blog_id, current_user_id=current_user_id)


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def no_encontrado(e):
    """Maneja errores 404."""
    app.logger.warning('404 - Página no encontrada: %s', e)
    return render_template('error.html', codigo=404, mensaje='Página no encontrada'), 404


@app.errorhandler(500)
def error_servidor(e):
    """Maneja errores 500."""
    app.logger.exception('500 - Error interno del servidor: %s', e)
    return render_template('error.html', codigo=500, mensaje='Error interno del servidor'), 500


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

if __name__ == '__main__':
    # Crear tabla de usuarios al iniciar
    crear_tabla_usuarios()
    
    # Ejecutar la aplicación
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )


# Directorio de uploads para fotos
UPLOAD_DIR = BASE_DIR / 'static' / 'uploads'
os.makedirs(str(UPLOAD_DIR), exist_ok=True)


@app.route('/upload_foto', methods=['POST'])
@login_requerido
def upload_foto():
    """Recibe una foto de perfil, la guarda y actualiza la ruta en la BD."""
    if 'foto' not in request.files:
        return jsonify({'success': False, 'mensaje': 'No se recibió archivo.'}), 400
    foto = request.files['foto']
    if foto.filename == '':
        return jsonify({'success': False, 'mensaje': 'Nombre de archivo inválido.'}), 400

    filename = f"{session.get('usuario_id')}_{int(datetime.now().timestamp())}_{secure_filename(foto.filename)}"
    save_path = UPLOAD_DIR / filename
    try:
        foto.save(str(save_path))
        # Guardar ruta relativa para usar con url_for('static', filename=...)
        ruta_rel = f"uploads/{filename}"
        exito, msg = actualizar_foto_perfil(session.get('usuario_id'), ruta_rel)
        if exito:
            return jsonify({'success': True, 'ruta': ruta_rel})
        else:
            return jsonify({'success': False, 'mensaje': msg}), 500
    except Exception as e:
        app.logger.exception('Error guardando foto de perfil')
        return jsonify({'success': False, 'mensaje': str(e)}), 500
