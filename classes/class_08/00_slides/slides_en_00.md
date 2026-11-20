---
title: 47138 - Introduction to Computer Engineering
subtitle: "Network Programming: Sockets, REST APIs & MQTT"
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

## Session Overview

  * **Part I — Network Programming Foundations: Raw Sockets (TCP vs. UDP) and Concurrency:**
      * Bridging from Class 07 (`IP:Port`, `127.0.0.1` vs. `0.0.0.0`, `ss`/`lsof`), **TCP vs. UDP**, 3-way handshake vs. datagrams, Python `socket` programming, **Blocking I/O**, and concurrency with **`asyncio`**.
  * **Part II — From Transport to Application Layer: HTTP and REST APIs:**
      * What travels inside a TCP socket when using `curl`, **REST API** principles, **JSON**, building services with **FastAPI**, and automatic interactive docs (*Swagger UI*).
  * **Part III — The Publish/Subscribe Paradigm and MQTT (IoT & Real-Time):**
      * *Request/Response* vs. *Publish/Subscribe*, decoupling and *fan-out*, **Eclipse Mosquitto** broker architecture (TCP `1883` + WebSockets `9001`), **Topics**, *Wildcards*, **QoS**, **LWT**, and Python telemetry (`paho-mqtt` + `psutil`).
  * **Architectural Summary & Resources:**
      * Comparison of the architectures covered in this session and reference documentation.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: Raw Sockets (TCP vs. UDP) and Concurrency}}
\end{center}

-----

## From Class 07 to Code: What Is a *Socket*?

In Class 07, we used `ss -tuln` / `lsof`, `curl`, and `nc` to inspect running services. How does an application open a port on the operating system?

  * **The *Socket* (Layer 4 — Transport):**
      * A bidirectional communication endpoint managed by the OS kernel and exposed to programs as a file descriptor.
      * Every listening socket is bound to an **`IP:Port`** pair (e.g., `127.0.0.1:9000` or `0.0.0.0:8000`).
  * **Recalling Class 07 (`bind address`):**
      * **`127.0.0.1` (*Loopback*):** Accepts connections only from the local machine (ideal for local development).
      * **`0.0.0.0` (`INADDR_ANY`):** Accepts connections on all network interfaces of the machine (LAN, Docker, Wi-Fi).
  * **Two core Internet transport protocols:**
      * **TCP** (*Transmission Control Protocol* $\rightarrow$ `socket.SOCK_STREAM`)
      * **UDP** (*User Datagram Protocol* $\rightarrow$ `socket.SOCK_DGRAM`)

-----

## TCP vs. UDP: The Two Pillars of Transport

| Feature | TCP (*Transmission Control Protocol*) | UDP (*User Datagram Protocol*) |
| :--- | :--- | :--- |
| **Connection** | Connection-oriented (establishes a session) | Connectionless (*stateless*, fire and forget) |
| **Reliability** | **Reliable:** Guarantees delivery, order, and retries | **Unreliable:** No delivery or ordering guarantees |
| **Overhead** | High (3-way handshake, ACKs, flow control) | Minimal (only an 8-byte header) |
| **Latency** | Higher due to acknowledgments and ordering | Lower, no connection setup overhead |
| **Python Constant** | `socket.SOCK_STREAM` (continuous byte stream) | `socket.SOCK_DGRAM` (discrete datagrams) |
| **Use Cases** | Web (HTTP/REST), SSH, Email, File Transfer | Audio/video streaming, Online gaming, DNS, VoIP |

\vspace{0.5em}

  * **Practical note:** With TCP we read a continuous byte stream; with UDP we receive individual datagrams along with the sender's address on every packet.

-----

## Communication Patterns: TCP (*Handshake*) vs. UDP (Datagrams)

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
% --- Left Side: TCP ---
\node[font=\footnotesize\bfseries] at (2.2, 5.2) {TCP (Connection-Oriented)};
\node[actor] (tc) at (0.7, 4.65) {Client};
\node[actor] (ts) at (3.7, 4.65) {Server};
\draw[lifeline] (tc.south) -- (0.7, 0.40);
\draw[lifeline] (ts.south) -- (3.7, 0.40);

