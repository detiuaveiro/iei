---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Programación en Redes: Sockets, APIs REST & MQTT"
institute: Universidade de Aveiro
date: November 16, 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
  - "DejaVu Sans:"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\footnotesize}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guion Práctico de Laboratorio

**Contexto Pedagógico y Objetivos:**
En la **Clase 07**, inspeccionamos interfaces de red, diagnosticamos conexiones con `ss`/`lsof`, `curl` y `nc`, y analizamos por qué redes como `eduroam` bloquean las conexiones directas entre dispositivos (*Client Isolation*). En esta sesión de laboratorio de **3 horas**, totalmente ejecutable **en software** en tu portátil (Linux, macOS o WSL) sin necesidad de hardware dedicado ni redes Wi-Fi especiales, pasamos de la observación a la **construcción de aplicaciones en red en Python** a través de dos grandes bloques:

* **Parte 0 — Preparación del Entorno y Buenas Prácticas en Python:** Instalación de las utilidades necesarias, configuración de entornos virtuales (`venv`), uso correcto del módulo `logging` y arquitectura de comunicación local frente a *brokers* en `eduroam`.
* **Bloque 1 — Comunicación Directa Cliente-Servidor (*Request/Response*):**
  * **Ejercicio 1.1:** Implementación y prueba de un Servidor y Cliente de Eco con **Sockets Puros** en Python (`tcp` y `udp`), prueba con `nc` (`netcat`) e inspección de puertos en escucha (`ss` / `lsof`).
  * **Ejercicio 1.2:** Desmitificar el protocolo **HTTP** observando, directamente en el servidor de *sockets* TCP, el texto enviado por el comando `curl`.
  * **Ejercicio 1.3:** Construcción y prueba de una **API REST** con **FastAPI** y caché local (`ex03`), actuando simultáneamente como servidor REST local (`127.0.0.1:8000` y `/docs`) y cliente de una API externa.
* **Bloque 2 — Comunicación Desacoplada en Tiempo Real (*Publish/Subscribe* con MQTT):**
  * **Ejercicio 2.1:** Ejecución de un *broker* **Eclipse Mosquitto** en Docker y de una aplicación Web de **Chat *Serverless* sobre WebSockets** (`ex04`), probando *Last Will and Testament (LWT)* y comunicación en clase sobre `eduroam` a través de un *broker* público.
  * **Ejercicio 2.2:** Sistema de **Telemetría en Tiempo Real** en Python (`paho-mqtt` y `psutil`) con *dashboard* gráfico Plotly (`ex05`), soportando **datos ambientales simulados** (`--mode env`), **telemetría real de CPU/RAM del portátil** (`--mode system`) y un suscriptor de alertas en línea de comandos (`subscriber.py`).

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Antes de iniciar los ejercicios, crea y accede al directorio de trabajo dedicado a esta clase:

```bash
$ mkdir -p ~/IEI/aula08
$ cd ~/IEI/aula08
```

> **Nota sobre rutas de ficheros:**
> Los comandos presentados en este guion asumen que la sesión de terminal se encuentra ubicada en el directorio `~/IEI/aula08` (o en la subcarpeta del ejercicio correspondiente).

-----

## Parte 0: Preparación del Entorno y Buenas Prácticas en Python

Asegúrate de tener instalados **Docker** (con Docker Compose), **`curl`**, **`netcat` (`nc`)** y los módulos **`pip`** y **`venv`** de Python 3:

* **En Linux (Ubuntu / Debian / WSL):**
  ```bash
  $ sudo apt update
  $ sudo apt install -y curl wget netcat-openbsd python3-pip python3-venv
  ```
* **En macOS:**
  Las utilidades `curl`, `nc` y `python3` ya se encuentran disponibles de forma nativa en el sistema (o mediante *Xcode Command Line Tools*). Si utilizas Homebrew para gestionar una versión reciente de Python, ejecuta solo si es necesario:
  ```bash
  $ brew install python3
  ```

Verifica rápidamente que Docker y Python están operativos:

```bash
$ python3 --version
$ docker compose version
```

-----

