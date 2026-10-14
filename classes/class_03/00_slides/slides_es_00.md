---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Virtualización: Arquitectura, Hipervisores & Virtualización de Sistemas"
institute: Universidade de Aveiro
date: October 12, 2026
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

Esta sesión aborda los fundamentos arquitecturales y los mecanismos prácticos de la virtualización de sistemas:

  * **Fundamentos de Virtualización & Hipervisores:** Abstracción de hardware, anillos de privilegio de la CPU, hipervisores Tipo-1 vs. Tipo-2.
  * **Emulación vs. Virtualización:** Principios de traducción por software, rendimiento relativo y casos de uso en ingeniería.
  * **E/S, Almacenamiento & Redes Virtuales:** Marco VirtIO, formatos de disco (QCOW2, VDI) y topologías de red (NAT, Bridge, Host-Only).
  * **Herramientas Prácticas de Virtualización:** Oracle VirtualBox, CLI de QEMU/KVM, Proxmox VE y matriz comparativa.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos \& Hipervisores}}
\end{center}

-----

## Virtualización: Definición

La **Virtualización** abstrae el hardware físico para instanciar múltiples entornos virtuales aislados (*VMs*) en un único ordenador físico:

  * **Anfitrión (Host):** Plataforma física de hardware (CPU, memoria, almacenamiento, interfaces de red).
  * **Hipervisor (VMM):** Software que gestiona el hardware, aísla instancias y planifica los recursos físicos.
  * **Máquina Virtual (VM):** Límite de abstracción aislado que expone hardware virtual (vCPU, vRAM, vDisk, vNIC).
  * **Huésped (Guest):** Sistema operativo y aplicaciones que se ejecutan dentro de una VM.

\vspace{0.2em}

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.50\textheight,keepaspectratio]{virtual_vs_traditional_architecture.png}
\end{center}

-----

## El Desafío de la Virtualización: Anillos de Privilegio

Las arquitecturas modernas de procesadores imponen niveles de privilegio de hardware (anillos) para aislar el código de aplicación de la ejecución del kernel:

  * **Ring 3 (Espacio de Usuario):** Las aplicaciones ejecutan instrucciones no privilegiadas. Las operaciones privilegiadas requieren invocar llamadas al sistema (`syscall`) al kernel.
  * **Ring 0 (Espacio de Kernel / Modo Supervisor):** El kernel del sistema operativo ejecuta instrucciones privilegiadas (ej.: control directo de la MMU, gestión de interrupciones, puertos de E/S).

  **¿Cómo pueden los múltiples Guests ejecutar instrucciones privilegiadas y gestionar el hardware de forma segura?**

  * La respuesta reside en el hipervisor como mediador y árbitro. Los hipervisores interceptan las instrucciones críticas y supervisan el acceso al hardware, delegando la ejecución al hardware real siempre que es posible.

-----

## Tipos de Hipervisores: Tipo-1 y Tipo-2

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.75\textheight,keepaspectratio]{hypervisor_types.png}
\end{center}

-----

## Hipervisores Tipo-1 (Bare-Metal)

Los **Hipervisores Tipo-1** se ejecutan directamente sobre el hardware físico, sin la intermediación de un sistema operativo de propósito general:

  * **Capa de Ejecución:** Opera directamente en la capa de privilegio de hardware. El hipervisor actúa como kernel primario y árbitro de recursos.
  * **Arquitectura:** Los controladores de dispositivos y dominios de gestión se ejecutan dentro de un microkernel mínimo del hipervisor o en una partición de gestión dedicada (ej.: Xen Dom0, Linux KVM).
  * **Características Principales:**
      * Sobrecarga de abstracción insignificante y latencia de hipervisor sub-milisegundo.
      * Alto rendimiento de E/S y máxima eficiencia de aprovechamiento del hardware.
      * Independencia del ciclo de vida o fallos de un sistema operativo de escritorio.
  * **Ejemplos en Producción:** VMware ESXi, Proxmox VE / KVM, Microsoft Hyper-V, Xen.

-----

## Hipervisores Tipo-2 (Hospedados)

