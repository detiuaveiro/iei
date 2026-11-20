---
title: 47138 - Introduction to Computer Engineering
subtitle: "Network Programming: Sockets, REST APIs & MQTT"
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

# Practical Laboratory Guide

**Educational Context & Objectives:**
In **Class 07**, we inspected network interfaces, diagnosed connections using `ss`/`lsof`, `curl`, and `nc`, and observed why networks such as `eduroam` block direct connections between student devices (*Client Isolation*). In this **3-hour** laboratory session — designed to run **100% in software** on your laptop (Linux, macOS, or WSL) without requiring dedicated hardware or special Wi-Fi networks — we move from observation to **building networked applications in Python** across two core blocks:

* **Part 0 — Environment Setup & Python Best Practices:** Installing required utilities, configuring virtual environments (`venv`), using the `logging` module properly, and understanding local communication vs. MQTT brokers on `eduroam`.
* **Block 1 — Direct Client-Server Communication (*Request/Response*):**
  * **Exercise 1.1:** Implementing and testing a TCP/UDP Echo Server and Client using **Raw Sockets** in Python (`socket`), testing with `nc` (`netcat`), and inspecting listening ports (`ss` / `lsof`).
  * **Exercise 1.2:** Demystifying **HTTP** by inspecting the raw HTTP request text sent by `curl` directly inside your TCP socket server.
  * **Exercise 1.3:** Running and testing a **REST API** with **FastAPI** and local caching (`ex03`), acting simultaneously as a local REST server (`127.0.0.1:8000` and `/docs`) and a client of an external API.
* **Block 2 — Decoupled Real-Time Communication (*Publish/Subscribe* with MQTT):**
  * **Exercise 2.1:** Running an **Eclipse Mosquitto** broker in Docker alongside a **Serverless Web Chat over WebSockets** (`ex04`), testing *Last Will and Testament (LWT)* and classroom-wide communication over `eduroam` via a public broker.
  * **Exercise 2.2:** Building a **Real-Time Telemetry** pipeline in Python (`paho-mqtt` and `psutil`) with a live Plotly web dashboard (`ex05`), supporting both **simulated environmental data** (`--mode env`), **real laptop CPU/RAM telemetry** (`--mode system`), and a terminal alert subscriber (`subscriber.py`).

\vspace{0.5em}

### Working Directory Setup

Before starting the exercises, create and navigate into a dedicated working directory for this session:

```bash
$ mkdir -p ~/IEI/aula08
$ cd ~/IEI/aula08
```

> **Note on file paths:**
> Commands in this guide assume your terminal session is positioned inside `~/IEI/aula08` (or the corresponding exercise subfolder).

-----

## Part 0: Environment Setup & Python Best Practices

### Step 1: Install System Utilities and Python Tools

Ensure that **Docker** (with Docker Compose), **`curl`**, **`netcat` (`nc`)**, and Python 3's **`pip`** and **`venv`** modules are installed:

* **On Linux (Ubuntu / Debian / WSL):**
  ```bash
  $ sudo apt update
  $ sudo apt install -y curl wget netcat-openbsd python3-pip python3-venv
  ```
* **On macOS:**
  The `curl`, `nc`, and `python3` utilities are available natively (or via *Xcode Command Line Tools*). If you manage Python through Homebrew, run only if needed:
  ```bash
  $ brew install python3
  ```

Verify that Python and Docker Compose are working:

```bash
$ python3 --version
$ docker compose version
```

### Step 2: Python Best Practices (`venv` and `logging`)

For every Python exercise in this session, follow this clean dependency isolation workflow:

1. Create and enter the exercise directory (e.g., `mkdir -p ~/IEI/aula08/ex01 && cd ~/IEI/aula08/ex01`).
2. Create and activate an isolated virtual environment:
   ```bash
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   ```
3. Whenever a `requirements.txt` file is provided, install dependencies inside the active environment:
   ```bash
   $ pip install -r requirements.txt
   ```
4. Use Python's **`logging`** module instead of `print()` to record network events, connections, and errors cleanly:
   ```python
   import logging

   logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
   logger = logging.getLogger(__name__)

   logger.info("Server started successfully.")
   ```

### Step 3: Classroom Network Architecture (No Dedicated Wi-Fi Required)

In **Class 07**, you saw that the university `eduroam` network enforces **Client Isolation**, preventing two student laptops from opening direct connections to each other's private IP addresses.

