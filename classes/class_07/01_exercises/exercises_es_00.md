---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Redes Informáticas: Fundamentos, Configuración y Diagnóstico"
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

# Guión Práctico de Laboratorio

**Contexto Pedagógico y Objetivos:**
En las sesiones anteriores se han empleado diversas funcionalidades de red —tales como solicitudes HTTP mediante `curl`, mapeo de puertos en contenedores Docker (`-p 8080:80`) y autenticación remota vía SSH con GitHub. En esta sesión de laboratorio de **3 horas**, el objetivo consiste en analizar la configuración de las interfaces de red, comprender el enrutamiento de paquetes hacia Internet y **ejecutar procedimientos sistemáticos de diagnóstico (*troubleshooting*) cuando una aplicación o servidor experimenta fallos de conectividad** (competencia fundamental para los proyectos de la asignatura y para la **Class 08**, dedicada a la programación de aplicaciones en red en Python):

* **Parte 0 — Preparación del Entorno y Servidor de Prueba (Docker SSH):** Instalación de utilidades de diagnóstico de red (Linux y macOS), generación de un par de claves criptográficas SSH (`ed25519`) e instanciación de un contenedor Docker con un servidor OpenSSH aislado para pruebas de administración remota.
* **Parte 1 — Inspección de la Máquina Local y de la Red Local (LAN):** Identificación de interfaces de red, dirección física (**MAC**), dirección lógica (**IPv4**) y máscara de subred (`/24`) mediante `ip a` / `ifconfig`, verificación de la interfaz de *loopback* (`127.0.0.1`), identificación del router local (*Default Gateway* con `ip r` / `netstat -rn`) e inspección de la tabla **ARP** (`ip neigh` / `arp -an`).
* **Parte 2 — De la Red Local a Internet (WAN, NAT y DNS):** Pruebas de conectividad y latencia por dirección IP vs. nombre de dominio (`ping`), análisis de enrutamiento entre saltos intermedios (`traceroute`), resolución de nombres en el sistema **DNS** (`dig` y `/etc/hosts`) y determinación de la **Dirección IP Pública** y del mecanismo de **NAT** (`curl`).
* **Parte 3 — Puertos, Servicios y Diagnóstico de Conexiones (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`):** Inspección de *sockets* activos en estado de escucha (*LISTEN*) en el sistema anfitrión (`ss -tuln` / `lsof`), análisis experimental de la diferencia crítica entre vincular a `127.0.0.1` y `0.0.0.0` (preparación para la Class 08) y escaneo de puertos con `nmap`.
* **Parte 4 — Administración Remota Segura (SSH, `rsync` y Reenvío de Puertos SSH):** Conexión remota mediante `ssh`, sincronización incremental de directorios con `rsync` y establecimiento de un **Túnel SSH (`ssh -L` — *Local Port Forwarding*)** para acceder de forma segura a servicios web internos no expuestos directamente.
* **Parte 5 — Ejercicios Complementarios de Consolidación:** Captura e inspección de tráfico de red en tiempo real con `tcpdump` y representación geográfica de rutas IP (Geo-Traceroute).

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Antes de comenzar las actividades, cree y acceda al directorio de trabajo reservado para esta sesión:

```bash
$ mkdir -p ~/IEI/aula07
$ cd ~/IEI/aula07
```

Todos los ficheros generados a lo largo del laboratorio deberán permanecer organizados dentro de este directorio.

> **Nota sobre rutas de ficheros:**
> Las instrucciones y comandos indicados en este guión asumen que la sesión de terminal se encuentra posicionada en el directorio `~/IEI/aula07`.

-----

## Parte 0: Preparación del Entorno y Servidor de Prueba (Docker SSH)

Antes de analizar el funcionamiento de la red, instale las herramientas de diagnóstico en su sistema operativo (Linux o macOS) y proceda al arranque de un servidor OpenSSH en un contenedor Docker, el cual actuará como máquina remota de prueba.

### Paso 1: Instalar las Herramientas de Diagnóstico de Red

Abra el terminal e instale los paquetes de software necesarios:

* **En Linux (Ubuntu / Debian):**
  ```bash
  $ sudo apt update
  $ sudo apt install -y iproute2 net-tools dnsutils traceroute nmap curl \
    python3-pip python3-venv python3-tk
  ```
* **En macOS (vía Homebrew):**
  Las herramientas `ping`, `traceroute`, `dig`, `curl`, `arp`, `lsof`, `netstat`, `ssh`, `rsync` y `tcpdump` se encuentran instaladas de forma nativa en macOS. Instale el paquete `nmap` (y opcionalmente `iproute2mac` si desea disponer de los comandos `ip a` e `ip r` en macOS):
  ```bash
  $ brew install nmap iproute2mac
  ```

Resumen de herramientas:

  * `ip` / `ifconfig` / `arp` / `ss` / `lsof`: Inspección de interfaces de red, direcciones IP, tablas de enrutamiento, caché ARP y *sockets* de transporte.
  * `dig`: Consultas directas a servidores DNS para la resolución de nombres de dominio.
  * `traceroute`: Identificación de la secuencia de encaminadores (*hops*) en la ruta hacia un destino.
  * `nmap`: Escaneo de puertos y detección de servicios activos en un sistema objetivo.
  * `curl`: Emisión de peticiones HTTP/HTTPS a servidores y APIs desde la línea de comandos.

### Paso 2: Verificar o Generar un Par de Claves SSH

La autenticación remota segura se fundamenta en criptografía asimétrica mediante un par de claves (**Clave Privada**, conservada confidencialmente en el equipo cliente, y **Clave Pública**, instalada en el servidor remoto).

1. Compruebe si ya dispone de un par de claves `ed25519` en el directorio `~/.ssh`:
   ```bash
   $ ls -la ~/.ssh/id_ed25519*
   ```
2. **En caso de no existir**, genere un nuevo par sin *passphrase*:
   ```bash
   $ ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
   ```
   *(Nota de seguridad: El fichero `~/.ssh/id_ed25519.pub` corresponde a la clave pública y puede compartirse libremente; el fichero `~/.ssh/id_ed25519` contiene la clave privada y **nunca** debe transferirse ni divulgarse).*

### Paso 3: Instanciar el Servidor SSH de Prueba (Docker Compose)

Utilice Docker Compose para desplegar un contenedor Linux con OpenSSH configurado para escuchar en el puerto **`2222`**:

1. Cree el subdirectorio `ssh-server` y acceda a él:
   ```bash
   $ mkdir -p ~/IEI/aula07/ssh-server
   $ cd ~/IEI/aula07/ssh-server
   ```

2. Cree el fichero `custom-openssh-server.Dockerfile`, que amplía la imagen base de OpenSSH incorporando `rsync` y `python3`:
   ```dockerfile
   FROM lscr.io/linuxserver/openssh-server:latest
   RUN apk update && apk add rsync python3 && rm -rf /var/cache/apk/*
   ```

3. Cree el fichero `compose.yml` para configurar el servicio y mapear el puerto `2222`:
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
         - "2222:2222" # Mapea puerto 2222 anfitrión -> puerto 2222 contenedor
       restart: unless-stopped
   ```

4. Cree el directorio `authorized_keys` y copie en su interior su **clave pública**, autorizando el acceso al usuario `student`:
   ```bash
   $ mkdir -p authorized_keys
   $ cp ~/.ssh/id_ed25519.pub ./authorized_keys/student.pub
   ```

5. Construya e inicie el contenedor en segundo plano (*detached mode*), verificando su correcto estado de ejecución:
   ```bash
   $ docker compose up -d --build
   $ docker compose ps
   ```

6. Regrese al directorio principal de trabajo:
   ```bash
   $ cd ~/IEI/aula07
   ```

-----

## Parte 1: Inspección de la Máquina Local y de la Red Local (LAN)

En el diagnóstico de incidencias de conectividad, la primera fase consiste en inspeccionar la configuración de las interfaces de red del propio equipo.

### Ejercicio 1: Identificar Dirección MAC, Dirección IP y Máscara de Subred (`ip a` / `ifconfig`)

Enumere las interfaces de red configuradas en el sistema operativo:

* **En Linux** (o en macOS con `iproute2mac`):
  ```bash
  $ ip a
  ```
* **En macOS (nativo):**
  ```bash
  $ ifconfig
  ```

Analice la salida del comando e identifique los siguientes elementos:

1. **La interfaz `lo` (Linux) o `lo0` (macOS) — *Loopback*:** Muestra las direcciones `inet 127.0.0.1` e `inet6 ::1`. Se trata de la interfaz virtual interna que enruta tráfico hacia el propio computador (`localhost`).
2. **Su interfaz de red principal** (habitualmente identificada como `eth0`, `enp0s3` o `wlan0` en Linux, y como **`en0`** en macOS):
   * **Dirección MAC (Capa de Enlace de Datos — L2):** Localice el campo `link/ether` (en `ip a`) o `ether` (en `ifconfig` de macOS), por ejemplo `08:00:27:1a:2b:3c`. Constituye el identificador físico de 48 bits de la tarjeta de red en el enlace local.
   * **Dirección IPv4 y Máscara de Subred (Capa de Red — L3):** Localice el campo `inet` (ej.: `192.168.1.50/24` en Linux, o `inet 192.168.1.50 netmask 0xffffff00` en `ifconfig` de macOS, donde el valor hexadecimal `0xffffff00` equivale a `255.255.255.0` o `/24`).
     * El prefijo `/24` (`255.255.255.0`) indica que los 3 primeros octetos determinan el **prefijo de red local**, mientras que el último octeto identifica el **equipo anfitrión (*host*) en dicha subred** (rango utilizable de `.1` a `.254`).
   * **Dirección IPv6 *Link-Local*:** Localice el campo `inet6 fe80::...`, que corresponde a la dirección IPv6 autoconfigurada válida únicamente en el segmento local.
3. **La interfaz `docker0` / `br-...` (en Linux):** En instalaciones nativas de Linux, Docker crea un puente de red virtual con direccionamiento privado (habitualmente en el rango `172.17.0.1/16`) para comunicar contenedores *(en macOS, Docker Desktop opera sobre una máquina virtual Linux ligera, por lo que dicha interfaz reside internamente en la máquina virtual)*.

### Ejercicio 2: Verificar la Pila TCP/IP Local (`localhost` / Loopback)

Antes de comprobar la conectividad en el medio físico (Ethernet o Wi-Fi), conviene cerciorarse de que la pila protocolar TCP/IP del sistema operativo opera correctamente. Envíe 4 paquetes ICMP Echo Request (`-c 4`) a las direcciones de *loopback*:

```bash
# Probar interfaz de Loopback en IPv4 (Linux y macOS)
$ ping -c 4 127.0.0.1

# Probar interfaz de Loopback en IPv6 (en Linux)
$ ping -c 4 ::1

# Probar interfaz de Loopback en IPv6 (en macOS se utiliza ping6)
$ ping6 -c 4 ::1
```

Examine el tiempo de respuesta (`time=... ms`) y la tasa de pérdida de paquetes (`0% packet loss`). Dado que las tramas se procesan íntegramente en la memoria del núcleo del sistema operativo sin transmitirse por el medio físico, la latencia es prácticamente nula (típicamente inferior a `0.1 ms`).

### Ejercicio 3: Identificar el Default Gateway y Comprobar la Conectividad en la LAN

Para encaminar paquetes dirigidos a redes externas (como Internet), el computador local debe conocer la dirección IP del router de la red local —denominado **Default Gateway**.

1. Consulte la tabla de enrutamiento del sistema operativo para determinar la ruta predeterminada (`default`):
   * **En Linux** (o en macOS con `iproute2mac`):
     ```bash
     $ ip route show default
     ```
     *(O abreviadamente `ip r`).* La salida presentará la estructura `default via 192.168.1.1 dev eth0`, donde la dirección IP tras **`via`** corresponde al **Default Gateway**.
   * **En macOS (nativo):**
     ```bash
     $ netstat -rn -f inet | grep default
     # o:
     $ route -n get default
     ```
     La dirección reflejada en la columna `Gateway` (o en el campo `gateway:`) indica el **Default Gateway**.

2. Verifique la conectividad directa con el router mediante el comando `ping` (sustituya por la IP obtenida en el paso previo):
   ```bash
   $ ping -c 4 <IP_DEL_DEFAULT_GATEWAY>
   ```
   La recepción de respuestas con `0% packet loss` ratifica que el enlace físico (cable o Wi-Fi) y la conectividad a nivel de red local (LAN) funcionan correctamente.

### Ejercicio 4: Inspeccionar la Resolución de Direcciones en la Tabla ARP (`ip neigh` / `arp -an`)

Para encapsular el paquete IP dirigido al Default Gateway dentro de una trama Ethernet (Capa 2), el sistema operativo recurrió previamente al protocolo **ARP (*Address Resolution Protocol*)** con el fin de descubrir la **dirección MAC física** asociada a la dirección IPv4 del router.

Consulte la tabla ARP almacenada en el sistema:

* **En Linux:**
  ```bash
  $ ip neigh
  ```
* **En macOS (y también disponible en Linux):**
  ```bash
  $ arp -an
  ```

Localice la entrada correspondiente a la dirección IP de su Default Gateway: observará junto a ella su dirección MAC física. Esta correspondencia permite a la interfaz de red direccionar las tramas Ethernet en el segmento local.

-----

## Parte 2: De la Red Local a Internet (WAN, NAT y DNS)

Una vez confirmada la conectividad en la red local hasta el Default Gateway, se analiza a continuación el enrutamiento hacia redes externas (WAN / Internet) y el mecanismo de resolución de nombres de dominio.

### Ejercicio 5: Probar la Conectividad Externa por Dirección IP frente a Nombre de Dominio (`ping`)

La imposibilidad de acceder a recursos externos puede originarse tanto por la ausencia de enrutamiento IP hacia el exterior como por un fallo específico en el servicio de resolución de nombres (**DNS**). Para aislar la causa, realice dos comprobaciones:

1. Pruebe la conectividad IP directa frente a una **dirección IP pública** externa reconocida (por ejemplo, el servidor público `8.8.8.8` operado por Google):
   ```bash
   $ ping -c 4 8.8.8.8
   ```
   *La recepción de respuestas confirma la operatividad del enrutamiento IP hacia Internet.* Compare la latencia (*Round-Trip Time* — `time=... ms`) con la de la red local: al transitar por múltiples encaminadores intermedios y centros de datos externos, la latencia se situará habitualmente entre `8 ms` y `30 ms`.

2. Ejecute ahora la prueba empleando un **nombre de dominio**:
   ```bash
   $ ping -c 4 ua.pt
   ```
   Observe en la primera línea de salida que el sistema operativo consultó previamente al servicio **DNS** para resolver el nombre `ua.pt` en su dirección IPv4 correspondiente (ej.: `193.136.172.10`) antes de enviar los paquetes ICMP.

> **Principio de Diagnóstico:** Si el comando `ping 8.8.8.8` tiene éxito pero `ping ua.pt` genera un error de resolución (*"Temporary failure in name resolution"* o *"cannot resolve...: Unknown host"*), la conectividad IP a Internet se encuentra operativa, localizándose el problema exclusivamente en la configuración de **DNS**.

### Ejercicio 6: Trazado de la Ruta de Enrutamiento (`traceroute`)

Para identificar la secuencia de encaminadores (*routers*) atravesados por un paquete desde el equipo anfitrión hasta el sistema de destino, ejecute `traceroute`:

```bash
$ traceroute 8.8.8.8
```

Analice la relación ordenada de saltos (*hops*):

* El **Salto 1** corresponde siempre al encaminador de la red local (*Default Gateway*).
* Los saltos sucesivos corresponden a routers del proveedor de servicios de Internet (ISP), de la red troncal académica y de proveedores de tránsito hasta alcanzar la red de destino.
* *(Nota técnica: La presencia de asteriscos `* * *` en una línea indica que el router intermedio descarta o limita el envío de respuestas ICMP Time Exceeded, lo cual no impide que el tráfico continúe su avance hacia los saltos siguientes).*

Compruebe también la secuencia de saltos hasta el servidor web de la Universidade de Aveiro:
```bash
$ traceroute ua.pt
```

### Ejercicio 7: Resolución de Nombres de Dominio (`dig` y `/etc/hosts`)

Para examinar en detalle la traducción de nombres de dominio en direcciones IP numéricas:

1. Emplee la herramienta `dig` para consultar el registro de dirección IPv4 (tipo **`A`**) asignado a `ua.pt`:
   ```bash
   $ dig ua.pt A
   ```
   En el bloque `;; ANSWER SECTION:` se visualiza la dirección IPv4 obtenida y su periodo de validez (*TTL*). Para obtener una respuesta condensada (únicamente la IP), añada el modificador `+short`:
   ```bash
   $ dig ua.pt A +short
   ```

2. Efectúe una consulta DNS inversa mediante el parámetro `-x` para determinar el nombre de dominio vinculado a una IP pública:
   ```bash
   $ dig -x 8.8.8.8 +short
   ```

3. Inspeccione el fichero estático local `/etc/hosts` (que el sistema operativo consulta **antes** de formular peticiones a servidores DNS externos):
   ```bash
   $ cat /etc/hosts
   ```
   Compruebe la entrada `127.0.0.1 localhost`, responsable de asignar localmente `localhost` a la dirección de *loopback* sin requerir tráfico DNS en la red.

### Ejercicio 8: Determinación de la Dirección IP Pública y Mecanismo de NAT (`curl`)

> **Concepto de NAT (*Network Address Translation*):**
> Como se constató en el Ejercicio 1, las interfaces locales operan con **Direcciones IP Privadas** (pertenecientes a los rangos reservados `10.0.0.0/8`, `172.16.0.0/12` o `192.168.0.0/16`), válidas exclusivamente en la red local (LAN) y no enrutables en Internet. Para permitir que múltiples equipos de una red privada accedan a Internet compartiendo una única **Dirección IP Pública**, el router de frontera aplica **NAT**: al reenviar un paquete de la LAN a la WAN, el router sustituye la IP privada de origen por su propia **IP Pública** y anota la traducción en una tabla de estado; cuando regresa el paquete de respuesta desde Internet, el router consulta dicha tabla, restablece la IP privada como destino y entrega el paquete al equipo correspondiente.

Para conocer la **Dirección IP Pública** con la que su equipo se presenta ante los servidores externos en Internet, consulte la API pública de `ipinfo.io` mediante `curl`:

```bash
$ curl -s https://ipinfo.io/json
```

Analice la respuesta en formato JSON:

* `ip`: La **Dirección IP Pública** asignada al router de salida de la red (compartida vía NAT por los dispositivos de la LAN).
* `city` / `region` / `org`: Ubicación geográfica aproximada y proveedor de conectividad (ISP / Sistema Autónomo).

-----

## Parte 3: Puertos, Servicios y Diagnóstico de Conexiones (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`)

En la administración de contenedores (**Docker**) y en el desarrollo de servicios en red (**Class 08 — Programación en Redes**), es fundamental comprobar qué puertos de transporte se encuentran a la escucha (*LISTEN*) y comprender cómo la dirección de vinculación (*bind address*) condiciona la accesibilidad de un servicio.

### Ejercicio 9: Inspeccionar Puertos en Estado de Escucha en el Sistema Local (`ss` / `lsof` y `nmap`)

En la Parte 0 se inició un contenedor con un servidor SSH expuesto en el puerto anfitrión `2222`. Verifique en el sistema operativo anfitrión que dicho puerto se encuentra abierto y en espera de conexiones:

1. Enumere los *sockets* de red en estado de escucha (*LISTEN*) en su equipo:
   * **En Linux (`ss -tuln` — listado numérico de *sockets* TCP/UDP en escucha):**
     ```bash
     $ ss -tuln
     ```
   * **En macOS (`lsof` — listado de puertos TCP en estado `LISTEN` sin resolución de nombres):**
     ```bash
     $ lsof -nP -iTCP -sTCP:LISTEN
     ```
   Identifique la línea que finaliza en **`:2222`** (ej.: `0.0.0.0:2222` en Linux o `*:2222 (LISTEN)` en macOS). Esto constata que un proceso local acepta activamente conexiones TCP en el puerto `2222`.

2. Efectúe un escaneo de puertos sobre la interfaz local (`localhost`) utilizando **`nmap`** (la sintaxis es idéntica en Linux y macOS):
   ```bash
   $ nmap localhost
   ```
   Compruebe en la tabla `PORT / STATE / SERVICE` que el puerto `2222/tcp` figura con estado **`open`**.

### Ejercicio 10: Vinculación de Servicios a Interfaces de Red (`127.0.0.1` frente a `0.0.0.0`)

> **Significado de la dirección `0.0.0.0` en la configuración de servidores:**
> A diferencia de `127.0.0.1` (que designa exclusivamente a la interfaz virtual de *loopback*), la dirección `0.0.0.0` no representa una interfaz individual, sino una **meta-constante de configuración (`INADDR_ANY`)**. Cuando un servidor se asocia (*bind*) a `0.0.0.0`, indica al sistema operativo que debe aceptar conexiones dirigidas a dicho puerto procedentes de **cualquier interfaz de red activa en el sistema** (incluidas `localhost`, adaptadores Ethernet/Wi-Fi de la LAN y puentes virtuales de Docker).

Para comprobar experimentalmente la diferencia de comportamiento entre vincular un proceso a **`127.0.0.1`** o a **`0.0.0.0`**:

1. Cree un directorio temporal con un fichero HTML básico:
   ```bash
   $ mkdir -p ~/IEI/aula07/teste-web && cd ~/IEI/aula07/teste-web
   $ echo "<h1>Servidor de Teste IEI</h1>" > index.html
   ```

2. **Escenario A — Vinculación exclusiva a `127.0.0.1` (Solo *Loopback*):**
   Inicie el servidor HTTP de Python en el puerto `8000` restringido a la dirección `127.0.0.1`:
   ```bash
   $ python3 -m http.server 8000 --bind 127.0.0.1
   ```
   *(Mantenga abierto este terminal con el servidor activo y **abra una segunda ventana de terminal**).*

3. En la **segunda ventana de terminal**, compruebe el estado del *socket* en el puerto `8000`:
   * **En Linux:**
     ```bash
     $ ss -tuln | grep 8000
     ```
   * **En macOS:**
     ```bash
     $ lsof -nP -iTCP -sTCP:LISTEN | grep 8000
     ```
   Observe que el *socket* se encuentra vinculado a **`127.0.0.1:8000`**:
   * Una petición originada en el propio equipo (`curl -I http://127.0.0.1:8000`) responde satisfactoriamente con **`HTTP/1.0 200 OK`**.
   * Sin embargo, cualquier intento de conexión procedente de otro equipo de la LAN (o del anfitrión hacia un contenedor Docker configurado de este modo) **será denegado (`Connection refused`)**, ya que el servidor no escucha en las interfaces de red externas.

4. En el primer terminal, detenga el servidor con **`Ctrl+C`** y reinícielo vinculándolo a **`0.0.0.0`** (todas las interfaces de red):
   ```bash
   $ python3 -m http.server 8000 --bind 0.0.0.0
   ```

5. En la segunda ventana de terminal, ejecute nuevamente la orden de verificación (`ss -tuln | grep 8000` en Linux, o `lsof -nP -iTCP -sTCP:LISTEN | grep 8000` en macOS):

   Verifique que el *socket* figura ahora vinculado a **`0.0.0.0:8000`** (Linux) o **`*:8000`** (macOS), aceptando conexiones recibidas a través de cualquier interfaz. Compruebe el acceso con `curl -I http://localhost:8000`, cierre el segundo terminal y finalice el servidor en el primer terminal mediante **`Ctrl+C`**.

   Regrese al directorio principal de trabajo:
   ```bash
   $ cd ~/IEI/aula07
   ```

### Ejercicio 11: Escaneo de Puertos en un Servidor Público de Prueba Autorizado (`nmap`)

> **Consideración Ética y Legal:** Realizar escaneos de puertos contra sistemas o redes de terceros sin autorización expresa no está permitido. Con fines didácticos, el proyecto Nmap dispone del servidor oficial de pruebas **`scanme.nmap.org`**.

Inspeccione los puertos abiertos en dicho servidor autorizado:

```bash
$ nmap scanme.nmap.org
```

Analice la tabla de servicios devuelta, localizando puertos estándar en estado `open`, tales como **`22/tcp` (`ssh`)** para administración remota y **`80/tcp` (`http`)** para tráfico web.

-----

## Parte 4: Administración Remota Segura (SSH, `rsync` y Reenvío de Puertos SSH)

En este bloque se utiliza el contenedor Linux con OpenSSH instanciado en la Parte 0 (accesible en el puerto `2222`) para realizar tres procedimientos esenciales de administración remota: acceso por consola con SSH, sincronización incremental de ficheros con `rsync` y reenvío local de puertos mediante túneles SSH (*SSH Local Port Forwarding*).

### Ejercicio 12: Establecer Sesión Remota mediante `ssh`

Inicie sesión con el usuario `student` en el servidor local que escucha en el puerto `2222`:

```bash
$ ssh student@localhost -p 2222
```

*(En la primera conexión a un nuevo servidor, el cliente SSH solicita confirmar la huella digital del host: `Are you sure you want to continue connecting (yes/no/[fingerprint])?` — escriba **`yes`** y pulse Enter).*

Observe que el *prompt* del terminal cambia, indicando que la sesión se ejecuta **dentro del contenedor remoto** (habiéndose autenticado automáticamente mediante el par de claves SSH generado previamente):

```bash
# Comandos ejecutados EN EL INTERIOR del servidor remoto:
$ whoami
$ pwd
$ ls -la
```

Para salir de la sesión remota y volver al anfitrión:
```bash
$ exit
```

### Ejercicio 13: Sincronización Incremental de Directorios con `rsync`

Para transferir y sincronizar directorios entre el equipo local y un servidor remoto a través de una conexión cifrada SSH, se utiliza **`rsync`**:

1. En el sistema local (en `~/IEI/aula07`), cree el directorio `meu-projeto` con dos ficheros de prueba:
   ```bash
   $ mkdir -p ~/IEI/aula07/meu-projeto
   $ echo "# Projeto de Redes IEI" > ~/IEI/aula07/meu-projeto/README.md
   $ echo "print('En el servidor remoto')" > ~/IEI/aula07/meu-projeto/app.py
   ```

2. Sincronice el directorio con la cuenta del servidor remoto empleando `rsync`:
   ```bash
   # -a: modo archivo (preserva permisos y marcas temporales); -v: detallado;
   # -z: compresión en tránsito; -P: indicador de progreso;
   # -e "ssh -p 2222": especifica la utilización de SSH en el puerto 2222.
   $ rsync -avzP -e "ssh -p 2222" ~/IEI/aula07/meu-projeto student@localhost:~/
   ```

3. Para constatar el algoritmo de transferencia diferencial (*delta-transfer*) de `rsync`, añada una línea al fichero `README.md` y repita el comando de sincronización:
   ```bash
   $ echo "Modificacion incremental" >> ~/IEI/aula07/meu-projeto/README.md
   $ rsync -avzP -e "ssh -p 2222" ~/IEI/aula07/meu-projeto student@localhost:~/
   ```
   Verifique en la salida que `rsync` **transfirió únicamente el fichero alterado (`README.md`)**, omitiendo el fichero `app.py` al no presentar cambios.

### Ejercicio 14: Reenvío Local de Puertos mediante Túnel SSH (*Local Port Forwarding*)

Considere el siguiente escenario común en administración de infraestructuras:
Un servicio web interno se ejecuta en el puerto **`8000`** de un servidor remoto, pero dicho puerto **no se encuentra expuesto al exterior** (en el fichero `compose.yml` de la Parte 0 únicamente se publicó el puerto `2222`). El **Reenvío Local de Puertos (*SSH Local Port Forwarding*)** permite acceder a dicho servicio interno desde el navegador del equipo local a través de la conexión cifrada existente.

> **Aviso Técnico — Habilitación de *TCP Forwarding* en el Servidor SSH:**
> Por motivos de seguridad, diversas distribuciones del servidor OpenSSH (incluida la imagen Alpine Linux empleada en el contenedor `iei-ssh-server` y ciertas configuraciones predeterminadas en Linux/macOS) deshabilitan por defecto el reenvío de puertos TCP (`AllowTcpForwarding no`), generando el error `channel X: open failed: administratively prohibited` al intentar utilizar el túnel.
> Antes de iniciar el ejercicio, active la directiva `AllowTcpForwarding yes` en el servidor ejecutando en la **máquina anfitriona**:
> ```bash
> # En el contenedor Docker iei-ssh-server:
> $ docker exec iei-ssh-server sed -i 's/AllowTcpForwarding no/AllowTcpForwarding yes/g' /config/sshd/sshd_config /etc/ssh/sshd_config
> $ docker restart iei-ssh-server
> ```
> *(Nota: En un servidor Linux/macOS nativo, esta directiva se encuentra en el fichero `/etc/ssh/sshd_config` y requiere reiniciar el servicio `sshd` tras su modificación).*

1. Acceda al servidor remoto mediante SSH:
   ```bash
   $ ssh student@localhost -p 2222
   ```

2. **En la sesión remota**, cree una página HTML e inicie el servidor web Python en el puerto **`8000`**:
   ```bash
   $ mkdir -p ~/servico-interno && cd ~/servico-interno
   $ echo "<h1>Accedido mediante Tunel SSH (Port Forwarding)</h1>" > index.html
   $ python3 -m http.server 8000
   ```
   *(Mantenga este terminal abierto con el servidor en ejecución dentro del contenedor).*

3. Abra una **nueva ventana de terminal en el equipo local** e intente acceder directamente al puerto `8000`:
   ```bash
   $ curl http://localhost:8000
   ```
   La petición es rechazada con **`Connection refused`**, dado que el puerto `8000` no está expuesto fuera del contenedor.

4. En esa segunda ventana de terminal local, establezca el **Túnel SSH**, redirigiendo el puerto local **`8080`** hacia el puerto **`8000`** del servidor remoto a través del canal SSH en el puerto `2222`:
   ```bash
   $ ssh -N -L 8080:localhost:8000 student@localhost -p 2222
   ```
   *(El modificador `-N` indica que no deben ejecutarse comandos remotos, dedicando la conexión exclusivamente al reenvío de puertos; mantenga en ejecución este proceso).*

5. En el **Navegador Web** del equipo local, acceda a la dirección:
   **[http://localhost:8080](http://localhost:8080)**

   Compruebe la carga de la página web servida por el proceso remoto. La solicitud dirigida al puerto local `8080` viaja encapsulada y cifrada a través de SSH (puerto `2222`) y es entregada internamente en el puerto `8000` del servidor.

6. Concluida la comprobación, cierre el túnel pulsando **`Ctrl+C`** en el segundo terminal y detenga el servidor HTTP Python en el primer terminal (`Ctrl+C`, seguido de `exit` para cerrar la sesión SSH).

-----

## Parte 5: Ejercicios Complementares de Consolidación

Si completa los ejercicios anteriores antes del cierre de la sesión práctica, realice las siguientes actividades avanzadas:

### Desafío A: Captura e Inspección de Paquetes en Tiempo Real con `tcpdump`

Para monitorizar a bajo nivel el intercambio de paquetes en la interfaz de red:

1. En un terminal, inicie el analizador de tráfico `tcpdump` filtrando por el protocolo `icmp` (empleado por `ping`) y deshabilitando la resolución numérica (`-n`):
   ```bash
   $ sudo tcpdump -i any icmp -n
   ```
2. En un segundo terminal, emita 2 paquetes ICMP Echo Request a `8.8.8.8`:
   ```bash
   $ ping -c 2 8.8.8.8
   ```
3. Observe en el primer terminal las parejas de paquetes `ICMP echo request` (emitidos desde la IP local) e `ICMP echo reply` (recibidos desde `8.8.8.8`). Para concluir la captura, pulse `Ctrl+C`.

### Desafío B: Representación Geográfica de Rutas IP (Geo-Traceroute)

Utilice la herramienta `geotraceroute` en Python para combinar el trazado de encaminadores con geolocalización IP en un mapa interactivo:
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

## Síntesis de Comandos Abordados

| Comando (Linux / macOS) | Finalidad Técnica (Diagnóstico y Administración) | Ejemplo de Uso |
| :--- | :--- | :--- |
| `ip a` (Linux) / `ifconfig` (macOS) | Listar interfaces de red, dirección física (MAC), dirección IPv4/IPv6 y máscara (`/24`). | `ip a` / `ifconfig` |
| `ip r` (Linux) / `netstat -rn -f inet` (macOS) | Consultar la tabla de enrutamiento e identificar el *Default Gateway*. | `ip r` / `route -n get default` |
| `ip neigh` (Linux) / `arp -an` (macOS) | Consultar la tabla ARP (asociación entre IPs locales y direcciones MAC). | `ip neigh` / `arp -an` |
| `ping -c 4` (`ping6 -c 4` p/ IPv6 en macOS) | Verificar conectividad IP (ICMP) y cuantificar latencia de ida y vuelta (`ms`). | `ping -c 4 8.8.8.8` |
| `traceroute <destino>` | Identificar la secuencia de encaminadores (*hops*) hasta el destino. | `traceroute ua.pt` |
| `dig <dominio> +short` | Consultar servidores DNS para resolver nombres de dominio en direcciones IP. | `dig ua.pt +short` |
| `curl <url>` | Emitir peticiones HTTP/HTTPS a servidores web o APIs desde el terminal. | `curl -I http://localhost:8000` |
| `ss -tuln` (Linux) / `lsof -nP -iTCP -sTCP:LISTEN` (macOS) | Listar *sockets* y puertos TCP/UDP en estado de escucha (*LISTEN*) en el anfitrión. | `ss -tuln` |
| `nmap <objetivo>` | Realizar escaneo de puertos para identificar servicios activos en un sistema. | `nmap localhost` |
| `ssh <usuario>@<host>` | Iniciar sesión remota cifrada por consola en un servidor SSH. | `ssh student@localhost -p 2222` |
| `rsync -avzP` | Transferir y sincronizar directorios de forma incremental sobre SSH. | `rsync -avzP ./dir student@host:~/` |
| `ssh -N -L <p1>:localhost:<p2>` | Crear un túnel SSH de reenvío local de puertos entre el puerto local `p1` y el remoto `p2`. | `ssh -N -L 8080:localhost:8000 user@host` |

