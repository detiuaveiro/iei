---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Redes Informáticas: Fundamentos, Configuración y Diagnóstico"
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

## Visión General de la Sesión

  * **Parte I — ¿Cómo se Construye una Red? (Del Portátil a Internet):**
      * Las escalas de red (**PAN**, **LAN**, **MAN**, **WAN**), los equipos cotidianos (**Switch**, **Access Point**, **Router**, **ONT**) y el **Modelo OSI (7 capas)** con encapsulamiento.
  * **Parte II — Direcciones y Puertos (Localizar la Máquina y el Programa):**
      * Dirección física (**MAC**) frente a dirección lógica (**IP**), enrutamiento (*Switch* vs. *Routers*), **Default Gateway** y **ARP**, **IPv4** y máscara de subred (`/24`), direcciones especiales, **IPv6** y **Puertos de Transporte** (incluyendo mapeo en Docker y el desafío de *Reverse Proxy*).
  * **Parte III — Configuración de IP (DHCP vs. Estático) y DNS:**
      * Los 4 parámetros esenciales de red, configuración automática (**DHCP**) frente a manual (**IP Estática**), resolución de nombres (**DNS**) y la jerarquía en árbol de servidores DNS.
  * **Parte IV — Configuración, Diagnóstico (Debug) y Acceso Remoto:**
      * Herramientas esenciales en Linux (`ip`, `ping`, `traceroute`, `dig`, `ss`, `nmap`, `curl`), **Firewalls** y aislamiento de clientes en `eduroam`, metodología de **Diagnóstico en 5 Pasos** y administración remota segura con **SSH**, **`rsync`** y **Túneles SSH**.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: ¿Cómo se Construye una Red? (Del Portátil a Internet)}}
\end{center}

-----

## ¿Qué es una Red? PAN, LAN, MAN y WAN

Una red de computadores es un sistema de dispositivos interconectados que se comunican y comparten recursos. Según su escala geográfica:

\vspace{0.2em}

\begin{center}
\includegraphics[width=0.96\linewidth,height=0.40\textheight,keepaspectratio]{figures/network_scales_lan_man_wan.jpg}
\end{center}

\vspace{-0.4em}

::::: columns
::: {.column width="50%"}

  * **PAN (*Personal Area*):** Dispositivos en el entorno del usuario (~pocos metros; Bluetooth / Wi-Fi Direct).
  * **LAN (*Local Area*):** Hogar, laboratorio, edificio o Docker (alta velocidad mediante cable Ethernet y Wi-Fi).

:::
::: {.column width="50%"}

  * **MAN (*Metropolitan Area*):** Múltiples edificios o sedes en una ciudad o campus universitario (anillos de fibra).
  * **WAN (*Wide Area*):** Ciudades, países y continentes interconectados (la **Internet** global vía cables submarinos y satélites).

:::
:::::

-----

## Equipos de la Red Local: Switch y Access Point

Interconexión de dispositivos dentro de la misma LAN:

::::: columns
::: {.column width="54%"}

  * **Switch (Conmutador):**
      * Conecta dispositivos mediante cable de red (Ethernet).
      * Entrega paquetes **únicamente** al puerto físico del destinatario.
      * *(Sustituyó al antiguo **Hub**, que difundía a todos los puertos provocando colisiones).*
  * **Access Point (AP — Punto de Acceso):**
      * Conecta dispositivos inalámbricos (Wi-Fi) a la infraestructura cableada.
      * Integra portátiles y dispositivos móviles en la misma LAN.

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/network_devices_router_switch_ap.jpg}

\vspace{0.2em}
{\tiny \textit{Switches y Access Points interconectan dispositivos en la misma LAN.}}
\end{center}

:::
:::::

-----

## La Frontera con Internet: Router y ONT

Comunicación más allá de los límites de la red local:

::::: columns
::: {.column width="54%"}

  * **Router (Encaminador):**
      * Interconecta **redes distintas** (LAN 1, LAN 2 e Internet).
      * Enruta paquetes entre redes a través de la ruta óptima.
  * **ONT (*Optical Network Terminal*):**
      * Convierte señales ópticas (fibra del proveedor) en eléctricas (Ethernet).
  * **El "Router Doméstico":**
      * Dispositivo **4 en 1**: integra ONT, Router, Switch y Access Point en una sola unidad física.

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/network_devices_router_switch_ap.jpg}

\vspace{0.2em}
{\tiny \textit{El Router interconecta redes distintas (LAN 1, LAN 2 e Internet).}}
\end{center}

