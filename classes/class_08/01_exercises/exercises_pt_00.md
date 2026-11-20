---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Programação em Redes: Sockets, APIs REST & MQTT"
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

# Guião Prático de Laboratório

**Enquadramento Pedagógico & Objetivos:**
Na **Aula 07**, inspecionámos interfaces de rede, diagnosticámos ligações com `ss`/`lsof`, `curl` e `nc` e analisámos porque é que redes como a `eduroam` bloqueiam ligações diretas entre dispositivos (*Client Isolation*). Nesta sessão laboratorial de **3 horas**, totalmente executável **em software** no seu portátil (Linux, macOS ou WSL) sem necessidade de hardware dedicado ou redes Wi-Fi especiais, passamos da observação à **construção de aplicações em rede em Python** através de dois grandes blocos:

* **Parte 0 — Preparação do Ambiente & Boas Práticas em Python:** Instalação dos utilitários necessários, configuração de ambientes virtuais (`venv`), utilização correta do módulo `logging` e arquitetura de comunicação local vs. *brokers* na `eduroam`.
* **Bloco 1 — Comunicação Direta Cliente-Servidor (*Request/Response*):**
  * **Exercício 1.1:** Implementação e teste de um Servidor e Cliente de Eco com **Sockets Puros** em Python (`tcp` e `udp`), teste com `nc` (`netcat`) e inspeção de portas em escuta (`ss` / `lsof`).
  * **Exercício 1.2:** Desmistificar o protocolo **HTTP** observando, diretamente no servidor de *sockets* TCP, o texto enviado pelo comando `curl`.
  * **Exercício 1.3:** Construção e teste de uma **API REST** com **FastAPI** e cache local (`ex03`), atuando simultaneamente como servidor REST local (`127.0.0.1:8000` e `/docs`) e cliente de uma API externa.
* **Bloco 2 — Comunicação Desacoplada em Tempo Real (*Publish/Subscribe* com MQTT):**
  * **Exercício 2.1:** Execução de um *broker* **Eclipse Mosquitto** em Docker e de uma aplicação Web de **Chat *Serverless* sobre WebSockets** (`ex04`), testando *Last Will and Testament (LWT)* e comunicação em turma na `eduroam` através de um *broker* público.
  * **Exercício 2.2:** Sistema de **Telemetria em Tempo Real** em Python (`paho-mqtt` e `psutil`) com *dashboard* gráfico Plotly (`ex05`), suportando **dados ambientais simulados** (`--mode env`), **telemetria real de CPU/RAM do portátil** (`--mode system`) e um subscritor de alertas em linha de comandos (`subscriber.py`).

\vspace{0.5em}

### Preparação do Diretório de Trabalho

Antes de iniciar os exercícios, crie e aceda ao diretório de trabalho dedicado a esta aula:

```bash
$ mkdir -p ~/IEI/aula08
$ cd ~/IEI/aula08
```

> **Nota sobre caminhos de ficheiros:**
> Os comandos apresentados neste guião assumem que a sessão de terminal se encontra posicionada no diretório `~/IEI/aula08` (ou na subpasta do respetivo exercício).

-----

## Parte 0: Preparação do Ambiente & Boas Práticas em Python

Certifique-se de que tem o **Docker** (com Docker Compose), o **`curl`**, o **`netcat` (`nc`)** e os módulos **`pip`** e **`venv`** do Python 3 instalados:

* **No Linux (Ubuntu / Debian / WSL):**
  ```bash
  $ sudo apt update
  $ sudo apt install -y curl wget netcat-openbsd python3-pip python3-venv
  ```
* **No macOS:**
  Os utilitários `curl`, `nc` e `python3` já se encontram disponíveis nativamente no sistema (ou via *Xcode Command Line Tools*). Caso utilize Homebrew para gerir uma versão recente do Python, execute apenas se necessário:
  ```bash
  $ brew install python3
  ```

Verifique rapidamente se o Docker e o Python estão operacionais:

```bash
$ python3 --version
$ docker compose version
```

