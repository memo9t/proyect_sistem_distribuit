# Importamos librerías para hacer peticiones HTTP, generar aleatoriedad y manejar el tiempo
import requests
import random
import time

# -------------------------------
# Funciones de distribución de tiempo entre consultas
# -------------------------------

# Distribución Poisson (modelo de llegadas exponenciales)
def poisson_delay(rate):
    return random.expovariate(rate)

# Distribución Uniforme (entre dos tiempos)
def uniform_delay(min_t=0.5, max_t=2.0):
    return random.uniform(min_t, max_t)

# Distribución Normal (con media y desviación estándar, se asegura que sea positiva)
def normal_delay(mean=1.0, std_dev=0.3):
    return max(0.1, random.gauss(mean, std_dev))  # Evita tiempos negativos

# -------------------------------
# Generador de tráfico simulado
# -------------------------------
def run_generator(rate=1.0, distribution="poisson"):
    while True:
        try:
            # Solicita todos los eventos almacenados en el backend
            events = requests.get("http://storage:5000/events").json()
            if events:
                # Selecciona un evento aleatorio para simular una consulta
                event = random.choice(events)
                print(f"[GENERATOR] Consulta evento id {event['id']}")
                # Envía el evento al sistema de caché
                requests.post("http://cache:6000/query", json=event)
        except Exception as e:
            print(f"[GENERATOR] Error: {e}")

        # Espera un tiempo antes de la siguiente consulta según la distribución seleccionada
        if distribution == "poisson":
            time.sleep(poisson_delay(rate))
        elif distribution == "uniform":
            time.sleep(uniform_delay())
        elif distribution == "normal":
            time.sleep(normal_delay())
        else:
            time.sleep(1.0)  # Tiempo por defecto si la distribución no es reconocida

# -------------------------------
# Punto de entrada del script
# -------------------------------
if __name__ == "__main__":
    # Puedes modificar aquí qué distribución usar y con qué parámetros
    # run_generator(rate=1.0, distribution="uniform")
    # run_generator(rate=1.0, distribution='poisson')
    run_generator(rate=1.0, distribution='normal')  # Activado por defecto