## Bloque 1: Comunicación Directa Cliente-Servidor (*Request/Response*)

En este primer bloque exploramos el paradigma clásico **Cliente-Servidor**, empezando a nivel de la **Capa 4 (Transporte — TCP y UDP)** con *sockets* puros en Python hasta llegar a la **Capa 7 (Aplicación — HTTP / API REST)**.

### Ejercicio 1.1: El Clásico Servidor de Eco con Sockets Puros (TCP vs. UDP)

**Objetivo:** Comprender cómo una aplicación abre un *socket* en el sistema operativo para escuchar en un puerto (`IP:Puerto`) y comparar en la práctica los protocolos **TCP** (orientado a la conexión, fiable) y **UDP** (sin conexión, datagramas).

**Ficheros de apoyo:** Descarga `ex01.zip` desde la carpeta `"resources"` asociada a esta clase en el eLearning de la asignatura (`echo_server.py` y `echo_client.py`).

#### Parte A — Preparar los Ficheros de Apoyo (`echo_server.py` y `echo_client.py`)

Crea la carpeta del ejercicio y extrae el contenido de `ex01.zip` en ella:

```bash
$ mkdir -p ~/IEI/aula08/ex01
$ cd ~/IEI/aula08/ex01
# (Extrae aquí el fichero ex01.zip de eLearning: unzip ex01.zip)
```

Antes de ejecutar, analiza brevemente el fichero `echo_server.py`: observa que utiliza el módulo nativo `socket` de Python (sin `asyncio`, de forma bloqueante) e implementa dos funciones distintas — `run_tcp_server` (`SOCK_STREAM`, con `listen()` y `accept()`) y `run_udp_server` (`SOCK_DGRAM`, directamente con `recvfrom()` y `sendto()`).

#### Parte B — Probar el Modo TCP con `nc` e Inspeccionar el Socket

1. **Terminal 1 (Servidor TCP):** Inicia el servidor en el puerto `9000`:
   ```bash
   $ python3 echo_server.py tcp --port 9000
   ```
2. **Terminal 2 (Inspección de Red — repaso de la Clase 07):** Verifica que el proceso Python abrió un *socket* TCP en estado **`LISTEN`**:
   * **En Linux:** `ss -tulnp | grep 9000`
   * **En macOS:** `lsof -nP -iTCP:9000 -sTCP:LISTEN`
3. **Terminal 2 (Cliente `netcat`):** Establece una conexión TCP con el servidor y envía mensajes:
   ```bash
   $ nc 127.0.0.1 9000
   ```
   Escribe `Hola TCP` y pulsa Enter; deberías recibir `Hola TCP` de vuelta.
   * **Experimento de Bloqueo:** Sin cerrar este cliente en el Terminal 2, abre un **Terminal 3** y ejecuta también `nc 127.0.0.1 9000`, escribiendo `Segundo cliente`. Observa que el segundo cliente no recibe eco inmediato porque el servidor TCP está **bloqueado** en el `conn.recv()` del primer cliente.
   * Cierra el cliente en el Terminal 2 con **`Ctrl+C`** (o `Ctrl+D`) y observa en el Terminal 1 el registro de desconexión y la entrada inmediata del segundo cliente. Cierra también el cliente en el Terminal 3 y detén el servidor en el Terminal 1 (`Ctrl+C`).

#### Parte C — Probar el Modo UDP y Comparar con el Cliente Python

1. **Terminal 1 (Servidor UDP):**
   ```bash
   $ python3 echo_server.py udp --port 9000
   ```
2. **Terminal 2 (Inspección):** Ejecuta `ss -uln | grep 9000` (Linux) o `lsof -nP -iUDP:9000` (macOS). Observa que en **UDP no existe estado `LISTEN` ni `accept()`** porque no hay sesión previa (*stateless*).
3. **Terminal 2 (Cliente `nc` o `echo_client.py`):**
   ```bash
   $ nc -u 127.0.0.1 9000
   ```
   Escribe `Hola UDP` y pulsa Enter (termina después con `Ctrl+C`).
   Opcionalmente, prueba también con el cliente Python `echo_client.py` de apoyo:
   ```bash
   $ python3 echo_client.py udp --port 9000 --message "Prueba UDP en Python"
   ```
   **No detengas todavía** el servidor — para el ejercicio siguiente, cierra el modo UDP (`Ctrl+C`) y vuelve a iniciarlo en modo **TCP**.