Los **Hipervisores Tipo-2** se ejecutan como procesos estándar en el espacio de usuario sobre un sistema operativo anfitrión preexistente:

  * **Capa de Ejecución:** Depende del kernel del sistema operativo anfitrión para la planificación de recursos físicos, gestión de memoria y controladores de dispositivos.
  * **Arquitectura:** Utiliza controladores en modo kernel para acceder a las extensiones de virtualización por hardware, enrutando las peticiones de E/S a través de los subsistemas del SO anfitrión.
  * **Características Principales:**
      * Sobrecarga de doble planificación: el kernel huésped planifica procesos virtuales y el SO anfitrión planifica los procesos del hipervisor.
      * Gran facilidad de instalación y uso en estaciones de trabajo y portátiles personales.
      * Cómoda integración de escritorio entre anfitrión y huésped (portapapeles compartido, redimensionamiento dinámico de ventana, carpetas compartidas).
  * **Ejemplos en Producción:** Oracle VirtualBox, VMware Workstation, Parallels Desktop.

-----

## Comparación de Hipervisores: Tipo-1 vs. Tipo-2

| Dimensión Arquitectural | Tipo-1 (Bare-Metal) | Tipo-2 (Hospedado) |
| :--- | :--- | :--- |
| **Capa de Ejecución** | Directamente sobre el hardware físico | Sobre el SO Anfitrión |
| **Requisito de SO Anfitrión** | Ninguno (el hipervisor es el kernel) | SO de escritorio/servidor estándar obligatorio |
| **Sobrecarga de Rendimiento** | Mínima (< 2% de CPU) | Moderada (latencia del doble planificador y pila de E/S) |
| **Latencia de E/S** | Directa / Casi nativa | Mediada por los controladores del SO anfitrión |
| **Aislamiento de Fallos** | Alto (VMs independientes) | Vinculado a la estabilidad del SO anfitrión |
| **Casos de Uso Principales** | Centros de Datos, Nube (AWS, GCP) | Desarrollo de Software, Pruebas, Docencia |
| **Herramientas Representativas**| Proxmox VE, VMware ESXi, KVM | Oracle VirtualBox, VMware Workstation |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Emulación vs. Virtualización}}
\end{center}

-----

## Emulación: Definición y Casos de Uso

La **Emulación** recrea el comportamiento del hardware y del conjunto de instrucciones (ISA) de un sistema diferente íntegramente mediante software:

  * **Mecanismo:** Intérprete de software o Traductor Binario Dinámico (JIT). El emulador traduce en tiempo real cada instrucción del sistema huésped a instrucciones nativas de la CPU del anfitrión.
  * **Independencia Arquitectural:** El ISA huésped puede diferir por completo del ISA anfitrión (ej.: ejecutar código ARM64, PowerPC o x86-16 clásico en un anfitrión x86-64).
  * **Sobrecarga de Rendimiento:** Penalización computacional muy elevada (típicamente entre 5x y 20x más lento que la ejecución nativa).
  * **Casos de Uso en Ingeniería:**
      * Ejecución de sistemas operativos y software heredados (ej.: FreeDOS con emulación de tarjeta de sonido SoundBlaster en la Parte 2 del laboratorio).
      * Desarrollo cruzado para sistemas embebidos (ej.: QEMU para ARM o RISC-V).
      * Simulación de plataformas móviles (ej.: Android Virtual Device / AVD).

-----

## Emulación vs. Virtualización

| Dimensión | Emulación por Software | Virtualización Asistida por Hardware |
| :--- | :--- | :--- |
| **Conjunto de Instrucciones (ISA)** | Puede diferir (ej.: ARM en x86) | Idéntico (ej.: x86 en x86) |
| **Ejecución de Instrucciones** | Traducido instrucción a instrucción por software | Ejecutado directamente en el silicio de la CPU |
| **Rendimiento de CPU** | Muy lento (penalización de 5x a 20x) | Casi nativo (< 3% de sobrecarga) |
| **Rendimiento de E/S** | Muy lento (circuitos simulados en código) | Acelerado por controladores paravirtualizados (VirtIO) |
| **Flexibilidad** | Máxima (cualquier hardware simulable) | Restringida a la arquitectura física del procesador |
| **Ejemplo Práctico** | FreeDOS / DOOM (Parte 2 del laboratorio) | Alpine Linux / VirtualBox (Parte 3 del laboratorio) |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: E/S, Almacenamiento \& Redes Virtuales}}
\end{center}

-----

## Virtualización de E/S: Hardware Emulado vs. Marco VirtIO