-----

## Bloco 1: Comunicação Direta Cliente-Servidor (*Request/Response*)

Neste primeiro bloco exploramos o paradigma clássico **Cliente-Servidor**, começando ao nível da **Camada 4 (Transporte — TCP e UDP)** com *sockets* puros em Python até chegar à **Camada 7 (Aplicação — HTTP / API REST)**.

### Exercício 1.1: O Clássico Servidor de Eco com Sockets Puros (TCP vs. UDP)

**Objetivo:** Compreender como uma aplicação abre um *socket* no sistema operativo para escutar numa porta (`IP:Porta`) e comparar na prática os protocolos **TCP** (orientado à conexão, fiável) e **UDP** (sem conexão, datagramas).

**Ficheiros de apoio:** Descarregue `ex01.zip` a partir da pasta `"resources"` associada a esta aula no eLearning da disciplina (`echo_server.py` e `echo_client.py`).

#### Parte A — Preparar os Ficheiros de Apoio (`echo_server.py` e `echo_client.py`)

Crie a pasta do exercício e extraia o conteúdo de `ex01.zip` para a mesma:

```bash
$ mkdir -p ~/IEI/aula08/ex01
$ cd ~/IEI/aula08/ex01
# (Extraia aqui o ficheiro ex01.zip do eLearning: unzip ex01.zip)
```

Antes de executar, analise brevemente o ficheiro `echo_server.py`: repare que utiliza o módulo nativo `socket` do Python (sem `asyncio`, de forma bloqueante) e implementa duas funções distintas — `run_tcp_server` (`SOCK_STREAM`, com `listen()` e `accept()`) e `run_udp_server` (`SOCK_DGRAM`, diretamente com `recvfrom()` e `sendto()`).

#### Parte B — Testar o Modo TCP com `nc` e Inspecionar o Socket

1. **Terminal 1 (Servidor TCP):** Inicie o servidor na porta `9000`:
   ```bash
   $ python3 echo_server.py tcp --port 9000
   ```
2. **Terminal 2 (Inspeção de Rede — revisão da Aula 07):** Verifique que o processo Python abriu um *socket* TCP em estado **`LISTEN`**:
   * **No Linux:** `ss -tulnp | grep 9000`
   * **No macOS:** `lsof -nP -iTCP:9000 -sTCP:LISTEN`
3. **Terminal 2 (Cliente `netcat`):** Estabeleça uma ligação TCP ao servidor e envie mensagens:
   ```bash
   $ nc 127.0.0.1 9000
   ```
   Escreva `Ola TCP` e prima Enter; deverá receber `Ola TCP` de volta.
   * **Experiência de Bloqueio:** Sem fechar este cliente no Terminal 2, abra um **Terminal 3** e execute também `nc 127.0.0.1 9000`, escrevendo `Segundo cliente`. Repare que o segundo cliente não recebe eco imediato porque o servidor TCP está **bloqueado** no `conn.recv()` do primeiro cliente!
   * Feche o cliente no Terminal 2 com **`Ctrl+C`** (ou `Ctrl+D`) e observe no Terminal 1 o registo de desconexão e a entrada imediata do segundo cliente. Feche também o cliente no Terminal 3 e pare o servidor no Terminal 1 (`Ctrl+C`).

#### Parte C — Testar o Modo UDP e Comparar com o Cliente Python

1. **Terminal 1 (Servidor UDP):**
   ```bash
   $ python3 echo_server.py udp --port 9000
   ```
2. **Terminal 2 (Inspeção):** Execute `ss -uln | grep 9000` (Linux) ou `lsof -nP -iUDP:9000` (macOS). Note que em **UDP não existe estado `LISTEN` nem `accept()`** porque não há sessão prévia (*stateless*).
3. **Terminal 2 (Cliente `nc` ou `echo_client.py`):**
   ```bash
   $ nc -u 127.0.0.1 9000
   ```
   Escreva `Ola UDP` e prima Enter (termine depois com `Ctrl+C`).
   Opcionalmente, descarregue e teste também com o cliente Python `echo_client.py` de suporte:
   ```bash
   $ python3 echo_client.py udp --port 9000 --message "Teste UDP em Python"
   ```
   **Não pare ainda** o servidor — para o exercício seguinte, feche o modo UDP (`Ctrl+C`) e volte a iniciá-lo em modo **TCP**.