In this **100% software** guide, we handle this cleanly:

* **For local Client-Server tests (Block 1 and the start of Block 2):** All servers and clients run on your own laptop, communicating over the *loopback* interface (`127.0.0.1` / `localhost`) and local Docker containers.
* **For classroom-wide collaboration over `eduroam` (Block 2 — Exercise 2.1):** Because every laptop can open **outbound** connections to the Internet, the **Publish/Subscribe (MQTT)** pattern enables all students to exchange messages in real time through an external **MQTT Broker** without knowing each other's IP addresses or switching Wi-Fi networks.

-----

## Block 1: Direct Client-Server Communication (*Request/Response*)

In this first block, we explore the classic **Client-Server** model, starting at **Layer 4 (Transport — TCP and UDP)** with raw Python *sockets* and moving up to **Layer 7 (Application — HTTP / REST API)**.

### Exercise 1.1: The Classic Echo Server with Raw Sockets (TCP vs. UDP)

**Goal:** Understand how an application opens a *socket* on the operating system to listen on an `IP:Port` endpoint, and compare **TCP** (connection-oriented, reliable) with **UDP** (connectionless, datagrams).

**Support Files:** Download `ex01.zip` from the `"resources"` folder associated with this class on the course eLearning platform (`echo_server.py` and `echo_client.py`).

#### Part A — Prepare the Support Files (`echo_server.py` and `echo_client.py`)

Create the exercise directory and extract `ex01.zip` into it:

```bash
$ mkdir -p ~/IEI/aula08/ex01
$ cd ~/IEI/aula08/ex01
# (Extract ex01.zip from eLearning here: unzip ex01.zip)
```

Before running it, briefly inspect `echo_server.py`: notice that it uses Python's built-in `socket` module (blocking I/O, without `asyncio`) and implements two separate functions — `run_tcp_server` (`SOCK_STREAM`, with `listen()` and `accept()`) and `run_udp_server` (`SOCK_DGRAM`, directly using `recvfrom()` and `sendto()`).

#### Part B — Test TCP Mode with `nc` and Inspect the Listening Socket

1. **Terminal 1 (TCP Server):** Start the server on port `9000`:
   ```bash
   $ python3 echo_server.py tcp --port 9000
   ```
2. **Terminal 2 (Network Inspection — Class 07 review):** Verify that the Python process opened a TCP socket in **`LISTEN`** state:
   * **On Linux:** `ss -tulnp | grep 9000`
   * **On macOS:** `lsof -nP -iTCP:9000 -sTCP:LISTEN`
3. **Terminal 2 (`netcat` Client):** Connect via TCP and send messages:
   ```bash
   $ nc 127.0.0.1 9000
   ```
   Type `Hello TCP` and press Enter; the server echoes `Hello TCP` back.
   * **Blocking I/O Experiment:** Without closing this first client in Terminal 2, open a **Terminal 3** and run `nc 127.0.0.1 9000`, typing `Second client`. Notice that the second client receives no reply yet because the TCP server is **blocked** inside `conn.recv()` for the first client!
   * Close the Terminal 2 client with **`Ctrl+C`** (or `Ctrl+D`) and watch Terminal 1 log the disconnection and immediately serve the second client. Close Terminal 3's client and stop the server (`Ctrl+C`).

#### Part C — Test UDP Mode and Compare with the Python Client

1. **Terminal 1 (UDP Server):**
   ```bash
   $ python3 echo_server.py udp --port 9000
   ```
2. **Terminal 2 (Inspection):** Run `ss -uln | grep 9000` (Linux) or `lsof -nP -iUDP:9000` (macOS). Notice that **UDP has no `LISTEN` state or `accept()`** because it is connectionless (*stateless*).
3. **Terminal 2 (`nc` or `echo_client.py`):**
   ```bash
   $ nc -u 127.0.0.1 9000
   ```
   Type `Hello UDP` and press Enter (exit with `Ctrl+C`).
   Optionally, download and test with the support client `echo_client.py`:
   ```bash
   $ python3 echo_client.py udp --port 9000 --message "Python UDP test"
   ```
   Before moving on, stop the UDP server (`Ctrl+C`) and restart it in **TCP** mode for the next exercise.

-----

### Exercise 1.2: Demystifying HTTP over a TCP Socket