:::
:::::

-----

## Cómo se Organiza la Red: El Modelo OSI (7 Capas)

El modelo **OSI** (*Open Systems Interconnection*) estandariza la comunicación entre sistemas a través de **7 capas**:

\vspace{0.3em}

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/network_7_layers_osi_encapsulation.jpg}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Direcciones y Puertos (Localizar la Máquina y el Programa)}}
\end{center}

-----

## Dos Direcciones en Cada Dispositivo: MAC vs. IP

Cada interfaz de red (Ethernet o Wi-Fi) opera con **dos niveles de direccionamiento**:

::::: columns
::: {.column width="50%"}

  * **Dirección MAC (Física / Capa 2 — Enlace de Datos):**
      * Ejemplo: `00:1A:2B:3C:4D:5E` (48 bits en notación hexadecimal).
      * Grabada de fábrica en la tarjeta de red (inmutable en hardware).
      * **Propósito:** Identifica la interfaz en el **enlace local inmediato (*hop-by-hop*)**. La MAC de destino cambia en cada salto de router.
      * **Analogía:** Documento de Identidad (identifica el dispositivo localmente).

:::
::: {.column width="50%"}

  * **Dirección IP (Lógica / Capa 3 — Red):**
      * Ejemplo: `192.168.1.10` (IPv4).
      * Asignada lógicamente por la topología de la red.
      * **Propósito:** Identifica el **origen y destino final (*end-to-end*)** a través de múltiples redes interconectadas.
      * **Analogía:** Dirección Postal (cambia al trasladarse a otra red).

:::
:::::

\vspace{0.6em}

\begin{center}
\textbf{La IP define el destino global final; la MAC define quién recibe la trama en el siguiente salto local (sea un router o el equipo de destino en la LAN).}
\end{center}

-----

## Enrutamiento en la Práctica: Envío Local (Switch) vs. Salto a Salto (Routers)

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/network_routing_mac_vs_ip.png}
\end{center}

-----

## Cómo Funciona el Enrutamiento: El Rol del Gateway y de ARP

  * **1. Comunicación Remota (Otra Red):**
      * El **Portátil 4** (`192.168.3.90`) transmite datos al **Portátil 1** (`192.168.1.100` en otra red).
      * La **Dirección de Red Destino (IP: `192.168.1.100`) permanece constante (*end-to-end*)** durante todo el trayecto.
      * Como el destino está fuera de la subred local, el Portátil 4 entrega la trama física a su puerta de salida: el **Default Gateway (Router 1)**, estableciendo `MAC Destino = FF:FF:FF:FF:FF:FF`.
      * El **Router 1** desencapsula la trama, consulta su tabla de rutas, reenvía hacia la red `192.168.1.0` y actualiza la cabecera MAC en cada salto (*hop-by-hop*).
  * **2. Comunicación Local (Misma Red):**
      * Cuando el Portátil 2 (`192.168.1.101`) transmite al Portátil 1 (`192.168.1.100`), la trama viaja **directamente a través del Switch** con `MAC Destino = AA:AA:AA:AA:AA:AA` (¡no atraviesa ningún router!).
  * **3. El Rol de ARP (*Address Resolution Protocol*):**
      * Para completar la MAC física en la trama Ethernet:
      * **Destino en la misma subred $\rightarrow$** ARP resuelve la dirección MAC de la propia máquina de destino.
      * **Destino fuera de la subred $\rightarrow$** ARP resuelve la dirección MAC del **Default Gateway**.

-----

## Direcciones IPv4 y Máscara de Subred (Simplificado)

Una dirección IPv4 consta de 4 octetos comprendidos entre `0` y `255` separados por puntos, y se acompaña **siempre** de una **Máscara de Subred**:

  * **Dirección IP:** `192.168.1.10`
  * **Máscara de Subred:** `255.255.255.0` (representada también en notación CIDR como **`/24`**).
  * **Interpretación Intuitiva:**
      * Donde la máscara tiene `255`, los octetos identifican **la Red (la Calle)**: `192.168.1.x`
      * Donde la máscara tiene `0`, el octeto identifica **el Dispositivo (el Número de Portal)**: `.10` (utilizable de `.1` a `.254`).

\vspace{0.4em}

```text
Dirección IP:     192  .  168  .   1   .   10
Máscara (/24):    255  .  255  .  255  .   0
                [---- PREFIJO DE RED ----] [HOST]
```

