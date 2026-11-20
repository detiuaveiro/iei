---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Programación en Redes: Sockets, APIs REST y MQTT"
institute: Universidade de Aveiro
date: November 16, 2026
colorlinks: true
highlight-style: tango
mainfont: NotoSans
fontsize: 9pt
titlegraphic: "../../../resources/ua_logo2.png"
titlegraphicoptions: "width=6.5cm"
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
  - "DejaVu Sans:"
header-includes:
 - \usetheme[sectionpage=none,numbering=fraction,progressbar=none]{metropolis}
 - \definecolor{uagreen}{HTML}{92D400}
 - \setbeamercolor{title separator}{fg=uagreen}
 - \setbeamersize{text margin left=1.5em, text margin right=1.5em}
 - |
    \setbeamertemplate{title graphic}{
      \begin{tikzpicture}[remember picture,overlay]
        \node[anchor=north west, xshift=0cm, yshift=-0cm] at (current page.north west) {
          \inserttitlegraphic
        };
        \node[anchor=south east, xshift=-0.2cm, yshift=0.6cm, opacity=0.08] at (current page.south east) {
          \includegraphics[width=4.8cm]{../../../resources/_deti_black.png}
        };
      \end{tikzpicture}
    }
 - \usepackage{tikz}
 - \usetikzlibrary{positioning,arrows.meta,calc}
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \BeforeBeginEnvironment{Shaded}{\vspace{0.8em}}
 - \AfterEndEnvironment{Shaded}{\vspace{0.5em}}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Visión General de la Sesión

  * **Parte I — Fundamentos de Programación en Red: Sockets Puros (TCP vs. UDP) y Concurrencia:**
      * Puente con la Clase 07 (`IP:Puerto`, `127.0.0.1` vs. `0.0.0.0`, `ss`/`lsof`), **TCP vs. UDP**, *3-way handshake* vs. datagramas, implementación en Python (`socket`), **E/S Bloqueante** y concurrencia con **`asyncio`**.
  * **Parte II — De la Capa de Transporte a la Aplicación: HTTP y APIs REST:**
      * Qué viaja dentro de un *socket* TCP cuando usamos `curl`, principios de **APIs REST**, formato **JSON**, construcción de servicios con **FastAPI** y documentación automática (*Swagger UI*).
  * **Parte III — El Paradigma Publish/Subscribe y el Protocolo MQTT (IoT y Tiempo Real):**
      * *Request/Response* vs. *Publish/Subscribe*, desacoplamiento y *fan-out*, arquitectura con **Broker Mosquitto** (TCP `1883` + WebSockets `9001`), **Tópicos**, *Wildcards*, **QoS**, **LWT** y telemetría en Python (`paho-mqtt` + `psutil`).
  * **Síntesis Arquitectónica y Recursos:**
      * Comparación de las arquitecturas abordadas en la sesión y documentación de referencia.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Sockets Puros (TCP vs. UDP) y Concurrencia}}
\end{center}

-----

## De la Clase 07 al Código: ¿Qué es un *Socket*?

En la Clase 07 usamos `ss -tuln` / `lsof`, `curl` y `nc` para inspeccionar servicios en ejecución. Pero ¿cómo abre un programa un puerto en el sistema operativo?

  * **El *Socket* (Capa 4 — Transporte):**
      * Es un punto terminal (*endpoint*) de comunicación bidireccional gestionado por el *kernel* del sistema operativo y expuesto al programa como un descriptor de archivo.
      * Cada *socket* a la escucha se identifica por el par **`IP:Puerto`** (p. ej., `127.0.0.1:9000` o `0.0.0.0:8000`).
  * **Recordando la Clase 07 (`bind address`):**
      * **`127.0.0.1` (*Loopback*):** El *socket* acepta únicamente conexiones originadas en la propia máquina (ideal para desarrollo local).
      * **`0.0.0.0` (`INADDR_ANY`):** El *socket* acepta conexiones en todas las interfaces de red de la máquina (LAN, Docker, Wi-Fi).
  * **Dos protocolos fundamentales de Internet:**
      * **TCP** (*Transmission Control Protocol* $\rightarrow$ `socket.SOCK_STREAM`)
      * **UDP** (*User Datagram Protocol* $\rightarrow$ `socket.SOCK_DGRAM`)