**Goal:** Verify experimentally that **HTTP** (used by web browsers and REST APIs) is simply **structured plain text sent over a TCP socket**.

1. **Terminal 1:** Ensure your echo server is running in **TCP** mode:
   ```bash
   $ python3 echo_server.py tcp --port 9000
   ```
2. **Terminal 2:** Instead of `nc`, send an HTTP request using **`curl`**:
   ```bash
   $ curl -v http://127.0.0.1:9000/hello
   ```
3. **Inspect what happened in both terminals:**
   * In **Terminal 1 (`echo_server.py`)**, the server received and logged the raw HTTP request sent by `curl`:
     ```text
     GET /hello HTTP/1.1
     Host: 127.0.0.1:9000
     User-Agent: curl/...
     Accept: */*
     ```
   * In **Terminal 2 (`curl`)**, the command failed (e.g., `Unsupported HTTP version` or `Received HTTP/0.9 when not allowed`). **Why?** Because `echo_server.py` echoed the raw `GET /hello HTTP/1.1...` request back instead of returning a valid HTTP response (`HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n...`).
4. Stop the TCP server in Terminal 1 (`Ctrl+C`).

> **Takeaway:** You *could* manually parse HTTP methods (`GET`, `POST`), paths (`/hello`), headers, and status codes (`200`, `404`) over raw TCP sockets — but you would be reinventing an HTTP server. Frameworks like **FastAPI** handle all of that for you.

-----

### Exercise 1.3: FastAPI IP Geolocation Caching Service (REST API)

**Goal:** Run and test a Python **REST API** built with **FastAPI** that automates the IP geolocation lookup (performed manually with `curl` in Class 07) and implements a **local disk cache** (`ip_cache.json`).

**Architecture Details (`ex03/main.py`):**

* **Local REST Server:** Exposes `GET /ip/{ip_address}` on port `8000` and automatically generates interactive documentation at `/docs`.
* **External REST Client:** On a *Cache Miss* (or after `CACHE_DEADLINE_SECONDS`), the service uses `requests` to query `http://ip-api.com/json/{ip_address}`.
* **HTTP Status Codes:** Private IP addresses (RFC 1918, such as `192.168.x.x`) are not routable on the public Internet, so the external lookup fails and FastAPI returns **`404 Not Found`**.

**Instructions:**

1. Create the `ex03` directory, download and extract `ex03.zip` (from the `"resources"` folder associated with this class on the course eLearning platform — `main.py`, `requirements.txt`, `ip-address.png`), activate a virtual environment, and install dependencies:
   ```bash
   $ mkdir -p ~/IEI/aula08/ex03 && cd ~/IEI/aula08/ex03
   # (Extract ex03.zip from eLearning here: unzip ex03.zip)
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
2. **Start the FastAPI server using Uvicorn (Terminal 1):**
   ```bash
   $ uvicorn main:app --reload
   ```
3. **Test the API from a second terminal (`curl`):**
   * **Test 1 — *Cache Miss* (queries external API):**
     ```bash
     # Private IP (expected HTTP 404)
     $ curl -i http://127.0.0.1:8000/ip/192.168.132.132

     # Google DNS, MEO, and University of Aveiro
     $ curl -s http://127.0.0.1:8000/ip/8.8.8.8
     $ curl -s http://127.0.0.1:8000/ip/144.64.3.83
     $ curl -s http://127.0.0.1:8000/ip/193.137.169.135
     ```
     Check Terminal 1 logs: you should see `"Querying external API for ..."`.
   * **Test 2 — *Cache Hit* (served from local cache):**
     Repeat the requests for `8.8.8.8` and `193.137.169.135`. Check the logs (`"Returning cached data for ..."`) and inspect the generated cache file (`cat ip_cache.json`).
4. **Inspect the Code (`main.py`):**
   Open `main.py` and locate:
   * How and where the IP lookup REST endpoint is implemented;
   * Which library and external API URL are called on a *Cache Miss*;
   * How responses are stored and reused via `ip_cache.json`.
5. **Explore Interactive Documentation (Swagger UI):**
   Open **`http://127.0.0.1:8000/docs`** in your web browser and test an endpoint directly from the web UI (*Try it out*).
6. Stop `uvicorn` in Terminal 1 (`Ctrl+C`) and exit the virtual environment (`deactivate`).