-----

### Ejercicio 1.2: HTTP sobre un Socket TCP

**Objetivo:** Confirmar experimentalmente que el protocolo **HTTP** (usado por navegadores y APIs REST) no es un mecanismo separado de la red, sino **texto estructurado transportado dentro de un *socket* TCP**.

1. **Terminal 1:** Asegúrate de que tu servidor de eco está ejecutándose en modo **TCP**:
   ```bash
   $ python3 echo_server.py tcp --port 9000
   ```
2. **Terminal 2:** En lugar de `nc`, ejecuta una petición HTTP con la utilidad **`curl`**:
   ```bash
   $ curl -v http://127.0.0.1:9000/hola
   ```
3. **Analiza lo que ocurrió en ambos terminales:**
   * En el **Terminal 1 (`echo_server.py`)**, el servidor recibió e imprimió el mensaje enviado por `curl`:
     ```text
     GET /hola HTTP/1.1
     Host: 127.0.0.1:9000
     User-Agent: curl/...
     Accept: */*
     ```
   * En el **Terminal 2 (`curl`)**, el comando falló (p. ej.: `Unsupported HTTP version` o `Received HTTP/0.9 when not allowed`). **¿Por qué?** Porque `echo_server.py` devolvió exactamente la petición `GET /hola HTTP/1.1...` en eco, en lugar de construir una respuesta HTTP válida (`HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n...`).
4. Detén el servidor TCP en el Terminal 1 con `Ctrl+C`.

> **Conclusión:** Podríamos programar manualmente el *parsing* de métodos (`GET`, `POST`), rutas (`/hola`), cabeceras y códigos de estado (`200`, `404`) sobre *sockets* TCP — pero estaríamos reinventando el servidor HTTP. Es exactamente por eso que usamos *frameworks* como **FastAPI**.

-----

### Ejercicio 1.3: API REST de Geolocalización IP con Caché Local (FastAPI)

**Objetivo:** Ejecutar y analizar una **API REST** en Python con **FastAPI** que automatiza la consulta de geolocalización IP e implementa un mecanismo de **caché en disco** (`ip_cache.json`).

**Detalles de la Arquitectura (`ex03/main.py`):**

* **Servidor REST local:** Expone el *endpoint* `GET /ip/{ip_address}` en el puerto `8000` y genera automáticamente documentación interactiva en `/docs`.
* **Cliente REST externo:** En caso de *Cache Miss* (o expiración tras `CACHE_DEADLINE_SECONDS`), el servicio usa la biblioteca `requests` para consultar `http://ip-api.com/json/{ip_address}`.
* **Validación y Errores HTTP:** Las direcciones IP privadas (RFC 1918, como `192.168.x.x`) no son enrutables en la Internet pública, por lo que la API externa falla y FastAPI devuelve el código de estado HTTP **`404 Not Found`**.

**Instrucciones:**