-----

## TCP vs. UDP: Los Dos Pilares de la Capa de Transporte

| Característica | TCP (*Transmission Control Protocol*) | UDP (*User Datagram Protocol*) |
| :--- | :--- | :--- |
| **Conexión** | Orientado a conexión (establece sesión) | Sin conexión (*stateless*, "disparar y olvidar") |
| **Fiabilidad** | **Fiable:** Garantiza entrega, orden y retransmisión | **No fiable:** Sin garantía de entrega ni de orden |
| **Sobrecarga** | Elevada (*3-way handshake*, ACKs, control de flujo) | Mínima (cabecera de solo 8 bytes) |
| **Latencia** | Más lenta debido a las confirmaciones y ordenación | Más rápida, sin establecimiento previo de sesión |
| **Módulo Python** | `socket.SOCK_STREAM` (flujo continuo de bytes) | `socket.SOCK_DGRAM` (mensajes discretos) |
| **Casos de Uso** | Web (HTTP/REST), SSH, Email, Transferencia de archivos | Streaming audio/vídeo, Juegos online, DNS, VoIP |

\vspace{0.5em}

  * **Nota práctica:** En TCP leemos un flujo continuo de bytes (*stream*); en UDP recibimos datagramas individuales con la dirección del remitente adjunta a cada paquete.

-----

## Patrones de Comunicación: TCP (*Handshake*) vs. UDP (Datagramas)

\vspace{0.2em}

\begin{center}
\begin{tikzpicture}[
    actor/.style={rectangle, draw=black!75, fill=black!5, rounded corners=2pt, thick, font=\scriptsize\bfseries, minimum width=1.6cm, minimum height=0.50cm},
    lifeline/.style={dashed, color=black!45, thick},
    msg/.style={-{Latex[length=1.5mm]}, thick, color=uagreen!75!black},
    datamsg/.style={-{Latex[length=1.5mm]}, thick, color=black!80},
    lostmsg/.style={-{Latex[length=1.5mm]}, dashed, thick, color=red!75!black},
    udpmsg/.style={-{Latex[length=1.5mm]}, thick, color=blue!70!black},
    note/.style={rectangle, draw=orange!70!black, fill=orange!10, rounded corners=2pt, font=\tiny, align=center, inner sep=3pt}
]
% --- Lado Izquierdo: TCP ---
\node[font=\footnotesize\bfseries] at (2.2, 5.2) {TCP (Orientado a Conexión)};
\node[actor] (tc) at (0.7, 4.65) {Cliente};
\node[actor] (ts) at (3.7, 4.65) {Servidor};
\draw[lifeline] (tc.south) -- (0.7, 0.40);
\draw[lifeline] (ts.south) -- (3.7, 0.40);

% 3-way handshake
\draw[msg] (0.7, 4.20) -- node[above, sloped, font=\tiny\ttfamily] {1. SYN} (3.7, 4.02);
\draw[msg] (3.7, 3.84) -- node[above, sloped, font=\tiny\ttfamily] {2. SYN-ACK} (0.7, 3.66);
\draw[msg] (0.7, 3.48) -- node[above, sloped, font=\tiny\ttfamily] {3. ACK} (3.7, 3.30);

% Envío normal + ACK
\draw[datamsg] (0.7, 2.98) -- node[above, sloped, font=\tiny\ttfamily] {Datos 1 ("Hola")} (3.7, 2.80);
\draw[msg] (3.7, 2.62) -- node[above, sloped, font=\tiny\ttfamily] {ACK 1} (0.7, 2.44);