Los dispositivos de entrada/salida (disco y red) constituyen el principal desafío de rendimiento en la virtualización:

  * **Hardware Emulado (Compatible, pero Lento):**
      * El hipervisor simula circuitos clásicos mediante software (ej.: tarjeta de red Intel E1000, controlador de disco IDE).
      * Permite que cualquier sistema operativo funcione sin controladores adicionales, pero cada lectura/escritura debe ser interceptada y procesada por software por el hipervisor.
      * Ocasiona alta latencia y sobrecarga bajo tráfico de red intenso o transferencias pesadas de disco.
  * **E/S Paravirtualizada con VirtIO (Cooperativa y Eficiente):**
      * El sistema operativo huésped utiliza controladores dedicados (**VirtIO**), siendo consciente de que se ejecuta en una máquina virtual.
      * Elimina la simulación de hardware: el huésped y el hipervisor intercambian datos directamente a través de colas de memoria compartida.
      * Agrupa peticiones por lotes con sobrecarga mínima, logrando un rendimiento casi nativo (el estándar en la nube y en QEMU con `-device virtio-net-pci`).

-----

## Acceso Directo a Hardware: Passthrough & IOMMU

El **Passthrough** otorga a una máquina virtual el control exclusivo y directo sobre un periférico físico (PCIe o USB) del anfitrión:

  * **Rendimiento Nativo:** El sistema operativo huésped interactúa directamente con el dispositivo real, eludiendo cualquier intermediación o retardo del hipervisor.
  * **El Papel de la IOMMU (Aislamiento de Seguridad):**
      * Componente de hardware en el procesador y placa base (Intel **VT-d**, AMD **AMD-Vi**).
      * **Aislamiento de Memoria:** Garantiza que el dispositivo físico acceda estrictamente a la memoria RAM asignada a esa máquina virtual, impidiendo que un dispositivo acceda a la memoria del anfitrión o de otras VMs.
  * **Casos de Uso en Ingeniería:**
      * **GPU Dedicada:** Aceleración gráfica y entrenamiento de modelos de Inteligencia Artificial / Machine Learning dentro de la VM.
      * **Periféricos USB:** Conexión directa de placas de desarrollo y microcontroladores (Arduino, ESP32) a la máquina virtual.

-----

## Almacenamiento Virtual: Arquitecturas de Discos Virtuales

Las máquinas virtuales almacenan datos persistentes en archivos de imagen de disco virtual que encapsulan los bloques del sistema de archivos huésped:

  * **Formato RAW:**
      * Réplica lineal sector a sector del disco físico.
      * Máximo rendimiento de lectura y escritura secuencial.
      * No admite de forma nativa instantáneas (snapshots), aprovisionamiento dinámico ni compresión interna.
  * **Formato QCOW2 (QEMU Copy-On-Write 2):**
      * Formato avanzado con soporte para asignación dinámica, compresión (zstd/zlib) y múltiples niveles de snapshots.
      * Implementa imágenes base (backing files): una imagen modelo de base puede ser compartida por varias VMs mediante capas diferenciales de escritura.
  * **Formatos VDI (VirtualBox) & VMDK (VMware):**
      * Formatos orientados a estaciones de trabajo con soporte para expansión dinámica e instantáneas puntuales.

-----

## Aprovisionamiento de Almacenamiento: Asignación Fija vs. Dinámica

Las imágenes de disco virtual admiten dos estrategias fundamentales de asignación de almacenamiento:

  * **Asignación Preasignada (Fija / Preallocated):**
      * El hipervisor reserva de inmediato la capacidad total especificada en el disco del anfitrión en el momento de creación (ej.: crea de inmediato un archivo de 20 GB).
      * Ventajas: Elimina la fragmentación en el sistema de archivos del anfitrión y garantiza latencias de escritura predecibles bajo cargas intensivas.
      * Desventaja: Desperdicia espacio de disco en el anfitrión mientras el sistema de archivos huésped permanezca vacío.
  * **Asignación Dinámica (Dispersa / Thin Provisioned):**
      * El archivo de disco virtual comienza con un tamaño reducido de metadatos y crece a medida que el SO huésped escribe nuevos bloques.
      * Ventajas: Maximiza la densidad de almacenamiento y permite sobreasignación (overcommit) de almacenamiento físico.
      * Desventaja: Ligera penalización de escritura al asignar nuevos bloques y riesgo de agotamiento de espacio si el disco del anfitrión se satura.

-----

## Red Virtual: Modo NAT & Redireccionamiento de Puertos