\vspace{0.3em}

  * **Criterio Práctico:**
      * Destino `192.168.1.25` $\rightarrow$ Comienza por `192.168.1.` $\rightarrow$ **¡Misma subred (LAN)!** Se envía directamente mediante el Switch.
      * Destino `8.8.8.8` $\rightarrow$ No coincide con `192.168.1.` $\rightarrow$ **¡Red externa (Internet)!** Se envía al **Default Gateway**.

-----

## Direcciones IP Especiales y Rangos Reservados

  * **`127.0.0.1` (`localhost` / Interfaz de Loopback):**
      * Representa **"este propio equipo"**. El tráfico es procesado internamente por el sistema operativo y nunca transita por la tarjeta de red física o Wi-Fi.
      * Esencial para probar servidores y aplicaciones localmente sin depender de conectividad externa.
  * **Direcciones Reservadas en la Subred (ej.: en una red `/24`):**
      * **Primera dirección (`... .0`):** Identificador de la **propia red** (no asignable a equipos individuales).
      * **Última dirección (`... .255`):** Dirección de **Difusión (*Broadcast*)** (los paquetes enviados a ella son recibidos por todos los equipos de la LAN).
  * **Direcciones IP Privadas (RFC 1918 — Exclusivas para LAN):**
      * Rangos reservados: `10.0.0.0/8` (empresas / campus universitarios), `172.16.0.0/12` (redes internas Docker) y `192.168.0.0/16` (redes domésticas).
      * **No enrutables en la Internet pública:** Destinadas exclusivamente al enrutamiento interno en redes locales.
  * **Direcciones IP Públicas:**
      * Únicas globalmente y directamente accesibles a través de Internet (ej.: Google `8.8.8.8` o UA `193.136.172.10`).

-----

## ¿Y qué hay de IPv6?

IPv4 solo permite aproximadamente **4.300 millones** de direcciones —las cuales se encuentran agotadas. **IPv6** fue diseñado para proporcionar un espacio de direccionamiento prácticamente inagotable:

::::: columns
::: {.column width="56%"}

  * **Formato y Estructura de la Dirección:**
      * Utiliza **8 bloques hexadecimales** separados por dos puntos (`:`), con una longitud de 128 bits:
        `2001:0db8:85a3::8a2e:0370:7334`
      * *(La notación `::` permite comprimir bloques consecutivos de ceros).*
  * **Direcciones IPv6 Clave:**
      * **`::1`** $\rightarrow$ El **`localhost`** de IPv6 (equivalente a `127.0.0.1`).
      * **`fe80::...`** (*Link-Local*) $\rightarrow$ Autoconfigurada por la interfaz para comunicarse en el enlace local.
      * **`fd00::...`** (*Unique Local*) $\rightarrow$ Equivalente a los **rangos privados** de IPv4 (redes internas).

:::
::: {.column width="44%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/ipv4vsipv6.png}

\vspace{0.2em}
{\tiny \textit{IPv4 (32 bits) frente a IPv6 (128 bits).}}
\end{center}

:::
:::::

-----

## La IP Llega a la Máquina, el Puerto Llega a la Aplicación

Múltiples aplicaciones se comunican simultáneamente en un mismo computador: la **Dirección IP** identifica al equipo y el **Puerto de Transporte (Capa 4)** identifica a la aplicación de destino.

\vspace{0.2em}

\begin{center}
\includegraphics[width=\linewidth,height=0.78\textheight,keepaspectratio]{figures/network_ip_port_analogy.png}
\end{center}

-----

## Puertos Convencionales y Mapeo de Puertos (Docker)

Cada conexión de red se identifica mediante el par **`IP:Puerto`** (los puertos de transporte van de `0` a `65535`, ej.: `192.168.1.10:80`):

::::: columns
::: {.column width="52%"}

  * **Puertos Estándar:**
      * **`22`:** SSH (Terminal remoto y Git sobre SSH)
      * **`53`:** DNS (Resolución de nombres)
      * **`80` / `443`:** HTTP / HTTPS (Tráfico web y APIs)
      * **`3000`, `5000`, `8000`, `8080`:** Desarrollo local (Node.js, Flask, FastAPI)

:::
::: {.column width="48%"}

  * **Mapeo en Docker (`-p`):**
      * Ejemplo:
        ```bash
        docker run -p 8080:80 nginx
        ```
      * Redirige el tráfico recibido en el puerto `8080` del anfitrión (*host*) hacia el puerto `80` del contenedor.

:::
:::::

-----

## Para Reflexionar: ¿Múltiples Servicios Web en el Mismo Puerto 80?

Si la regla de transporte establece que *"solo una aplicación puede escuchar en un puerto específico"*, surge una cuestión práctica en arquitecturas de producción:

  * **El Dilema:**
      * En un servidor deseamos alojar varios servicios Web públicos (ej.: `ua.pt`, `moodle.ua.pt` y `mail.ua.pt`).
      * Todos ellos son servicios públicos y los navegadores acceden por defecto al **puerto `80` (HTTP)** o **`443` (HTTPS)**, sin requerir números adicionales en el URL.
      * **Si solo disponemos de un puerto `80` en el servidor, ¿cómo podemos diferenciar y entregar las peticiones a los servicios correspondientes?**

\vspace{0.8em}

  * **Trabajo de Investigación:**
      * ¿Cómo solucionan este problema las plataformas web y los equipos de infraestructura en producción?
      * Queda propuesto investigar los conceptos de **Proxy Directo** y **Reverse Proxy** (ej.: *Nginx*, *Traefik*, *HAProxy* o *Caddy*).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Configuración de IP (DHCP vs. Estático) y DNS}}