-----

## Block 2: Decoupled Real-Time Communication (MQTT)

In **Block 1**, every client needed to know the server's exact **IP and Port**, and direct peer-to-peer connections between laptops are blocked on `eduroam`.
In **Block 2**, we switch to the **Publish/Subscribe** pattern using an **MQTT Broker**: clients only connect outbound to the *broker* and publish/subscribe to hierarchical **topics**, completely decoupling senders from receivers.

### Exercise 2.1: Docker MQTT Broker & Serverless WebSocket Chat

**Goal:** Run an **Eclipse Mosquitto** broker in Docker and connect a pure JavaScript web client (`MQTT.js` over WebSockets) to build a real-time chat application **without writing any server code**.

**Architecture Details (`ex04`):**

* **Broker (`mosquitto`):** `compose.yml` launches `eclipse-mosquitto` configured via `mqtt/mosquitto.conf` with anonymous access and two listeners: **`1883`** (standard MQTT over TCP) and **`9001`** (MQTT over **WebSockets**, required by browsers).
* **Frontend (`nginx`):** `nginx:alpine` serves `html/index.html` on port **`8080`**.
* **Last Will and Testament (LWT):** Upon connecting, each client registers a "last will" message with the broker; if a browser tab closes abruptly, the broker automatically publishes the leave notification.

**Instructions:**

1. Create the `ex04` directory, download and extract `ex04.zip` (from the `"resources"` folder associated with this class on the course eLearning platform — `compose.yml`, `mqtt/mosquitto.conf`, `html/index.html`), and start the containers:
   ```bash
   $ mkdir -p ~/IEI/aula08/ex04 && cd ~/IEI/aula08/ex04
   # (Extract ex04.zip from eLearning here: unzip ex04.zip)
   $ docker compose up -d
   $ docker compose ps
   ```
2. **Local Multi-Tab Test:**
   * Open **`http://localhost:8080/`** in **two separate browser tabs**.
   * Keep the *Broker URL* as `ws://localhost:9001` and the topic as `class/chat/main_room`.
   * Enter different usernames (e.g., `alice` and `bob`), click **Connect**, and exchange messages between tabs.
   * **LWT Test:** Abruptly close `alice`'s browser tab and observe `"alice left the chat."` appear automatically in `bob`'s tab after a few seconds.
3. **Classroom Collaboration over `eduroam` (No Special Wi-Fi Needed):**
   * Reload `http://localhost:8080/`.
   * While staying on `eduroam`, change the *Broker URL* from `ws://localhost:9001` to a public WebSocket-enabled MQTT broker:
     * `ws://broker.hivemq.com:8000/mqtt` *(or `ws://test.mosquitto.org:8080`)*
   * Set a shared classroom topic (e.g., **`ua/iei/aula08/chat`**), enter your username, and click **Connect**.
   * Chat with the rest of the class! *(Notice how isolated laptops on `eduroam` communicate in real time because all connections are outbound to the shared broker).*
4. **Inspect the Implementation (`compose.yml`, `mqtt/mosquitto.conf`, and `html/index.html`):**
   Open the project files and identify, in broad terms, how the application is put together:
   * **Infrastructure (`compose.yml` and `mqtt/mosquitto.conf`):** which containers are started, which ports separate standard MQTT from WebSockets, and what access rules are configured on the broker;
   * **Web Client (`html/index.html`):** which JavaScript library connects to the broker, how `subscribe` and `publish` are handled (including the message payload structure), and where the *Last Will and Testament (LWT)* message is configured.
5. **Mandatory Cleanup:** Stop the containers before starting Exercise 2.2 so ports `1883`, `9001`, and `8080` are freed:
   ```bash
   $ docker compose down
   ```

-----

### Exercise 2.2: Real-Time Telemetry with `paho-mqtt`, `psutil`, and Plotly

**Goal:** Build a **100% software** IoT/system telemetry pipeline: a Python publisher (`paho-mqtt`) streams JSON measurements to the Mosquitto broker, feeding both a **live browser chart** (Plotly.js) and a **CLI alert subscriber** simultaneously.

The publisher (`main.py`) supports **two telemetry modes**:
* **`--mode env` (Simulated Environmental Data):** Simulates a temperature (`°C`) and humidity (`%`) sensor using a smooth random walk.
* **`--mode system` (Real Laptop Telemetry):** Reads your computer's live **CPU (%)** and **RAM (%)** utilization using `psutil`.