% 3-way handshake
\draw[msg] (0.7, 4.20) -- node[above, sloped, font=\tiny\ttfamily] {1. SYN} (3.7, 4.02);
\draw[msg] (3.7, 3.84) -- node[above, sloped, font=\tiny\ttfamily] {2. SYN-ACK} (0.7, 3.66);
\draw[msg] (0.7, 3.48) -- node[above, sloped, font=\tiny\ttfamily] {3. ACK} (3.7, 3.30);

% Normal delivery + ACK
\draw[datamsg] (0.7, 2.98) -- node[above, sloped, font=\tiny\ttfamily] {Data 1 ("Hello")} (3.7, 2.80);
\draw[msg] (3.7, 2.62) -- node[above, sloped, font=\tiny\ttfamily] {ACK 1} (0.7, 2.44);

% Loss + Timeout + Retransmission + ACK
\draw[lostmsg] (0.7, 2.12) -- node[above, sloped, font=\tiny\ttfamily] {Data 2 ("IEI")} (2.35, 2.00);
\node[font=\tiny\bfseries, color=red!75!black] at (2.55, 2.00) {X};
\node[font=\tiny\itshape, color=orange!80!black, anchor=east] at (0.65, 1.72) {Timeout};
\draw[datamsg, color=orange!80!black] (0.7, 1.66) -- node[above, sloped, font=\tiny\ttfamily] {Retransm. Data 2} (3.7, 1.48);
\draw[msg] (3.7, 1.30) -- node[above, sloped, font=\tiny\ttfamily] {ACK 2} (0.7, 1.12);

% Teardown
\draw[msg, color=red!70!black] (0.7, 0.78) -- node[above, sloped, font=\tiny\ttfamily] {FIN / ACK} (3.7, 0.60);
\node[note] at (2.2, 0.15) {Server receives: \textbf{"Hello IEI"} (complete \& ordered)};

% Center divider
\draw[dotted, thick, color=black!35] (5.3, 5.3) -- (5.3, 0.05);

% --- Right Side: UDP ---
\node[font=\footnotesize\bfseries] at (8.2, 5.2) {UDP (Connectionless Datagrams)};
\node[actor] (uc) at (6.7, 4.65) {Client};
\node[actor] (us) at (9.7, 4.65) {Server};
\draw[lifeline] (uc.south) -- (6.7, 0.40);
\draw[lifeline] (us.south) -- (9.7, 0.40);

\draw[udpmsg] (6.7, 4.00) -- node[above, sloped, font=\tiny\ttfamily] {Datagram 1 ("Hello")} (9.7, 3.76);
\draw[lostmsg] (6.7, 3.15) -- node[above, sloped, font=\tiny\ttfamily] {Datagram 2 ("IEI")} (8.35, 3.00);
\node[font=\tiny\bfseries, color=red!75!black] at (8.80, 3.00) {X (lost)};
\draw[udpmsg] (9.7, 2.25) -- node[above, sloped, font=\tiny\ttfamily] {Reply Datagram} (6.7, 2.01);
\node[note] at (8.2, 0.90) {Server receives only: \textbf{"Hello"}\\(no ACK, no retransmission, lower latency).};
\end{tikzpicture}
\end{center}

-----

## TCP Socket Lifecycle in Python (Server & Client)

