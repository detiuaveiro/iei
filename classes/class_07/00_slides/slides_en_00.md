---
title: 47138 - Introduction to Computer Engineering
subtitle: "Computer Networks: Fundamentals, Configuration & Diagnostics"
institute: Universidade de Aveiro
date: November 09, 2026
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
 - \BeforeBeginEnvironment{Shaded}{\vspace{1.0em}}
 - \AfterEndEnvironment{Shaded}{\vspace{0.6em}}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Session Overview

  * **Part I — How is a Network Built? (From Laptop to the Internet):**
      * Network scales (**PAN**, **LAN**, **MAN**, **WAN**), everyday equipment (**Switch**, **Access Point**, **Router**, **ONT**), and the **OSI Model (7 layers)** with encapsulation.
  * **Part II — Addresses and Ports (Locating the Machine and the Program):**
      * Physical address (**MAC**) vs. logical address (**IP**), routing (*Switch* vs. *Routers*), **Default Gateway** and **ARP**, **IPv4** and subnet mask (`/24`), special IP ranges, **IPv6**, and **Transport Ports** (including Docker mapping and the *Reverse Proxy* challenge).
  * **Part III — IP Configuration (DHCP vs. Static) and DNS:**
      * The 4 essential network parameters, automatic configuration (**DHCP**) vs. manual (**Static IP**), domain name resolution (**DNS**), and the hierarchical DNS tree structure.
  * **Part IV — Configuration, Diagnostics (Debug), and Remote Access:**
      * Essential Linux diagnostics (`ip`, `ping`, `traceroute`, `dig`, `ss`, `nmap`, `curl`), **Firewalls** and client isolation in `eduroam`, a **5-Step Network Troubleshooting** methodology, and secure remote operations with **SSH**, **`rsync`**, and **SSH Tunnels**.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: How is a Network Built? (From Laptop to the Internet)}}
\end{center}

-----

## What is a Network? PAN, LAN, MAN, and WAN

A computer network is an interconnected system of devices that communicate and share resources. Classified by geographical scale:

\vspace{0.2em}

\begin{center}
\includegraphics[width=0.96\linewidth,height=0.40\textheight,keepaspectratio]{figures/network_scales_lan_man_wan.jpg}
\end{center}

\vspace{-0.4em}

::::: columns
::: {.column width="50%"}

  * **PAN (*Personal Area*):** Devices centered around a single user (~a few meters; Bluetooth / Wi-Fi Direct).
  * **LAN (*Local Area*):** Home, lab, building, or Docker (high speed via Ethernet cable and Wi-Fi).

:::
::: {.column width="50%"}

  * **MAN (*Metropolitan Area*):** Multiple buildings across a city or university campus (fiber-optic rings).
  * **WAN (*Wide Area*):** Interconnected cities, countries, and continents (the global **Internet** via submarine cables and satellites).

:::
:::::

-----

## Local Network Equipment: Switch and Access Point

Interconnecting devices within the same LAN:

::::: columns
::: {.column width="54%"}

  * **Switch:**
      * Connects devices via Ethernet cables.
      * Delivers packets **only** to the intended recipient's physical port.
      * *(Replaced the legacy **Hub**, which broadcast to all ports and caused collisions).*
  * **Access Point (AP):**
      * Connects wireless devices (Wi-Fi) to the wired infrastructure.
      * Integrates laptops and mobile devices into the same LAN.

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/network_devices_router_switch_ap.jpg}

\vspace{0.2em}
{\tiny \textit{Switches and Access Points interconnect devices within the same LAN.}}
\end{center}

:::
:::::

-----

## The Frontier with the Internet: Router and ONT

Communication beyond the local network boundary:

::::: columns
::: {.column width="54%"}

  * **Router:**
      * Interconnects **distinct networks** (LAN 1, LAN 2, and the Internet).
      * Forwards packets between networks along the optimal path.
  * **ONT (*Optical Network Terminal*):**
      * Converts optical signals (fiber from ISP) into electrical signals (Ethernet).
  * **The "Home Gateway / Router":**
      * A **4-in-1** appliance: integrates ONT, Router, Switch, and Access Point in a single physical unit.

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/network_devices_router_switch_ap.jpg}

