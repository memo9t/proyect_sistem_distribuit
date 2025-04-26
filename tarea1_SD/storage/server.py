# Importamos Flask y utilidades para manejar peticiones y respuestas JSON
from flask import Flask, request, jsonify

# Creamos una aplicación Flask
app = Flask(__name__)

# Lista en memoria que actuará como almacenamiento temporal de eventos
storage = []

# Ruta que recibe eventos desde el scraper (método POST)
@app.route("/events", methods=["POST"])
def save_events():
    global storage
    # Obtenemos la lista de eventos enviada en formato JSON
    events = request.json
    # Agregamos los eventos recibidos al almacenamiento
    storage.extend(events)
    # Retornamos una respuesta con la cantidad de eventos recibidos
    return jsonify({"status": "ok", "received": len(events)})

# Ruta que permite consultar todos los eventos almacenados (método GET)
@app.route("/events", methods=["GET"])
def get_events():
    # Devolvemos toda la lista de eventos en formato JSON
    return jsonify(storage)

# Ejecutamos la aplicación en el puerto 5000 y disponible en todas las IPs del host
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