\end{center}

-----

## Configuración de IP: Automática (DHCP) vs. Manual (Estática)

Para operar en la red y acceder a Internet, cualquier dispositivo requiere **4 parámetros fundamentales**:
**1. Dirección IP** | **2. Máscara de Subred** | **3. Default Gateway** | **4. Servidor DNS**.

::::: columns
::: {.column width="50%"}

  * **Configuración Automática — DHCP (Clientes):**
      * Al conectarse a la red, el dispositivo carece inicialmente de configuración IP.
      * El protocolo **DHCP** negocia automáticamente los 4 parámetros con el router:
          1. *Cliente:* "¿Hay algún servidor DHCP que me asigne IP?" (*Discover*)
          2. *Servidor DHCP (Router):* "Utiliza `192.168.1.50` con concesión de 24 horas" (*Offer / ACK*)

:::
::: {.column width="50%"}

  * **Configuración Manual — IP Estática (Servidores):**
      * Si la IP de un **servidor**, router o impresora cambiara a diario, los clientes no podrían localizarlo.
      * Los administradores reservan un rango dinámico para clientes DHCP (ej.: `.100` a `.200`) y asignan **IPs Estáticas** a servidores (ej.: `.10`) y gateways (`.1`).

:::
:::::

-----

## La "Guía Telefónica" de Internet: DNS (*Domain Name System*)

Los usuarios memorizan nombres de dominio (`ua.pt`, `google.com`), pero el enrutamiento de paquetes IP opera exclusivamente con direcciones numéricas (`193.136.172.10`):

  * **Propósito del DNS:**
      * Sistema distribuido que traduce **Nombres de Dominio $\rightarrow$ Direcciones IP** con anterioridad al establecimiento de las conexiones.
      * **Registros Principales:**
          * **`A`:** Resuelve un nombre de dominio en una dirección IPv4.
          * **`AAAA`:** Resuelve un nombre de dominio en una dirección IPv6.
          * **`CNAME`:** Alias canónico que apunta a otro nombre de dominio.
  * **Mecanismos Cotidianos de Resolución:**
      1. **Fichero `/etc/hosts`:** Tabla local consultada por el sistema operativo **antes** de interrogar a los servidores DNS externos.
      2. **Nombres `.local` (mDNS):** Descubrimiento automático de equipos en la misma LAN sin servidor central (ej.: `raspberrypi.local`).
      3. **DNS Interno de Docker:** En la Clase 04, la resolución del nombre de servicio `db` fue gestionada por el DNS integrado de Docker.

-----

## Jerarquía del DNS: El "Árbol" de Servidores Distribuidos

No existe un servidor único que contenga todos los registros mundiales: el DNS se organiza como un **árbol jerárquico distribuido**, resolviéndose de derecha a izquierda (ej.: `elearning.ua.pt.`):

\vspace{0.2em}

\begin{center}
\includegraphics[width=\linewidth,height=0.76\textheight,keepaspectratio]{figures/network_dns_hierarchy_tree.png}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Configuración, Diagnóstico (Debug) y Acceso Remoto}}
\end{center}

-----

## Dónde Consultar y Configurar la Red en Linux