\vspace{0.2em}
{\tiny \textit{The Router interconnects distinct networks (LAN 1, LAN 2, and the Internet).}}
\end{center}

:::
:::::

-----

## How the Network is Structured: The OSI Model (7 Layers)

The **OSI** (*Open Systems Interconnection*) model standardizes network communication across **7 layers**:

\vspace{0.3em}

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/network_7_layers_osi_encapsulation.jpg}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part II: Addresses and Ports (Locating the Machine and the Program)}}
\end{center}

-----

## Two Addresses on Every Device: MAC vs. IP

Each network interface (Ethernet or Wi-Fi) operates with **two distinct addressing schemes**:

::::: columns
::: {.column width="50%"}

  * **MAC Address (Physical / Layer 2 — Data Link):**
      * Example: `00:1A:2B:3C:4D:5E` (48 bits in hexadecimal notation).
      * Burned into hardware during manufacturing (immutable in NIC).
      * **Purpose:** Identifies the interface within the **immediate local link (*hop-by-hop*)**. The destination MAC changes at every router hop.
      * **Analogy:** National Identity Card (identifies the device locally).

:::
::: {.column width="50%"}

  * **IP Address (Logical / Layer 3 — Network):**
      * Example: `192.168.1.10` (IPv4).
      * Assigned logically by the network topology.
      * **Purpose:** Identifies the **origin and final destination (*end-to-end*)** across multiple interconnected networks.
      * **Analogy:** Postal Mailing Address (changes when moving to another network).

:::
:::::

\vspace{0.6em}

\begin{center}
\textbf{The IP defines the global final destination; the MAC defines who receives the frame on the next local hop (whether a router or the target host on the LAN).}
\end{center}

-----

## Routing in Practice: Local Delivery (Switch) vs. Hop-by-Hop (Routers)

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/network_routing_mac_vs_ip.png}
\end{center}

-----

## How Routing Works: The Role of the Gateway and ARP

  * **1. Remote Communication (Different Network):**
      * **Laptop 4** (`192.168.3.90`) transmits data to **Laptop 1** (`192.168.1.100` on a remote subnet).
      * The **Destination Network Address (IP: `192.168.1.100`) remains constant (*end-to-end*)** throughout the entire transit.
      * Because the destination lies outside the local subnet, Laptop 4 forwards the physical frame to its local exit: the **Default Gateway (Router 1)**, setting `Destination MAC = FF:FF:FF:FF:FF:FF`.
      * **Router 1** decapsulates the frame, consults its routing table, forwards the packet toward `192.168.1.0`, and rewrites the MAC header at each hop (*hop-by-hop*).
  * **2. Local Communication (Same Network):**
      * When Laptop 2 (`192.168.1.101`) transmits to Laptop 1 (`192.168.1.100`), the frame travels **directly across the Switch** with `Destination MAC = AA:AA:AA:AA:AA:AA` (without traversing any router).
  * **3. The Role of ARP (*Address Resolution Protocol*):**
      * To populate the destination MAC in the Ethernet frame:
      * **Target host on the same subnet $\rightarrow$** ARP resolves the physical MAC of the destination host directly.
      * **Target host outside the subnet $\rightarrow$** ARP resolves the physical MAC of the **Default Gateway**.

-----

## IPv4 Addresses and Subnet Masks (Simplified)

An IPv4 address consists of 4 octets ranging from `0` to `255` separated by dots, and is **always** paired with a **Subnet Mask**:

  * **IP Address:** `192.168.1.10`
  * **Subnet Mask:** `255.255.255.0` (also written concisely in CIDR notation as **`/24`**).
  * **Intuitive Interpretation:**
      * Where the mask contains `255`, the octets identify **the Network Prefix (the Street)**: `192.168.1.x`
      * Where the mask contains `0`, the octet identifies **the Host Identifier (the House Number)**: `.10` (usable from `.1` to `.254`).