El hipervisor gestiona la conectividad de las máquinas virtuales con las redes externas:

  * **Modo NAT (Predeterminado):**
      * La máquina virtual comparte la conexión de red del ordenador anfitrión.
      * **Acceso a Internet:** El huésped accede a internet de forma transparente sin configuraciones adicionales (ej.: descarga de paquetes o navegación web).
      * **Aislamiento Entrante:** Los dispositivos externos en la red local no pueden iniciar conexiones directamente hacia la VM.
  * **Redireccionamiento de Puertos (Port Forwarding):**
      * Crea un canal de comunicación desde un puerto específico del anfitrión hacia un servicio dentro de la VM.
      * **Ejemplo Práctico:** Mapear `localhost:8006` en el anfitrión hacia el puerto `8006` de la VM permite acceder a la consola web de Proxmox en el navegador sin exponer la VM a la red física.

-----

## Red Virtual: Modo Bridge & Modo Host-Only

Topologías alternativas para despliegues de servidores o bancos de pruebas aislados:

  * **Modo Bridge (Puente de Red):**
      * La máquina virtual pasa a comportarse como un dispositivo físico independiente conectado al router local.
      * Obtiene su propia dirección IP en la red local (ej.: `192.168.1.x`), exactamente igual que un ordenador físico o un smartphone en la red.
      * **Ideal para Servidores:** Cualquier dispositivo en la red local puede acceder a los servicios de la VM (como se demuestra en la práctica del servidor web con Alpine).
  * **Modo Host-Only (Solo Anfitrión):**
      * Crea una red privada y aislada exclusivamente entre el anfitrión y sus máquinas virtuales.
      * Sin salida a internet ni acceso a la red local; idóneo para entornos de pruebas seguros y controlados.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Herramientas Prácticas de Virtualización}}
\end{center}

-----

## Oracle VirtualBox: Arquitectura & Flujo de Trabajo Desktop

Oracle VirtualBox proporciona una plataforma de virtualización Tipo-2 de nivel de producción optimizada para estaciones de trabajo:

  * **Componentes Principales:**
      * **Administrador Gráfico VirtualBox:** Interfaz de escritorio intuitiva para creación de VMs, gestión de instantáneas y configuración de medios virtuales.
      * **CLI VBoxManage:** Interfaz de línea de comandos programable que ofrece control total de todas las funcionalidades del hipervisor.
      * **VirtualBox Guest Additions:** Módulos de kernel instalados dentro del huésped para aceleración gráfica, integración fluida del cursor, redimensionamiento dinámico de pantalla, sincronización horaria y portapapeles bidireccional.
  * **Extension Pack:** Paquete complementario para soporte de controladores USB 2.0/3.0, passthrough de cámara web y cifrado RDP.

-----

## QEMU + KVM: Arquitectura & Integración con el Kernel

La combinación de QEMU + KVM constituye la columna vertebral de la virtualización de servidores Linux modernos y de la infraestructura en la nube:

  * **KVM (Kernel-based Virtual Machine):**
      * Módulo integrado en el kernel Linux (`kvm.ko`, `kvm-intel.ko` / `kvm-amd.ko`) que expone el dispositivo `/dev/kvm`.
      * Convierte el kernel Linux en un hipervisor Tipo-1, gestionando la planificación de CPU, paginación de memoria (EPT/NPT) y ejecución asistida por hardware.
  * **QEMU (Quick EMUlator):**
      * Proceso en espacio de usuario responsable de la emulación de dispositivos de E/S, buses, almacenamiento y renderizado de pantalla.
      * Al ejecutarse con la opción `-enable-kvm`, las instrucciones de CPU huésped se ejecutan directamente en el procesador físico mediante KVM, alcanzando rendimiento casi nativo.

-----

## Configuración y Permisos de QEMU/KVM

Configuración del entorno de virtualización KVM en distribuciones basadas en Debian/Ubuntu:

  * **1. Instalación de Paquetes del Hipervisor:**
    ```bash
    $ sudo apt update
    $ sudo apt install qemu-system-x86 kvm bridge-utils
    ```
  * **2. Permisos de Ejecución:** Añadir el usuario al grupo `kvm` para permitir el acceso directo a `/dev/kvm` sin privilegios de `root`:
    ```bash
    $ sudo usermod -aG kvm $USER
    ```

-----

## Gestión de Discos con `qemu-img`

