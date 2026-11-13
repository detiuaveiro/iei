---
title: 47138 - Introduction to Computer Engineering
subtitle: "Computer Networks: Fundamentals, Configuration & Diagnostics"
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

# Practical Laboratory Guide

**Educational Context & Objectives:**
In previous sessions, various networking mechanisms were employed — such as executing HTTP requests via `curl`, port mapping in Docker containers (`-p 8080:80`), and authenticating remotely with Git via SSH. In this **3-hour** laboratory session, the goal is to inspect network interface configurations, understand packet routing towards the Internet, and **execute systematic diagnostic procedures (*troubleshooting*) when an application or server encounters connectivity failures** (a critical competency for course projects and for **Class 08**, which is dedicated to network programming in Python):

* **Part 0 — Environment Setup & Test Server (Docker SSH):** Installation of network diagnostic utilities (Linux and macOS), generation of an SSH asymmetric cryptographic key pair (`ed25519`), and instantiation of an isolated OpenSSH server container for remote administration exercises.
* **Part 1 — Inspecting the Local Machine and the Local Area Network (LAN):** Identification of network interfaces, physical address (**MAC**), logical address (**IPv4**), and subnet mask (`/24`) using `ip a` / `ifconfig`, verification of the loopback interface (`127.0.0.1`), discovery of the local router (*Default Gateway* with `ip r` / `netstat -rn`), and inspection of the **ARP** table (`ip neigh` / `arp -an`).
* **Part 2 — From Local Area Network to the Internet (WAN, NAT, and DNS):** Connectivity and latency verification by IP address vs. domain name (`ping`), analysis of intermediate routing hops (`traceroute`), domain name resolution queries in the **DNS** system (`dig` and `/etc/hosts`), and determination of the **Public IP Address** and the role of **NAT** (`curl`).
* **Part 3 — Ports, Services, and Socket Diagnostics (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`):** Inspection of active listening sockets (*LISTEN*) on the host system (`ss -tuln` / `lsof`), experimental analysis of the critical distinction between binding to `127.0.0.1` vs. `0.0.0.0` (direct preparation for Class 08), and port scanning with `nmap`.
* **Part 4 — Secure Remote Administration (SSH, `rsync`, and SSH Port Forwarding):** Remote session establishment via `ssh`, incremental file synchronization with `rsync`, and configuration of an **SSH Tunnel (`ssh -L` — *Local Port Forwarding*)** to access internal web services securely.
* **Part 5 — Optional Consolidation Challenges:** Real-time packet capture and inspection with `tcpdump` and geographic route visualization (Geo-Traceroute).

\vspace{0.5em}

### Working Directory Setup

Before starting the exercises, create and navigate to the dedicated working directory for this session:

```bash
$ mkdir -p ~/IEI/aula07
$ cd ~/IEI/aula07
```

All files created during the laboratory session must remain organized inside this directory.

> **Note on file paths:**
> The commands throughout this guide assume that your terminal session is positioned in `~/IEI/aula07`.

-----

## Part 0: Environment Setup & Test Server (Docker SSH)

Before exploring network operations, install the required diagnostic tools on your operating system (Linux or macOS) and instantiate an OpenSSH server inside a Docker container, which will serve as our isolated remote test machine.

### Step 1: Install Network Diagnostic Utilities

Open your terminal and install the required utility packages:

* **On Linux (Ubuntu / Debian):**
  ```bash
  $ sudo apt update
  $ sudo apt install -y iproute2 net-tools dnsutils traceroute nmap curl python3-pip python3-venv python3-tk
  ```
* **On macOS (via Homebrew):**
  The utilities `ping`, `traceroute`, `dig`, `curl`, `arp`, `lsof`, `netstat`, `ssh`, `rsync`, and `tcpdump` are natively installed on macOS. Install `nmap` (and optionally `iproute2mac` to enable the Linux `ip a` and `ip r` command syntax on macOS):
  ```bash
  $ brew install nmap iproute2mac
  ```

Summary of tools:
  * `ip` / `ifconfig` / `arp` / `ss` / `lsof`: Commands to inspect network interfaces, IP addresses, routing tables, ARP cache, and transport sockets.
  * `dig`: Tool to query DNS name servers directly.
  * `traceroute`: Tool to identify intermediate routers (*hops*) towards a destination host.
  * `nmap`: Security scanner to probe open transport ports and services on a target system.
  * `curl`: Utility to transfer data and execute HTTP/HTTPS requests from the command line.

### Step 2: Verify or Generate an SSH Key Pair

Secure remote authentication relies on asymmetric cryptography via an SSH key pair (**Private Key**, kept confidential on your client computer, and **Public Key**, installed on the target server).

1. Check whether an `ed25519` key pair already exists in `~/.ssh`:
   ```bash
   $ ls -la ~/.ssh/id_ed25519*
   ```
2. **If it does not exist**, generate a new key pair without a passphrase:
   ```bash
   $ ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
   ```
   *(Security notice: `~/.ssh/id_ed25519.pub` is your public key and can be distributed freely; `~/.ssh/id_ed25519` contains your private key and **must never** be shared or copied to other machines).*

### Step 3: Instantiate the Test SSH Server (Docker Compose)

Use Docker Compose to instantiate an OpenSSH Linux server listening on host port **`2222`**:

1. Create a dedicated subfolder named `ssh-server` and enter it:
   ```bash
   $ mkdir -p ~/IEI/aula07/ssh-server
   $ cd ~/IEI/aula07/ssh-server
   ```

2. Create the file `custom-openssh-server.Dockerfile`, which extends a lightweight OpenSSH image with `rsync` and `python3`:
   ```dockerfile
   FROM lscr.io/linuxserver/openssh-server:latest
   RUN apk update && apk add rsync python3 && rm -rf /var/cache/apk/*
   ```

3. Create the `compose.yml` file to configure the container and map port `2222`:
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
         - "2222:2222" # Maps host port 2222 to container port 2222
       restart: unless-stopped
   ```

4. Create the `authorized_keys` directory and copy your **public key** into it, granting access to the `student` user:
   ```bash
   $ mkdir -p authorized_keys
   $ cp ~/.ssh/id_ed25519.pub ./authorized_keys/student.pub
   ```

5. Build and launch the container in the background (*detached mode*), then verify its execution status:
   ```bash
   $ docker compose up -d --build
   $ docker compose ps
   ```

6. Return to the session working directory:
   ```bash
   $ cd ~/IEI/aula07
   ```

-----

## Part 1: Inspecting the Local Machine and the Local Area Network (LAN)

When diagnosing network connectivity issues, the first diagnostic step involves inspecting the configuration of the local host's network interfaces.

### Exercise 1: Identify MAC Address, IP Address, and Subnet Mask (`ip a` / `ifconfig`)

List the network interfaces configured on your host system:

* **On Linux** (or on macOS with `iproute2mac`):
  ```bash
  $ ip a
  ```
* **On macOS (native):**
  ```bash
  $ ifconfig
  ```

Inspect the output and locate the following components:
1. **The `lo` (Linux) or `lo0` (macOS) Interface — Loopback:** Notice the assigned addresses `inet 127.0.0.1` and `inet6 ::1`. This is the virtual internal interface routing traffic within the host itself (`localhost`).
2. **Your Primary Network Interface** (typically named `eth0`, `enp0s3`, or `wlan0` on Linux, and **`en0`** on macOS):
   * **MAC Address (Layer 2 — Data Link):** Identify the line `link/ether` (with `ip a`) or `ether` (with `ifconfig` on macOS), e.g., `08:00:27:1a:2b:3c`. This is the 48-bit physical identifier of your network card on the local link.
   * **IPv4 Address and Subnet Mask (Layer 3 — Network):** Identify the `inet` line (e.g., `192.168.1.50/24` on Linux, or `inet 192.168.1.50 netmask 0xffffff00` on macOS `ifconfig`, where hexadecimal `0xffffff00` corresponds to `255.255.255.0` or `/24`).
     * The `/24` prefix (`255.255.255.0`) indicates that the first 3 octets define the **network prefix**, while the final octet identifies the **specific host within that subnet** (usable range `.1` to `.254`).
   * **IPv6 Link-Local Address:** Locate the `inet6 fe80::...` address, which is automatically assigned for communication strictly within the local link.
3. **The `docker0` / `br-...` Interface (on Linux):** On native Linux installations, Docker creates a dedicated virtual bridge interface with a private IP range (typically `172.17.0.1/16`) to interconnect containers *(on macOS, Docker Desktop runs within an underlying lightweight Linux virtual machine, so that interface resides within the VM)*.

### Exercise 2: Verify the Local TCP/IP Stack (`localhost` / Loopback)

Before testing physical link connectivity (Ethernet or Wi-Fi), verify that the operating system's internal TCP/IP network stack is operating properly. Send 4 ICMP Echo Request packets (`-c 4`) to the loopback addresses:

```bash
# Test Loopback interface in IPv4 (Linux and macOS)
$ ping -c 4 127.0.0.1

# Test Loopback interface in IPv6 (on Linux)
$ ping -c 4 ::1

# Test Loopback interface in IPv6 (on macOS ping6 is used)
$ ping6 -c 4 ::1
```

Examine the response time (`time=... ms`) and packet loss rate (`0% packet loss`). Because packets are handled entirely in memory by the operating system kernel without traversing any physical medium, latency is virtually instantaneous (typically below `0.1 ms`).

### Exercise 3: Identify the Default Gateway and Test LAN Connectivity

To route packets destined for external networks (such as the Internet), the local host must identify the IP address of the local network router — known as the **Default Gateway**.

1. Query the operating system routing table to discover the default route:
   * **On Linux** (or on macOS with `iproute2mac`):
     ```bash
     $ ip route show default
     ```
     *(Or simply `ip r`).* The output format is `default via 192.168.1.1 dev eth0`, where the IP following **`via`** is your **Default Gateway**.
   * **On macOS (native):**
     ```bash
     $ netstat -rn -f inet | grep default
     # or:
     $ route -n get default
     ```
     The address listed under `Gateway` (or the `gateway:` field) indicates your **Default Gateway**.

2. Test network connectivity to your router using `ping` (replace with the IP obtained above):
   ```bash
   $ ping -c 4 <DEFAULT_GATEWAY_IP>
   ```
   Receiving replies with `0% packet loss` confirms that your physical link (cable or Wi-Fi) and Layer 2/3 connectivity to the local router are fully functional.

### Exercise 4: Inspect Address Resolution in the ARP Table (`ip neigh` / `arp -an`)

To encapsulate an IP packet destined for the Default Gateway within an Ethernet frame (Layer 2), the operating system uses the **ARP (*Address Resolution Protocol*)** to discover the **physical MAC address** corresponding to that router's IPv4 address.

Inspect the ARP cache stored in your operating system:

* **On Linux:**
  ```bash
  $ ip neigh
  ```
* **On macOS (and also supported on Linux):**
  ```bash
  $ arp -an
  ```

Find the entry corresponding to your Default Gateway's IP: you will see its physical MAC address alongside. This translation allows the network interface to properly address Layer 2 Ethernet frames on the local link.

-----

## Part 2: From Local Area Network to the Internet (WAN, NAT, and DNS)

Having verified local connectivity to the Default Gateway, we now trace traffic forwarded across the wide-area boundary (WAN / Internet) and analyze domain name resolution.

### Exercise 5: Test External Connectivity by IP Address vs. Domain Name (`ping`)

Connectivity failures can stem either from a lack of IP routing to external networks or exclusively from failures within the Domain Name System (**DNS**). To differentiate between the two, perform two separate checks:

1. Test raw IP reachability directly against a well-known public external IP address (e.g., Google's public DNS at `8.8.8.8`):
   ```bash
   $ ping -c 4 8.8.8.8
   ```
   *Successful responses verify end-to-end IP routing to the Internet.* Observe the Round-Trip Time (`time=... ms`): because packets traverse physical fiber-optic lines across multiple autonomous systems and datacenters, latency will typically range between `8 ms` and `30 ms`.

2. Now test reachability using a **domain name**:
   ```bash
   $ ping -c 4 ua.pt
   ```
   Notice the first line of output: the operating system first queried the **DNS** service to resolve `ua.pt` to its corresponding IPv4 address (e.g., `193.136.172.10`) before dispatching ICMP packets.

> **Diagnostic Principle:** If `ping 8.8.8.8` succeeds but `ping ua.pt` returns a resolution error (*"Temporary failure in name resolution"* or *"cannot resolve...: Unknown host"*), IP connectivity is fully functional; the failure is isolated to your **DNS** configuration.

### Exercise 6: Trace Intermediate Network Hops (`traceroute`)

To identify each intermediate router traversed by an IP packet from your machine to a destination, run `traceroute`:

```bash
$ traceroute 8.8.8.8
```

Examine the ordered sequence of hops:
* **Hop 1** is always your local Default Gateway.
* Subsequent hops correspond to upstream routers belonging to your Internet Service Provider (ISP), the national academic backbone (RCTS / FCCN), and transit providers until reaching Google's network edge.
* *(Technical note: Lines displaying asterisks `* * *` indicate that an intermediate router is configured to discard or rate-limit ICMP Time Exceeded diagnostic messages, which does not necessarily impede packet forwarding to subsequent hops).*

Execute a trace towards the University of Aveiro web server:
```bash
$ traceroute ua.pt
```

### Exercise 7: Domain Name Resolution (`dig` and `/etc/hosts`)

Inspect the process of resolving human-readable domain names into IP addresses:

1. Use `dig` to query the IPv4 host address (Type **`A`** record) for `ua.pt`:
   ```bash
   $ dig ua.pt A
   ```
   Under `;; ANSWER SECTION:`, locate the resolved IPv4 address along with its Time-to-Live (*TTL*). To obtain a concise numerical answer, append `+short`:
   ```bash
   $ dig ua.pt A +short
   ```

2. Perform a reverse DNS lookup using the `-x` parameter to discover the hostname associated with a public IP address:
   ```bash
   $ dig -x 8.8.8.8 +short
   ```

3. Inspect your local static resolution file `/etc/hosts` (which the operating system checks **prior** to sending DNS requests across the network):
   ```bash
   $ cat /etc/hosts
   ```
   Notice the standard entry `127.0.0.1 localhost`, which maps `localhost` directly to the loopback IP address without requiring network DNS queries.

### Exercise 8: Determine Your Public IP Address and Understand NAT (`curl`)

> **The Concept of NAT (*Network Address Translation*):**
> As observed in Exercise 1, host network interfaces are assigned **Private IP Addresses** (belonging to RFC 1918 ranges such as `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`), which are valid strictly within the LAN and cannot be routed across the public Internet. To allow multiple devices within a private network to access the Internet concurrently while sharing a single **Public IP Address**, the border router performs **NAT**: when forwarding an outbound packet from the LAN to the WAN, the router translates the private source IP to its own **Public IP** and records this mapping in an internal state table; when response packets return from the Internet, the router inspects the table, restores the destination IP to the appropriate private host address, and delivers the packet.

To discover the **Public IP Address** through which your host is viewed by external servers on the Internet, query the public `ipinfo.io` API via `curl`:

```bash
$ curl -s https://ipinfo.io/json
```

Analyze the JSON response:
* `ip`: The **Public IP Address** currently assigned to your network's border router (shared via NAT among all hosts on your local network).
* `city` / `region` / `org`: Approximate geographical location and the Autonomous System / ISP providing network connectivity.

-----

## Part 3: Ports, Services, and Socket Diagnostics (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`)

In container orchestration (**Docker**) and distributed application development (**Class 08 — Network Programming**), it is essential to determine which transport ports are in a listening state (*LISTEN*) and understand how socket binding parameters control service accessibility.

### Exercise 9: Inspect Listening Ports on the Local Host (`ss` / `lsof` and `nmap`)

In Part 0, an OpenSSH container was launched with port `2222` mapped to the host system. Verify at the operating system level that this port is open and actively awaiting connections:

1. List all network sockets in a listening state (*LISTEN*) on your machine:
   * **On Linux (`ss -tuln` — numeric TCP/UDP listening sockets):**
     ```bash
     $ ss -tuln
     ```
   * **On macOS (`lsof` — lists TCP sockets in state `LISTEN` without hostname/port resolution):**
     ```bash
     $ lsof -nP -iTCP -sTCP:LISTEN
     ```
   Locate the entry ending in **`:2222`** (e.g., `0.0.0.0:2222` on Linux or `*:2222 (LISTEN)` on macOS). This confirms that a process on your host is actively accepting TCP connections on port `2222`.

2. Execute a port scan against your local machine (`localhost`) using **`nmap`** (syntax is identical on Linux and macOS):
   ```bash
   $ nmap localhost
   ```
   Verify in the `PORT / STATE / SERVICE` table that port `2222/tcp` is reported as **`open`**.

### Exercise 10: Binding Services to Network Interfaces (`127.0.0.1` vs. `0.0.0.0`)

> **The Meaning of `0.0.0.0` in Server Socket Binding:**
> Unlike `127.0.0.1` (which binds exclusively to the virtual loopback interface), the address `0.0.0.0` is not an individual host interface, but rather a **meta-constant convention (`INADDR_ANY`)**. When a server binds to `0.0.0.0`, it instructs the operating system kernel to accept incoming connections destined for that port across **all network interfaces available on the system** (including `localhost`, physical Ethernet/Wi-Fi adapters, and virtual Docker bridge networks).

To observe experimentally the critical difference between binding a server to **`127.0.0.1`** vs. **`0.0.0.0`**, execute the following steps:

1. Create a temporary testing directory containing a simple HTML document:
   ```bash
   $ mkdir -p ~/IEI/aula07/teste-web && cd ~/IEI/aula07/teste-web
   $ echo "<h1>Servidor de Teste IEI</h1>" > index.html
   ```

2. **Scenario A — Binding Exclusively to `127.0.0.1` (Loopback Only):**
   Launch Python's built-in HTTP server on port `8000` bound strictly to `127.0.0.1`:
   ```bash
   $ python3 -m http.server 8000 --bind 127.0.0.1
   ```
   *(Keep this terminal open with the server running, and **open a second terminal window**).*

3. In the **second terminal window**, inspect the listening socket for port `8000`:
   * **On Linux:**
     ```bash
     $ ss -tuln | grep 8000
     ```
   * **On macOS:**
     ```bash
     $ lsof -nP -iTCP -sTCP:LISTEN | grep 8000
     ```
   Notice that the socket is bound to **`127.0.0.1:8000`**:
   * A request from the local machine (`curl -I http://127.0.0.1:8000`) succeeds with **`HTTP/1.0 200 OK`**.
   * However, any connection attempt from another computer on the LAN (or from the host into a Docker container configured this way) **will be refused (`Connection refused`)**, because the process does not listen on external network interfaces.

4. In the first terminal, terminate the server with **`Ctrl+C`**, and restart it bound to **`0.0.0.0`** (all network interfaces):
   ```bash
   $ python3 -m http.server 8000 --bind 0.0.0.0
   ```

5. In the second terminal, rerun the diagnostic command (`ss -tuln | grep 8000` on Linux, or `lsof -nP -iTCP -sTCP:LISTEN | grep 8000` on macOS):
   The socket now shows **`0.0.0.0:8000`** (Linux) or **`*:8000`** (macOS), accepting connections across all network interfaces. Test reachability with `curl -I http://localhost:8000`, close the second terminal, and stop the Python server in the first terminal with **`Ctrl+C`**.

   Return to the session working directory:
   ```bash
   $ cd ~/IEI/aula07
   ```

### Exercise 11: Port Scanning on an Authorized Public Test Server (`nmap`)

> **Legal and Ethical Notice:** Performing port scans against systems or networks without explicit authorization is strictly prohibited. For educational exploration, the Nmap project maintains the officially authorized test server **`scanme.nmap.org`**.

Scan the open ports on this public test host:

```bash
$ nmap scanme.nmap.org
```

Review the detected services in the output table, identifying standard open ports such as **`22/tcp` (`ssh`)** for remote administration and **`80/tcp` (`http`)** for web services.

-----

## Part 4: Secure Remote Administration (SSH, `rsync`, and SSH Port Forwarding)

We now utilize the OpenSSH Linux server container instantiated in Part 0 (listening on port `2222`) to execute three fundamental system administration workflows: remote shell access, incremental file synchronization, and secure port forwarding.

### Exercise 12: Establish a Remote Shell Session via `ssh`

Connect as user `student` to the server running on `localhost` at port `2222`:

```bash
$ ssh student@localhost -p 2222
```

*(On your first connection to a new host, SSH prompts you to accept its host key fingerprint: `Are you sure you want to continue connecting (yes/no/[fingerprint])?` — type **`yes`** and press Enter).*

Notice that the shell prompt changes, indicating that commands are executing **inside the remote container** (authenticated automatically via the SSH key pair configured in Part 0):

```bash
# Commands executed INSIDE the remote server:
$ whoami
$ pwd
$ ls -la
```

To disconnect from the remote session and return to your local machine:
```bash
$ exit
```

### Exercise 13: Incremental Directory Synchronization with `rsync`

To synchronize project files between your local machine and a remote server over an encrypted SSH connection, use **`rsync`**:

1. On your local machine (in `~/IEI/aula07`), create a directory named `meu-projeto` with two sample files:
   ```bash
   $ mkdir -p ~/IEI/aula07/meu-projeto
   $ echo "# Projeto de Redes IEI" > ~/IEI/aula07/meu-projeto/README.md
   $ echo "print('Running on remote server')" > ~/IEI/aula07/meu-projeto/app.py
   ```

2. Synchronize this directory to the remote server using `rsync`:
   ```bash
   # -a: archive mode (preserves permissions and timestamps); -v: verbose;
   # -z: in-transit compression; -P: progress indicator;
   # -e "ssh -p 2222": specifies SSH protocol on port 2222.
   $ rsync -avzP -e "ssh -p 2222" ~/IEI/aula07/meu-projeto student@localhost:~/
   ```

3. To observe `rsync`'s differential transfer algorithm (*delta-transfer*), append a single line to `README.md` and execute the exact same command again:
   ```bash
   $ echo "Incremental update in file" >> ~/IEI/aula07/meu-projeto/README.md
   $ rsync -avzP -e "ssh -p 2222" ~/IEI/aula07/meu-projeto student@localhost:~/
   ```
   Notice in the command output that `rsync` **transferred only the modified file (`README.md`)**, skipping `app.py` because its contents remained identical.

### Exercise 14: Local Port Forwarding via SSH Tunnel (*SSH Local Port Forwarding*)

Consider the following common systems engineering scenario:
An internal web service runs on port **`8000`** inside a remote server, but that port **is not exposed to external networks** (in our `compose.yml` from Part 0, only port `2222` was mapped). **SSH Local Port Forwarding** allows a local client to securely access that internal service through the established SSH connection.

> **Technical Notice — Enabling TCP Forwarding on the SSH Server:**
> For security reasons, several OpenSSH server distributions (including the Alpine Linux image used in the `iei-ssh-server` container and certain default Linux/macOS server installations) disable TCP port forwarding by default (`AllowTcpForwarding no`), which triggers the error `channel X: open failed: administratively prohibited` when attempting to use the tunnel.
> Before starting the exercise, enable `AllowTcpForwarding yes` on the server by executing on your **host machine**:
> ```bash
> # On the iei-ssh-server Docker container:
> $ docker exec iei-ssh-server sed -i 's/AllowTcpForwarding no/AllowTcpForwarding yes/g' /config/sshd/sshd_config /etc/ssh/sshd_config
> $ docker restart iei-ssh-server
> ```
> *(Note: On a native Linux/macOS SSH server, this directive is located in `/etc/ssh/sshd_config` and requires restarting the `sshd` daemon after modification).*

1. Open an SSH session to the remote server:
   ```bash
   $ ssh student@localhost -p 2222
   ```

2. **Inside the remote server session**, create a test web page and start a Python HTTP server on port **`8000`**:
   ```bash
   $ mkdir -p ~/servico-interno && cd ~/servico-interno
   $ echo "<h1>Internal Web Service accessed via SSH Tunnel (Port Forwarding)</h1>" > index.html
   $ python3 -m http.server 8000
   ```
   *(Keep this terminal open with the server running inside the container).*

3. Open a **new terminal window on your local machine** and attempt to connect directly to port `8000`:
   ```bash
   $ curl http://localhost:8000
   ```
   The connection fails with **`Connection refused`**, because port `8000` is internal to the container and unexposed on the host.

4. In that second local terminal window, establish an **SSH Tunnel**, forwarding local port **`8080`** to port **`8000`** on the remote server via the SSH connection on port `2222`:
   ```bash
   $ ssh -N -L 8080:localhost:8000 student@localhost -p 2222
   ```
   *(The `-N` option specifies that no remote commands should be executed, dedicating the session solely to port forwarding; leave this command running).*

5. In your local machine's **Web Browser**, navigate to:
   **[http://localhost:8080](http://localhost:8080)**

   The browser renders the web page served by the internal Python process. HTTP traffic directed to local port `8080` is encapsulated and encrypted across the SSH connection (port `2222`) and delivered directly to internal port `8000` on the server.

6. Once verified, close the tunnel by pressing **`Ctrl+C`** in the second terminal, and stop the Python HTTP server in the first terminal (`Ctrl+C`, followed by `exit` to close the SSH session).

-----

## Part 5: Optional Consolidation Challenges

If you complete the preceding exercises before the end of the lab session, undertake these advanced challenges:

### Challenge A: Real-Time Packet Capture and Inspection with `tcpdump`

To monitor packet transmission and reception directly at the network interface level:
1. In a terminal window, launch `tcpdump` with a filter for `icmp` traffic (used by `ping`) and disable numeric name resolution (`-n`):
   ```bash
   $ sudo tcpdump -i any icmp -n
   ```
2. In a second terminal window, send 2 ICMP Echo Request packets to `8.8.8.8`:
   ```bash
   $ ping -c 2 8.8.8.8
   ```
3. Observe in the first terminal the paired `ICMP echo request` (dispatched from your local IP) and `ICMP echo reply` (returned from `8.8.8.8`). Press `Ctrl+C` to terminate the capture.

### Challenge B: Geographic Route Mapping (Geo-Traceroute)

Use the Python `geotraceroute` utility to combine hop tracing with geolocation data, rendering packet routes on an interactive map:
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

## Summary of Diagnostic and Administration Commands

| Command (Linux / macOS) | Technical Purpose (Diagnostics & Administration) | Practical Example |
| :--- | :--- | :--- |
| `ip a` (Linux) / `ifconfig` (macOS) | List network interfaces, physical MAC address, IPv4/IPv6 addresses, and subnet mask (`/24`). | `ip a` / `ifconfig` |
| `ip r` (Linux) / `netstat -rn -f inet` (macOS) | Inspect routing table and identify the *Default Gateway*. | `ip r` / `route -n get default` |
| `ip neigh` (Linux) / `arp -an` (macOS) | Inspect ARP cache (mapping between local IPv4 addresses and MAC addresses). | `ip neigh` / `arp -an` |
| `ping -c 4` (`ping6 -c 4` for IPv6 on macOS) | Test end-to-end IP reachability (ICMP) and measure Round-Trip latency (`ms`). | `ping -c 4 8.8.8.8` |
| `traceroute <destination>` | Identify intermediate routing hops to destination host. | `traceroute ua.pt` |
| `dig <domain> +short` | Query DNS servers to resolve domain names to IP addresses. | `dig ua.pt +short` |
| `curl <url>` | Issue HTTP/HTTPS requests to web servers or APIs from the terminal. | `curl -I http://localhost:8000` |
| `ss -tuln` (Linux) / `lsof -nP -iTCP -sTCP:LISTEN` (macOS) | List listening transport sockets (*LISTEN*) on the local host. | `ss -tuln` |
| `nmap <target>` | Probe open transport ports to identify active services on a target system. | `nmap localhost` |
| `ssh <user>@<host>` | Establish an encrypted remote shell session on an SSH server. | `ssh student@localhost -p 2222` |
| `rsync -avzP` | Synchronize directories incrementally over an encrypted SSH connection. | `rsync -avzP ./dir student@host:~/` |
| `ssh -N -L <p1>:localhost:<p2>` | Configure an SSH Local Port Forwarding tunnel between local port `p1` and remote port `p2`. | `ssh -N -L 8080:localhost:8000 user@host` |
