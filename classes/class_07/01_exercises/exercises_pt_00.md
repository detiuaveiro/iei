---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Redes Informáticas: Fundamentos, Configuração & Diagnóstico"
institute: Universidade de Aveiro
date: November 09, 2026
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
 - \AtBeginEnvironment{longtable}{\tiny}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guião Prático de Laboratório

**Enquadramento Pedagógico & Objetivos:**
Nas sessões anteriores foram utilizadas diversas funcionalidades de rede — designadamente pedidos HTTP via `curl`, mapeamento de portas em contentores Docker (`-p 8080:80`) e autenticação remota via SSH no GitHub. Nesta sessão laboratorial de **3 horas**, o objetivo consiste em analisar a configuração das interfaces de rede, compreender o encaminhamento de pacotes até à Internet e **executar procedimentos sistemáticos de diagnóstico (*troubleshooting*) quando uma aplicação ou servidor apresenta falhas de conectividade** (competência fundamental para os projetos da unidade curricular e para a **Class 08**, dedicada à programação de aplicações em rede em Python):

* **Parte 0 — Preparação do Ambiente & Servidor de Teste (Docker SSH):** Instalação dos utilitários de diagnóstico de rede (Linux e macOS), geração de um par de chaves criptográficas SSH (`ed25519`) e instanciação de um contentor Docker com um servidor OpenSSH isolado para testes de administração remota.
* **Parte 1 — Inspeção da Máquina Local e da Rede Local (LAN):** Identificação de interfaces de rede, endereço físico (**MAC**), endereço lógico (**IPv4**) e máscara de sub-rede (`/24`) através de `ip a` / `ifconfig`, verificação da interface de *loopback* (`127.0.0.1`), identificação do encaminhador local (*Default Gateway* com `ip r` / `netstat -rn`) e consulta da tabela **ARP** (`ip neigh` / `arp -an`).
* **Parte 2 — Da Rede Local para a Internet (WAN, NAT e DNS):** Testes de conectividade e latência por endereço IP vs. nome de domínio (`ping`), análise de encaminhamento entre múltiplos encaminhadores (`traceroute`), resolução de nomes no sistema **DNS** (`dig` e `/etc/hosts`) e determinação do **Endereço IP Público** e do mecanismo de **NAT** (`curl`).
* **Parte 3 — Portas, Serviços e Diagnóstico de Ligações (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`):** Inspeção de *sockets* ativos em estado de escuta (*LISTEN*) no sistema local (`ss -tuln` / `lsof`), análise experimental da diferença entre associação (*binding*) aos endereços `127.0.0.1` e `0.0.0.0` (preparação para a Class 08) e sondagem de portas com `nmap`.
* **Parte 4 — Administração Remota Segura (SSH, `rsync` e Encaminhamento de Portas SSH):** Autenticação remota via `ssh`, sincronização incremental de diretórios através de `rsync` e estabelecimento de um **Túnel SSH (`ssh -L` — *Local Port Forwarding*)** para acesso seguro a serviços internos não expostos diretamente.
* **Parte 5 — Exercícios Complementares de Consolidação:** Captura e inspeção de tráfego de rede em tempo real com `tcpdump` e representação geográfica de rotas IP (Geo-Traceroute).

\vspace{0.5em}

### Preparação do Diretório de Trabalho

Antes de iniciar os exercícios, crie e aceda ao diretório de trabalho dedicado a esta aula:

```bash
$ mkdir -p ~/IEI/aula07
$ cd ~/IEI/aula07
```

Todos os ficheiros criados durante a sessão laboratorial deverão permanecer organizados neste diretório.

> **Nota sobre caminhos de ficheiros:**
> Os comandos apresentados neste guião assumem que a sessão de terminal se encontra posicionada no diretório `~/IEI/aula07`.

-----

## Parte 0: Preparação do Ambiente & Servidor de Teste (Docker SSH)

Antes de iniciar a análise de rede, proceda à instalação dos utilitários de diagnóstico no sistema operativo (Linux ou macOS) e à inicialização de um servidor OpenSSH num contentor Docker, o qual funcionará como sistema remoto de teste.

### Passo 1: Instalar os Utilitários de Diagnóstico de Rede

Abra o terminal e instale os pacotes necessários para a realização das atividades laboratoriais:

* **No Linux (Ubuntu / Debian):**
  ```bash
  $ sudo apt update
  $ sudo apt install -y iproute2 net-tools dnsutils traceroute nmap curl \
    python3-pip python3-venv python3-tk
  ```
* **No macOS (via Homebrew):**
  Os utilitários `ping`, `traceroute`, `dig`, `curl`, `arp`, `lsof`, `netstat`, `ssh`, `rsync` e `tcpdump` encontram-se instalados nativamente no macOS. Instale adicionalmente o pacote `nmap` (e, opcionalmente, o pacote `iproute2mac`, que disponibiliza a sintaxe dos comandos `ip a` e `ip r` do Linux no macOS):
  ```bash
  $ brew install nmap iproute2mac
  ```

Síntese dos utilitários:

  * `ip` / `ifconfig` / `arp` / `ss` / `lsof`: Inspeção de interfaces de rede, endereços IP, tabelas de encaminhamento, cache ARP e *sockets* de transporte.
  * `dig`: Consulta direta a servidores DNS para resolução de nomes de domínio.
  * `traceroute`: Identificação da sequência de encaminhadores (*hops*) no trajeto até um endereço de destino.
  * `nmap`: Sondagem de portas de transporte e identificação de serviços ativos num sistema.
  * `curl`: Execução de pedidos HTTP/HTTPS a servidores Web e APIs a partir da linha de comandos.
  * `ssh`: Estabelecimento de sessão remota segura de linha de comandos num servidor SSH.
  * `rsync`: Transferência e sincronização de diretórios de forma incremental sobre SSH.

### Passo 2: Verificar ou Gerar um Par de Chaves SSH

A autenticação segura em sistemas remotos baseia-se em criptografia assimétrica através de um par de chaves (**Chave Privada**, armazenada confidencialmente na máquina cliente, e **Chave Pública**, copiada para o servidor remoto).

1. Verifique a existência de um par de chaves `ed25519` no diretório `~/.ssh`:
   ```bash
   $ ls -la ~/.ssh/id_ed25519*
   ```
2. **Caso não exista**, gere um novo par de chaves sem *passphrase*:
   ```bash
   $ ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
   ```
   *(Nota de segurança: O ficheiro `~/.ssh/id_ed25519.pub` corresponde à chave pública e pode ser copiado para servidores remotos; o ficheiro `~/.ssh/id_ed25519` contém a chave privada e **nunca** deve ser partilhado ou transferido para terceiros).*

### Passo 3: Instanciar o Servidor SSH de Teste (Docker Compose)

Utilize o Docker Compose para instanciar um servidor Linux OpenSSH configurado para escutar na porta **`2222`**:

1. Crie o subdiretório `ssh-server` e aceda ao mesmo:
   ```bash
   $ mkdir -p ~/IEI/aula07/ssh-server
   $ cd ~/IEI/aula07/ssh-server
   ```

2. Crie o ficheiro `custom-openssh-server.Dockerfile`, que estende a imagem base do servidor OpenSSH com a instalação dos pacotes `rsync` e `python3`:
   ```dockerfile
   FROM lscr.io/linuxserver/openssh-server:latest
   RUN apk update && apk add rsync python3 && rm -rf /var/cache/apk/*
   ```

3. Crie o ficheiro `compose.yml` para definir o serviço e mapear a porta `2222`:
   ```yaml
   services:
     ssh:
       build:
         context: .
         dockerfile: custom-openssh-server.Dockerfile
       container_name: iei-ssh-server
       environment:
         - PUID=1000
         - PGID=1000
         - TZ=Europe/Lisbon
         - USER_NAME=student
         - PUBLIC_KEY_FILE=/config/authorized_keys/student.pub
       volumes:
         - ./authorized_keys:/config/authorized_keys
       ports:
         - "2222:2222" # Mapeia porta 2222 do anfitrião -> porta 2222 do contentor
       restart: unless-stopped
   ```

4. Crie o diretório `authorized_keys` e copie para o seu interior a sua **chave pública**, autorizando a autenticação do utilizador `student`:
   ```bash
   $ mkdir -p authorized_keys
   $ cp ~/.ssh/id_ed25519.pub ./authorized_keys/student.pub
   ```

5. Construa e inicie o contentor em segundo plano (*detached mode*), verificando de seguida o respetivo estado de execução:
   ```bash
   $ docker compose up -d --build
   $ docker compose ps
   ```

6. Regresse ao diretório principal da aula:
   ```bash
   $ cd ~/IEI/aula07
   ```

-----

## Parte 1: Inspeção da Máquina Local e da Rede Local (LAN)

No diagnóstico de problemas de conectividade em rede, a primeira etapa consiste na verificação da configuração das interfaces de rede do próprio sistema.

### Exercício 1: Identificar Endereço MAC, Endereço IP e Máscara de Sub-rede (`ip a` / `ifconfig`)

Liste as interfaces de rede configuradas no sistema:

* **No Linux** (ou no macOS com `iproute2mac`):
  ```bash
  $ ip a
  ```
* **No macOS (nativo):**
  ```bash
  $ ifconfig
  ```

Analise a saída do comando e identifique os seguintes elementos:

1. **Interface `lo` (Linux) ou `lo0` (macOS) — *Loopback*:** Apresenta os endereços `inet 127.0.0.1` (IPv4) e `inet6 ::1` (IPv6). Trata-se da interface virtual interna utilizada para comunicação entre processos no próprio sistema local (`localhost`).
2. **Interface de rede física principal** (tipicamente designada por `eth0`, `enp0s3` ou `wlan0` no Linux, e por **`en0`** no macOS):
   * **Endereço MAC (Camada de Ligação de Dados — L2):** Identifique o campo `link/ether` (no `ip a`) ou `ether` (no `ifconfig` do macOS), por exemplo `08:00:27:1a:2b:3c`. Constitui o identificador físico de 48 bits associado à interface na rede local.
   * **Endereço IPv4 e Máscara de Sub-rede (Camada de Rede — L3):** Identifique o campo `inet` (ex.: `192.168.1.50/24` no Linux, ou `inet 192.168.1.50 netmask 0xffffff00` no `ifconfig` do macOS, onde a representação hexadecimal `0xffffff00` equivale a `255.255.255.0`, isto é, ao prefixo `/24`).
     * O prefixo `/24` (`255.255.255.0`) determina que os primeiros 3 octetos identificam o **prefixo da rede local** e o último octeto identifica o **sistema anfitrião (*host*) dentro dessa sub-rede** (intervalo utilizável de `.1` a `.254`).
   * **Endereço IPv6 *Link-Local*:** Identifique o campo `inet6 fe80::...`, correspondente ao endereço IPv6 autoconfigurado válido apenas no segmento de rede local.
3. **Interface `docker0` / `br-...` (no Linux):** Em sistemas Linux nativos, o serviço Docker cria uma interface de ponte virtual (*bridge*) com endereçamento privado próprio (tipicamente `172.17.0.1/16`) para interligar os contentores *(no macOS, o Docker Desktop executa os contentores no interior de uma máquina virtual Linux, pelo que essa interface reside nessa máquina virtual)*.

### Exercício 2: Verificar a Pilha TCP/IP Local (`localhost` / *Loopback*)

Antes de testar a conectividade na rede física (Ethernet ou Wi-Fi), deve confirmar-se o correto funcionamento da pilha protocolar TCP/IP do sistema operativo. Envie 4 pacotes ICMP Echo Request (`-c 4`) para os endereços de *loopback*:

```bash
# Testar interface de Loopback em IPv4 (Linux e macOS)
$ ping -c 4 127.0.0.1

# Testar interface de Loopback em IPv6 (no Linux)
$ ping -c 4 ::1

# Testar interface de Loopback em IPv6 (no macOS utiliza-se ping6)
$ ping6 -c 4 ::1
```

Analise o tempo de resposta (`time=... ms`) e a taxa de perda de pacotes (`0% packet loss`). Uma vez que o tráfego é processado exclusivamente em memória pelo núcleo (*kernel*) do sistema operativo sem transitar pelo meio físico, a latência registada é reduzida (tipicamente inferior a `0.1 ms`).

### Exercício 3: Identificar o *Default Gateway* e Testar a Conectividade na LAN

Para encaminhar pacotes destinados a redes externas (como a Internet), o sistema local necessita de conhecer o endereço IP do encaminhador da rede local — designado por **Default Gateway**.

1. Consulte a tabela de encaminhamento (*routing table*) do sistema operativo para identificar a rota predefinida (`default`):
   * **No Linux** (ou no macOS com `iproute2mac`):
     ```bash
     $ ip route show default
     ```
     *(Ou abreviadamente `ip r`).* A saída apresentará o formato `default via 192.168.1.1 dev eth0`, onde o endereço IP indicado após **`via`** corresponde ao **Default Gateway**.
   * **No macOS (nativo):**
     ```bash
     $ netstat -rn -f inet | grep default
     # ou:
     $ route -n get default
     ```
     O endereço apresentado na coluna `Gateway` (ou no campo `gateway:`) identifica o **Default Gateway** da rede.

2. Teste a conectividade direta até ao encaminhador local utilizando o comando `ping` (substitua pelo endereço IP obtido na alínea anterior):
   ```bash
   $ ping -c 4 <IP_DO_DEFAULT_GATEWAY>
   ```
   A receção de respostas sem perda de pacotes (`0% packet loss`) confirma o funcionamento do meio físico (cabo ou Wi-Fi) e a conectividade ao nível da rede local (LAN).

### Exercício 4: Inspecionar a Resolução de Endereços na Tabela ARP (`ip neigh` / `arp -an`)

Para encapsular o pacote IP dirigido ao *Default Gateway* numa trama Ethernet (Camada 2), o sistema operativo utilizou previamente o protocolo **ARP (*Address Resolution Protocol*)** para determinar o **endereço MAC** associado ao endereço IPv4 desse encaminhador.

Consulte a tabela ARP (*ARP cache*) armazenada no sistema:

* **No Linux:**
  ```bash
  $ ip neigh
  ```
* **No macOS (e também suportado no Linux):**
  ```bash
  $ arp -an
  ```

Identifique a entrada correspondente ao endereço IP do *Default Gateway* e verifique o endereço MAC associado. Esta associação permite à interface de rede endereçar as tramas Ethernet no segmento local.

-----

## Parte 2: Da Rede Local para a Internet (WAN, NAT e DNS)

Confirmada a conectividade na rede local até ao *Default Gateway*, analisa-se de seguida o encaminhamento de tráfego para redes externas (WAN / Internet) e o processo de resolução de nomes de domínio.

### Exercício 5: Testar a Conectividade Externa por Endereço IP vs. Nome de Domínio (`ping`)

Uma falha no acesso a recursos Web pode resultar quer da ausência de encaminhamento IP para o exterior, quer de uma falha exclusiva no serviço de resolução de nomes (**DNS**). Para isolar a causa, realizam-se dois testes distintos:

1. Teste a conectividade IP direta para um **endereço IP público** externo (por exemplo, o servidor público `8.8.8.8` operado pela Google):
   ```bash
   $ ping -c 4 8.8.8.8
   ```
   *A receção de respostas confirma a existência de conectividade IP até à Internet.* Compare o tempo de ida e volta (*Round-Trip Time* — `time=... ms`) com o obtido na rede local: como os pacotes atravessam múltiplos encaminhadores externos, a latência situa-se tipicamente na ordem das dezenas de milissegundos.

2. Efetue agora o teste utilizando um **nome de domínio**:
   ```bash
   $ ping -c 4 ua.pt
   ```
   Observe na primeira linha da saída que o sistema realizou previamente uma consulta ao serviço **DNS** para traduzir o nome `ua.pt` no respetivo endereço IPv4 (ex.: `193.136.172.10`) antes de iniciar o envio dos pacotes ICMP.

> **Princípio de Diagnóstico:** Caso o comando `ping 8.8.8.8` tenha sucesso mas o comando `ping ua.pt` produza um erro de resolução (*"Temporary failure in name resolution"* ou *" cannot resolve...: Unknown host"*), a conectividade IP à Internet encontra-se operacional, residindo a falha exclusivamente na configuração de **DNS**.

### Exercício 6: Rastreio da Rota de Encaminhamento (`traceroute`)

Para identificar a sequência de encaminhadores (*routers*) atravessados por um pacote desde a máquina de origem até ao sistema de destino, execute o utilitário `traceroute`:

```bash
$ traceroute 8.8.8.8
```

Analise a lista sequencial de saltos (*hops*):

* O **Salto 1** corresponde ao encaminhador da rede local (*Default Gateway*).
* Os saltos subsequentes correspondem aos encaminhadores da infraestrutura do operador de telecomunicações (ou da rede académica RCTS / FCCN) até atingir a rede de destino.
* *(Nota técnica: A presença de asteriscos `* * *` num determinado salto indica que o encaminhador intermédio não enviou mensagens ICMP Time Exceeded de resposta, por política de filtragem ou limitação de taxa, sem que isso impeça o reencaminhamento do tráfego para os saltos seguintes).*

Execute igualmente o rastreio de rota para o domínio da Universidade de Aveiro:
```bash
$ traceroute ua.pt
```

### Exercício 7: Resolução de Nomes de Domínio (`dig` e `/etc/hosts`)

Para inspecionar detalhadamente o processo de tradução de nomes de domínio em endereços IP, realize os seguintes passos:

1. Utilize o utilitário `dig` para consultar o registo de endereço IPv4 (registo do tipo **`A`**) associado ao domínio `ua.pt`:
   ```bash
   $ dig ua.pt A
   ```
   Na secção `;; ANSWER SECTION:` é apresentado o endereço IPv4 correspondente e o respetivo tempo de validade em cache (*TTL*). Para obter apenas o endereço IP resultante, adicione o parâmetro `+short`:
   ```bash
   $ dig ua.pt A +short
   ```

2. Efetue uma consulta DNS inversa (*reverse DNS lookup*) através da opção `-x` para determinar o nome de domínio associado a um endereço IP público:
   ```bash
   $ dig -x 8.8.8.8 +short
   ```

3. Inspecione o ficheiro de resolução estática local `/etc/hosts` (consultado pelo sistema operativo **antes** de efetuar pedidos a servidores DNS externos):
   ```bash
   $ cat /etc/hosts
   ```
   Verifique a entrada `127.0.0.1 localhost`, responsável por mapear localmente o identificador `localhost` para o endereço de *loopback* `127.0.0.1` sem necessidade de tráfego DNS na rede.

### Exercício 8: Determinação do Endereço IP Público e Mecanismo de NAT (`curl`)

> **Conceito de NAT (*Network Address Translation*):**
> Conforme verificado no Exercício 1, a interface da máquina local utiliza um **Endereço IP Privado** (pertencente às gamas reservadas `10.0.0.0/8`, `172.16.0.0/12` ou `192.168.0.0/16`), o qual é válido apenas no interior da rede local (LAN) e não é encaminhável na Internet pública. Para permitir que múltiplos dispositivos de uma rede privada comuniquem com a Internet partilhando um único **Endereço IP Público**, o encaminhador de fronteira executa o mecanismo de **NAT**: ao encaminhar um pacote da LAN para a WAN, o encaminhador substitui o endereço IP privado de origem pelo seu próprio **Endereço IP Público** e regista essa tradução numa tabela de estado; quando o pacote de resposta regressa da Internet, o encaminhador consulta essa tabela, repõe o endereço IP privado como destinatário e entrega o pacote à máquina interna correspondente.

Para determinar o **Endereço IP Público** com que as ligações originadas na sua rede se apresentam perante servidores externos na Internet, efetue um pedido à API `ipinfo.io` utilizando o utilitário `curl`:

```bash
$ curl -s https://ipinfo.io/json
```

Analise os campos do objeto JSON retornado:

* `ip`: O **Endereço IP Público** atribuído ao encaminhador de fronteira da rede (partilhado via NAT pelos dispositivos da LAN).
* `city` / `region` / `org`: A localização geográfica associada ao bloco de endereços e a entidade ou operador de telecomunicações (*Autonomous System* / ISP) titular do endereço.

-----

## Parte 3: Portas, Serviços e Diagnóstico de Ligações (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`)

Na administração de contentores **Docker** e no desenvolvimento de aplicações distribuídas (**Class 08 — Programação em Redes**), é fundamental verificar que portas de transporte se encontram em estado de escuta (*LISTEN*) e compreender o impacto do endereço de associação (*bind address*) na acessibilidade de um serviço.

### Exercício 9: Inspecionar Portas em Estado de Escuta no Sistema Local (`ss` / `lsof` e `nmap`)

Na Parte 0 foi iniciado um contentor Docker com um servidor SSH mapeado na porta `2222`. Verifique, ao nível do sistema operativo anfitrião, que essa porta se encontra efetivamente aberta e a aguardar ligações:

1. Liste os *sockets* de rede em estado de escuta (*LISTEN*) na máquina local:
   * **No Linux (`ss -tuln` — listagem numérica de *sockets* TCP e UDP em escuta):**
     ```bash
     $ ss -tuln
     ```
   * **No macOS (`lsof` — listagem de *sockets* TCP em estado `LISTEN` sem resolução de nomes ou portas):**
     ```bash
     $ lsof -nP -iTCP -sTCP:LISTEN
     ```
   Identifique a entrada referente à porta **`:2222`** (ex.: `0.0.0.0:2222` no Linux ou `*:2222 (LISTEN)` no macOS), confirmando a existência de um processo ativo a aceitar ligações TCP nessa porta.

2. Efetue uma sondagem de portas (*port scan*) à interface local (`localhost`) utilizando o utilitário **`nmap`** (sintaxe idêntica em Linux e macOS):
   ```bash
   $ nmap localhost
   ```
   Confirme na tabela `PORT / STATE / SERVICE` que a porta `2222/tcp` apresenta o estado **`open`**.

### Exercício 10: Associação de Serviços a Interfaces de Rede (`127.0.0.1` vs. `0.0.0.0`)

> **Significado do endereço `0.0.0.0` na configuração de servidores:**
> Ao contrário de `127.0.0.1` (que identifica especificamente a interface virtual de *loopback*), o endereço `0.0.0.0` não representa uma interface individual, mas sim uma **meta-constante de configuração (`INADDR_ANY`)**. Quando um processo servidor efetua o *bind* ao endereço `0.0.0.0`, instrui o sistema operativo para aceitar ligações destinadas a essa porta provenientes de **qualquer interface de rede configurada no sistema** (incluindo `localhost`, interfaces Ethernet/Wi-Fi da LAN ou interfaces virtuais de contentores Docker).

Para verificar experimentalmente a diferença comportamental entre associar um servidor a **`127.0.0.1`** ou a **`0.0.0.0`**, execute o seguinte procedimento:

1. Crie um diretório de teste contendo um ficheiro HTML simples:
   ```bash
   $ mkdir -p ~/IEI/aula07/teste-web && cd ~/IEI/aula07/teste-web
   $ echo "<h1>Servidor de Teste IEI</h1>" > index.html
   ```

2. **Cenário A — Associação exclusiva ao endereço `127.0.0.1` (*Loopback* apenas):**
   Inicie o servidor HTTP integrado do Python na porta `8000`, restringindo a escuta ao endereço `127.0.0.1`:
   ```bash
   $ python3 -m http.server 8000 --bind 127.0.0.1
   ```
   *(Mantenha este terminal em execução e **abra uma segunda janela de terminal**).*

3. Na **segunda janela de terminal**, inspecione o estado do *socket* na porta `8000`:
   * **No Linux:**
     ```bash
     $ ss -tuln | grep 8000
     ```
   * **No macOS:**
     ```bash
     $ lsof -nP -iTCP -sTCP:LISTEN | grep 8000
     ```
   Observe que o *socket* se encontra associado especificamente a **`127.0.0.1:8000`**:
   * Um pedido originado na própria máquina (`curl -I http://127.0.0.1:8000`) é aceite e devolve **`HTTP/1.0 200 OK`**.
   * Contudo, qualquer tentativa de ligação proveniente de outro dispositivo na LAN (ou do sistema anfitrião para o interior de um contentor Docker configurado deste modo) **será recusada (`Connection refused`)**, uma vez que o serviço não escuta na interface de rede externa.

4. No primeiro terminal, interrompa a execução do servidor com **`Ctrl+C`** e reinicie-o associando-o ao endereço **`0.0.0.0`** (todas as interfaces de rede):
   ```bash
   $ python3 -m http.server 8000 --bind 0.0.0.0
   ```

5. Na segunda janela de terminal, execute novamente o comando de verificação do passo 3 (`ss -tuln | grep 8000` no Linux, ou `lsof -nP -iTCP -sTCP:LISTEN | grep 8000` no macOS):
   Verifique que o *socket* surge agora associado a **`0.0.0.0:8000`** (Linux) ou **`*:8000`** (macOS), passando a aceitar ligações provenientes de qualquer interface de rede. Valide o acesso com `curl -I http://localhost:8000`, encerre o segundo terminal e termine o servidor no primeiro terminal com **`Ctrl+C`**.

   Regresse ao diretório principal da aula:
   ```bash
   $ cd ~/IEI/aula07
   ```

### Exercício 11: Sondagem de Portas num Servidor Público de Teste (`nmap`)

> **Enquadramento Ético e Legal:** A execução de sondagens de portas (*port scanning*) contra sistemas e redes de terceiros sem autorização prévia não é permitida. Para fins exclusivamente pedagógicos e de validação da ferramenta, o projeto Nmap disponibiliza publicamente o servidor autorizado **`scanme.nmap.org`**.

Efetue uma sondagem às portas abertas nesse servidor de teste:

```bash
$ nmap scanme.nmap.org
```

Analise os resultados obtidos na tabela de serviços, identificando portas padrão em estado `open`, tais como **`22/tcp` (`ssh`)** para administração remota e **`80/tcp` (`http`)** para disponibilização de conteúdos Web.

-----

## Parte 4: Administração Remota Segura (SSH, `rsync` e Encaminhamento de Portas SSH)

Nesta secção utiliza-se o servidor Linux OpenSSH instanciado na Parte 0 (acessível na porta `2222`) para executar três procedimentos padrão de administração de sistemas remotos: acesso por linha de comandos via SSH, sincronização incremental de ficheiros via `rsync` e encaminhamento seguro de portas (*SSH Port Forwarding*).

### Exercício 12: Estabelecer Sessão Remota via `ssh`

Inicie uma ligação SSH com o utilizador `student` para o servidor local em escuta na porta `2222`:

```bash
$ ssh student@localhost -p 2222
```

*(Na primeira ligação a um novo servidor, o cliente SSH solicita a confirmação da impressão digital da chave do servidor: `Are you sure you want to continue connecting (yes/no/[fingerprint])?` — introduza **`yes`** e prima Enter).*

Verifique a alteração do *prompt* da linha de comandos, indicando que a sessão se encontra ativa **no interior do contentor remoto** (tendo a autenticação ocorrido automaticamente através do par de chaves SSH configurado na Parte 0):

```bash
# Comandos executados na sessão remota:
$ whoami
$ pwd
$ ls -la
```

Para encerrar a sessão remota e regressar ao terminal da máquina anfitriã, execute:
```bash
$ exit
```

### Exercício 13: Sincronização Incremental de Diretórios com `rsync`

Para transferir e manter sincronizados diretórios de código entre a máquina local e um servidor remoto sobre uma ligação cifrada SSH, utiliza-se o utilitário **`rsync`**:

1. No sistema local (em `~/IEI/aula07`), crie o diretório `meu-projeto` com dois ficheiros de teste:
   ```bash
   $ mkdir -p ~/IEI/aula07/meu-projeto
   $ echo "# Projeto de Redes IEI" > ~/IEI/aula07/meu-projeto/README.md
   $ echo "print('Execucao no servidor remoto')" > ~/IEI/aula07/meu-projeto/app.py
   ```

2. Transfira e sincronize o diretório para a área de utilizador do servidor remoto utilizando `rsync`:
   ```bash
   # -a: modo de arquivo (preserva permissões e datas); -v: modo detalhado;
   # -z: compressão em trânsito; -P: apresenta progresso da transferência;
   # -e "ssh -p 2222": especifica a utilização do protocolo SSH na porta 2222.
   $ rsync -avzP -e "ssh -p 2222" ~/IEI/aula07/meu-projeto student@localhost:~/
   ```

3. Para verificar o algoritmo de transferência incremental (*delta-transfer*) do `rsync`, adicione uma linha apenas ao ficheiro `README.md` e execute novamente o comando de sincronização:
   ```bash
   $ echo "Alteracao incremental no documento" >> ~/IEI/aula07/meu-projeto/README.md
   $ rsync -avzP -e "ssh -p 2222" ~/IEI/aula07/meu-projeto student@localhost:~/
   ```
   Observe na saída do comando que o `rsync` **transferiu apenas o ficheiro modificado (`README.md`)**, omitindo o ficheiro `app.py` por não ter sofrido alterações.

### Exercício 14: Encaminhamento Local de Portas via Túnel SSH (*Local Port Forwarding*)

Considere o seguinte cenário de administração de sistemas:
Um serviço Web interno encontra-se em execução na porta **`8000`** de um servidor remoto, mas essa porta **não se encontra exposta para o exterior** (na configuração `compose.yml` da Parte 0, apenas a porta `2222` do serviço SSH foi publicada). O mecanismo de **Encaminhamento Local de Portas (*SSH Local Port Forwarding*)** permite aceder a esse serviço interno a partir do navegador da máquina local através da ligação cifrada SSH existente.

> **Ativação do *TCP Forwarding* no Servidor SSH:**
> Por motivos de segurança, diversas imagens e instalações do servidor OpenSSH (incluindo a imagem Alpine Linux utilizada no contentor `iei-ssh-server` e algumas configurações predefinidas em Linux/macOS) trazem o encaminhamento TCP desativado por omissão (`AllowTcpForwarding no`), o que origina o erro `channel X: open failed: administratively prohibited` ao tentar utilizar o túnel.
> Antes de iniciar o exercício, ative a diretiva `AllowTcpForwarding yes` no servidor executando na **máquina anfitriã**:
> ```bash
> # No contentor Docker iei-ssh-server:
> $ docker exec iei-ssh-server sed -i \
    's/AllowTcpForwarding no/AllowTcpForwarding yes/g' \
    /config/sshd/sshd_config /etc/ssh/sshd_config
> $ docker restart iei-ssh-server
> ```
> *(Nota: Num servidor Linux/macOS nativo, esta configuração reside no ficheiro `/etc/ssh/sshd_config`, exigindo o reinício do serviço `sshd` após a alteração).*

1. Inicie uma sessão SSH no servidor remoto:
   ```bash
   $ ssh student@localhost -p 2222
   ```

2. **No interior da sessão remota**, crie um diretório com uma página HTML e inicie um servidor HTTP Python na porta **`8000`**:
   ```bash
   $ mkdir -p ~/servico-interno && cd ~/servico-interno
   $ echo "<h1>Servico acedido via Tunel SSH (Port Forwarding)</h1>" > index.html
   $ python3 -m http.server 8000
   ```
   *(Mantenha este terminal aberto com o processo servidor em execução no contentor).*

3. Abra uma **nova janela de terminal na máquina local** e tente aceder diretamente à porta `8000`:
   ```bash
   $ curl http://localhost:8000
   ```
   A ligação falha com o erro **`Connection refused`**, dado que a porta `8000` do contentor não se encontra mapeada para o sistema anfitrião.

4. Nessa segunda janela de terminal da máquina local, estabeleça um **Túnel SSH**, encaminhando a porta local **`8080`** para a porta **`8000`** do servidor remoto através da ligação SSH na porta `2222`:
   ```bash
   $ ssh -N -L 8080:localhost:8000 student@localhost -p 2222
   ```
   *(A opção `-N` instrui o cliente SSH a não executar comandos remotos, dedicando a ligação exclusivamente ao encaminhamento de portas; mantenha o comando em execução).*

5. No navegador Web (*browser*) da máquina local, aceda ao endereço:
   **[http://localhost:8080](http://localhost:8080)**

   Confirme a apresentação da página HTML servida pelo processo remoto. O pedido HTTP dirigido à porta local `8080` foi encapsulado e cifrado através do túnel SSH (porta `2222`) e entregue na porta `8000` interna do servidor remoto.

6. Concluída a verificação, encerre o túnel SSH premindo **`Ctrl+C`** no segundo terminal e termine o servidor HTTP Python no primeiro terminal (`Ctrl+C`, seguido de `exit` para fechar a sessão SSH).

-----

## Parte 5: Exercícios Complementares de Consolidação

Caso conclua os exercícios anteriores antes do término da sessão laboratorial, realize as seguintes atividades complementares:

### Desafio A: Captura e Inspeção de Pacotes em Tempo Real com `tcpdump`

Para observar ao nível de pacote o envio e receção de mensagens de controlo na interface de rede:

1. Num terminal, inicie o analisador de tráfego `tcpdump` aplicando um filtro para o protocolo `icmp` (utilizado pelo utilitário `ping`) e desativando a resolução numérica (`-n`):
   ```bash
   $ sudo tcpdump -i any icmp -n
   ```
2. Num segundo terminal, envie 2 pacotes ICMP Echo Request para o endereço `8.8.8.8`:
   ```bash
   $ ping -c 2 8.8.8.8
   ```
3. Analise no primeiro terminal os registos capturados em tempo real, identificando os pares `ICMP echo request` (pacote enviado pelo endereço IP local) e `ICMP echo reply` (pacote de resposta proveniente de `8.8.8.8`). Para terminar a captura, prima `Ctrl+C`.

### Desafio B: Representação Geográfica de Rotas IP (Geo-Traceroute)

Utilize a ferramenta `geotraceroute` em Python para combinar o rastreio de encaminhadores (`traceroute`) com geolocalização de endereços IP públicos num mapa:
```bash
$ cd ~/IEI/aula07
$ git clone https://github.com/mariolpantunes/geotraceroute.git
$ cd geotraceroute
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python3 geotraceroute.py google.com
```

-----

## Síntese dos Comandos Abordados

| Comando (Linux / macOS) | Finalidade Técnica (Diagnóstico & Administração) | Exemplo de Utilização |
| :--- | :--- | :--- |
| `ip a` (Linux) / `ifconfig` (macOS) | Listar interfaces de rede, endereço físico (MAC), endereço IPv4/IPv6 e máscara (`/24`). | `ip a` / `ifconfig` |
| `ip r` (Linux) / `netstat -rn -f inet` (macOS) | Consultar a tabela de encaminhamento e identificar o *Default Gateway*. | `ip r` / `route -n get default` |
| `ip neigh` (Linux) / `arp -an` (macOS) | Consultar a tabela ARP (associação entre endereços IPv4 locais e endereços MAC). | `ip neigh` / `arp -an` |
| `ping -c 4` (`ping6 -c 4` p/ IPv6 no macOS) | Testar a conectividade IP (ICMP) até um sistema e medir a latência (`ms`). | `ping -c 4 8.8.8.8` |
| `traceroute <destino>` | Identificar a sequência de encaminhadores (*hops*) até ao endereço de destino. | `traceroute ua.pt` |
| `dig <nome> +short` | Consultar servidores DNS para resolução de nomes de domínio em endereços IP. | `dig ua.pt +short` |
| `curl <url>` | Executar pedidos HTTP/HTTPS a servidores Web ou APIs a partir do terminal. | `curl -I http://localhost:8000` |
| `ss -tuln` (Linux) / `lsof -nP -iTCP -sTCP:LISTEN` (macOS) | Listar *sockets* e portas TCP/UDP em estado de escuta (*LISTEN*) no sistema local. | `ss -tuln` |
| `nmap <alvo>` | Efetuar sondagem de portas (*port scan*) para identificar serviços ativos num sistema. | `nmap localhost` |
| `ssh <user>@<host>` | Estabelecer sessão remota segura de linha de comandos num servidor SSH. | `ssh student@localhost -p 2222` |
| `rsync -avzP` | Transferir e sincronizar diretórios de forma incremental sobre SSH. | `rsync -avzP ./dir student@host:~/` |
| `ssh -N -L <p1>:localhost:<p2>` | Estabelecer encaminhamento local de portas (*SSH Tunnel*) entre a porta local `p1` e a porta remota `p2`. | `ssh -N -L 8080:localhost:8000 user@host` |

