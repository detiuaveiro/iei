---
title: Virtualización
subtitle: Introducción a la Ingeniería Informática
institute: Universidade de Aveiro
date: October 12, 2026
colorlinks: true
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guía Práctica de Laboratorio

Esta guía ha sido diseñada para una sesión de **3 horas** y se estructura en cinco partes progresivas de experimentación con sistemas de virtualización:

* **Parte 1 — Configuración del Entorno de Virtualización:** Preparación de las plataformas de virtualización de referencia mediante dos paradigmas: interfaz gráfica (Oracle VirtualBox) y línea de comandos (QEMU en Linux y macOS).
* **Parte 2 — Emulación de Plataformas Heredadas con FreeDOS:** Emulación por software de instrucciones de CPU x86-16, periféricos de audio clásicos (SoundBlaster 16) e inyección de medios de almacenamiento secundario.
* **Parte 3 — Virtualización de Sistemas con Alpine Linux:** Despliegue de una distribución Linux minimalista, evaluación de topologías de red virtual (NAT vs. Adaptador Puente) y alojamiento de servicios de red (HTTP).
* **Parte 4 — Virtualización Anidada con Proxmox VE:** Despliegue de un hipervisor Tipo-1 bare-metal dentro de una máquina virtual (*nested virtualization*) y administración mediante consola web.
* **Parte 5 — Extensión Autónoma: Emulación de Arquitecturas Móviles (Android):** Simulación de plataformas móviles y gestión de periféricos virtuales mediante Android Virtual Device (AVD).

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Antes de comenzar las prácticas, cree y acceda a la carpeta de trabajo dedicada para esta sesión:

```bash
$ mkdir -p ~/IEI/clase03
$ cd ~/IEI/clase03
```

Todos los archivos generados a lo largo de la sesión (discos virtuales `*.qcow2`, imágenes ISO descargadas y carpetas compartidas) deberán mantenerse dentro de este directorio.

> **Nota sobre rutas de archivos:**
> Todos los comandos de esta guía asumen que el terminal se encuentra en el directorio de trabajo `~/IEI/clase03`. En caso de descargar imágenes ISO en otra ubicación (como la carpeta de descargas del navegador), muévalas a `~/IEI/clase03` o especifique la ruta completa correspondiente en el comando (ej.: `"$HOME/Downloads/FD14LIVE.iso"`).

-----

## Parte 1: Configuración del Entorno de Virtualización

La guía proporciona dos enfoques fundamentales para llevar a cabo las prácticas: un **enfoque gráfico** basado en Oracle VirtualBox y un **enfoque de línea de comandos (CLI)** basado en QEMU. Puede elegir uno de ellos o explorar ambos simultáneamente.

### Enfoque A: Interfaz Gráfica (Desktop) — Oracle VirtualBox
*(Disponible para Windows, macOS y Linux)*