1. Crea la carpeta `ex03`, descarga y extrae `ex03.zip` (de la carpeta `"resources"` asociada a esta clase en el eLearning de la asignatura — `main.py`, `requirements.txt`, `ip-address.png`), activa un entorno virtual e instala las dependencias:
   ```bash
   $ mkdir -p ~/IEI/aula08/ex03 && cd ~/IEI/aula08/ex03
   # (Extrae aquí el fichero ex03.zip de eLearning: unzip ex03.zip)
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
2. **Inicia el servidor FastAPI con Uvicorn (Terminal 1):**
   ```bash
   $ uvicorn main:app --reload
   ```
3. **Prueba el servicio en un segundo terminal (`curl`):**
   * **Prueba 1 — *Cache Miss* (consulta a la API externa):**
     ```bash
     # Dirección IP privada (debe devolver HTTP 404)
     $ curl -i http://127.0.0.1:8000/ip/192.168.132.132

     # DNS Google, MEO y Universidade de Aveiro
     $ curl -s http://127.0.0.1:8000/ip/8.8.8.8
     $ curl -s http://127.0.0.1:8000/ip/144.64.3.83
     $ curl -s http://127.0.0.1:8000/ip/193.137.169.135
     ```
     Observa en los logs del Terminal 1 el mensaje: `"Querying external API for ..."`.
   * **Prueba 2 — *Cache Hit* (respuesta servida directamente desde la caché local):**
     Repite las peticiones para `8.8.8.8` y `193.137.169.135`. Observa en los logs: `"Returning cached data for ..."` e inspecciona el fichero generado `cat ip_cache.json`.
4. **Analizar el Código (`main.py`):**
   Abre el fichero `main.py` y localiza:
   * Cómo y dónde está implementado el *endpoint* REST de consulta de IP;
   * Qué biblioteca y qué URL de API externa se invocan cuando ocurre *Cache Miss*;
   * Cómo se guarda y reutiliza la respuesta a través del fichero `ip_cache.json`.
5. **Explorar la Documentación Automática (Swagger UI):**
   Abre **`http://127.0.0.1:8000/docs`** en tu navegador Web y ejecuta una petición de prueba directamente desde la interfaz gráfica (*Try it out*).
6. Cuando termines, detén el servidor `uvicorn` en el Terminal 1 (`Ctrl+C`) y desactiva el entorno virtual (`deactivate`).

-----

## Bloque 2: Comunicación Desacoplada en Tiempo Real (MQTT)

En el **Bloque 1**, el cliente necesitaba conocer siempre exactamente la **IP y el Puerto** del servidor, y ambos debían ser directamente accesibles.
En este **Bloque 2**, pasamos al patrón **Publish/Subscribe** mediante un **Broker MQTT**: los clientes solo se conectan al *broker* y publican/suscriben **tópicos** jerárquicos, quedando totalmente desacoplados entre sí.

### Ejercicio 2.1: Broker MQTT en Docker & Chat Web *Serverless* sobre WebSockets

**Objetivo:** Ejecutar un *broker* **Eclipse Mosquitto** en Docker y conectarle una aplicación Web en JavaScript puro (`MQTT.js` sobre WebSockets) para construir un chat en tiempo real **sin escribir ningún código de servidor**.

**Detalles de la Arquitectura (`ex04`):**

* **Broker (`mosquitto`):** El fichero `compose.yml` arranca el contenedor `eclipse-mosquitto` configurado por `mqtt/mosquitto.conf` con acceso anónimo y dos puertos: **`1883`** (MQTT estándar sobre TCP) y **`9001`** (MQTT sobre **WebSockets**, necesario para navegadores).
* **Frontend (`nginx`):** El contenedor `nginx:alpine` sirve el fichero `html/index.html` en el puerto **`8080`**.
* **Funcionalidad *Last Will and Testament (LWT)*:** Al conectarse, cada cliente registra un mensaje de despedida en el *broker*; si la pestaña del navegador se cierra abruptamente, el propio *broker* publica la salida de ese usuario.

**Instrucciones:**

1. Crea la carpeta `ex04`, descarga y extrae `ex04.zip` (de la carpeta `"resources"` asociada a esta clase en el eLearning de la asignatura — `compose.yml`, `mqtt/mosquitto.conf`, `html/index.html`) e inicia los contenedores:
   ```bash
   $ mkdir -p ~/IEI/aula08/ex04 && cd ~/IEI/aula08/ex04
   # (Extrae aquí el fichero ex04.zip de eLearning: unzip ex04.zip)
   $ docker compose up -d
   $ docker compose ps
   ```
2. **Prueba Local en Múltiples Pestañas:**
   * Abre **`http://localhost:8080/`** en **dos pestañas** del navegador Web.
   * Mantén el *Broker URL* como `ws://localhost:9001` y el tópico `class/chat/main_room`.
   * Introduce nombres de usuario diferentes (p. ej., `alice` y `bob`), haz clic en **Connect** e intercambia mensajes entre ambas pestañas.
   * **Prueba de LWT:** Cierra abruptamente (haz clic en la `X` de la pestaña) la pestaña de `alice` y observa que en la pestaña de `bob` aparece automáticamente la notificación `"alice left the chat."` enviada por el *broker* tras unos segundos.