-----

### Exercício 1.2: HTTP sobre um Socket TCP

**Objetivo:** Confirmar experimentalmente que o protocolo **HTTP** (usado por *browsers* e APIs REST) não é um mecanismo separado da rede, mas sim **texto estruturado transportado dentro de um *socket* TCP**.

1. **Terminal 1:** Garanta que o seu servidor de eco está a correr em modo **TCP**:
   ```bash
   $ python3 echo_server.py tcp --port 9000
   ```
2. **Terminal 2:** Em vez de `nc`, execute um pedido HTTP com o utilitário **`curl`**:
   ```bash
   $ curl -v http://127.0.0.1:9000/ola
   ```
3. **Analise o que aconteceu nos dois terminais:**
   * No **Terminal 1 (`echo_server.py`)**, o servidor recebeu e imprimiu a mensagem enviada pelo `curl`:
     ```text
     GET /ola HTTP/1.1
     Host: 127.0.0.1:9000
     User-Agent: curl/...
     Accept: */*
     ```
   * No **Terminal 2 (`curl`)**, o comando falhou (ex.: `Unsupported HTTP version` ou `Received HTTP/0.9 when not allowed`). **Porquê?** Porque o `echo_server.py` devolveu exatamente o pedido `GET /ola HTTP/1.1...` em eco, em vez de construir uma resposta HTTP válida (`HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n...`).
4. Termine o servidor TCP no Terminal 1 com `Ctrl+C`.

> **Conclusão:** Poderíamos programar manualmente o *parsing* de métodos (`GET`, `POST`), caminhos (`/ola`), cabeçalhos e códigos de estado (`200`, `404`) sobre *sockets* TCP — mas estaríamos a reinventar o servidor HTTP. É exatamente por isso que usamos frameworks como o **FastAPI**.

-----

### Exercício 1.3: API REST de Geolocalização IP com Cache Local (FastAPI)

**Objetivo:** Executar e analisar uma **API REST** em Python com **FastAPI** que automatiza a consulta de geolocalização IP e implementa um mecanismo de **cache em disco** (`ip_cache.json`).

**Detalhes da Arquitetura (`ex03/main.py`):**

* **Servidor REST local:** Expõe o *endpoint* `GET /ip/{ip_address}` na porta `8000` e gera automaticamente documentação interativa em `/docs`.
* **Cliente REST externo:** Em caso de *Cache Miss* (ou expiração após `CACHE_DEADLINE_SECONDS`), o serviço usa a biblioteca `requests` para consultar `http://ip-api.com/json/{ip_address}`.
* **Validação e Erros HTTP:** Endereços IP privados (RFC 1918, como `192.168.x.x`) não são roteáveis na Internet pública, pelo que a API externa falha e o FastAPI devolve o código de estado HTTP **`404 Not Found`**.

**Instruções:**

