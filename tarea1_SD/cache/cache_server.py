from flask import Flask, request, jsonify
from collections import OrderedDict

app = Flask(__name__)

# Caché implementado con OrderedDict para política LRU (Least Recently Used)
cache = OrderedDict()

# Tamaño máximo del caché
MAX_SIZE = 200

# Métricas de rendimiento
hits = 0
misses = 0
evictions = 0

@app.route("/query", methods=["POST"])
def handle_query():
    global cache, hits, misses, evictions
    event = request.json
    key = str(event['id'])

    if key in cache:
        # ✅ LRU: movemos el elemento al final para marcarlo como el más recientemente usado
        cache.move_to_end(key)
        hits += 1
        print(f"[CACHE - LRU] HIT para evento id {key}")

        # ❌ FIFO: no mover el elemento (comentado)
        # print(f"[CACHE - FIFO] HIT para evento id {key}")

    else:
        misses += 1
        print(f"[CACHE - LRU] MISS para evento id {key}")

        # Si el caché está lleno, eliminamos el menos recientemente usado (primer elemento)
        if len(cache) >= MAX_SIZE:
            cache.popitem(last=False)
            evictions += 1

        # Agregamos el nuevo evento al final
        cache[key] = event

    return jsonify({"status": "processed"})

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)

