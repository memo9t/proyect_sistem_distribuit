# Importamos librerías necesarias para enviar peticiones HTTP, medir tiempo y generar datos aleatorios
import requests
import time
import random

# Esta función genera un evento simulado con un ID, ubicación aleatoria, tipo de evento y timestamp
def generate_fake_event(i):
    return {
        "id": i,
        "location": {
            "lat": round(-33.4 + random.random() * 0.5, 6),   # Latitud dentro del rango de la RM
            "lon": round(-70.6 + random.random() * 0.5, 6)    # Longitud dentro del rango de la RM
        },
        "type": random.choice(["ACCIDENT", "TRAFFIC_JAM", "ROAD_CLOSED"]),  # Tipo de incidente vial
        "timestamp": time.time()  # Marca de tiempo actual
    }

# Esta función ejecuta el scraper en un ciclo infinito
def run_scraper():
    while True:
        # Se generan 100 eventos falsos en cada iteración
        events = [generate_fake_event(i) for i in range(100)]
        print(f"[SCRAPER] Enviando 100 eventos al almacenamiento", flush=True)

        # Se realiza un POST con la lista de eventos hacia el servicio de almacenamiento
        try:
            requests.post("http://storage:5000/events", json=events)
        except Exception as e:
            # Se imprime un error si no se logra enviar los datos
            print(f"[SCRAPER] Error al enviar: {e}", flush=True)

        # Espera 10 segundos antes de enviar los siguientes 100 eventos
        time.sleep(10)

# Punto de entrada principal del script: se llama a run_scraper
if __name__ == "__main__":
    run_scraper()