**Instructions:**

1. Create the `ex05` directory, download and extract `ex05.zip` (from the `"resources"` folder associated with this class on the course eLearning platform):
   ```bash
   $ mkdir -p ~/IEI/aula08/ex05 && cd ~/IEI/aula08/ex05
   # (Extract ex05.zip from eLearning here: unzip ex05.zip)
   ```
2. **Start the Docker infrastructure (`mosquitto` + `nginx`):**
   ```bash
   $ docker compose up -d
   ```
3. **Set up the Python virtual environment:**
   ```bash
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
4. **Open the Web Dashboard:**
   * Navigate to **`http://localhost:8080/`** in your browser.
   * Verify *Broker Host* is **`localhost`** and *Topic* is **`deti/pico/dht11`**.
   * Click **Connect** (status should change to `Status: Connected`).
5. **Scenario A — Publish Simulated Environmental Data (`--mode env`):**
   In **Terminal 1** (with `.venv` active), start the publisher in environmental mode:
   ```bash
   $ python main.py --mode env
   ```
   Watch the Temperature (`°C`) and Humidity (`%`) traces update every 2 seconds in real time on the web chart.
6. **Scenario B — Run a Second CLI Alert Subscriber (`subscriber.py`):**
   Open **Terminal 2**, activate the virtual environment, and launch the subscriber using an MQTT single-level wildcard (`+`) and a threshold:
   ```bash
   $ cd ~/IEI/aula08/ex05
   $ source .venv/bin/activate
   $ python subscriber.py --topic "deti/pico/+" --threshold 24.0
   ```
   Observe that **both the web dashboard and the Python terminal receive every message simultaneously** (*broker fan-out*), and `[WARNING] ALERT ...` logs appear whenever the threshold is exceeded.
7. **Scenario C — Publish Real Laptop Telemetry (`--mode system`):**
   In **Terminal 1**, stop `--mode env` (`Ctrl+C`) and start system telemetry mode:
   ```bash
   $ python main.py --mode system
   ```
   * Notice in the browser that the chart axes automatically switch to **CPU Usage (%)** and **RAM Usage (%)**.
   * Open a heavy web page or run a CPU-intensive command to observe live CPU spikes both on the Plotly chart and in Terminal 2's alerts!
8. **Inspect and Modify the Code (`main.py`, `subscriber.py`, and `html/index.html`):**
   * **Inspect the Implementation:** locate in `main.py` how metrics are collected with `psutil` and how the JSON payload is structured; then compare with `subscriber.py` and `html/index.html` to see how both subscribers distinguish between environmental and system modes and update their alerts/charts accordingly.
   * **Try a Modification:** test changing the publish rate using `main.py`'s `--interval` option, and try modifying `subscriber.py` so it also logs an alert whenever the secondary metric (humidity or RAM) exceeds a threshold of your choice.
9. **Optional Challenge (Class-wide Telemetry over `eduroam`):**
   Pass `--host test.mosquitto.org` to `main.py` and `subscriber.py` (and set *Broker Host* in the browser to `test.mosquitto.org`) using a unique topic such as `--topic "ua/iei/aula08/<student_id>"`, then subscribe to a classmate's topic to visualize their machine's telemetry live.
10. **Cleanup:** Stop the Python scripts (`Ctrl+C`) and tear down the Docker stack:
   ```bash
   $ docker compose down
   ```

-----

## Comparative Summary: Block 1 vs. Block 2

| Dimension | Block 1: Raw Sockets & REST API | Block 2: MQTT (Publish/Subscribe) |
| :--- | :--- | :--- |
| **Paradigm** | **Request / Response** (Direct Client-Server) | **Publish / Subscribe** (Event-driven via Broker) |
| **Protocols** | TCP / UDP (`socket`) and HTTP (`FastAPI`) | MQTT over TCP (`1883`) and WebSockets (`9001`) |
| **Coupling** | Client must know the server's exact `IP:Port` | Decoupled: clients only know the Broker and **Topic** |
| **Over `eduroam`** | Blocked between students (*Client Isolation*) | Works across students via an external Broker |
| **Typical Use Cases** | Web services, public APIs, direct transfers, games | IoT telemetry, real-time monitoring, chat, notifications |