3. **Prueba Colaborativa en Clase sobre `eduroam`:**
   * Recarga la página `http://localhost:8080/`.
   * Sin salir de la red `eduroam`, cambia la dirección del *Broker* de `ws://localhost:9001` a un *broker* MQTT público con soporte para WebSockets:
     * `ws://broker.hivemq.com:8000/mqtt` *(o `ws://test.mosquitto.org:8080`)*
   * Define un tópico compartido con tus compañeros del aula (p. ej.: **`ua/iei/aula08/chat`**), introduce tu nombre y haz clic en **Connect**.
   * ¡Intercambia mensajes con la clase! *(Observa cómo decenas de portátiles aislados por `eduroam` se comunican en tiempo real porque todas las conexiones son salientes hacia el mismo broker).*
4. **Analizar la Implementación (`compose.yml`, `mqtt/mosquitto.conf` y `html/index.html`):**
   Abre los ficheros del proyecto e identifica, en líneas generales, cómo está estructurada la aplicación:
   * **Infraestructura (`compose.yml` y `mqtt/mosquitto.conf`):** qué contenedores se lanzan, qué puertos distinguen el acceso MQTT estándar del acceso vía WebSockets y qué reglas de acceso están definidas en el *broker*;
   * **Cliente Web (`html/index.html`):** qué biblioteca JavaScript establece la conexión con el *broker*, cómo se realizan `subscribe` y `publish` (incluido el formato de los mensajes intercambiados) y dónde se configura el mensaje de *Last Will and Testament (LWT)*.
5. **Limpieza Obligatoria:** Detén los contenedores antes de avanzar al Ejercicio 2.2 (para liberar los puertos `1883`, `9001` y `8080`):
   ```bash
   $ docker compose down
   ```

-----

### Ejercicio 2.2: Telemetría en Tiempo Real con `paho-mqtt`, `psutil` y Dashboard Plotly

**Objetivo:** Construir una *pipeline* completa de telemetría IoT/Sistemas **100% en software**: un script publicador en Python (`paho-mqtt`) envía mediciones en JSON al *broker* Mosquitto, alimentando simultáneamente un **dashboard gráfico en tiempo real** en el navegador (Plotly.js) y un **suscriptor de alertas en línea de comandos**.

El publicador (`main.py`) soporta **dos modos de recogida de datos**:
* **`--mode env` (Datos Ambientales Simulados):** Simula un sensor de temperatura (`°C`) y humedad (`%`) con variación continua (*random walk*).
* **`--mode system` (Telemetría Real de la Máquina):** Lee en tiempo real el porcentaje de uso de **CPU (%)** y de **Memoria RAM (%)** de tu propio ordenador mediante la biblioteca `psutil`.

**Instrucciones:**

1. Crea la carpeta `ex05`, descarga y extrae `ex05.zip` (de la carpeta `"resources"` asociada a esta clase en el eLearning de la asignatura):
   ```bash
   $ mkdir -p ~/IEI/aula08/ex05 && cd ~/IEI/aula08/ex05
   # (Extrae aquí el fichero ex05.zip de eLearning: unzip ex05.zip)
   ```
2. **Inicia la infraestructura Docker (`mosquitto` + `nginx`):**
   ```bash
   $ docker compose up -d
   ```
3. **Prepara el entorno virtual Python:**
   ```bash
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
4. **Abre el Dashboard Web en el Navegador:**
   * Accede a **`http://localhost:8080/`**.
   * Confirma que *Broker Host* está rellenado con **`localhost`** y *Topic* con **`deti/pico/dht11`**.
   * Haz clic en **Connect** (el estado debe pasar a `Status: Connected`).