\vspace{0.4em}

```text
IP Address:       192  .  168  .   1   .   10
Mask (/24):       255  .  255  .  255  .   0
                [---- NETWORK PREFIX ----] [HOST]
```

\vspace{0.3em}

  * **Operational Decision:**
      * Destination `192.168.1.25` $\rightarrow$ Prefix matches `192.168.1.` $\rightarrow$ **Local Subnet (LAN)!** Forward directly through the Switch.
      * Destination `8.8.8.8` $\rightarrow$ Prefix differs from `192.168.1.` $\rightarrow$ **External Network (Internet)!** Forward to the **Default Gateway**.

-----

## Special IP Addresses and Address Blocks

  * **`127.0.0.1` (`localhost` / Loopback Interface):**
      * Designates **"the local host itself"**. Network traffic is processed entirely in memory by the operating system kernel and never transits through physical interfaces.
      * Crucial for testing local servers and network applications in isolation.
  * **Reserved Subnet Addresses (e.g., in a `/24` subnet):**
      * **First Address (`... .0`):** Identifies the **Network ID** itself (cannot be assigned to individual hosts).
      * **Last Address (`... .255`):** **Subnet Broadcast Address** (packets addressed here are delivered to all active hosts on the LAN).
  * **Private IP Addresses (RFC 1918 — LAN usage only):**
      * Reserved blocks: `10.0.0.0/8` (enterprise / campus networks), `172.16.0.0/12` (internal Docker bridges), and `192.168.0.0/16` (home and SOHO networks).
      * **Non-routable on the public Internet:** Reserved exclusively for local network routing.
  * **Public IP Addresses:**
      * Globally unique across the Internet and directly routable worldwide (e.g., Google DNS `8.8.8.8` or UA `193.136.172.10`).

-----

## What About IPv6?

IPv4 only provides approximately **4.3 billion** addresses — which have been fully exhausted. **IPv6** was designed to provide an virtually inexhaustible address space:

::::: columns
::: {.column width="56%"}

  * **Address Format and Structure:**
      * Uses **8 hexadecimal blocks** separated by colons (`:`), spanning 128 bits:
        `2001:0db8:85a3::8a2e:0370:7334`
      * *(The notation `::` abbreviates contiguous blocks of zeroes).*
  * **Key IPv6 Addresses to Recognize:**
      * **`::1`** $\rightarrow$ IPv6 **`localhost`** (equivalent to `127.0.0.1`).
      * **`fe80::...`** (*Link-Local*) $\rightarrow$ Autoconfigured by the interface for direct communication on the local link.
      * **`fd00::...`** (*Unique Local*) $\rightarrow$ IPv6 equivalent of **private addresses** for internal routing.