1. Crie a pasta `ex03`, descarregue e extraia `ex03.zip` (da pasta `"resources"` associada a esta aula no eLearning da disciplina — `main.py`, `requirements.txt`, `ip-address.png`), ative um ambiente virtual e instale as dependências:
   ```bash
   $ mkdir -p ~/IEI/aula08/ex03 && cd ~/IEI/aula08/ex03
   # (Extraia aqui o ficheiro ex03.zip do eLearning: unzip ex03.zip)
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
2. **Inicie o servidor FastAPI com o Uvicorn (Terminal 1):**
   ```bash
   $ uvicorn main:app --reload
   ```
3. **Teste o serviço num segundo terminal (`curl`):**
   * **Teste 1 — *Cache Miss* (consulta à API externa):**
     ```bash
     # Endereço IP privado (deve devolver HTTP 404)
     $ curl -i http://127.0.0.1:8000/ip/192.168.132.132

     # DNS Google, MEO e Universidade de Aveiro
     $ curl -s http://127.0.0.1:8000/ip/8.8.8.8
     $ curl -s http://127.0.0.1:8000/ip/144.64.3.83
     $ curl -s http://127.0.0.1:8000/ip/193.137.169.135
     ```
     Observe nos logs do Terminal 1 a mensagem: `"Querying external API for ..."`.
   * **Teste 2 — *Cache Hit* (resposta servida diretamente da cache local):**
     Repita os pedidos para `8.8.8.8` e `193.137.169.135`. Observe nos logs: `"Returning cached data for ..."` e inspecione o ficheiro gerado `cat ip_cache.json`.
4. **Analisar o Código (`main.py`):**
   Abra o ficheiro `main.py` e localize:
   * Como e onde está implementado o *endpoint* REST de consulta de IP;
   * Que biblioteca e que URL de API externa são invocados quando ocorre *Cache Miss*;
   * Como a resposta é guardada e reutilizada através do ficheiro `ip_cache.json`.
5. **Explorar a Documentação Automática (Swagger UI):**
   Abra **`http://127.0.0.1:8000/docs`** no seu navegador Web e execute um pedido de teste diretamente através da interface gráfica (*Try it out*).
6. Quando terminar, pare o servidor `uvicorn` no Terminal 1 (`Ctrl+C`) e desative o ambiente virtual (`deactivate`).

-----

## Bloco 2: Comunicação Desacoplada em Tempo Real (MQTT)

No **Bloco 1**, o cliente precisava sempre de conhecer exatamente o **IP e a Porta** do servidor, e ambos tinham de estar diretamente acessíveis.
Neste **Bloco 2**, mudamos para o padrão **Publish/Subscribe** através de um **Broker MQTT**: os clientes apenas se ligam ao *broker* e publicam/subscrevem **tópicos** hierárquicos, ficando totalmente desacoplados entre si.

### Exercício 2.1: Broker MQTT em Docker & Chat Web *Serverless* sobre WebSockets

**Objetivo:** Executar um *broker* **Eclipse Mosquitto** em Docker e ligar-lhe uma aplicação Web em JavaScript puro (`MQTT.js` sobre WebSockets) para construir um chat em tempo real **sem escrever qualquer código de servidor**.

**Detalhes da Arquitetura (`ex04`):**

* **Broker (`mosquitto`):** O ficheiro `compose.yml` arranca o contentor `eclipse-mosquitto` configurado por `mqtt/mosquitto.conf` com acesso anónimo e duas portas: **`1883`** (MQTT padrão sobre TCP) e **`9001`** (MQTT sobre **WebSockets**, necessário para browsers).
* **Frontend (`nginx`):** O contentor `nginx:alpine` serve o ficheiro `html/index.html` na porta **`8080`**.
* **Funcionalidade *Last Will and Testament (LWT)*:** Ao ligar-se, cada cliente regista uma mensagem de despedida no *broker*; se o separador do browser fechar abruptamente, o próprio *broker* publica a saída desse utilizador.

**Instruções:**

1. Crie a pasta `ex04`, descarregue e extraia `ex04.zip` (da pasta `"resources"` associada a esta aula no eLearning da disciplina — `compose.yml`, `mqtt/mosquitto.conf`, `html/index.html`) e inicie os contentores:
   ```bash
   $ mkdir -p ~/IEI/aula08/ex04 && cd ~/IEI/aula08/ex04
   # (Extraia aqui o ficheiro ex04.zip do eLearning: unzip ex04.zip)
   $ docker compose up -d
   $ docker compose ps
   ```