5. **Escenario A — Publicar Datos Ambientales Simulados (`--mode env`):**
   En el **Terminal 1** (con el `.venv` activo), ejecuta el publicador en modo ambiental:
   ```bash
   $ python main.py --mode env
   ```
   Observa en el navegador el gráfico de Temperatura (`°C`) y Humedad (`%`) actualizándose cada 2 segundos en tiempo real.
6. **Escenario B — Ejecutar un Segundo Suscriptor de Alertas en el Terminal (`subscriber.py`):**
   Abre un **Terminal 2**, activa el mismo entorno virtual e inicia el suscriptor usando un *wildcard* MQTT (`+`) en el tópico y un umbral de alerta:
   ```bash
   $ cd ~/IEI/aula08/ex05
   $ source .venv/bin/activate
   $ python subscriber.py --topic "deti/pico/+" --threshold 24.0
   ```
   Verifica que **tanto el Dashboard Web como el terminal Python reciben los mismos mensajes simultáneamente** (*fan-out* del *broker*) y que se imprimen avisos `[WARNING] ALERT ...` cuando el valor supera el umbral.
7. **Escenario C — Publicar Telemetría Real del Portátil (`--mode system`):**
   En el **Terminal 1**, detén el modo `env` (`Ctrl+C`) y ejecuta el publicador en modo sistema:
   ```bash
   $ python main.py --mode system
   ```
   * Observa en el navegador que los ejes del gráfico se ajustan automáticamente a **CPU Usage (%)** y **RAM Usage (%)**.
   * ¡Prueba a abrir una pestaña pesada en el navegador o ejecutar un comando en el terminal para generar carga en la CPU y observa el pico reflejado en el gráfico y en las alertas del **Terminal 2**!
8. **Explorar y Modificar el Código (`main.py`, `subscriber.py` y `html/index.html`):**
   * **Explorar la Implementación:** localiza en `main.py` cómo se recogen las métricas con `psutil` y cómo se construye el *payload* JSON publicado en el *broker*; compara después con `subscriber.py` y `html/index.html` para entender cómo ambos suscriptores distinguen el modo ambiental del modo de sistema y actualizan sus respectivas alertas/gráficos.
   * **Probar una Modificación:** prueba a cambiar la cadencia de envío mediante la opción `--interval` de `main.py` e intenta modificar `subscriber.py` para emitir también una alerta cuando la métrica secundaria (humedad o memoria RAM) supere un umbral de tu elección.
9. **Desafío Extra (Opcional — Publicación en Clase vía `eduroam`):**
   Cambia el parámetro `--host` tanto en `main.py` como en `subscriber.py` (y en el campo *Broker Host* de la página Web) a `test.mosquitto.org` y usa un tópico único con tu número mecanográfico, por ejemplo `--topic "ua/iei/aula08/<nmec>"`, visualizando en tu navegador la telemetría del portátil de un compañero (suscribiendo `ua/iei/aula08/<nmec_compañero>`).
10. **Cierre:** Detén los scripts Python (`Ctrl+C`) y apaga los contenedores Docker:
   ```bash
   $ docker compose down
   ```

-----

## Síntesis Comparativa: Bloque 1 vs. Bloque 2

| Dimensión | Bloque 1: Sockets Puros & API REST | Bloque 2: MQTT (Publish/Subscribe) |
| :--- | :--- | :--- |
| **Paradigma** | **Request / Response** (Cliente-Servidor directo) | **Publish / Subscribe** (Orientado a eventos vía Broker) |
| **Protocolos** | TCP / UDP (`socket`) y HTTP (`FastAPI`) | MQTT sobre TCP (`1883`) y WebSockets (`9001`) |
| **Acoplamiento** | El cliente debe conocer `IP:Puerto` exacto del servidor | Desacoplado: los clientes solo conocen el Broker y el **Tópico** |
| **Comunicación `eduroam`** | Bloqueada entre alumnos (*Client Isolation*) | Funciona entre alumnos conectándose a un Broker externo |
| **Casos de Uso Típicos** | Servicios Web, APIs públicas, transferencia directa, juegos | Telemetría IoT, monitorización en tiempo real, chats, notificaciones |