En entornos Linux, existen tres vías principales para inspeccionar y modificar los ajustes de red:

  * **1. Entorno Gráfico de Escritorio (NetworkManager):**
      * El módulo de configuración de red (o las herramientas de terminal `nmcli` / `nmtui`) permite alternar entre DHCP automático o definir IPs estáticas y servidores DNS.
  * **2. Inspección de Interfaces y Rutas en Terminal (`ip`):**
      * `ip addr show` (o abreviadamente **`ip a`**): Muestra las interfaces de red, direcciones físicas MAC (`link/ether`) y direcciones IP con máscara (`inet`).
      * `ip route show` (o abreviadamente **`ip r`**): Muestra la tabla de enrutamiento e identifica el **Default Gateway** activo (`default via ...`).
  * **3. Comprobación del Servidor DNS Activo:**
      * Puede consultarse el fichero `/etc/resolv.conf` o ejecutarse el comando `resolvectl status`.

-----

## Herramientas de Diagnóstico (I): `ping` y `traceroute`

Ante incidencias de conectividad, estas son las dos herramientas iniciales de diagnóstico en terminal:

::::: columns
::: {.column width="50%"}

  * **`ping` — Verificación de Alcance y Latencia:**
      * Envía paquetes ICMP Echo Request y mide el tiempo de ida y vuelta (**latencia** en milisegundos, `ms`).
      * En Linux, utilice el parámetro `-c 4` para enviar exactamente 4 paquetes y finalizar:
      ```bash
      $ ping -c 4 8.8.8.8
      64 bytes from 8.8.8.8: time=8.2 ms
      ```

:::
::: {.column width="50%"}

  * **`traceroute` — Trazado de Saltos Intermedios:**
      * Identifica cada router (**salto** / *hop*) atravesado por los paquetes desde el equipo local hasta el destino.
      * Permite verificar si la interrupción ocurre en el gateway local (Salto 1) o en la red del proveedor de telecomunicaciones:
      ```bash
      $ traceroute 8.8.8.8
       1  192.168.1.1 (Router)  1.2 ms
       2  10.254.0.1 (ISP)     6.4 ms
      ```

:::
:::::

-----

## Herramientas de Diagnóstico (II): `dig`, `ss`, `nmap` y `curl`

Para diagnosticar incidencias de resolución de nombres, inspeccionar puertos o depurar servicios que no responden:

  * **`dig` (Herramienta de Consulta DNS):**
      * Consulta directamente los registros a servidores DNS: `dig ua.pt +short` (o resolución inversa mediante `dig -x 8.8.8.8 +short`).
  * **`ss -tuln` (Listar Sockets en Escucha en la Máquina Local):**
      * Muestra los procesos actualmente asociados y a la escucha en puertos TCP (`-t`) o UDP (`-u`) en formato numérico (`-n`).
  * **`nmap` (Exploración de Redes y Escaneo de Puertos):**
      * Efectúa un escaneo para descubrir qué puertos aceptan conexiones en un objetivo (ej.: `nmap localhost`). *(Nota: Utilícese únicamente en sistemas propios o en destinos autorizados como `scanme.nmap.org`).*
  * **`curl -I` (Inspección HTTP por Línea de Comandos):**
      * Emite peticiones HTTP HEAD para verificar códigos de estado del servidor (`200 OK`, `404 Not Found`, `500 Internal Server Error`): `curl -I http://localhost:8000`.

-----

## Firewalls y Aislamiento de Clientes (El Caso de `eduroam`)

Incluso con una dirección IP válida y el servicio activo en el puerto adecuado, las conexiones pueden ser rechazadas por **políticas de filtrado**:

  * **Firewalls (En el Sistema Operativo o en Perímetro):**
      * Filtran el tráfico en función del **puerto**, **protocolo** y **dirección** (ej.: `ufw` en Linux o Firewall de Windows).
      * Por defecto, permiten conexiones salientes (ej.: acceder a sitios web en puerto `443`), pero **bloquean conexiones entrantes no solicitadas** en puertos no autorizados (ej.: puerto `8000`).

  * **Aislamiento de Clientes (*Client Isolation*) en `eduroam`:**
      * Las redes Wi-Fi públicas o académicas (como **`eduroam`**) impiden por seguridad la comunicación directa entre dispositivos conectados al mismo punto de acceso.
      * **Consecuencia Práctica:** Dos portátiles conectados a `eduroam` acceden a Internet sin restricciones, pero **no pueden establecer conexiones directas entre sí**.

-----

## Guía de Supervivencia: Diagnóstico de Red en 5 Pasos

Ante una pérdida de conectividad en red, aplique esta metodología sistemática de diagnóstico (*bottom-up*):

\vspace{0.15em}

