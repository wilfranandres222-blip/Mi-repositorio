from flask import Flask, jsonify, render_template

# Base de datos removida: el manejo de la DB se hará por separado.
# Se expone contenido estático temporalmente para pruebas/local.
PLANET_DATA = {
    'id': 1,
    'name': 'Nexena',
    'composition': 'Rocky core, thin atmosphere, scattered oceans',
    'temperature': 'Variable: -20°C to 45°C',
    'rotation': '24.6h (approx)',
    'description': 'Planeta de Blocs: un planeta ficticio organizado en tarjetas y bloques visuales.',
    'color': '#b3e5fc'
}

app = Flask(__name__, static_folder='static', template_folder='templates')

# Database-related functions removed. PLANET_DATA used as temporary source.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/planet')
def api_planet():
    # Devuelve datos estáticos; la DB será manejada por separado.
    return jsonify(PLANET_DATA)

@app.route('/api/planet/<field>')
def api_planet_field(field):
    allowed = {'name', 'composition', 'temperature', 'rotation', 'description', 'color'}
    if field not in allowed:
        return jsonify({'error': 'Field not allowed'}), 400
    # Obtener campo desde fuente estática temporal
    value = PLANET_DATA.get(field)
    if value is None:
        return jsonify({'error': 'No planet found'}), 404
    return jsonify({field: value})

if __name__ == '__main__':
    app.run(debug=True)
