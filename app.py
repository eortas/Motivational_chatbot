from flask import Flask, request, jsonify
from flask_cors import CORS
from groq_utils import get_motivational_response
from db import crear_tabla_si_no_existe, guardar_interaccion

app = Flask(__name__)
CORS(app)

crear_tabla_si_no_existe()

@app.route('/motivacion', methods=['POST'])
def motivacion():
    data = request.json
    estado_emocional = data.get('estado', '')
    respuesta = get_motivational_response(estado_emocional)
    guardar_interaccion(estado_emocional, respuesta)
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)