\begin{center}
\begin{tikzpicture}[
    stepbox/.style={rectangle, draw=black!75, rounded corners=3pt, thick, text width=11.2cm, minimum height=0.76cm, inner sep=3.5pt, align=left, font=\scriptsize},
    arr/.style={-{Latex[length=1.6mm]}, thick, color=uagreen!80!black}
]
\node[stepbox, fill=black!5]    (s1) at (0, 4.08) {\textbf{Paso 1 — ¿La interfaz de red está activa y tiene IP asignada?}\\Ejecute \texttt{ip a}. Si no tiene IP, compruebe el cable/Wi-Fi o el servicio DHCP.};
\node[stepbox, fill=uagreen!12] (s2) at (0, 3.06) {\textbf{Paso 2 — ¿Tengo conectividad con el Default Gateway (Router)?}\\Consulte el gateway con \texttt{ip r} y compruebe la LAN con \texttt{ping -c 4 <IP\_Gateway>}.};
\node[stepbox, fill=blue!10]    (s3) at (0, 2.04) {\textbf{Paso 3 — ¿Existe salida hacia Internet (por dirección IP)?}\\Ejecute \texttt{ping -c 4 8.8.8.8} (o \texttt{traceroute}). Si falla, el enrutamiento externo está afectado.};
\node[stepbox, fill=orange!12]  (s4) at (0, 1.02) {\textbf{Paso 4 — ¿El servidor DNS traduce correctamente los nombres?}\\Si \texttt{ping 8.8.8.8} funciona pero \texttt{ping ua.pt} falla $\rightarrow$ fallo de DNS (pruebe con \texttt{dig ua.pt}).};
\node[stepbox, fill=red!10]     (s5) at (0, 0.00) {\textbf{Paso 5 — ¿El servicio escucha en el puerto y sin bloqueo de Firewall?}\\Compruebe con \texttt{ss -tuln} (local), \texttt{nmap}/\texttt{curl -I} (remoto) y revise las reglas de Firewall.};

\draw[arr] (s1.south) -- (s2.north);
\draw[arr] (s2.south) -- (s3.north);
\draw[arr] (s3.south) -- (s4.north);
\draw[arr] (s4.south) -- (s5.north);
\end{tikzpicture}
\end{center}

\vspace{0.15em}

  * **Inspección Profunda de Tráfico:** Cuando se requiere analizar tramas y paquetes al detalle, se utilizan analizadores de red como **Wireshark** (interfaz gráfica) o **`tcpdump`** (terminal).

-----

## Administración Remota Segura (I): SSH y Sincronización con `rsync`

En entornos profesionales, los servidores Linux se ejecutan habitualmente en la nube sin periféricos de entrada/salida físicos. ¿Cómo se administran remotamente?

  * **1. Conexión de Terminal Segura con `ssh` (*Secure Shell* — Puerto 22):**
      * Establece una sesión remota cifrada (utilizando el par de claves pública/privada `ed25519`):
      ```bash
      # Conectar con el usuario 'student' en el servidor remoto (en el puerto 2222)
      $ ssh student@localhost -p 2222
      ```
  * **2. Sincronización Incremental de Directorios con `rsync` (sobre SSH):**
      * Reemplaza a protocolos legados inseguros como FTP. **`rsync`** compara los directorios local y remoto y **transfiere únicamente los bloques de datos modificados**:
      ```bash
      # -a: modo archivo; -v: detallado; -z: compresión; -P: progreso
      $ rsync -avzP -e "ssh -p 2222" ./mi-proyecto/ student@servidor:~/proyectos/
      ```

-----

## Administración Remota Segura (II): Túneles SSH y VS Code Remote

¿Qué ocurre si un servicio web interno se ejecuta en un servidor remoto en `localhost:8000`, pero el puerto `8000` está cerrado al exterior por un firewall?

  * **Reenvío Local de Puertos mediante Túnel SSH (*Local Port Forwarding* — `-L`):**
      * Establece un canal cifrado dentro de la conexión SSH que vincula el puerto `8080` de la máquina local con el puerto `8000` del servidor remoto:
      ```bash
      $ ssh -N -L 8080:localhost:8000 student@servidor -p 2222
      ```
      * Al acceder a **`http://localhost:8080`** en el navegador local, se consulta de forma transparente y segura el servicio interno remoto.
  * **VS Code Remote - SSH:**
      * La extensión oficial *Remote - SSH* opera sobre este mismo principio: el entorno gráfico corre en el portátil local, mientras que la edición, ejecución y depuración ocurren directamente en el servidor remoto.

