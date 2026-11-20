---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Programação em Redes: Sockets, APIs REST & MQTT"
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

## Visão Geral da Sessão

  * **Parte I — Fundamentos de Programação em Rede: Sockets Puros (TCP vs. UDP) e Concorrência:**
      * Ponte com a Aula 07 (`IP:Porta`, `127.0.0.1` vs. `0.0.0.0`, `ss`/`lsof`), **TCP vs. UDP**, *3-way handshake* vs. datagramas, implementação em Python (`socket`), **I/O Bloqueante** e concorrência com **`asyncio`**.
  * **Parte II — Da Camada de Transporte à Aplicação: HTTP e APIs REST:**
      * O que viaja dentro de um *socket* TCP quando usamos `curl`, princípios de **APIs REST**, formato **JSON**, construção de serviços com **FastAPI** e documentação automática (*Swagger UI*).
  * **Parte III — O Paradigma Publish/Subscribe e o Protocolo MQTT (IoT & Tempo Real):**
      * *Request/Response* vs. *Publish/Subscribe*, desacoplamento e *fan-out*, arquitetura com **Broker Mosquitto** (TCP `1883` + WebSockets `9001`), **Tópicos**, *Wildcards*, **QoS**, **LWT** e telemetria em Python (`paho-mqtt` + `psutil`).
  * **Síntese Arquitetural & Recursos:**
      * Comparação das arquiteturas abordadas na sessão e documentação de referência.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Sockets Puros (TCP vs. UDP) e Concorrência}}
\end{center}

-----

## Da Aula 07 para o Código: O Que é um *Socket*?

Na Aula 07 usámos `ss -tuln` / `lsof`, `curl` e `nc` para inspecionar serviços em execução. Mas como é que um programa abre uma porta no sistema operativo?

  * **O *Socket* (Camada 4 — Transporte):**
      * É um ponto terminal (*endpoint*) de comunicação bidirecional gerido pelo *kernel* do sistema operativo e exposto ao programa como um descritor de ficheiro.
      * Cada *socket* em escuta é identificado pelo par **`IP:Porta`** (ex.: `127.0.0.1:9000` ou `0.0.0.0:8000`).
  * **Recordar a Aula 07 (`bind address`):**
      * **`127.0.0.1` (*Loopback*):** O *socket* aceita apenas ligações originadas na própria máquina (ideal para desenvolvimento local).
      * **`0.0.0.0` (`INADDR_ANY`):** O *socket* aceita ligações em todas as interfaces de rede da máquina (LAN, Docker, Wi-Fi).
  * **Dois protocolos fundamentais da Internet:**
      * **TCP** (*Transmission Control Protocol* $\rightarrow$ `socket.SOCK_STREAM`)
      * **UDP** (*User Datagram Protocol* $\rightarrow$ `socket.SOCK_DGRAM`)

-----

## TCP vs. UDP: Os Dois Pilares da Camada de Transporte

| Característica | TCP (*Transmission Control Protocol*) | UDP (*User Datagram Protocol*) |
| :--- | :--- | :--- |
| **Conexão** | Orientado à conexão (estabelece sessão) | Sem conexão (*stateless*, "disparar e esquecer") |
| **Fiabilidade** | **Fiável:** Garante entrega, ordem e retransmissão | **Não fiável:** Sem garantia de entrega nem de ordem |
| **Sobrecarga** | Elevada (*3-way handshake*, ACKs, controlo de fluxo) | Mínima (cabeçalho de apenas 8 bytes) |
| **Latência** | Mais lenta devido às confirmações e ordenação | Mais rápida, sem estabelecimento prévio de sessão |
| **Módulo Python** | `socket.SOCK_STREAM` (fluxo contínuo de bytes) | `socket.SOCK_DGRAM` (mensagens discretas) |
| **Casos de Uso** | Web (HTTP/REST), SSH, Email, Transferência de ficheiros | Streaming áudio/vídeo, Jogos online, DNS, VoIP |

\vspace{0.5em}

  * **Nota prática:** Em TCP lemos um fluxo contínuo de bytes (*stream*); em UDP recebemos datagramas individuais com o endereço do remetente anexado a cada pacote.

-----