2. **Teste Local em Múltiplos Separadores:**
   * Abra **`http://localhost:8080/`** em **dois separadores** do navegador Web.
   * Mantenha o *Broker URL* como `ws://localhost:9001` e o tópico `class/chat/main_room`.
   * Introduza nomes de utilizador diferentes (ex.: `alice` e `bob`), clique em **Connect** e troque mensagens entre os dois separadores.
   * **Teste de LWT:** Feche abruptamente (clique no `X` do separador) o separador da `alice` e observe que no separador do `bob` surge automaticamente a notificação `"alice left the chat."` enviada pelo *broker* após alguns segundos.
3. **Teste Colaborativo em Turma na `eduroam`:**
   * Recarregue a página `http://localhost:8080/`.
   * Sem sair da rede `eduroam`, altere o endereço do *Broker* de `ws://localhost:9001` para um *broker* MQTT público com suporte a WebSockets:
     * `ws://broker.hivemq.com:8000/mqtt` *(ou `ws://test.mosquitto.org:8080`)*
   * Defina um tópico partilhado com os colegas da sala (ex.: **`ua/iei/aula08/chat`**), introduza o seu nome e clique em **Connect**.
   * Troque mensagens com a turma! *(Repare como dezenas de portáteis isolados pela `eduroam` comunicam em tempo real porque todas as ligações são de saída para o mesmo broker).*
4. **Analisar a Implementação (`compose.yml`, `mqtt/mosquitto.conf` e `html/index.html`):**
   Abra os ficheiros do projeto e identifique, em linhas gerais, como a aplicação está estruturada:
   * **Infraestrutura (`compose.yml` e `mqtt/mosquitto.conf`):** que contentores são lançados, que portas distinguem o acesso MQTT padrão do acesso via WebSockets e que regras de acesso estão definidas no *broker*;
   * **Cliente Web (`html/index.html`):** que biblioteca JavaScript estabelece a ligação ao *broker*, como são feitos o `subscribe` e o `publish` (incluindo o formato das mensagens trocadas) e onde é configurada a mensagem de *Last Will and Testament (LWT)*.
5. **Limpeza Obrigatória:** Pare os contentores antes de avançar para o Exercício 2.2 (para libertar as portas `1883`, `9001` e `8080`):
   ```bash
   $ docker compose down
   ```

-----

### Exercício 2.2: Telemetria em Tempo Real com `paho-mqtt`, `psutil` e Dashboard Plotly

**Objetivo:** Construir uma *pipeline* completa de telemetria IoT/Sistemas **100% em software**: um script publicador em Python (`paho-mqtt`) envia medições em JSON para o *broker* Mosquitto, alimentando simultaneamente um **dashboard gráfico em tempo real** no browser (Plotly.js) e um **subscritor de alertas em linha de comandos**.

O publicador (`main.py`) suporta **dois modos de recolha de dados**:
* **`--mode env` (Dados Ambientais Simulados):** Simula um sensor de temperatura (`°C`) e humidade (`%`) com variação contínua (*random walk*).
* **`--mode system` (Telemetria Real da Máquina):** Lê em tempo real a percentagem de utilização do **CPU (%)** e da **Memória RAM (%)** do seu próprio computador através da biblioteca `psutil`.

**Instruções:**

1. Crie a pasta `ex05`, descarregue e extraia `ex05.zip` (da pasta `"resources"` associada a esta aula no eLearning da disciplina):
   ```bash
   $ mkdir -p ~/IEI/aula08/ex05 && cd ~/IEI/aula08/ex05
   # (Extraia aqui o ficheiro ex05.zip do eLearning: unzip ex05.zip)
   ```
2. **Inicie a infraestrutura Docker (`mosquitto` + `nginx`):**
   ```bash
   $ docker compose up -d
   ```
3. **Prepare o ambiente virtual Python:**
   ```bash
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
4. **Abra o Dashboard Web no Browser:**
   * Aceda a **`http://localhost:8080/`**.
   * Confirme que *Broker Host* está preenchido com **`localhost`** e *Topic* com **`deti/pico/dht11`**.
   * Clique em **Connect** (o estado deve passar a `Status: Connected`).