:::
::: {.column width="44%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/ipv4vsipv6.png}

\vspace{0.2em}
{\tiny \textit{IPv4 (32 bits) vs. IPv6 (128 bits).}}
\end{center}

:::
:::::

-----

## The IP Reaches the Computer, the Port Reaches the Application

Multiple applications communicate simultaneously on a single host: the **IP Address** identifies the machine, while the **Port Number (Layer 4)** identifies the destination process.

\vspace{0.2em}

\begin{center}
\includegraphics[width=\linewidth,height=0.78\textheight,keepaspectratio]{figures/network_ip_port_analogy.png}
\end{center}

-----

## Well-Known Ports and Port Mapping (Docker)

Network connections are identified by an **`IP:Port`** tuple (transport ports range from `0` to `65535`, e.g., `192.168.1.10:80`):

::::: columns
::: {.column width="52%"}

  * **Well-Known Ports:**
      * **`22`:** SSH (Remote terminal and Git over SSH)
      * **`53`:** DNS (Domain name resolution)
      * **`80` / `443`:** HTTP / HTTPS (Web traffic and APIs)
      * **`3000`, `5000`, `8000`, `8080`:** Local development services (Node.js, Flask, FastAPI)

:::
::: {.column width="48%"}

  * **Docker Port Mapping (`-p`):**
      * Example:
        ```bash
        docker run -p 8080:80 nginx
        ```
      * Maps traffic arriving at port `8080` on the host system to port `80` inside the container.

:::
:::::

-----

## Food for Thought: Multiple Web Services on the Same Port 80?

Given the fundamental transport networking rule *"only one process may listen on a given port at any time"*, a practical architectural question arises:

  * **The Dilemma:**
      * A single server needs to host multiple distinct Web services (e.g., `ua.pt`, `moodle.ua.pt`, and `mail.ua.pt`).
      * All of them are public services, and standard browsers connect by default to **port `80` (HTTP)** or **`443` (HTTPS)** without requiring non-standard port numbers in the URL.
      * **If the host has only one port `80`, how can incoming requests be distinguished and delivered to the correct backend services?**

\vspace{0.8em}

  * **Research Challenge:**
      * How do production systems and cloud platforms address this challenge?
      * Investigate the architectural concepts of **Forward Proxy** and **Reverse Proxy** (e.g., *Nginx*, *Traefik*, *HAProxy*, or *Caddy*).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: IP Configuration (DHCP vs. Static) and DNS}}
\end{center}

-----

## IP Configuration: Automatic (DHCP) vs. Manual (Static)

To participate in network communications and access the Internet, any device requires **4 configuration parameters**:
**1. IP Address** | **2. Subnet Mask** | **3. Default Gateway** | **4. DNS Server**.

::::: columns
::: {.column width="50%"}

  * **Automatic Configuration — DHCP (Clients):**
      * When connecting to Wi-Fi or Ethernet, a device has no initial IP configuration.
      * The **DHCP** protocol automatically negotiates all 4 parameters with the router:
          1. *Client:* "Can any DHCP server assign an IP configuration?" (*Discover*)
          2. *DHCP Server (Router):* "Use IP `192.168.1.50` with a 24-hour lease!" (*Offer / ACK*)

:::
::: {.column width="50%"}

  * **Manual Configuration — Static IP (Servers):**
      * If a **server**, router, or networked printer changed its IP dynamically, clients would fail to locate it.
      * Administrators allocate a dynamic range for DHCP clients (e.g., `.100` to `.200`) and assign **Static IP** addresses to servers (e.g., `.10`) and default gateways (`.1`).

:::
:::::

-----

## The Internet's "Phonebook": DNS (*Domain Name System*)

Human users rely on memorable domain names (`ua.pt`, `google.com`), but IP packet routing operates exclusively with numerical addresses (`193.136.172.10`):

  * **What DNS Does:**
      * A distributed directory service that maps **Domain Names $\rightarrow$ IP Addresses** prior to establishing transport connections.
      * **Primary Resource Records:**
          * **`A`:** Resolves domain name to an IPv4 address.
          * **`AAAA`:** Resolves domain name to an IPv6 address.
          * **`CNAME`:** Canonical name alias pointing to another domain name.
  * **Name Resolution Mechanisms:**
      1. **`/etc/hosts` File:** Local lookup table queried by the operating system **before** consulting external DNS servers.
      2. **`.local` Names (mDNS):** Multicast DNS enabling zero-configuration host discovery across a local LAN (e.g., `raspberrypi.local`).
      3. **Docker Embedded DNS:** In Class 04, interconnecting containers by service name (`db`) was enabled by Docker's internal DNS resolver.

-----

## DNS Hierarchy: The Distributed Server "Tree"

No single server maintains all global domain records. The DNS architecture is organized as a **hierarchical distributed tree**, resolved from right to left (e.g., `elearning.ua.pt.`):

\vspace{0.2em}

\begin{center}
\includegraphics[width=\linewidth,height=0.76\textheight,keepaspectratio]{figures/network_dns_hierarchy_tree.png}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part IV: Configuration, Diagnostics (Debug), and Remote Access}}
\end{center}

-----