## Padrões de Comunicação: TCP (*Handshake*) vs. UDP (Datagramas)

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
% --- Lado Esquerdo: TCP ---
\node[font=\footnotesize\bfseries] at (2.2, 5.2) {TCP (Orientado à Conexão)};
\node[actor] (tc) at (0.7, 4.65) {Cliente};
\node[actor] (ts) at (3.7, 4.65) {Servidor};
\draw[lifeline] (tc.south) -- (0.7, 0.40);
\draw[lifeline] (ts.south) -- (3.7, 0.40);

% 3-way handshake
\draw[msg] (0.7, 4.20) -- node[above, sloped, font=\tiny\ttfamily] {1. SYN} (3.7, 4.02);
\draw[msg] (3.7, 3.84) -- node[above, sloped, font=\tiny\ttfamily] {2. SYN-ACK} (0.7, 3.66);
\draw[msg] (0.7, 3.48) -- node[above, sloped, font=\tiny\ttfamily] {3. ACK} (3.7, 3.30);

% Envio normal + ACK
\draw[datamsg] (0.7, 2.98) -- node[above, sloped, font=\tiny\ttfamily] {Dados 1 ("Ola")} (3.7, 2.80);
\draw[msg] (3.7, 2.62) -- node[above, sloped, font=\tiny\ttfamily] {ACK 1} (0.7, 2.44);

% Falha + Timeout + Retransmissão + ACK
\draw[lostmsg] (0.7, 2.12) -- node[above, sloped, font=\tiny\ttfamily] {Dados 2 ("IEI")} (2.35, 2.00);
\node[font=\tiny\bfseries, color=red!75!black] at (2.55, 2.00) {X};
\node[font=\tiny\itshape, color=orange!80!black, anchor=east] at (0.65, 1.72) {Timeout};
\draw[datamsg, color=orange!80!black] (0.7, 1.66) -- node[above, sloped, font=\tiny\ttfamily] {Retransm. Dados 2} (3.7, 1.48);
\draw[msg] (3.7, 1.30) -- node[above, sloped, font=\tiny\ttfamily] {ACK 2} (0.7, 1.12);

% Fecho
\draw[msg, color=red!70!black] (0.7, 0.78) -- node[above, sloped, font=\tiny\ttfamily] {FIN / ACK} (3.7, 0.60);
\node[note] at (2.2, 0.15) {Resultado no Servidor: \textbf{"Ola IEI"} (completo e ordenado)};

% Separador central
\draw[dotted, thick, color=black!35] (5.3, 5.3) -- (5.3, 0.05);

% --- Lado Direito: UDP ---
\node[font=\footnotesize\bfseries] at (8.2, 5.2) {UDP (Datagramas sem Sessão)};
\node[actor] (uc) at (6.7, 4.65) {Cliente};
\node[actor] (us) at (9.7, 4.65) {Servidor};
\draw[lifeline] (uc.south) -- (6.7, 0.40);
\draw[lifeline] (us.south) -- (9.7, 0.40);

\draw[udpmsg] (6.7, 4.00) -- node[above, sloped, font=\tiny\ttfamily] {Datagrama 1 ("Ola")} (9.7, 3.76);
\draw[lostmsg] (6.7, 3.15) -- node[above, sloped, font=\tiny\ttfamily] {Datagrama 2 ("IEI")} (8.35, 3.00);
\node[font=\tiny\bfseries, color=red!75!black] at (8.95, 3.00) {X (perdido)};
\draw[udpmsg] (9.7, 2.25) -- node[above, sloped, font=\tiny\ttfamily] {Datagrama Resposta} (6.7, 2.01);
\node[note] at (8.2, 0.90) {Resultado no Servidor: apenas \textbf{"Ola"}\\(sem ACK, sem retransmissão, menor latência).};
\end{tikzpicture}
\end{center}

-----

## Ciclo de Vida de um Socket TCP em Python (Servidor e Cliente)