Creación e inspección de imágenes de disco virtual desde la línea de comandos:

  * **Crear Imagen QCOW2 con Asignación Dinámica:**
    ```bash
    $ qemu-img create -f qcow2 disco_alpine.qcow2 8G
    ```
  * **Inspeccionar Formato y Ocupación Real:**
    ```bash
    $ qemu-img info disco_alpine.qcow2
    ```

-----

## Lanzamiento de una Máquina Virtual en QEMU

Comando completo para iniciar una VM combinando aceleración KVM, disco VirtIO y red:

```bash
$ qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -smp 4 \
    -cpu host \
    -drive file=disco_alpine.qcow2,if=virtio,format=qcow2 \
    -netdev user,id=net0,hostfwd=tcp::8080-:80 \
    -device virtio-net-pci,netdev=net0 \
    -display gtk
```

  * `-enable-kvm` & `-cpu host`: Activa la aceleración nativa por hardware mediante el módulo KVM del kernel.
  * `-m 4096` & `-smp 4`: Asigna 4 GB de memoria RAM y 4 núcleos virtuales de procesamiento.
  * `-drive if=virtio`: Disco virtual de alto rendimiento utilizando controladores VirtIO.
  * `-netdev ... -device virtio-net-pci`: Tarjeta de red VirtIO en modo NAT con reenvío del puerto `8080` (anfitrión) al puerto `80` (VM).
  * `-display gtk`: Abre la ventana gráfica para visualización e interacción con la consola del sistema huésped.

-----

## Proxmox Virtual Environment (VE)

**Proxmox VE** es una plataforma empresarial abierta para la gestión integral de virtualización en servidores:

  * **Arquitectura Subyacente:** Construido sobre Debian Linux, integrando KVM para virtualización asistida por hardware y LXC para contenedores de sistema.
  * **Interfaz de Gestión:** Consola web centralizada accesible por defecto en el puerto `8006` (`https://<ip-servidor>:8006`) con soporte completo de API REST.
  * **Almacenamiento y Redes:** Soporte nativo para almacenamiento empresarial (ZFS, Ceph, LVM-thin, NFS) y puentes de red Linux (`vmbr0`).
  * **Entornos de Laboratorio (Virtualización Anidada):** En estaciones de trabajo personales, puede ejecutarse dentro de otro hipervisor (VirtualBox o QEMU) mediante **virtualización anidada** (*nested virtualization*).

-----

## Ecosistema de Hipervisores: Matriz Comparativa

| Métrica de Evaluación | Oracle VirtualBox | QEMU + KVM | Proxmox VE |
| :--- | :--- | :--- | :--- |
| **Tipo de Hipervisor** | Tipo-2 (Hospedado) | Tipo-1 / Híbrido | Tipo-1 (Bare-Metal) |
| **Sistema Operativo Anfitrión**| Windows, macOS, Linux | Linux | Base Debian Dedicada |
| **Interfaz Primaria** | GUI de Escritorio | Línea de Comandos (CLI) | Portal Web Centralizado |
| **Sobrecarga de Rendimiento** | Moderada | Mínima (Casi nativa) | Mínima (Nivel de producción) |
| **Capacidad de Automatización**| VBoxManage (Buena) | Flags CLI / Libvirt (Amplia)| API REST / CLI / GUI (Total)|
| **Formatos de Almacenamiento** | VDI, VMDK | RAW, QCOW2 | ZFS, Ceph, QCOW2, LVM |
| **Público Objetivo** | Usuarios desktop, estudiantes| Desarrolladores kernel, sysadmins| Centros de datos, clústeres |

-----

## Referencias Técnicas Autorizadas

Documentación oficial y especificaciones arquitecturales para el estudio en ingeniería de sistemas:

  * **Kernel-based Virtual Machine (KVM):**
      * [Documentación de Virtualización del Kernel Linux](https://docs.kernel.org/virt/kvm/)
  * **Emulación de Sistemas con QEMU:**
      * [Manual de Usuario de Emulación de Sistemas QEMU](https://www.qemu.org/docs/master/system/index.html)
  * **Oracle VirtualBox:**
      * [Manual de Usuario de Oracle VirtualBox](https://www.virtualbox.org/manual/)
  * **Proxmox Virtual Environment:**
      * [Guía de Administración de Proxmox VE](https://pve.proxmox.com/pve-docs/)
  * **Especificación VirtIO:**
      * [Especificación Estándar VirtIO (OASIS)](https://docs.oasis-open.org/virtio/virtio/v1.2/virtio-v1.2.html)