## Where to View and Configure Network Interfaces in Linux

In Linux environments, network settings are typically inspected and configured through three interfaces:

  * **1. Desktop Graphical Interface (NetworkManager):**
      * The desktop network settings applet (or the CLI tools `nmcli` / `nmtui`) allows toggling between automatic DHCP and static IP / DNS configurations.
  * **2. Terminal Inspection of Interfaces and Routes (`ip`):**
      * `ip addr show` (or simply **`ip a`**): Displays all network interfaces, physical MAC addresses (`link/ether`), and assigned IP addresses with masks (`inet`).
      * `ip route show` (or simply **`ip r`**): Displays the routing table and identifies the active **Default Gateway** (`default via ...`).
  * **3. Active DNS Server Inspection:**
      * Inspect `/etc/resolv.conf` or query system resolver status via `resolvectl status`.

-----

## Diagnostic Tools (I): `ping` and `traceroute`

When connectivity fails, these are the primary baseline command-line diagnostic utilities:

::::: columns
::: {.column width="50%"}

  * **`ping` — Verifying Reachability & Latency:**
      * Transmits ICMP Echo Request packets and measures Round-Trip Time (**latency** in milliseconds, `ms`).
      * Usage tip: In Linux, pass `-c 4` to transmit exactly 4 probes and exit automatically:
      ```bash
      $ ping -c 4 8.8.8.8
      64 bytes from 8.8.8.8: time=8.2 ms
      ```

:::
::: {.column width="50%"}

  * **`traceroute` — Tracing Intermediary Hops:**
      * Discloses every router (**hop**) traversed by packets from the local host to the destination.
      * Useful for pinpointing whether communication stalls at the local gateway (Hop 1) or further upstream:
      ```bash
      $ traceroute 8.8.8.8
       1  192.168.1.1 (Router)  1.2 ms
       2  10.254.0.1 (ISP)     6.4 ms
      ```

:::
:::::

-----

## Diagnostic Tools (II): `dig`, `ss`, `nmap`, and `curl`

For diagnosing name resolution failures, inspecting port bindings, or debugging unresponsive services:

  * **`dig` (DNS Query Tool):**
      * Queries DNS servers directly for resource records: `dig ua.pt +short` (or reverse lookup via `dig -x 8.8.8.8 +short`).
  * **`ss -tuln` (Inspecting Listening Sockets on the Local Host):**
      * Lists all processes currently bound and listening on TCP (`-t`) or UDP (`-u`) ports in numeric format (`-n`).
  * **`nmap` (Network Exploration and Port Scanning):**
      * Probes target hosts to discover open transport ports (e.g., `nmap localhost`). *(Note: Must only be executed on systems you own or authorized targets such as `scanme.nmap.org`).*
  * **`curl -I` (Command-Line HTTP Inspection):**
      * Issues HTTP HEAD requests to verify status codes (e.g., `200 OK`, `404 Not Found`, or `500 Server Error`): `curl -I http://localhost:8000`.

-----

## Firewalls and Client Isolation (The `eduroam` Case)

Even when an IP address is valid and a service is running, connections may be rejected due to **security filtering policies**:

  * **Firewalls (Host-Based or Network Perimeter):**
      * Enforce packet filtering by **port**, **protocol**, and **direction** (e.g., `ufw` on Linux, macOS Packet Filter, or Windows Firewall).
      * Default configuration typically permits outbound connections (e.g., port `443` HTTPS), but **blocks unsolicited inbound connections** on non-whitelisted ports (e.g., port `8000`).

  * **Client Isolation on Enterprise Wi-Fi (`eduroam`):**
      * Public and university wireless networks frequently enforce **Client Isolation** at the Access Point / Controller level.
      * **Practical Consequence:** Two laptops connected to `eduroam` can communicate outward with the Internet, but **cannot establish direct peer-to-peer connections with each other**.

-----

## Survival Guide: Network Troubleshooting in 5 Steps

When diagnosing network connectivity failures, follow this structured *bottom-up* methodology:

\vspace{0.15em}

\begin{center}
\begin{tikzpicture}[
    stepbox/.style={rectangle, draw=black!75, rounded corners=3pt, thick, text width=11.2cm, minimum height=0.76cm, inner sep=3.5pt, align=left, font=\scriptsize},
    arr/.style={-{Latex[length=1.6mm]}, thick, color=uagreen!80!black}
]
\node[stepbox, fill=black!5]    (s1) at (0, 4.08) {\textbf{Step 1 — Is the network interface active with an assigned IP?}\\Run \texttt{ip a}. If unconfigured, verify physical cable/Wi-Fi or the DHCP service.};
\node[stepbox, fill=uagreen!12] (s2) at (0, 3.06) {\textbf{Step 2 — Can I reach the Default Gateway (Router)?}\\Identify gateway via \texttt{ip r} and test LAN connectivity with \texttt{ping -c 4 <Gateway\_IP>}.};
\node[stepbox, fill=blue!10]    (s3) at (0, 2.04) {\textbf{Step 3 — Is there outbound Internet connectivity (by IP)?}\\Execute \texttt{ping -c 4 8.8.8.8} (or \texttt{traceroute}). If it fails, external routing is impaired.};
\node[stepbox, fill=orange!12]  (s4) at (0, 1.02) {\textbf{Step 4 — Is the DNS server properly resolving names?}\\If \texttt{ping 8.8.8.8} works but \texttt{ping ua.pt} fails $\rightarrow$ DNS failure (test via \texttt{dig ua.pt}).};
\node[stepbox, fill=red!10]     (s5) at (0, 0.00) {\textbf{Step 5 — Is the service listening on the port without Firewall drops?}\\Verify with \texttt{ss -tuln} (local), \texttt{nmap}/\texttt{curl -I} (remote), and inspect Firewall rules.};

\draw[arr] (s1.south) -- (s2.north);
\draw[arr] (s2.south) -- (s3.north);
\draw[arr] (s3.south) -- (s4.north);
\draw[arr] (s4.south) -- (s5.north);
\end{tikzpicture}
\end{center}

\vspace{0.15em}

  * **Deep Packet Inspection:** When detailed packet analysis is required, engineers rely on packet capture analyzers such as **Wireshark** (graphical) or **`tcpdump`** (command line).

-----

## Secure Remote Work (I): SSH and Synchronization with `rsync`

In modern computing, Linux servers typically operate in cloud environments without physical displays or input peripherals. How do we manage them remotely?

  * **1. Secure Terminal Access with `ssh` (*Secure Shell* — Port 22):**
      * Establishes an encrypted remote session over the network (using asymmetric `ed25519` key pairs):
      ```bash
      # Connect as user 'student' to the remote host (on port 2222)
      $ ssh student@localhost -p 2222
      ```
  * **2. Incremental File Synchronization with `rsync` (over SSH):**
      * Replaces legacy insecure protocols like FTP. **`rsync`** analyzes differences between local and remote directories and **transmits only modified byte deltas**:
      ```bash
      # -a: archive mode; -v: verbose; -z: compression; -P: progress bar
      $ rsync -avzP -e "ssh -p 2222" ./my-project/ student@server:~/projects/
      ```

-----

## Secure Remote Work (II): SSH Tunnels and VS Code Remote

What if an internal service runs on a remote server at `localhost:8000`, but port `8000` is blocked by a firewall against public access?

  * **Local Port Forwarding via SSH Tunnel (`-L`):**
      * Creates an encrypted forwarding channel inside the SSH connection, binding local port `8080` to remote port `8000`:
      ```bash
      $ ssh -N -L 8080:localhost:8000 student@server -p 2222
      ```
      * Opening **`http://localhost:8080`** in a local browser transparently accesses the internal remote service.
  * **VS Code Remote - SSH:**
      * The official *Remote - SSH* extension builds on this exact mechanism: the GUI runs locally, while editing, debugging, and terminal execution occur natively on the remote server.