::::: columns
::: {.column width="56%"}

  * **Servidor TCP (`echo_server.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 9000))
    s.listen() # Coloca o socket em estado LISTEN
    while True:
        conn, addr = s.accept() # Bloqueia até haver cliente
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break # Cliente fechou a ligação
                conn.sendall(data) # Eco
```

:::
::: {.column width="44%"}

  * **Cliente TCP (`echo_client.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 9000))
    s.sendall(b"Ola, IEI!")
    reply = s.recv(1024)
    print(reply.decode())
```

:::
:::::

\vspace{0.3em}

  * **Fluxo típico:**
      1. `bind()` associa o *socket* a `IP:Porta` e `listen()` abre a fila de ligações.
      2. `accept()` cria um **novo *socket*** (`conn`) dedicado a cada cliente que se liga via `connect()`.
      3. O servidor pode ser testado com `nc 127.0.0.1 9000` e observado com `ss -tuln` / `lsof`.

-----

## Sockets sem Sessão em Python: Servidor e Cliente UDP

::::: columns
::: {.column width="54%"}

  * **Servidor UDP (`echo_server.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(("127.0.0.1", 9000))
    # Não existe listen() nem accept()!
    while True:
        data, addr = s.recvfrom(1024)
        s.sendto(data, addr) # Responde ao remetente
```

:::
::: {.column width="46%"}

  * **Cliente UDP (`echo_client.py`):**

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Ola UDP!", ("127.0.0.1", 9000))
    reply, addr = s.recvfrom(1024)
    print(reply.decode())
```

:::
:::::

\vspace{0.3em}

  * **Diferenças-chave face ao TCP:**
      1. Não aparece em estado `LISTEN` no `ss`/`lsof` (não existem `listen()` nem `accept()`).
      2. `recvfrom()` devolve os dados **e** o tuplo `(ip, porta)` do cliente para cada pacote recebido.
      3. O servidor pode ser testado com `nc -u 127.0.0.1 9000`.

-----

## O Problema do I/O Bloqueante (*Blocking I/O*)

Os *sockets* padrão em Python são **bloqueantes** por omissão:

  * `s.accept()` **para o programa** até um cliente estabelecer ligação.
  * `conn.recv(1024)` **para o programa** até chegarem bytes pela rede ou o cliente desligar.
  * **Consequência prática:** Enquanto o servidor está a atender o Cliente A no ciclo `recv()`, o Cliente B fica pendurado à espera!

\vspace{0.4em}

  * **Abordagem Tradicional — *Multi-threading*:**
      * Criar uma *thread* do sistema operativo por cada cliente ligado.
      * **Desvantagens:** Complexidade de sincronização (*locks*, *race conditions*), elevado consumo de memória com milhares de ligações e o **GIL (*Global Interpreter Lock*)** no CPython impede paralelismo real de CPU em código Python.

-----

## A Solução Moderna: Concorrência com I/O Assíncrono (`asyncio`)

O módulo **`asyncio`** permite que **uma única *thread*** gira milhares de ligações concorrentes usando um **Event Loop** (ciclo de eventos):

::::: columns
::: {.column width="44%"}

  * **Como funciona:**
      * As palavras-chave `async` e `await` suspendem uma tarefa enquanto espera por dados da rede, libertando o ciclo de eventos para atender outros clientes.
      * *Nota:* É **concorrência** (esperar eficientemente por I/O), não execução paralela de CPU.
      * É a base de frameworks modernas como o **FastAPI** e **`websockets`**.

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
{\LARGE \textbf{Parte II: HTTP e APIs REST}}
\end{center}

-----

## Desmistificar o HTTP: O Que Viaja Dentro do Socket TCP?

O protocolo **HTTP** (*HyperText Transfer Protocol*) não é magia: é simplesmente **texto estruturado enviado dentro de um *socket* TCP**!

::::: columns
::: {.column width="50%"}

  * **Quando executa no terminal:**
    ```bash
    $ curl http://127.0.0.1:9000/ola
    ```
  * **O seu servidor TCP (`echo_server.py`) recebe:**
    ```http
    GET /ola HTTP/1.1
    Host: 127.0.0.1:9000
    User-Agent: curl/8.5.0
    Accept: */*
    ```

:::
::: {.column width="50%"}

  * **O que o `curl` espera receber de volta:**
    ```http
    HTTP/1.1 200 OK
    Content-Type: application/json

    {"message": "Ola, IEI!"}
    ```
  * **Por que não fazemos APIs com sockets puros?** Teríamos de programar manualmente o *parsing* de rotas, cabeçalhos, códigos de erro e JSON. Por isso usamos frameworks como o **FastAPI**.

:::
:::::

-----

## APIs REST: A Linguagem Padrão da Web

**REST** (*REpresentational State Transfer*) é o estilo arquitetural dominante para serviços Web e APIs sobre HTTP:

::::: columns
::: {.column width="48%"}

  * **Princípios Essenciais:**
      * **Stateless (Sem estado):** Cada pedido contém toda a informação necessária para ser processado.
      * **Recursos:** Identificados por URIs (ex.: `/ip/8.8.8.8`, `/users/42`).
      * **Verbos HTTP:** `GET` (ler), `POST` (criar), `PUT` (atualizar), `DELETE` (apagar).
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

## O Formato de Dados: JSON (*JavaScript Object Notation*)

**JSON** é o padrão *de facto* para troca de dados estruturados em APIs REST (e também em mensagens MQTT):

::::: columns
::: {.column width="50%"}

  * **Características:**
      * Leve, textual e legível por humanos.
      * Pares chave-valor com tipos primitivos: *strings*, números, booleanos, listas (`[]`) e objetos aninhados (`{}`).
  * **Em Python (`import json`):**
      * `json.dumps(dict_py)` $\rightarrow$ converte dicionário para texto JSON.
      * `json.loads(texto_json)` $\rightarrow$ converte texto JSON para dicionário.

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

## Construção de APIs REST em Python com FastAPI

**FastAPI** é uma framework moderna sobre `asyncio` (executada com **`uvicorn`**) que valida tipos e gera documentação interativa automática em **`/docs`** (*Swagger UI*):

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

  * **Aceder aos *endpoints* da API (`uvicorn main:app --reload`):**
      * Raiz (`/`): `curl http://127.0.0.1:8000/` | Consulta IP: `curl http://127.0.0.1:8000/ip/8.8.8.8`
      * Documentação interativa (Swagger UI): `http://127.0.0.1:8000/docs`

-----

## Documentação Automática no FastAPI (*Swagger UI*)

\begin{center}
\includegraphics[width=\linewidth,height=0.76\textheight,keepaspectratio]{figures/fastapi_swagger_docs.jpg}
\end{center}

-----

## Sockets Puros vs. APIs REST: Quando Usar Cada Um?

| Característica | Sockets Puros (TCP / UDP) | APIs REST (HTTP + JSON) |
| :--- | :--- | :--- |
| **Nível de Abstração** | **Baixo nível** (Camada 4 — Transporte) | **Alto nível** (Camada 7 — Aplicação) |
| **Protocolo** | TCP / UDP com formato próprio | HTTP/HTTPS padronizado |
| **Estado** | Pode manter sessão aberta (*stateful*) | **Stateless** por definição |
| **Formato dos Dados** | Qualquer formato (binário ou texto) | Tipicamente **JSON** |
| **Ferramentas** | `nc`, `ss`/`lsof`, código `socket` | `curl`, browsers, Swagger (`/docs`), FastAPI |
| **Quando Usar** | Protocolos próprios, jogos, baixa latência | Serviços Web, backends, apps móveis, integração |

\vspace{0.5em}

  * **Limitação comum:** Tanto nos *sockets* puros como nas APIs REST, é o **cliente que inicia o pedido** (*client-pull*) e precisa de conhecer exatamente o **`IP:Porta`** do servidor.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: O Paradigma Publish/Subscribe e o Protocolo MQTT}}
\end{center}

-----

## Porquê Um Novo Paradigma? *Request/Response* vs. *Publish/Subscribe*

No modelo **Request/Response**, cliente e servidor estão acoplados: o emissor precisa de conhecer exatamente o **`IP:Porta`** de cada destinatário.

  * **Limitações do acoplamento direto:**
      * Difícil de escalar em cenários *1-para-N* ou *N-para-M*.
      * Exige acesso direto ao recetor (muitas vezes bloqueado por **NAT/Firewalls**) e que este esteja ativo no momento do envio.
  * **Solução — Padrão *Publish/Subscribe* (MQTT):**
      * **Publisher:** Publica mensagens num **Tópico** (ex.: `sensores/sala1/temp`), sem saber *quem* ouve.
      * **Subscriber:** Subscreve apenas os **Tópicos** que lhe interessam, sem saber *quem* publicou.
      * **Broker:** Intermédio que recebe as mensagens e as reencaminha apenas aos subscritores interessados.

\vspace{0.2em}

  * **Principais vantagens deste paradigma:**
      * **Subscrição Seletiva:** Cada recetor escolhe exatamente a informação que quer receber, sem listas de destinatários no emissor.
      * **Escalabilidade:** O *Publisher* envia uma única vez para o *Broker* (para 1 ou 10\,000 *Subscribers*), permitindo adicionar/remover clientes dinamicamente.

-----

## Arquitetura *Publish/Subscribe* no MQTT

\vspace{0.2em}

\begin{center}
\begin{tikzpicture}[
    nodebox/.style={rectangle, draw=black!75, fill=black!4, rounded corners=3pt, thick, font=\scriptsize, align=center, inner sep=4pt, minimum width=2.7cm, minimum height=0.85cm},
    broker/.style={rectangle, draw=uagreen!80!black, fill=uagreen!15, rounded corners=4pt, thick, font=\scriptsize\bfseries, align=center, inner sep=6pt, minimum width=2.8cm, minimum height=2.6cm},
    pubt/.style={-{Latex[length=1.7mm]}, thick, color=blue!75!black},
    pubf/.style={-{Latex[length=1.7mm]}, thick, color=orange!80!black}
]
% Publishers à esquerda
\node[nodebox] (p1) at (0, 2.3) {\textbf{Sensor Temperatura}\\{\tiny Publica: \texttt{casa/sala/temp}}};
\node[nodebox] (p2) at (0, 0.3) {\textbf{Sensor Fumo}\\{\tiny Publica: \texttt{casa/cozinha/fumo}}};

% Broker no centro
\node[broker] (b) at (4.8, 1.3) {\textbf{Broker MQTT}\\[0.2em]{\tiny Recebe e encaminha}\\{\tiny por \textbf{Tópico}}};

% Subscribers à direita
\node[nodebox] (s1) at (9.7, 2.6) {\textbf{App Telemóvel}\\{\tiny Subscreve: \texttt{casa/sala/temp}}};
\node[nodebox] (s2) at (9.7, 1.3) {\textbf{Painel Central}\\{\tiny Subscreve: \texttt{casa/\#}}};
\node[nodebox] (s3) at (9.7, 0.0) {\textbf{Sistema de Alarme}\\{\tiny Subscreve: \texttt{casa/+/fumo}}};

% Ligações
\draw[pubt] (p1.east) -- node[above, sloped, font=\tiny\ttfamily] {22.5 C} (b.north west);
\draw[pubf] (p2.east) -- node[below, sloped, font=\tiny\ttfamily] {OK} (b.south west);

\draw[pubt] (b.north east) -- node[above, sloped, font=\tiny\ttfamily] {temp} (s1.west);
\draw[pubt] ($(b.east)+(0,0.12)$) -- node[above, font=\tiny\ttfamily] {temp} ($(s2.west)+(0,0.12)$);
\draw[pubf] ($(b.east)-(0,0.12)$) -- node[below, font=\tiny\ttfamily] {fumo} ($(s2.west)-(0,0.12)$);
\draw[pubf] (b.south east) -- node[below, sloped, font=\tiny\ttfamily] {fumo} (s3.west);
\end{tikzpicture}
\end{center}

\vspace{0.2em}

  * **Desacoplamento:** Os sensores desconhecem quantos subscritores existem (e vice-versa); só o *Broker* conhece os clientes ligados.
  * ***Fan-out* Seletivo:** Cada mensagem é publicada **uma vez** e entregue em simultâneo apenas a quem subscreveu o respetivo tópico.

-----

## Conceitos Fundamentais do MQTT: Tópicos, *Wildcards*, QoS e LWT

  * **Tópicos Hierárquicos e *Wildcards*:**
      * Strings separadas por `/` (ex.: `deti/pico/dht11`, `ua/iei/aula08/chat`).
      * **`+` (nível único):** `deti/+/dht11` corresponde a `deti/pico/dht11` e `deti/sala1/dht11`.
      * **`#` (múltiplos níveis):** `deti/#` subscreve todos os subtópicos abaixo de `deti/`.
  * **Qualidade de Serviço (QoS — *Quality of Service*):**
      * **`QoS 0`:** No máximo uma vez (*fire and forget*, menor sobrecarga).
      * **`QoS 1`:** Pelo menos uma vez (garante entrega, pode duplicar).
      * **`QoS 2`:** Exatamente uma vez (garante entrega única, mais lento).
  * ***Last Will & Testament* (LWT):**
      * Mensagem registada previamente pelo cliente ao ligar-se; se a ligação cair abruptamente (ex.: fechar separador do browser), o **Broker** publica a mensagem em seu nome (ex.: `"alice left the chat"`).

-----

## MQTT na Prática (I): O *Broker* e Transportes (TCP vs. WebSockets)

O protocolo MQTT tradicional corre sobre **TCP (porta `1883`)**, mas os navegadores Web não permitem abrir *sockets* TCP puros em JavaScript:

::::: columns
::: {.column width="45%"}

  * **Configuração do *Broker* (`mosquitto.conf`):**
    ```text
    allow_anonymous true

    listener 1883
    protocol mqtt          # Clientes nativos

    listener 9001
    protocol websockets    # Browsers Web
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
% Caixa do Broker
\draw[brokerbox] (2.65, -0.35) rectangle (4.75, 2.85);
\node[font=\scriptsize\bfseries] at (3.70, 2.58) {Broker MQTT};
\node[font=\tiny, color=black!65] at (3.70, -0.12) {Docker / Público};

% Portas
\node[port] (p1) at (3.70, 1.85) {:1883 (TCP)};
\node[port] (p2) at (3.70, 0.55) {:9001 (WS)};

% Clientes
\node[client] (c1) at (0.0, 1.85) {\textbf{Clientes Nativos}\\{\tiny Python / CLI / IoT}};
\node[client] (c2) at (0.0, 0.55) {\textbf{Clientes Web}\\{\tiny Browser (JS)}};

% Ligações
\draw[arr1] (c1.east) -- node[above, font=\tiny\ttfamily] {mqtt://} (p1.west);
\draw[arr2] (c2.east) -- node[above, font=\tiny\ttfamily] {ws://} (p2.west);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## MQTT na Prática (II): Publicador de Telemetria em Python (`paho-mqtt`)

Com a biblioteca **`paho-mqtt`** e **`psutil`**, podemos enviar telemetria simulada ou métricas reais da máquina em formato **JSON**:

```python
import json, time
import paho.mqtt.client as mqtt
import psutil

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iei_pub_01")
client.connect("localhost", 1883, keepalive=60)
client.loop_start()  # Gere a rede numa thread em segundo plano

while True:
    payload = {
        "ts": time.time(),
        "t": round(psutil.cpu_percent(interval=None), 1),        # CPU (%) ou Temp
        "h": round(psutil.virtual_memory().percent, 1),          # RAM (%) ou Humidade
        "mode": "system",
    }
    client.publish("deti/pico/dht11", json.dumps(payload), qos=0)
    time.sleep(2)
```

-----

## MQTT na Prática (III): Subscritor e Monitorização de Alertas em Python

O cliente subscritor funciona de forma **orientada a eventos** através de funções de *callback* (`on_connect` e `on_message`):

```python
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe("deti/pico/+")  # Subscreve com wildcard '+'

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if data["t"] >= 28.0:
        print(f"ALERTA em {msg.topic}: valor={data['t']}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, keepalive=60)
client.loop_forever()  # Bloqueia processando mensagens e reconexões
```

-----

## Síntese Arquitetural & Recursos

| Arquitetura / Tecnologia | Paradigma | Ponto Forte Principal | Casos de Uso Típicos |
| :--- | :--- | :--- | :--- |
| **Sockets Puros (TCP/UDP)** | Request/Response ou livre | Controlo total (Camada 4) | Protocolos próprios, jogos, ensino |
| **Sockets com `asyncio`** | Concorrente (*Event Loop*) | Milhares de ligações sem *threads* | Servidores TCP/UDP escaláveis |
| **API REST (FastAPI)** | Request/Response (HTTP) | Padronização, JSON, `/docs` | Serviços Web, APIs públicas, backends |
| **MQTT (TCP & WebSockets)** | Publish/Subscribe (Broker) | Desacoplamento, *fan-out*, leve | Telemetria em tempo real, alertas, IoT |

\vspace{0.5em}

  * **Recursos e Documentação de Referência:**
      * [Python `socket` — Programação de Baixo Nível](https://docs.python.org/3/library/socket.html)
      * [Python `asyncio` — I/O Assíncrono](https://docs.python.org/3/library/asyncio.html)
      * [FastAPI — Documentação Oficial](https://fastapi.tiangolo.com/)
      * [Eclipse Paho-MQTT (Python)](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html) e [Especificação MQTT](https://mqtt.org/)
