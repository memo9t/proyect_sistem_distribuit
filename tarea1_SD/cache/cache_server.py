# Importamos Flask para construir la API y OrderedDict para implementar un caché LRU
from flask import Flask, request, jsonify
from collections import OrderedDict

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Creamos el caché como un OrderedDict para implementar política LRU (Least Recently Used)
cache = OrderedDict()

# 👇 Este parámetro define el tamaño máximo del caché (puede modificarse para hacer pruebas)
MAX_SIZE = 200

# Métricas del sistema de caché
hits = 0       # Número de veces que el evento estaba en el caché
misses = 0     # Número de veces que el evento no estaba en el caché
evictions = 0  # Número de eventos removidos por sobrepasar el tamaño máximo

# Ruta que recibe consultas desde el generador de tráfico (simula un "query" de evento)
@app.route("/query", methods=["POST"])
def handle_query():
    global cache, hits, misses, evictions
    event = request.json
    key = str(event['id'])  # Usamos el ID del evento como clave

    if key in cache:
        # Si ya está en caché, lo marcamos como recientemente usado
        cache.move_to_end(key)
        hits += 1
        print(f"[CACHE] HIT para evento id {key}")
    else:
        misses += 1
        print(f"[CACHE] MISS para evento id {key}")
        # Si el caché está lleno, eliminamos el menos recientemente usado (al principio)
        if len(cache) >= MAX_SIZE:
            cache.popitem(last=False)
            evictions += 1
        # Insertamos el nuevo evento al final (como el más recientemente usado)
        cache[key] = event

    # Respondemos que el evento fue procesado
    return jsonify({"status": "processed"})

# Ruta para consultar estadísticas del rendimiento del caché
@app.route("/stats", methods=["GET"])
def stats():
    total = hits + misses
    return jsonify({
        "hits": hits,
        "misses": misses,
        "total": total,
        "hit_rate": hits / total if total else 0,
        "miss_rate": misses / total if total else 0,
        "evictions": evictions,
        "current_cache_size": len(cache)
    })

# Ejecutamos el servidor Flask en el puerto 6000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