1. **Descarga e Instalación:**
   * Acceda a la [página oficial de descargas de VirtualBox](https://www.virtualbox.org/wiki/Downloads) y descargue el instalador binario correspondiente a su sistema operativo anfitrión.
   * Descargue asimismo el **VirtualBox Extension Pack** disponible en la misma página.
   * Ejecute el instalador siguiendo las opciones predeterminadas. En macOS, es obligatorio autorizar la extensión de sistema de Oracle en `Ajustes del Sistema > Privacidad y Seguridad`.
   * Abra el archivo del Extension Pack descargado para instalar los controladores avanzados (soporte para USB 2.0/3.0 y aceleración RDP).

2. **Flujo de Operación en VirtualBox:**
   * La gestión de máquinas virtuales se realiza mediante la interfaz gráfica de administración.
   * El botón **"Nueva"** inicia el asistente guiado para la configuración de una nueva máquina virtual (definición de nombre, tipo de SO, asignación de memoria RAM y disco virtual).
   * Las propiedades de hardware y dispositivos virtuales pueden modificarse seleccionando cualquier VM y accediendo al menú **"Configuración"**.

### Enfoque B: Línea de Comandos (CLI) — QEMU
*(Disponible de forma nativa en Linux, en WSL2 en Windows, nativamente en macOS mediante Homebrew, o en el terminal de la VM Ubuntu creada en la Clase 00 vía VirtualBox)*

1. **Instalación de QEMU:**
   * **En Linux / WSL2 (o dentro de la VM Ubuntu de la Clase 00):**
     Ejecute en el terminal:
     ```bash
     $ sudo apt update
     $ sudo apt install qemu-system-x86 qemu-system-i386 bridge-utils
     ```
     Añada su usuario al grupo `kvm` para permitir el acceso directo a `/dev/kvm` sin `sudo` (cierre sesión y vuelva a entrar para activar):
     ```bash
     $ sudo usermod -a -G kvm $USER
     ```
   * **En macOS:**
     Utilizando el gestor de paquetes Homebrew, ejecute en el terminal:
     ```bash
     $ brew install qemu
     ```

2. **Sintaxis General y Anatomía de Comandos:**
   QEMU opera mediante opciones explícitas en la línea de comandos, que se aplicarán en los ejercicios posteriores:
   * **Aprovisionamiento de Discos (`qemu-img`):** Utiliza la sintaxis `qemu-img create -f <formato> <archivo> <tamaño>` (por ejemplo, creando imágenes dinámicas en formato `qcow2`).
   * **Instanciación de Máquinas Virtuales (`qemu-system-*`):** Se invoca el binario correspondiente a la arquitectura objetivo (`qemu-system-i386` para 16/32-bit o `qemu-system-x86_64` para 64-bit), especificando los recursos asignados:
     * `-m <RAM>`: Asignación de memoria (ej.: `128` o `1G`);
     * `-cpu <modelo>` o `-accel <tipo>`: Tipo de procesador y aceleración por hardware (ej.: `tcg`, `kvm` o `hvf`);
     * `-hda <disco>` / `-drive ...`: Disco duro principal o unidades complementarias;
     * `-cdrom <iso>` y `-boot <orden>`: Medio de instalación y secuencia de arranque (ej.: `-boot d` para iniciar desde el CD).

-----

## Parte 2: Emulación de Plataformas Heredadas con FreeDOS

FreeDOS es una implementación libre y compatible con MS-DOS, constituyendo un sistema operativo monotarea de 16-bit. Esta práctica permite analizar la emulación por software de circuitería clásica (controladores gráficos Cirrus Logic VGA, periféricos de audio SoundBlaster 16 y temporizador de tiempo real RTC).

1. **Obtención de Recursos:**
   * Descargue la imagen **Live CD de FreeDOS 1.4** desde el [repositorio oficial](https://www.freedos.org/download/), utilizando el archivo comprimido `FD14-LiveCD.zip` [disponible aquí](https://www.ibiblio.org/pub/micro/pc-stuff/freedos/files/distributions/1.4/FD14-LiveCD.zip). Extraiga el archivo y coloque la imagen `FD14LIVE.iso` en su carpeta de trabajo `~/IEI/clase03/`.
   * Obtenga el archivo comprimido del juego shareware **DOOM** (`doom19s.zip`), disponible en la página de **eLearning** de la asignatura. Guárdelo en `~/IEI/clase03/` y extráigalo en la subcarpeta `./doom`:
     ```bash
     $ cd ~/IEI/clase03
     $ mkdir -p doom
     $ unzip -o doom19s.zip -d doom/
     ```

2. **Creación e Instalación de la Máquina Virtual FreeDOS:**

   #### Opción 1: Oracle VirtualBox (GUI)
   1. Seleccione **"Nueva"**. Defina el Nombre como `FreeDOS`, el Tipo como `Other` y la Versión como `DOS`.
   2. Memoria RAM: asigne `64 MB`.
   3. Disco Virtual: cree una nueva imagen VDI de tamaño fijo con `128 MB`.
   4. En **Configuración > Almacenamiento**, seleccione la unidad óptica virtual vacía en el controlador IDE y elija el archivo `FD14LIVE.iso` ubicado en su carpeta de trabajo.
   5. Inicie la VM y siga las instrucciones del asistente de FreeDOS. En la primera fase, el disco se particiona mediante FDISK y se solicita reiniciar; tras reiniciar, confirme el formateo de la unidad `C:` y complete la instalación de paquetes.
   6. Concluida la instalación, apague la VM y retire la imagen ISO de la unidad óptica virtual.

   #### Opción 2: QEMU (CLI)
   1. Asegúrese de encontrarse en la carpeta `~/IEI/clase03` y cree el disco virtual de 128 MB:
      ```bash
      $ cd ~/IEI/clase03
      $ qemu-img create -f qcow2 freedos.qcow2 128M
      ```
   2. Inicie la máquina virtual con el Live CD de instalación:
      * **En Linux / WSL2 (con aceleración KVM/TCG e interfaz gráfica GTK):**
        ```bash
        $ qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
            -k pt-pt -rtc base=localtime -device adlib -device sb16 \
            -device cirrus-vga -display gtk -hda freedos.qcow2 \
            -cdrom FD14LIVE.iso -boot d
        ```
      * **En macOS (con emulación TCG e interfaz gráfica nativa Cocoa):**
        ```bash
        $ qemu-system-i386 -accel tcg -m 128 -cpu pentium \
            -rtc base=localtime -device adlib -device sb16 \
            -device cirrus-vga -display cocoa -hda freedos.qcow2 \
            -cdrom FD14LIVE.iso -boot d
        ```
   3. **Instalación de FreeDOS:**
      * Seleccione "Install to harddisk".
      * El instalador opera en dos pasos: crea la partición mediante FDISK y solicita reiniciar la máquina. En el arranque posterior, confirme el formateo de la partición `C:` y espere a que finalice la copia de archivos.
      * Cuando aparezca el mensaje de confirmación final, cierre la ventana de QEMU.

3. **Inyección del Juego (DOOM) y Ejecución:**
   Para transferir los binarios del juego al entorno virtual:

   #### En VirtualBox:
   * Cree una imagen ISO a partir de la carpeta `./doom` (o utilice utilidades del sistema).
   * En **Configuración > Almacenamiento**, añada una unidad óptica con dicha imagen ISO.
   * Inicie FreeDOS. La unidad secundaria aparecerá con la letra `D:`.

   #### En QEMU (Linux y macOS):
   * Inicie FreeDOS desde el disco duro (`-boot c`), mapeando la carpeta local `./doom` directamente como unidad virtual secundaria FAT:
     * **En Linux / WSL2:**
       ```bash
       $ qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
           -k pt-pt -rtc base=localtime -device adlib -device sb16 \
           -device cirrus-vga -display gtk -hda freedos.qcow2 -boot c \
           -drive file=fat:rw:./doom,format=raw
       ```
     * **En macOS:**
       ```bash
       $ qemu-system-i386 -accel tcg -m 128 -cpu pentium \
           -rtc base=localtime -device adlib -device sb16 \
           -device cirrus-vga -display cocoa -hda freedos.qcow2 -boot c \
           -drive file=fat:rw:./doom,format=raw
       ```

4. **Instalación y Ejecución del Juego en FreeDOS:**
   * En la consola de comandos de FreeDOS (`C:\>`), cambie a la unidad secundaria:
     ```bat
     D:
     dir
     ```
   * Ejecute el instalador:
     ```bat
     INSTALL.BAT
     ```
   * Siga las opciones predeterminadas (instalación en `C:\DOOM`). En la configuración de sonido, elija **Sound Blaster** (Puerto 220, IRQ 5 o 7, DMA 1).
   * Inicie el juego:
     ```bat
     C:
     cd DOOM
     DOOM.EXE
     ```
   * Valide el comportamiento de la emulación: resolución gráfica en modo VGA (320x200), respuesta del temporizador RTC y síntesis de audio a través del dispositivo SoundBlaster 16 emulado.

-----

## Parte 3: Virtualización de Sistemas con Alpine Linux

Alpine Linux es una distribución orientada a la seguridad y a la eficiencia en el uso de recursos, basada en musl libc y BusyBox. Se utiliza ampliamente en la industria como imagen base de contenedores y en entornos virtuales ligeros.

1. **Obtención de la Imagen de Alpine Linux:**
   * Acceda a la [página oficial de descargas de Alpine Linux](https://alpinelinux.org/downloads/) y descargue la imagen **STANDARD**, guardándola en la carpeta `~/IEI/clase03/` con el nombre `alpine.iso`:
     * En sistemas con procesador x86-64 (Intel/AMD): descargue la ISO **x86_64**.
     * En macOS con procesadores Apple Silicon (M1/M2/M3/M4): descargue la ISO **aarch64** para beneficiarse de aceleración nativa por hardware con Hypervisor.framework (`-accel hvf`).

2. **Creación e Instalación de la Máquina Virtual:**

   #### Opción 1: Oracle VirtualBox (GUI)
   1. Cree una nueva VM: Nombre `Alpine`, Tipo `Linux`, Versión `Linux 2.6 / 3.x / 4.x (64-bit)`.
   2. Memoria RAM: `1 GB`. Disco Duro Virtual: `8 GB`.
   3. Asocie la imagen `alpine.iso` en **Configuración > Almacenamiento**.
   4. Inicie la máquina virtual e inicie sesión como usuario `root` (sin contraseña). Ejecute el asistente de instalación `setup-alpine`. Seleccione el modo de instalación `"sys"` en el disco `sda`. Al finalizar, apague la VM y retire la imagen ISO.

   #### Opción 2: QEMU (CLI)
   1. Asegúrese de encontrarse en la carpeta `~/IEI/clase03` y cree la imagen de disco virtual:
      ```bash
      $ cd ~/IEI/clase03
      $ qemu-img create -f qcow2 alpine.qcow2 8G
      ```
   2. Inicie la instalación a partir de la imagen ISO:
      * **En Linux / WSL2 (con KVM e imagen x86_64):**
        ```bash
        $ qemu-system-x86_64 -enable-kvm -m 1G -smp 2 -cpu host \
            -display gtk -hda alpine.qcow2 -cdrom alpine.iso -boot d
        ```
      * **En macOS Apple Silicon (con HVF nativo e imagen aarch64):**
        ```bash
        $ qemu-system-aarch64 -accel hvf -M virt -cpu host -m 1G -smp 2 \
            -display cocoa -hda alpine.qcow2 -cdrom alpine.iso -boot d
        ```
        *(Nota: si utiliza la imagen x86_64 en macOS Apple Silicon, utilice `qemu-system-x86_64` con `-accel tcg`).*
   3. En la consola de la VM, inicie sesión como `root` y ejecute `setup-alpine`. Seleccione la instalación `"sys"` en `sda`. Al concluir, apague la VM y arranque en los inicios posteriores sin el parámetro `-cdrom`.

3. **Análisis de Topologías de Red Virtual:**
   * **Modo NAT (Predeterminado):**
     Inicie la máquina virtual en modo NAT y compruebe su dirección IP:
     ```bash
     # En el terminal de la VM Alpine
     $ ip addr show
     ```
     Compruebe que la dirección IP asignada pertenece a una subred privada interna (ej.: `10.0.2.15`). Pruebe la conectividad externa con `ping google.com`. Observe que la VM accede a redes externas, pero los dispositivos de la red local física no pueden iniciar conexiones entrantes hacia la VM.
   * **Modo Bridge (Adaptador Puente):**
     Apague la máquina virtual para modificar la topología de red:
     * **En VirtualBox:** En **Configuración > Red**, cambie la opción **Conectado a:** de `NAT` a `Adaptador puente`.
     * **En QEMU (Linux):** Configure una interfaz de puente de red en el host Linux vinculada al adaptador físico:
       ```bash
       echo -e "Configurar Interfaz Bridge"
       sudo /sbin/ip link add virtbr0 type bridge
       sudo /sbin/ip link set dev $INTERFACE master virtbr0
       sudo /sbin/ip addr flush dev $INTERFACE
       sudo /sbin/dhclient virtbr0
       sudo /sbin/ip link set dev $INTERFACE up
       sudo /sbin/ip link set dev virtbr0 up

       echo -e "Iniciar Alpine (BRIDGE)"
       sudo qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
           -k pt-pt -rtc base=localtime -display gtk -hda alpine.qcow2 \
           -netdev bridge,id=net0,br=virtbr0 -device virtio-net-pci,netdev=net0

       echo -e "Limpiar Interfaz Bridge"
       sudo /sbin/ip link set virtbr0 down
       sudo /sbin/ip link del virtbr0
       sudo /sbin/dhclient $INTERFACE
       ```
     * Inicie la VM nuevamente y ejecute `ip addr show`. Confirme que la dirección IP obtenida pertenece ahora al mismo segmento de red física local que el ordenador anfitrión (ej.: `192.168.1.x`).

4. **Alojamiento de un Servicio Web (HTTP):**
   * BusyBox incluye un servidor HTTP integrado (`httpd`). Instale el paquete de utilidades extendidas:
     ```bash
     # En el terminal de la VM Alpine
     $ apk add busybox-extras
     ```
   * Cree el directorio para servir el contenido estático:
     ```bash
     $ mkdir -p /var/www/localhost/htdocs
     ```
   * Cree un documento HTML básico:
     ```bash
     $ echo '<h1>Laboratorio de Virtualización - Alpine Linux</h1>' > /var/www/localhost/htdocs/index.html
     ```
   * Inicie el servicio web escuchando en el puerto 80:
     ```bash
     $ httpd -f -p 80 -h /var/www/localhost/htdocs
     ```
   * Abra el navegador web en la máquina anfitriona y acceda a la dirección IP de la VM Alpine. Confirme la recepción de la respuesta HTTP.

-----

## Parte 4: Virtualización Anidada con Proxmox VE

Proxmox Virtual Environment (VE) es una plataforma empresarial abierta para la gestión integral de virtualización de servidores basada en Debian, integrando hipervisores KVM para máquinas virtuales completas y tecnología LXC para contenedores de sistema operativo.

> **NOTA TÉCNICA: Virtualización Anidada (Nested Virtualization)**
> La ejecución de un hipervisor dentro de otro hipervisor requiere propagar las instrucciones de virtualización de la CPU física (Intel VT-x o AMD-V) directamente hacia la vCPU de la máquina virtual. Esta técnica introduce una sobrecarga computacional apreciable y está destinada a fines estrictamente de experimentación en laboratorio.

1. **Obtención de Proxmox VE:**
   * Acceda a la [página oficial de descargas de Proxmox VE](https://www.proxmox.com/en/downloads) y descargue la imagen ISO del instalador más reciente, guardándola en `~/IEI/clase03/` con el nombre `proxmox.iso`.

2. **Aprovisionamiento de la Máquina Virtual Proxmox:**
   Esta máquina virtual requiere una mayor asignación de recursos físicos:

   #### Opción 1: Oracle VirtualBox (GUI)
   1. Cree una VM: Nombre `Proxmox`, Tipo `Linux`, Versión `Debian (64-bit)`.
   2. Memoria RAM: mínimo de `4096 MB`. Procesadores: mínimo de `2` vCPUs.
   3. Disco Virtual: `32 GB` o superior.
   4. En **Configuración > Sistema > Procesador**, marque obligatoriamente la casilla **Habilitar VT-x/AMD-V anidado**.
   5. En **Configuración > Red**, mantenga el modo `NAT`.
   6. Configure una regla de **Reenvío de Puertos (Port Forwarding)** mapeando el puerto `8006` del anfitrión al puerto `8006` del huésped.
   7. Asocie el archivo `proxmox.iso` en la controladora de almacenamiento.

   #### Opción 2: QEMU (CLI)
   1. Asegúrese de encontrarse en la carpeta `~/IEI/clase03` y cree el disco virtual de 32 GB:
      ```bash
      $ cd ~/IEI/clase03
      $ qemu-img create -f qcow2 proxmox.qcow2 32G
      ```
   2. Inicie la máquina virtual con soporte para virtualización anidada y reenvío del puerto web `8006`:
      * **En Linux / WSL2 (con aceleración KVM):**
        ```bash
        $ qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -cpu host \
            -hda proxmox.qcow2 -cdrom proxmox.iso -boot d \
            -netdev user,id=net0,hostfwd=tcp::8006-:8006 \
            -device virtio-net-pci,netdev=net0 -display gtk
        ```
      * **En macOS:**
        *(Nota: Proxmox VE requiere arquitectura x86-64. En macOS con procesadores Intel, puede ejecutarse con `-accel hvf`. En equipos Apple Silicon ARM64, ejecutar un hipervisor x86 requiere emulación completa por software mediante TCG; se recomienda realizar esta práctica en Linux nativo o VirtualBox x86).*

3. **Instalación y Configuración Inicial:**
   * Inicie la máquina virtual y continúe a través del instalador gráfico de Proxmox.
   * En la configuración de red estática, asigne una dirección IP de administración adecuada (ej.: `192.168.1.200/24`).
   * Al finalizar la instalación, reinicie el sistema huésped y extraiga la imagen ISO.

4. **Acceso a la Consola Web de Administración:**
   * En la consola de texto de Proxmox, compruebe la URL de administración HTTPS. Abra el navegador de su máquina anfitriona y acceda a `https://localhost:8006`.
   * Confirme la advertencia de seguridad correspondiente al certificado TLS autofirmado.
   * Autentíquese con el usuario `root` y la contraseña establecida durante la instalación.

5. **Despliegue de una Instancia Huésped en Proxmox:**
   * Explore la gestión de recursos virtualizados en la consola web de Proxmox.
   * Desafío práctico: Transfiera la imagen ISO de Alpine Linux al almacenamiento local de Proxmox y cree una máquina virtual anidada mediante la interfaz web de administración.

-----

## Parte 5: Extensión Autónoma — Emulación de Arquitecturas Móviles (Android)

La emulación de la plataforma Android permite simular la arquitectura de procesamiento y los subsistemas de periféricos de dispositivos móviles. Bajo la interfaz gráfica de Android Studio, el emulador oficial opera mediante una versión especializada del motor QEMU.

1. **Obtención e Instalación de Android Studio:**
   * Acceda al [portal oficial de Android Studio](https://developer.android.com/studio) y descargue el paquete de instalación correspondiente a su sistema operativo anfitrión.
   * Complete el asistente de instalación estándar, permitiendo la descarga de los paquetes SDK complementarios.

2. **Gestión de Dispositivos Virtuales (AVD Manager):**
   * Abra Android Studio (sin necesidad de crear un proyecto).
   * Desde la pantalla de bienvenida o a través del menú **Tools**, seleccione **Virtual Device Manager** (AVD).

3. **Aprovisionamiento del Dispositivo Virtual:**
   * Seleccione **"Create Virtual Device..."**.
   * Elija un perfil de hardware telefónico de referencia (ej.: Google Pixel 7).
   * Seleccione y descargue la imagen de sistema recomendada de Android.
   * Confirme las opciones de asignación de memoria y nombre el perfil AVD.

4. **Ejecución e Inspección del Sistema Emulado:**
   * En el gestor AVD, pulse el icono de inicio ("Play") del dispositivo creado.
   * El motor de emulación arrancará un sistema operativo Android completo en una ventana gráfica independiente. Analise el tiempo de inicialización, la fluidez del subsistema gráfico y los mecanismos de abstracción de sensores y periféricos del dispositivo móvil.
