#  Plataforma Distribuida para Análisis de Tráfico Vial

Este proyecto implementa una plataforma distribuida simulando el procesamiento de datos de tráfico tipo Waze, utilizando un sistema de almacenamiento, generador de consultas y un sistema de caché configurable.

---

##  Estructura del Proyecto

- scraper/: Simula scraping de eventos viales.
- storage/: Almacena eventos en memoria.
- traffic_generator/: Genera consultas de eventos con tasas de arribo variables.
- cache/: Implementa un sistema de caché con política LRU o FIFO.
- docker-compose.yml: Orquesta el despliegue de los servicios.

---

##  Requisitos previos

- Ubuntu 22.04 o superior
- Docker
- Docker Compose
- (Opcional) Python 3.9+ para ejecutar scripts de pruebas

---
Para instalar Docker y Docker Compose:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```
---
Instalación de python 3.9+ (opcional)
Actualiza repositorios:
```bash
sudo apt update
sudo apt upgrade -y
```
Instala Python 3.9 y pip:
```bash
sudo apt install python3.9 python3.9-venv python3-pip -y
```
Verifica la versión instalada:
```bash
python3.9 --version
```
## 🚀 Instalación y ejecución
---
1. Clona el repositorio:
```bash
git clone https://github.com/usuario/tarea1_sd.git
cd tarea1_sd
```
2. Construye e inicia todos los servicios:
```bash
docker-compose up --build
```
3.  Verifica que los contenedores estén activos:
```bash
docker ps
```

Deberías ver:

- tarea1_sd_scraper_1
- tarea1_sd_storage_1
- tarea1_sd_generator_1
- tarea1_sd_cache_1

---

## Descripción de módulos

- **scraper**: genera eventos falsos simulando datos reales de tráfico (tipo, latitud, longitud, timestamp).
- **storage**: recibe y guarda eventos en memoria accesible mediante API REST (`/events`).
- **generator**: consulta eventos de almacenamiento según una distribución (Poisson, Uniforme o Normal) y los envía al caché.
- **cache**: almacena eventos consultados aplicando política LRU (por defecto) o FIFO.

---

## Cambiar política de caché (LRU / FIFO)

Para usar LRU:

- Asegúrate de que en `cache_server.py` esté activa la línea:
  - `cache.move_to_end(key)`

Para usar FIFO:

- Comenta la línea `cache.move_to_end(key)` en `handle_query`.  

Ocupar cualquier modificador de codigo(como VS Code, en este caso utilizaremos nano)
```bash
nano cache/cache_server.py
```
Después de cualquier cambio:
```bash
docker-compose build cache
docker-compose up -d cache
```
---

## Pruebas experimentales

1. Modifica la distribución y tasa de arribo en el archivo `generator.py`.

   Ejemplo: cambiar a distribución Poisson:
```bash
nano traffic_generator/generator.py
```
Descomenta:
run_generator(rate=1.0, distribution='poisson')

O cambiar a Uniforme:

run_generator(rate=1.0, distribution='uniform')  
Despues:
```bash
docker-compose build generator
docker-compose up -d generator
```
recordar comentar la  distribucion que no se esta ocupando.  
2. Cambia el tamaño del caché modificando el parámetro `MAX_SIZE` en `cache_server.py`.
```bash
nano cache/cache_server.py
```
3. Consulta estadísticas del caché ejecutando:
```bash
curl http://localhost:6000/stats
```

Este endpoint mostrará:

- hit_rate
- miss_rate
- evictions
- current_cache_size
---

 Visualización de logs de los servicios
Para monitorear el funcionamiento de cada servicio en tiempo real, utiliza los siguientes comandos desde la terminal:

Logs del caché (para ver cuándo hay HITs y MISSes):

Ejecuta:  
```bash
docker logs -f tarea1_sd_cache_1
```
Logs del generador de tráfico (para ver las consultas realizadas):  
Ejecuta:
```bash
 docker logs -f tarea1_sd_generator_1
```
Logs del scraper (para ver los envíos de eventos hacia el almacenamiento):  
Ejecuta:
```bash
 docker logs -f tarea1_sd_scraper_1
```
Logs del almacenamiento (para ver la recepción de eventos):  
Ejecuta:
```bash
docker logs -f tarea1_sd_storage_1
```
---
## Notas finales

cualquier comando que no funcione pruebe a utilizar sudo 

---
##  Referencias

- [Docker Overview - Docker Documentation](https://docs.docker.com/engine/docker-overview/)
- [Flask Framework - Official Documentation](https://flask.palletsprojects.com/en/latest/)
- [Python collections.OrderedDict - Official Documentation](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
- [Poisson Distribution - Brilliant.org](https://brilliant.org/wiki/poisson-distribution/)
- [LRU Cache Implementation - GeeksforGeeks](https://www.geeksforgeeks.org/lru-cache-implementation/)
- [Caching Best Practices - Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching)
- [Cache Replacement Policies Explained - Cloudflare Blog](https://blog.cloudflare.com/cache-eviction-what-it-is-and-how-it-works/)
- [Best Practices for Dockerfiles - Docker Docs](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [REST API Best Practices - Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)

---