% Fallo + Timeout + Retransmisión + ACK
\draw[lostmsg] (0.7, 2.12) -- node[above, sloped, font=\tiny\ttfamily] {Datos 2 ("IEI")} (2.35, 2.00);
\node[font=\tiny\bfseries, color=red!75!black] at (2.55, 2.00) {X};
\node[font=\tiny\itshape, color=orange!80!black, anchor=east] at (0.65, 1.72) {Timeout};
\draw[datamsg, color=orange!80!black] (0.7, 1.66) -- node[above, sloped, font=\tiny\ttfamily] {Retransm. Datos 2} (3.7, 1.48);
\draw[msg] (3.7, 1.30) -- node[above, sloped, font=\tiny\ttfamily] {ACK 2} (0.7, 1.12);

% Cierre
\draw[msg, color=red!70!black] (0.7, 0.78) -- node[above, sloped, font=\tiny\ttfamily] {FIN / ACK} (3.7, 0.60);
\node[note] at (2.2, 0.15) {Resultado en el Servidor: \textbf{"Hola IEI"} (completo y ordenado)};

% Separador central
\draw[dotted, thick, color=black!35] (5.3, 5.3) -- (5.3, 0.05);

% --- Lado Derecho: UDP ---
\node[font=\footnotesize\bfseries] at (8.2, 5.2) {UDP (Datagramas sin Sesión)};
\node[actor] (uc) at (6.7, 4.65) {Cliente};
\node[actor] (us) at (9.7, 4.65) {Servidor};
\draw[lifeline] (uc.south) -- (6.7, 0.40);
\draw[lifeline] (us.south) -- (9.7, 0.40);

\draw[udpmsg] (6.7, 4.00) -- node[above, sloped, font=\tiny\ttfamily] {Datagrama 1 ("Hola")} (9.7, 3.76);
\draw[lostmsg] (6.7, 3.15) -- node[above, sloped, font=\tiny\ttfamily] {Datagrama 2 ("IEI")} (8.35, 3.00);
\node[font=\tiny\bfseries, color=red!75!black] at (8.95, 3.00) {X (perdido)};
\draw[udpmsg] (9.7, 2.25) -- node[above, sloped, font=\tiny\ttfamily] {Datagrama Respuesta} (6.7, 2.01);
\node[note] at (8.2, 0.90) {Resultado en el Servidor: solo \textbf{"Hola"}\\(sin ACK, sin retransmisión, menor latencia).};
\end{tikzpicture}
\end{center}

-----

## Ciclo de Vida de un Socket TCP en Python (Servidor y Cliente)