5. **Cenário A — Publicar Dados Ambientais Simulados (`--mode env`):**
   No **Terminal 1** (com o `.venv` ativo), execute o publicador em modo ambiental:
   ```bash
   $ python main.py --mode env
   ```
   Observe no browser o gráfico de Temperatura (`°C`) e Humidade (`%`) a atualizar a cada 2 segundos em tempo real.
6. **Cenário B — Executar um Segundo Subscritor de Alertas no Terminal (`subscriber.py`):**
   Abra um **Terminal 2**, ative o mesmo ambiente virtual e inicie o subscritor usando um *wildcard* MQTT (`+`) no tópico e um limiar de alerta:
   ```bash
   $ cd ~/IEI/aula08/ex05
   $ source .venv/bin/activate
   $ python subscriber.py --topic "deti/pico/+" --threshold 24.0
   ```
   Verifique que **tanto o Dashboard Web como o terminal Python recebem as mesmas mensagens simultaneamente** (*fan-out* do *broker*) e que são impressos avisos `[WARNING] ALERT ...` quando o valor ultrapassa o limiar.
7. **Cenário C — Publicar Telemetria Real do Portátil (`--mode system`):**
   No **Terminal 1**, interrompa o modo `env` (`Ctrl+C`) e execute o publicador em modo sistema:
   ```bash
   $ python main.py --mode system
   ```
   * Note no browser que os eixos do gráfico se ajustam automaticamente para **CPU Usage (%)** e **RAM Usage (%)**.
   * Experimente abrir um novo separador pesado no browser ou correr um comando no terminal para gerar carga no CPU e observe o pico refletido no gráfico e nos alertas do **Terminal 2**!
8. **Explorar e Modificar o Código (`main.py`, `subscriber.py` e `html/index.html`):**
   * **Explorar a Implementação:** localize no `main.py` como são recolhidas as métricas com `psutil` e como é construído o *payload* JSON publicado no *broker*; compare depois com o `subscriber.py` e o `html/index.html` para perceber como ambos os subscritores distinguem o modo ambiental do modo de sistema e atualizam os respetivos alertas/gráficos.
   * **Experimentar uma Alteração:** teste alterar a cadência de envio através da opção `--interval` do `main.py` e experimente modificar o `subscriber.py` para também emitir um alerta quando a métrica secundária (humidade ou memória RAM) ultrapassar um limiar à sua escolha.
9. **Desafio Extra (Opcional — Publicação na Turma via `eduroam`):**
   Altere a flag `--host` tanto no `main.py` como no `subscriber.py` (e no campo *Broker Host* da página Web) para `test.mosquitto.org` e use um tópico único com o seu número mecanográfico, por exemplo `--topic "ua/iei/aula08/<nmec>"`, visualizando no seu browser a telemetria do portátil de um colega (subscrevendo `ua/iei/aula08/<nmec_colega>`).
10. **Encerramento:** Interrompa os scripts Python (`Ctrl+C`) e encerre os contentores Docker:
   ```bash
   $ docker compose down
   ```

-----

## Síntese Comparativa: Bloco 1 vs. Bloco 2

| Dimensão | Bloco 1: Sockets Puros & API REST | Bloco 2: MQTT (Publish/Subscribe) |
| :--- | :--- | :--- |
| **Paradigma** | **Request / Response** (Cliente-Servidor direto) | **Publish / Subscribe** (Orientado a eventos via Broker) |
| **Protocolos** | TCP / UDP (`socket`) e HTTP (`FastAPI`) | MQTT sobre TCP (`1883`) e WebSockets (`9001`) |
| **Acoplamento** | Cliente tem de conhecer `IP:Porta` exato do servidor | Desacoplado: clientes conhecem apenas o Broker e o **Tópico** |
| **Comunicação `eduroam`** | Bloqueada entre alunos (*Client Isolation*) | Funciona entre alunos ligando-se a um Broker externo |
| **Casos de Uso Típicos** | Serviços Web, APIs públicas, transferência direta, jogos | Telemetria IoT, monitorização em tempo real, chats, notificações |