::::: columns
::: {.column width="56%"}

  * **TCP Server (`echo_server.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 9000))
    s.listen() # Put socket in LISTEN state
    while True:
        conn, addr = s.accept() # Blocks until client connects
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break # Client closed connection
                conn.sendall(data) # Echo back
```

:::
::: {.column width="44%"}

  * **TCP Client (`echo_client.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 9000))
    s.sendall(b"Hello, IEI!")
    reply = s.recv(1024)
    print(reply.decode())
```

:::
:::::

\vspace{0.3em}

  * **Typical flow:**
      1. `bind()` attaches the socket to `IP:Port` and `listen()` opens the connection queue.
      2. `accept()` returns a **new socket** (`conn`) dedicated to each client connecting via `connect()`.
      3. Testable with `nc 127.0.0.1 9000` and observable with `ss -tuln` / `lsof`.

-----

## Connectionless Sockets in Python: UDP Server & Client

::::: columns
::: {.column width="54%"}

  * **UDP Server (`echo_server.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(("127.0.0.1", 9000))
    # No listen() or accept()!
    while True:
        data, addr = s.recvfrom(1024)
        s.sendto(data, addr) # Reply to sender
```

:::
::: {.column width="46%"}

  * **UDP Client (`echo_client.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello UDP!", ("127.0.0.1", 9000))
    reply, addr = s.recvfrom(1024)
    print(reply.decode())
```

:::
:::::

\vspace{0.3em}

  * **Key differences vs. TCP:**
      1. Does not show up as `LISTEN` in `ss`/`lsof` (there is no `listen()` or `accept()`).
      2. `recvfrom()` returns both the payload **and** the sender's `(ip, port)` tuple on every packet.
      3. Testable with `nc -u 127.0.0.1 9000`.

-----

## The Problem of Blocking I/O

Standard Python sockets are **blocking** by default:

  * `s.accept()` **pauses the program** until a client connects.
  * `conn.recv(1024)` **pauses the program** until bytes arrive from the network or the client closes.
  * **Practical consequence (Lab Block 1):** While the server handles Client A inside its `recv()` loop, Client B stays queued and receives no echo!

\vspace{0.4em}

  * **Traditional Approach — *Multi-threading*:**
      * Spawn one OS thread per connected client.
      * **Drawbacks:** Synchronization complexity (*locks*, *race conditions*), high memory overhead at scale, and CPython's **GIL (*Global Interpreter Lock*)** prevents true parallel CPU execution in Python code.

-----

## The Modern Solution: Concurrency with Async I/O (`asyncio`)

Python's **`asyncio`** module lets **a single thread** manage thousands of concurrent connections using an **Event Loop**:

::::: columns
::: {.column width="44%"}

  * **How it works:**
      * `async` and `await` pause a task while waiting for network I/O, allowing the event loop to serve other clients in the meantime.
      * *Note:* This is **concurrency** (waiting efficiently for I/O), not CPU parallelism.
      * Powers modern frameworks such as **FastAPI** and **`websockets`**.

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
{\LARGE \textbf{Part II: HTTP and REST APIs}}
\end{center}

-----

## Demystifying HTTP: What Travels Inside a TCP Socket?

**HTTP** (*HyperText Transfer Protocol*) is not magic: it is simply **structured plain text transmitted over a TCP socket**!

::::: columns
::: {.column width="50%"}

  * **When you run in the terminal:**
    ```bash
    $ curl http://127.0.0.1:9000/hello
    ```
  * **Your TCP server (`echo_server.py`) receives:**
    ```http
    GET /hello HTTP/1.1
    Host: 127.0.0.1:9000
    User-Agent: curl/8.5.0
    Accept: */*
    ```

:::
::: {.column width="50%"}

  * **What `curl` expects back:**
    ```http
    HTTP/1.1 200 OK
    Content-Type: application/json

    {"message": "Hello, IEI!"}
    ```
  * **Why don't we build APIs on raw sockets?** We would have to manually parse routes, headers, status codes, and JSON. Frameworks like **FastAPI** handle this for us.

:::
:::::

-----

## REST APIs: The Standard Language of the Web

**REST** (*REpresentational State Transfer*) is the dominant architectural style for web APIs over HTTP:

::::: columns
::: {.column width="48%"}

  * **Core Principles:**
      * **Stateless:** Every request contains all information required to process it.
      * **Resources:** Identified by URIs (e.g., `/ip/8.8.8.8`, `/users/42`).
      * **HTTP Verbs:** `GET` (read), `POST` (create), `PUT` (update), `DELETE` (delete).
      * **Status Codes:** `200 OK`, `201 Created`, `404 Not Found`, `502 Bad Gateway`.

:::
::: {.column width="52%"}

\begin{center}
\begin{tikzpicture}[
    actor/.style={rectangle, draw=black!75, fill=black!5, rounded corners=2pt, thick, font=\scriptsize\bfseries, minimum width=1.6cm, minimum height=0.55cm},
    lifeline/.style={dashed, color=black!45, thick},
    req/.style={-{Latex[length=1.6mm]}, thick, color=blue!70!black},
    res/.style={-{Latex[length=1.6mm]}, thick, color=uagreen!75!black}
]
\node[actor] (c) at (0.6, 3.6) {Client};
\node[actor] (s) at (4.4, 3.6) {REST API};
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

## Data Format: JSON (*JavaScript Object Notation*)

**JSON** is the *de facto* standard for structured data exchange in REST APIs (and MQTT payloads):

::::: columns
::: {.column width="50%"}

  * **Characteristics:**
      * Lightweight, text-based, and human-readable.
      * Key-value pairs supporting strings, numbers, booleans, arrays (`[]`), and nested objects (`{}`).
  * **In Python (`import json`):**
      * `json.dumps(py_dict)` $\rightarrow$ serializes a dictionary to a JSON string.
      * `json.loads(json_str)` $\rightarrow$ parses a JSON string into a dictionary.

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

## Building REST APIs in Python with FastAPI

**FastAPI** is a modern `asyncio`-based framework (served with **`uvicorn`**) that validates types and generates interactive documentation at **`/docs`** (*Swagger UI*):

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

  * **Accessing the API endpoints (`uvicorn main:app --reload`):**
      * Root (`/`): `curl http://127.0.0.1:8000/` | IP Lookup: `curl http://127.0.0.1:8000/ip/8.8.8.8`
      * Interactive documentation (Swagger UI): `http://127.0.0.1:8000/docs`

-----

## Automatic Documentation in FastAPI (*Swagger UI*)

\begin{center}
\includegraphics[width=\linewidth,height=0.76\textheight,keepaspectratio]{figures/fastapi_swagger_docs.jpg}
\end{center}

-----

## Raw Sockets vs. REST APIs: When to Use Each?

| Feature | Raw Sockets (TCP / UDP) | REST APIs (HTTP + JSON) |
| :--- | :--- | :--- |
| **Abstraction Level** | **Low-level** (Layer 4 — Transport) | **High-level** (Layer 7 — Application) |
| **Protocol** | TCP / UDP with custom message format | Standardized HTTP/HTTPS |
| **State** | Can keep an open session (*stateful*) | **Stateless** by design |
| **Data Format** | Anything (binary or plain text) | Typically **JSON** |
| **Tooling** | `nc`, `ss`/`lsof`, `socket` code | `curl`, browsers, Swagger (`/docs`), FastAPI |
| **Best Used For** | Custom protocols, games, low latency | Web services, public APIs, mobile backends |

\vspace{0.5em}

  * **Shared limitation in Block 1:** In both raw sockets and REST APIs, the **client must initiate the request** (*client-pull*) and know the server's exact **`IP:Port`**.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: The Publish/Subscribe Paradigm and MQTT}}
\end{center}

-----

## Why a New Paradigm? *Request/Response* vs. *Publish/Subscribe*

In the **Request/Response** model, client and server are tightly coupled: the sender must know each destination's exact **`IP:Port`**.

  * **Limitations of direct coupling:**
      * Hard to scale in *1-to-N* or *N-to-M* scenarios.
      * Requires direct inbound reachability (often blocked by **NAT/Firewalls**) and the receiver to be online at send time.
  * **Solution — *Publish/Subscribe* Pattern (MQTT):**
      * **Publisher:** Publishes messages to a **Topic** (e.g., `sensors/room1/temp`), without knowing *who* listens.
      * **Subscriber:** Subscribes only to **Topics** of interest, without knowing *who* published.
      * **Broker:** Intermediary that receives messages and routes them only to interested subscribers.

\vspace{0.2em}

  * **Key advantages of this paradigm:**
      * **Selective Subscription:** Each receiver chooses exactly which information it wants, with no recipient lists on the sender.
      * **Scalability:** The *Publisher* sends once to the *Broker* (for 1 or 10,000 *Subscribers*), allowing clients to be added or removed dynamically.

-----

## Publish/Subscribe Architecture in MQTT

\vspace{0.2em}

\begin{center}
\begin{tikzpicture}[
    nodebox/.style={rectangle, draw=black!75, fill=black!4, rounded corners=3pt, thick, font=\scriptsize, align=center, inner sep=4pt, minimum width=2.7cm, minimum height=0.85cm},
    broker/.style={rectangle, draw=uagreen!80!black, fill=uagreen!15, rounded corners=4pt, thick, font=\scriptsize\bfseries, align=center, inner sep=6pt, minimum width=2.8cm, minimum height=2.6cm},
    pubt/.style={-{Latex[length=1.7mm]}, thick, color=blue!75!black},
    pubf/.style={-{Latex[length=1.7mm]}, thick, color=orange!80!black}
]
% Publishers on the left
\node[nodebox] (p1) at (0, 2.3) {\textbf{Temperature Sensor}\\{\tiny Publishes: \texttt{home/living/temp}}};
\node[nodebox] (p2) at (0, 0.3) {\textbf{Smoke Sensor}\\{\tiny Publishes: \texttt{home/kitchen/smoke}}};

% Broker in the center
\node[broker] (b) at (4.8, 1.3) {\textbf{MQTT Broker}\\[0.2em]{\tiny Routes messages}\\{\tiny by \textbf{Topic}}};

% Subscribers on the right
\node[nodebox] (s1) at (9.7, 2.6) {\textbf{Mobile App}\\{\tiny Subscribes: \texttt{home/living/temp}}};
\node[nodebox] (s2) at (9.7, 1.3) {\textbf{Central Dashboard}\\{\tiny Subscribes: \texttt{home/\#}}};
\node[nodebox] (s3) at (9.7, 0.0) {\textbf{Alarm System}\\{\tiny Subscribes: \texttt{home/+/smoke}}};

% Connections
\draw[pubt] (p1.east) -- node[above, sloped, font=\tiny\ttfamily] {22.5 C} (b.north west);
\draw[pubf] (p2.east) -- node[below, sloped, font=\tiny\ttfamily] {OK} (b.south west);

\draw[pubt] (b.north east) -- node[above, sloped, font=\tiny\ttfamily] {temp} (s1.west);
\draw[pubt] ($(b.east)+(0,0.12)$) -- node[above, font=\tiny\ttfamily] {temp} ($(s2.west)+(0,0.12)$);
\draw[pubf] ($(b.east)-(0,0.12)$) -- node[below, font=\tiny\ttfamily] {smoke} ($(s2.west)-(0,0.12)$);
\draw[pubf] (b.south east) -- node[below, sloped, font=\tiny\ttfamily] {smoke} (s3.west);
\end{tikzpicture}
\end{center}

\vspace{0.2em}

  * **Decoupling:** Sensors do not know how many subscribers exist (and vice versa); only the *Broker* tracks connected clients.
  * **Selective *Fan-out*:** Each message is published **once** and delivered simultaneously only to subscribers matching that topic.

-----

## Core MQTT Concepts: Topics, *Wildcards*, QoS, and LWT

  * **Hierarchical Topics and *Wildcards*:**
      * Slash-separated strings (e.g., `deti/pico/dht11`, `ua/iei/aula08/chat`).
      * **`+` (single level):** `deti/+/dht11` matches `deti/pico/dht11` and `deti/room1/dht11`.
      * **`#` (multi-level):** `deti/#` subscribes to every subtopic beneath `deti/`.
  * **Quality of Service (QoS):**
      * **`QoS 0`:** At most once (*fire and forget*, lowest overhead).
      * **`QoS 1`:** At least once (guaranteed delivery, duplicates possible).
      * **`QoS 2`:** Exactly once (guaranteed single delivery, slowest).
  * ***Last Will & Testament* (LWT):**
      * A message pre-registered by the client upon connecting; if the connection drops unexpectedly (e.g., closing a browser tab), the **Broker** publishes it on the client's behalf (e.g., `"alice left the chat"`).

-----

## MQTT in Practice (I): The *Broker* & Transports (TCP vs. WebSockets)

Standard MQTT runs over **TCP (port `1883`)**, but web browsers cannot open raw TCP sockets from JavaScript:

::::: columns
::: {.column width="45%"}

  * **Broker Configuration (`mosquitto.conf`):**
    ```text
    allow_anonymous true

    listener 1883
    protocol mqtt          # Native clients

    listener 9001
    protocol websockets    # Web browsers
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
% Broker container box
\draw[brokerbox] (2.65, -0.35) rectangle (4.75, 2.85);
\node[font=\scriptsize\bfseries] at (3.70, 2.58) {MQTT Broker};
\node[font=\tiny, color=black!65] at (3.70, -0.12) {Docker / Public};

% Listeners
\node[port] (p1) at (3.70, 1.85) {:1883 (TCP)};
\node[port] (p2) at (3.70, 0.55) {:9001 (WS)};

% Clients
\node[client] (c1) at (0.0, 1.85) {\textbf{Native Clients}\\{\tiny Python / CLI / IoT}};
\node[client] (c2) at (0.0, 0.55) {\textbf{Web Clients}\\{\tiny Browser (JS)}};

% Connections
\draw[arr1] (c1.east) -- node[above, font=\tiny\ttfamily] {mqtt://} (p1.west);
\draw[arr2] (c2.east) -- node[above, font=\tiny\ttfamily] {ws://} (p2.west);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## MQTT in Practice (II): Python Telemetry Publisher (`paho-mqtt`)

Using **`paho-mqtt`** and **`psutil`**, we can stream simulated environmental data or live machine metrics as **JSON**:

```python
import json, time
import paho.mqtt.client as mqtt
import psutil

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iei_pub_01")
client.connect("localhost", 1883, keepalive=60)
client.loop_start()  # Handles network I/O in a background thread

while True:
    payload = {
        "ts": time.time(),
        "t": round(psutil.cpu_percent(interval=None), 1),        # CPU (%) or Temp
        "h": round(psutil.virtual_memory().percent, 1),          # RAM (%) or Humidity
        "mode": "system",
    }
    client.publish("deti/pico/dht11", json.dumps(payload), qos=0)
    time.sleep(2)
```

-----

## MQTT in Practice (III): Python Alert Subscriber

The subscriber follows an **event-driven** model using callback functions (`on_connect` and `on_message`):

```python
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe("deti/pico/+")  # Subscribe using '+' wildcard

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if data["t"] >= 28.0:
        print(f"ALERT on {msg.topic}: value={data['t']}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, keepalive=60)
client.loop_forever()  # Blocks while processing traffic & reconnects
```

-----

## Architectural Summary & Resources

| Architecture / Technology | Paradigm | Key Strength | Typical Use Cases |
| :--- | :--- | :--- | :--- |
| **Raw Sockets (TCP/UDP)** | Request/Response or custom | Full control (Layer 4) | Custom protocols, gaming, learning |
| **Async Sockets (`asyncio`)** | Concurrent (*Event Loop*) | Thousands of clients without threads | Scalable TCP/UDP servers |
| **REST API (FastAPI)** | Request/Response (HTTP) | Standardization, JSON, `/docs` | Web services, public APIs, backends |
| **MQTT (TCP & WebSockets)** | Publish/Subscribe (Broker) | Decoupled, *fan-out*, lightweight | Live telemetry, alerts, IoT |

\vspace{0.5em}

  * **Resources and Reference Documentation:**
      * [Python `socket` — Low-Level Networking](https://docs.python.org/3/library/socket.html)
      * [Python `asyncio` — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
      * [FastAPI — Official Documentation](https://fastapi.tiangolo.com/)
      * [Eclipse Paho-MQTT (Python)](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html) and [MQTT Specification](https://mqtt.org/)