::::: columns
::: {.column width="56%"}

  * **Servidor TCP (`echo_server.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 9000))
    s.listen() # Pone el socket en estado LISTEN
    while True:
        conn, addr = s.accept() # Bloquea hasta recibir cliente
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break # El cliente cerró la conexión
                conn.sendall(data) # Eco
```

:::
::: {.column width="44%"}

  * **Cliente TCP (`echo_client.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 9000))
    s.sendall(b"Hola, IEI!")
    reply = s.recv(1024)
    print(reply.decode())
```

:::
:::::

\vspace{0.3em}

  * **Flujo típico:**
      1. `bind()` asocia el *socket* a `IP:Puerto` y `listen()` abre la cola de conexiones.
      2. `accept()` crea un **nuevo *socket*** (`conn`) dedicado a cada cliente que se conecta vía `connect()`.
      3. El servidor puede probarse con `nc 127.0.0.1 9000` y observarse con `ss -tuln` / `lsof`.

-----

## Sockets sin Sesión en Python: Servidor y Cliente UDP

::::: columns
::: {.column width="54%"}

  * **Servidor UDP (`echo_server.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(("127.0.0.1", 9000))
    # ¡No existe listen() ni accept()!
    while True:
        data, addr = s.recvfrom(1024)
        s.sendto(data, addr) # Responde al remitente
```

:::
::: {.column width="46%"}

  * **Cliente UDP (`echo_client.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hola UDP!", ("127.0.0.1", 9000))
    reply, addr = s.recvfrom(1024)
    print(reply.decode())
```

:::
:::::

\vspace{0.3em}

  * **Diferencias clave frente a TCP:**
      1. No aparece en estado `LISTEN` en `ss`/`lsof` (no existen `listen()` ni `accept()`).
      2. `recvfrom()` devuelve los datos **y** la tupla `(ip, puerto)` del cliente para cada paquete recibido.
      3. El servidor puede probarse con `nc -u 127.0.0.1 9000`.

-----

## El Problema de la E/S Bloqueante (*Blocking I/O*)

Los *sockets* estándar en Python son **bloqueantes** por defecto:

  * `s.accept()` **detiene el programa** hasta que un cliente establece conexión.
  * `conn.recv(1024)` **detiene el programa** hasta que llegan bytes por la red o el cliente se desconecta.
  * **Consecuencia práctica (Bloque 1 del Guion):** Mientras el servidor atiende al Cliente A en el bucle `recv()`, ¡el Cliente B queda en espera!

\vspace{0.4em}

  * **Enfoque Tradicional — *Multi-threading*:**
      * Crear un hilo (*thread*) del sistema operativo por cada cliente conectado.
      * **Desventajas:** Complejidad de sincronización (*locks*, *race conditions*), elevado consumo de memoria con miles de conexiones y el **GIL (*Global Interpreter Lock*)** en CPython impide el paralelismo real de CPU en código Python.

-----

## La Solución Moderna: Concurrencia con E/S Asíncrona (`asyncio`)

El módulo **`asyncio`** permite que **un único hilo** gestione miles de conexiones concurrentes usando un **Event Loop** (bucle de eventos):

::::: columns
::: {.column width="44%"}

  * **Cómo funciona:**
      * Las palabras clave `async` y `await` suspenden una tarea mientras espera datos de red, liberando el bucle de eventos para atender a otros clientes.
      * *Nota:* Es **concurrencia** (esperar eficientemente por E/S), no ejecución paralela de CPU.
      * Es la base de frameworks modernas como **FastAPI** y **`websockets`**.

:::
::: {.column width="56%"}

```python
import asyncio

async def handle_client(reader, writer):
    while data := await reader.read(1024):
        writer.write(data)
        await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 9000
    )
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: HTTP y APIs REST}}
\end{center}

-----

## Desmitificar HTTP: ¿Qué Viaja Dentro del Socket TCP?

El protocolo **HTTP** (*HyperText Transfer Protocol*) no es magia: es simplemente **texto estructurado enviado dentro de un *socket* TCP**!

::::: columns
::: {.column width="50%"}

  * **Cuando ejecuta en el terminal:**
    ```bash
    $ curl http://127.0.0.1:9000/hola
    ```
  * **Su servidor TCP (`echo_server.py`) recibe:**
    ```http
    GET /hola HTTP/1.1
    Host: 127.0.0.1:9000
    User-Agent: curl/8.5.0
    Accept: */*
    ```

:::
::: {.column width="50%"}

  * **Lo que `curl` espera recibir de vuelta:**
    ```http
    HTTP/1.1 200 OK
    Content-Type: application/json

    {"message": "Hola, IEI!"}
    ```
  * **¿Por qué no hacemos APIs con sockets puros?** Tendríamos que programar manualmente el *parsing* de rutas, cabeceras, códigos de error y JSON. Por eso usamos frameworks como **FastAPI**.

:::
:::::

-----

## APIs REST: El Lenguaje Estándar de la Web

**REST** (*REpresentational State Transfer*) es el estilo arquitectónico dominante para servicios Web y APIs sobre HTTP:

::::: columns
::: {.column width="48%"}

  * **Principios Esenciales:**
      * **Stateless (Sin estado):** Cada petición contiene toda la información necesaria para ser procesada.
      * **Recursos:** Identificados por URIs (p. ej., `/ip/8.8.8.8`, `/users/42`).
      * **Verbos HTTP:** `GET` (leer), `POST` (crear), `PUT` (actualizar), `DELETE` (eliminar).
      * **Códigos de Estado:** `200 OK`, `201 Created`, `404 Not Found`, `502 Bad Gateway`.

:::
::: {.column width="52%"}

\begin{center}
\begin{tikzpicture}[
    actor/.style={rectangle, draw=black!75, fill=black!5, rounded corners=2pt, thick, font=\scriptsize\bfseries, minimum width=1.6cm, minimum height=0.55cm},
    lifeline/.style={dashed, color=black!45, thick},
    req/.style={-{Latex[length=1.6mm]}, thick, color=blue!70!black},
    res/.style={-{Latex[length=1.6mm]}, thick, color=uagreen!75!black}
]
\node[actor] (c) at (0.6, 3.6) {Cliente};
\node[actor] (s) at (4.4, 3.6) {API REST};
\draw[lifeline] (c.south) -- (0.6, 0.2);
\draw[lifeline] (s.south) -- (4.4, 0.2);

\draw[req] (0.6, 2.9) -- node[above, font=\tiny\ttfamily] {GET /ip/8.8.8.8} (4.4, 2.9);
\draw[res] (4.4, 2.3) -- node[above, font=\tiny\ttfamily] {200 OK (JSON)} (0.6, 2.3);

\draw[req] (0.6, 1.4) -- node[above, font=\tiny\ttfamily] {GET /ip/192.168.1.1} (4.4, 1.4);
\draw[res, color=red!70!black] (4.4, 0.8) -- node[above, font=\tiny\ttfamily] {404 Not Found} (0.6, 0.8);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## El Formato de Datos: JSON (*JavaScript Object Notation*)

**JSON** es el estándar *de facto* para el intercambio de datos estructurados en APIs REST (y también en mensajes MQTT):

::::: columns
::: {.column width="50%"}

  * **Características:**
      * Ligero, textual y legible por humanos.
      * Pares clave-valor con tipos primitivos: *strings*, números, booleanos, listas (`[]`) y objetos anidados (`{}`).
  * **En Python (`import json`):**
      * `json.dumps(dict_py)` $\rightarrow$ convierte diccionario a texto JSON.
      * `json.loads(texto_json)` $\rightarrow$ convierte texto JSON a diccionario.

:::
::: {.column width="50%"}

```json
{
  "query": "193.137.169.135",
  "status": "success",
  "country": "Portugal",
  "city": "Aveiro",
  "isp": "FCCN - FCT"
}
```

:::
:::::

-----

## Construcción de APIs REST en Python con FastAPI

**FastAPI** es un framework moderno sobre `asyncio` (ejecutado con **`uvicorn`**) que valida tipos y genera documentación interactiva automática en **`/docs`** (*Swagger UI*):

```python
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="IEI Geolocation API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the IP API"}

@app.get("/ip/{ip_address}")
def get_ip_info(ip_address: str):
    resp = requests.get(f"http://ip-api.com/json/{ip_address}")
    data = resp.json()
    if data.get("status") == "fail":
        raise HTTPException(status_code=404, detail=data.get("message"))
    return data
```

\vspace{0.2em}

  * **Acceder a los *endpoints* de la API (`uvicorn main:app --reload`):**
      * Raíz (`/`): `curl http://127.0.0.1:8000/` | Consulta IP: `curl http://127.0.0.1:8000/ip/8.8.8.8`
      * Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`

-----

## Documentación Automática en FastAPI (*Swagger UI*)

\begin{center}
\includegraphics[width=\linewidth,height=0.76\textheight,keepaspectratio]{figures/fastapi_swagger_docs.jpg}
\end{center}

-----

## Sockets Puros vs. APIs REST: ¿Cuándo Usar Cada Uno?

| Característica | Sockets Puros (TCP / UDP) | APIs REST (HTTP + JSON) |
| :--- | :--- | :--- |
| **Nivel de Abstracción** | **Bajo nivel** (Capa 4 — Transporte) | **Alto nivel** (Capa 7 — Aplicación) |
| **Protocolo** | TCP / UDP con formato propio | HTTP/HTTPS estandarizado |
| **Estado** | Puede mantener sesión abierta (*stateful*) | **Stateless** por definición |
| **Formato de Datos** | Cualquier formato (binario o texto) | Típicamente **JSON** |
| **Herramientas** | `nc`, `ss`/`lsof`, código `socket` | `curl`, navegadores, Swagger (`/docs`), FastAPI |
| **Cuándo Usar** | Protocolos propios, juegos, baja latencia | Servicios Web, backends, apps móviles, integración |

\vspace{0.5em}

  * **Limitación común al Bloque 1:** Tanto en los *sockets* puros como en las APIs REST, es el **cliente quien inicia la petición** (*client-pull*) y necesita conocer exactamente el **`IP:Puerto`** del servidor.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: El Paradigma Publish/Subscribe y el Protocolo MQTT}}
\end{center}

-----

## ¿Por Qué un Nuevo Paradigma? *Request/Response* vs. *Publish/Subscribe*

En el modelo **Request/Response**, cliente y servidor están acoplados: el emisor necesita conocer exactamente el **`IP:Puerto`** de cada destinatario.

  * **Limitaciones del acoplamiento directo:**
      * Difícil de escalar en escenarios *1-a-N* o *N-a-M*.
      * Exige acceso directo al receptor (a menudo bloqueado por **NAT/Firewalls**) y que este esté activo en el momento del envío.
  * **Solución — Patrón *Publish/Subscribe* (MQTT):**
      * **Publisher:** Publica mensajes en un **Tópico** (p. ej., `sensores/sala1/temp`), sin saber *quién* escucha.
      * **Subscriber:** Se suscribe únicamente a los **Tópicos** que le interesan, sin saber *quién* publicó.
      * **Broker:** Intermediario que recibe los mensajes y los reenvía solo a los suscriptores interesados.

\vspace{0.2em}

  * **Principales ventajas de este paradigma:**
      * **Suscripción Selectiva:** Cada receptor elige exactamente la información que desea recibir, sin listas de destinatarios en el emisor.
      * **Escalabilidad:** El *Publisher* envía una sola vez al *Broker* (para 1 o 10\,000 *Subscribers*), permitiendo añadir o eliminar clientes dinámicamente.

-----

## Arquitectura *Publish/Subscribe* en MQTT

\vspace{0.2em}

\begin{center}
\begin{tikzpicture}[
    nodebox/.style={rectangle, draw=black!75, fill=black!4, rounded corners=3pt, thick, font=\scriptsize, align=center, inner sep=4pt, minimum width=2.7cm, minimum height=0.85cm},
    broker/.style={rectangle, draw=uagreen!80!black, fill=uagreen!15, rounded corners=4pt, thick, font=\scriptsize\bfseries, align=center, inner sep=6pt, minimum width=2.8cm, minimum height=2.6cm},
    pubt/.style={-{Latex[length=1.7mm]}, thick, color=blue!75!black},
    pubf/.style={-{Latex[length=1.7mm]}, thick, color=orange!80!black}
]
% Publishers a la izquierda
\node[nodebox] (p1) at (0, 2.3) {\textbf{Sensor Temperatura}\\{\tiny Publica: \texttt{casa/sala/temp}}};
\node[nodebox] (p2) at (0, 0.3) {\textbf{Sensor Humo}\\{\tiny Publica: \texttt{casa/cocina/humo}}};

% Broker en el centro
\node[broker] (b) at (4.8, 1.3) {\textbf{Broker MQTT}\\[0.2em]{\tiny Recibe y encamina}\\{\tiny por \textbf{Tópico}}};

% Subscribers a la derecha
\node[nodebox] (s1) at (9.7, 2.6) {\textbf{App Móvil}\\{\tiny Suscribe: \texttt{casa/sala/temp}}};
\node[nodebox] (s2) at (9.7, 1.3) {\textbf{Panel Central}\\{\tiny Suscribe: \texttt{casa/\#}}};
\node[nodebox] (s3) at (9.7, 0.0) {\textbf{Sistema de Alarma}\\{\tiny Suscribe: \texttt{casa/+/humo}}};

% Conexiones
\draw[pubt] (p1.east) -- node[above, sloped, font=\tiny\ttfamily] {22.5 C} (b.north west);
\draw[pubf] (p2.east) -- node[below, sloped, font=\tiny\ttfamily] {OK} (b.south west);

\draw[pubt] (b.north east) -- node[above, sloped, font=\tiny\ttfamily] {temp} (s1.west);
\draw[pubt] ($(b.east)+(0,0.12)$) -- node[above, font=\tiny\ttfamily] {temp} ($(s2.west)+(0,0.12)$);
\draw[pubf] ($(b.east)-(0,0.12)$) -- node[below, font=\tiny\ttfamily] {humo} ($(s2.west)-(0,0.12)$);
\draw[pubf] (b.south east) -- node[below, sloped, font=\tiny\ttfamily] {humo} (s3.west);
\end{tikzpicture}
\end{center}

\vspace{0.2em}

  * **Desacoplamiento:** Los sensores desconocen cuántos suscriptores existen (y viceversa); solo el *Broker* conoce los clientes conectados.
  * ***Fan-out* Selectivo:** Cada mensaje se publica **una vez** y se entrega simultáneamente solo a quienes se suscribieron al tópico correspondiente.

-----

## Conceptos Fundamentales de MQTT: Tópicos, *Wildcards*, QoS y LWT

  * **Tópicos Jerárquicos y *Wildcards*:**
      * Cadenas separadas por `/` (p. ej., `deti/pico/dht11`, `ua/iei/aula08/chat`).
      * **`+` (nivel único):** `deti/+/dht11` coincide con `deti/pico/dht11` y `deti/sala1/dht11`.
      * **`#` (múltiples niveles):** `deti/#` suscribe todos los subtópicos bajo `deti/`.
  * **Calidad de Servicio (QoS — *Quality of Service*):**
      * **`QoS 0`:** Como máximo una vez (*fire and forget*, menor sobrecarga).
      * **`QoS 1`:** Al menos una vez (garantiza entrega, puede duplicar).
      * **`QoS 2`:** Exactamente una vez (garantiza entrega única, más lento).
  * ***Last Will & Testament* (LWT):**
      * Mensaje registrado previamente por el cliente al conectarse; si la conexión cae abruptamente (p. ej., cerrar la pestaña del navegador), el **Broker** publica el mensaje en su nombre (p. ej., `"alice left the chat"`).

-----

## MQTT en la Práctica (I): El *Broker* y Transportes (TCP vs. WebSockets)

El protocolo MQTT tradicional funciona sobre **TCP (puerto `1883`)**, pero los navegadores Web no permiten abrir *sockets* TCP puros en JavaScript:

::::: columns
::: {.column width="45%"}

  * **Configuración del *Broker* (`mosquitto.conf`):**
    ```text
    allow_anonymous true

    listener 1883
    protocol mqtt          # Clientes nativos

    listener 9001
    protocol websockets    # Navegadores Web
    ```

:::
::: {.column width="55%"}

\begin{center}
\begin{tikzpicture}[
    client/.style={rectangle, draw=black!75, fill=black!4, rounded corners=3pt, thick, font=\tiny, align=center, inner sep=4pt, minimum width=1.9cm, minimum height=0.8cm},
    port/.style={rectangle, draw=uagreen!80!black, fill=white, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, align=center, inner sep=3pt, minimum width=1.6cm, minimum height=0.55cm},
    brokerbox/.style={rectangle, draw=uagreen!80!black, fill=uagreen!12, rounded corners=4pt, thick},
    arr1/.style={<->, >=Latex, thick, color=blue!75!black},
    arr2/.style={<->, >=Latex, thick, color=orange!80!black}
]
% Caja del Broker
\draw[brokerbox] (2.65, -0.35) rectangle (4.75, 2.85);
\node[font=\scriptsize\bfseries] at (3.70, 2.58) {Broker MQTT};
\node[font=\tiny, color=black!65] at (3.70, -0.12) {Docker / Público};

% Puertos
\node[port] (p1) at (3.70, 1.85) {:1883 (TCP)};
\node[port] (p2) at (3.70, 0.55) {:9001 (WS)};

% Clientes
\node[client] (c1) at (0.0, 1.85) {\textbf{Clientes Nativos}\\{\tiny Python / CLI / IoT}};
\node[client] (c2) at (0.0, 0.55) {\textbf{Clientes Web}\\{\tiny Navegador (JS)}};

% Conexiones
\draw[arr1] (c1.east) -- node[above, font=\tiny\ttfamily] {mqtt://} (p1.west);
\draw[arr2] (c2.east) -- node[above, font=\tiny\ttfamily] {ws://} (p2.west);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## MQTT en la Práctica (II): Publicador de Telemetría en Python (`paho-mqtt`)

Con las bibliotecas **`paho-mqtt`** y **`psutil`**, podemos enviar telemetría simulada o métricas reales de la máquina en formato **JSON**:

```python
import json, time
import paho.mqtt.client as mqtt
import psutil

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iei_pub_01")
client.connect("localhost", 1883, keepalive=60)
client.loop_start()  # Gestiona la red en un hilo en segundo plano

while True:
    payload = {
        "ts": time.time(),
        "t": round(psutil.cpu_percent(interval=None), 1),        # CPU (%) o Temp
        "h": round(psutil.virtual_memory().percent, 1),          # RAM (%) o Humedad
        "mode": "system",
    }
    client.publish("deti/pico/dht11", json.dumps(payload), qos=0)
    time.sleep(2)
```

-----

## MQTT en la Práctica (III): Suscriptor y Monitorización de Alertas en Python

El cliente suscriptor funciona de forma **orientada a eventos** mediante funciones *callback* (`on_connect` y `on_message`):

```python
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe("deti/pico/+")  # Suscribe con wildcard '+'

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if data["t"] >= 28.0:
        print(f"ALERTA en {msg.topic}: valor={data['t']}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, keepalive=60)
client.loop_forever()  # Bloquea procesando mensajes y reconexiones
```

-----

## Síntesis Arquitectónica y Recursos

| Arquitectura / Tecnología | Paradigma | Punto Fuerte Principal | Casos de Uso Típicos |
| :--- | :--- | :--- | :--- |
| **Sockets Puros (TCP/UDP)** | Request/Response o libre | Control total (Capa 4) | Protocolos propios, juegos, enseñanza |
| **Sockets con `asyncio`** | Concurrente (*Event Loop*) | Miles de conexiones sin *threads* | Servidores TCP/UDP escalables |
| **API REST (FastAPI)** | Request/Response (HTTP) | Estandarización, JSON, `/docs` | Servicios Web, APIs públicas, backends |
| **MQTT (TCP y WebSockets)** | Publish/Subscribe (Broker) | Desacoplamiento, *fan-out*, ligero | Telemetría en tiempo real, alertas, IoT |

\vspace{0.5em}

  * **Recursos y Documentación de Referencia:**
      * [Python `socket` — Programación de Bajo Nivel](https://docs.python.org/3/library/socket.html)
      * [Python `asyncio` — E/S Asíncrona](https://docs.python.org/3/library/asyncio.html)
      * [FastAPI — Documentación Oficial](https://fastapi.tiangolo.com/)
      * [Eclipse Paho-MQTT (Python)](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html) y [Especificación MQTT](https://mqtt.org/)
