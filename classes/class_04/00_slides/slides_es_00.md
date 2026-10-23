---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Contenedores: Arquitectura, Docker & Docker Compose"
institute: Universidade de Aveiro
date: October 19, 2026
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

  * **Parte I — Fundamentos & Arquitectura de Aislamiento:** El problema de la portabilidad, virtualización de SO, namespaces, cgroups y ejecución fuera de Linux.
  * **Parte II — Del Kernel a las Herramientas: Ecosistema & OCI:** La evolución de LXC a Docker, estandarización OCI (`runc`, especificaciones abiertas) y Podman.
  * **Parte III — Imágenes, Almacenamiento & Redes:** Terminología, etiquetas, ciclo de vida, capas (Copy-on-Write), volúmenes y redes con resolución DNS.
  * **Parte IV — Docker en la Práctica & Anatomía del `Dockerfile`:** Comandos CLI esenciales, instrucciones, formatos exec/shell y `CMD` vs. `ENTRYPOINT`.
  * **Parte V — Orquestación Local con Docker Compose:** Sintaxis de `compose.yml`, comandos de gestión y patrones arquitecturales multi-servicio.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos \& Arquitectura}}
\end{center}

-----

## El Desafío de la Portabilidad de Software

La heterogeneidad de configuraciones entre entornos de desarrollo, pruebas y producción constituye un desafío central en la ingeniería de software:

  * **Entorno de Desarrollo:**
      * Configuración local con versiones específicas de intérpretes (ej.: Python 3.11), bibliotecas dinámicas y variables de entorno locales.
  * **Entorno de Pruebas o Producción:**
      * Sistemas operativos con diferentes versiones de bibliotecas compartidas del sistema o políticas restrictivas de seguridad.
      * Riesgo de fallos en tiempo de ejecución por incompatibilidad de dependencias (*dependency hell*).

\vspace{1em}

\begin{center}
\textbf{Resulta fundamental encapsular la aplicación y todas sus dependencias en un artefacto estandarizado, garantizando una ejecución determinista y reproducible.}
\end{center}

-----

## ¿Las Máquinas Virtuales como Solución?

El aislamiento proporcionado por las Máquinas Virtuales conlleva costes elevados para la ejecución de aplicaciones:

  * **Propiedades de la Virtualización de Hardware:**
      * Aislamiento integral a nivel de hardware mediante un hipervisor.
      * Kernel y sistema operativo dedicados por cada máquina virtual.
  * **Limitaciones en el Ámbito Aplicativo:**
      * **Sobrecarga:** Asignación estática de gigabytes de RAM y disco por instancia.
      * **Redundancia:** Duplicación de sistemas operativos completos para ejecutar un único servicio.
      * **Latencia:** Arranque lento (minutos), lo que limita el escalado dinámico.

\vspace{1em}

\begin{center}
\textbf{La virtualización a nivel de hardware resulta desproporcionada para aislar y distribuir aplicaciones individuales.}
\end{center}

-----

## La Solución: Contenedores

La respuesta reside en la **virtualización a nivel de sistema operativo**:

  * **Concepto de Contenedor:** Unidad estandarizada que empaqueta la aplicación y todas sus dependencias.
  * **Cambio de Paradigma:**
      * Comparte el **kernel del anfitrión**, sin virtualizar hardware subyacente.
      * El aislamiento de los procesos lo garantiza **el propio kernel** (mediante *namespaces* y *cgroups*).
  * **Portabilidad Determinista:** Ejecución idéntica en estaciones de desarrollo, entornos de integración continua o infraestructuras en la nube.

\vspace{1em}

\begin{center}
\textbf{El contenedor marítimo desacopló las mercancías de los vehículos de transporte (barco, tren, camión). El contenedor de software desacopla la aplicación del sistema operativo anfitrión.}
\end{center}

-----

## Arquitectura Comparada: VMs vs. Contenedores

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{vm_vs_container_architecture.png}
\end{center}

-----

## Comparación Sistemática: VMs vs. Contenedores

| Dimensión Técnica | Máquinas Virtuales (VMs) | Contenedores |
| :--- | :--- | :--- |
| **Nivel de Abstracción** | **Virtualización de Hardware** | **Virtualización de SO** (Procesos) |
| **Kernel del Sistema** | Kernel invitado dedicado por VM | **Kernel del anfitrión compartido** |
| **Consumo de Memoria (RAM)** | Elevado (memoria estática asignada al SO) | **Mínimo** (solo lo que consume la app) |
| **Tamaño de la Imagen** | Gigabytes (GB) | Megabytes (MB) |
| **Tiempo de Inicialización** | Decenas de segundos a minutos | **Milisegundos a segundos** |
| **Sobrecarga de Rendimiento** | Baja a moderada (latencia del hipervisor) | **Casi nativa** (sin intermediación de hardware) |
| **Frontera de Aislamiento** | Muy fuerte (hardware / anillos CPU) | Fuerte (mecanismos de aislamiento en kernel) |
| **Caso de Uso Típico** | Entornos multi-OS, aislamiento estricto | Backends, Microservicios, APIs, Kubernetes |

-----

## Mecanismos del Kernel: Namespaces de Linux

Los **Namespaces de Linux** delimitan el perímetro de visibilidad de los recursos del sistema operativo (lo que el proceso puede **ver**):

  * **PID (Process ID):** Aísla la tabla de procesos (la aplicación opera como **PID 1** dentro del contenedor).
  * **NET (Network):** Interfaces virtuales propias (`eth0`), tablas de enrutamiento y espacio de puertos independiente.
  * **MNT (Mount):** Puntos de montaje aislados con un directorio raíz (`/`) dedicado.
  * **UTS (Hostnames):** Asignación de nombre de máquina (*hostname*) y dominio propios.
  * **USER:** Mapeo de usuarios (ej.: `root` en el contenedor sin privilegios administrativos en el anfitrión).
  * **IPC (Inter-Process Communication):** Aislamiento de memoria compartida y colas de mensajes entre procesos.

-----

## Aislamiento en Acción: Mapeo de Namespaces

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{linux_namespaces_isolation.png}
\end{center}

-----

## Mecanismos del Kernel: Control Groups (cgroups)

Los **Control Groups (cgroups)** permiten al kernel imponer límites estrictos de hardware a cada contenedor:

  * **CPU:** Limita la cuota de tiempo de procesador o el número de núcleos dedicados (ej.: máximo de 1.5 vCPUs).
  * **Memoria RAM:** Impone un techo máximo de memoria (ej.: 512 MB). Si se sobrepasa, el kernel finaliza el proceso (*Out Of Memory Killer - OOM*).
  * **E/S de Almacenamiento (Block I/O):** Evita que un contenedor monopolice el ancho de banda del disco con operaciones masivas de lectura/escritura.
  * **Control de PIDs (pids cgroup):** Limita el número de procesos hijos para proteger al anfitrión frente a *fork bombs*.

\vspace{1em}

\begin{center}
\textbf{Mientras que los \textit{namespaces} definen el perímetro de visibilidad y aislamiento lógico, los \textit{cgroups} imponen cuotas cuantitativas y garantías de asignación (\textit{fair-share}) sobre los recursos computacionales.}
\end{center}

-----

## Contenedores Linux Fuera de Linux: macOS y Windows

Al depender del kernel Linux (*namespaces* y *cgroups*), ejecutar **contenedores Linux** en macOS o Windows requiere una máquina virtual de soporte ligera (gestionada por herramientas como **Docker Desktop** o **Podman**):

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{docker_desktop_architecture.png}
\end{center}

-----

## Contenedores Linux Fuera de Linux: macOS y Windows

  * **En Linux (Ejecución Nativa):**
      * Ejecución directa sobre el kernel del anfitrión con rendimiento nativo.
      * Sin hipervisores ni sobrecarga de virtualización.
  * **En macOS y Windows (Docker Desktop, Podman, etc.):**
      * Los kernels anfitriones (Darwin / NT) no ejecutan binarios Linux de forma nativa.
      * Las herramientas ejecutan una **micro-VM Linux** (*Virtualization.framework* / *WSL2*) compartida por los contenedores.
      * *(Nota: Windows admite contenedores Windows nativos, pero la práctica totalidad del ecosistema utiliza imágenes Linux).*
  * **Impacto Operativo:**
      * Asignación fija de memoria RAM y CPU reservadas para la máquina virtual de soporte.
      * Mayor latencia de E/S en carpetas compartidas (*bind mounts*) a través de los límites de la VM.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Del Kernel a las Herramientas: Ecosistema \& OCI}}
\end{center}

-----

## La Evolución: Linux Containers (LXC) vs. Docker

La tecnología de contenedores no nació con Docker:

  * **LXC (Linux Containers, 2008):**
      * La primera solución integral que unificó cgroups y namespaces en el kernel Linux.
      * Orientado a **contenedores de sistema**: operan como VMs ligeras ejecutando un sistema `init` completo (systemd), múltiples procesos y servicios en segundo plano.
  * **La Revolución de Docker (2013):**
      * Docker utilizó inicialmente LXC como motor subyacente, añadiendo una capa de abstracción superior.
      * Popularizó el concepto de **contenedores de servicio / microservicio**: cada contenedor ejecuta **un único proceso principal**.
      * Introdujo el formato de imágenes en capas (`Dockerfile`) y el registro global compartido (Docker Hub), transformando el desarrollo de software moderno.

-----

## Normalización y Estándares Abiertos: La OCI

Para evitar la dependencia de una única empresa proveedora, la industria constituyó la **Open Container Initiative (OCI)**:

  * **Especificación de Imagen (Image Spec):**
      * Define el formato binario exacto de las capas y manifiestos de las imágenes.
      * Una imagen construida por Docker cumple la especificación OCI y puede ejecutarse sin cambios en Podman, containerd, CRI-O o Kubernetes.
  * **Especificación de Ejecución (Runtime Spec):**
      * Define la interfaz con el kernel para crear y gestionar contenedores.
      * La implementación de referencia abierta es **`runc`**, utilizada universalmente tanto por Docker como por Podman.

-----

## Podman y la Seguridad de Contenedores

**Podman** (desarrollado por Red Hat) surgió como respuesta moderna a los desafíos de seguridad y arquitectura de Docker tradicional:

  * **Arquitectura sin Demonio (*Daemonless*):**
      * Docker depende de un demonio central (`dockerd`) siempre activo como `root`. Si el demonio falla, la gestión de todos los contenedores se ve comprometida.
      * Podman no tiene demonio central: cada contenedor es un proceso hijo directo del usuario que lo invoca.
  * **Ejecución sin Privilegios (*Rootless by Design*):**
      * Permite a usuarios sin permisos de administración (sin `sudo`) descargar, construir y ejecutar contenedores en Linux mediante *User Namespaces*.
  * **Compatibilidad Total de Línea de Comandos:**
      * La sintaxis de comandos es 100% idéntica:
        ```bash
        $ alias docker=podman
        $ docker run -d -p 8080:80 nginx:alpine
        ```

\vspace{1em}

\begin{center}
\textbf{Ambas herramientas comparten los mismos comandos y normas OCI; dominar la interfaz Docker confiere competencias universales para todo el ecosistema de contenedores.}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Imágenes, Almacenamiento \& Redes}}
\end{center}

-----

## Terminología Fundamental: Imagen vs. Contenedor

Tres conceptos esenciales definen el modelo de contenedores:

  * **1. Imagen de Contenedor (Image):**
      * Plantilla estática e inmutable (*read-only*) que contiene el sistema de archivos, binarios, bibliotecas y metadatos.
      * **Analogía:** Equivale a una **Clase** (definición estática).
  * **2. Contenedor (Container):**
      * Instancia viva y en ejecución de una imagen, aislada por el kernel.
      * **Analogía:** Equivale a un **Objeto** (múltiples instancias pueden derivarse de la misma imagen).
  * **3. Registro (Registry):**
      * Servicio centralizado para almacenar, versionar y distribuir imágenes (ej.: Docker Hub, GitHub Packages).

-----

## El Ciclo de Vida de Docker

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{docker_lifecycle.png}
\end{center}

-----

## Identificación y Nomenclatura de Imágenes

Las imágenes se identifican siguiendo una sintaxis estandarizada:

$$\texttt{[registro/][repositorio/]nombre\textbf{:}tag}$$

  * **Repositorio Oficial:** Las imágenes oficiales de Docker Hub omiten el registro y usuario (ej.: `nginx`, `alpine`, `ubuntu`).
  * **Función del Tag (Etiqueta):** Especifica la versión o variante; por omisión adopta `:latest`.
  * **Ejemplos:**
      * `nginx:alpine` $\rightarrow$ NGINX sobre la distribución minimalista Alpine Linux (~20 MB).
      * `python:3.11-slim` $\rightarrow$ Python 3.11 sin herramientas pesadas de compilación.
      * `lscr.io/linuxserver/jellyfin:latest` $\rightarrow$ Imagen procedente de un registro externo (`lscr.io`).
  * **Digest (SHA-256):** Hash criptográfico único que garantiza la integridad e inmutabilidad exacta de la imagen.

-----

## La Anatomía de la Imagen: Capas & Copy-on-Write (CoW)

Una imagen Docker no es un archivo monolítico, sino una **pila de capas inmutables de solo lectura**:

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{container_layers_cow.png}
\end{center}

-----

## Mecanismo Copy-on-Write (CoW): Eficiencia e Inmutabilidad

  * **Compartición de Capas en Disco:**
      * Las capas base comunes (ej.: `alpine:3.20`) se almacenan en disco **una única vez**.
      * Ahorro sustancial de ancho de banda de red y capacidad de almacenamiento.
  * **Inmutabilidad de las Capas (*Read-Only*):**
      * La imagen base nunca se modifica ni se corrompe por la ejecución de los contenedores.
  * **Capa de Escritura del Contenedor (*Read-Write Layer*):**
      * Capa temporal creada en la cima de la pila al iniciar el contenedor.
      * **Lectura:** Los archivos se leen directamente de las capas compartidas inferiores.
      * **Modificación (CoW):** Al modificar un archivo existente, este se copia a la capa R/W antes de editarse.
      * **Destrucción:** Al eliminar el contenedor, solo esta capa volátil de escritura es destruida.

-----

## Persistencia de Datos: Tipos de Almacenamiento

Por omisión, el sistema de archivos de un contenedor es **efímero**. Para gestionar datos, Docker ofrece tres mecanismos:

  * **1. Capa de Escritura (Writable Layer):**
      * **Ciclo de Vida:** Efímera; se elimina definitivamente cuando el contenedor es destruido.
      * **Uso Típico:** Archivos de trabajo temporales y servicios *stateless* (sin estado).
  * **2. Montajes Locales (*Bind Mounts*):**
      * **Mecanismo:** Monta una carpeta del anfitrión directamente en el contenedor (`anfitrión:contenedor`).
      * **Uso Típico:** **Desarrollo local** (los cambios en el código se reflejan en vivo sin reconstruir la imagen).
  * **3. Volúmenes Gestionados (*Named Volumes*):**
      * **Mecanismo:** Espacio de almacenamiento gestionado por el motor en una zona dedicada del sistema.
      * **Uso Típico:** **Persistencia en producción** (bases de datos, alto rendimiento de E/S y supervivencia a la eliminación de contenedores).

-----

## Redes Virtuales: Modo Bridge y Mapeo de Puertos

Por defecto, cada contenedor se conecta a una red virtual privada en modo puente (*Bridge Network*):

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{docker_network_ports_dns.png}
\end{center}

-----

## Redes en Contenedores: Aislamiento y Resolución DNS

  * **Red Virtual Privada (*Bridge Network*):**
      * Aísla los contenedores de la red exterior mediante interfaces *bridge* y reglas de NAT en el kernel.
      * Cada contenedor recibe una dirección IP privada interna dinámica (ej.: `172.20.0.x`).
  * **Mapeo de Puertos (`-p <puerto_anfitrión>:<puerto_contenedor>`):**
      * Redirige el tráfico recibido en un puerto del anfitrión al puerto interno del contenedor (ej.: `-p 8080:80`).
      * Permite acceder al servicio desde el exterior mediante `http://localhost:8080`.
  * **Resolución por DNS Integrado:**
      * Los contenedores en la misma red privada se comunican directamente mediante el **nombre del servicio** (ej.: `postgres://db:5432`).
      * Desacoplamiento total respecto a direcciones IP dinámicas y efímeras.
  * **Aislamiento de Seguridad:**
      * Los servicios internos (ej.: base de datos `db`) operan sin exponer puertos al anfitrión.
      * Totalmente invisibles y protegidos de accesos directos desde la red externa o Internet.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Docker en la Práctica \& Anatomía del Dockerfile}}
\end{center}

-----

## Comandos Esenciales de Docker

La herramienta de línea de comandos `docker` controla el ciclo de vida completo de los contenedores:

| Comando | Descripción |
| :--- | :--- |
| `docker run [opciones] <imagen>` | Crea e inicia un nuevo contenedor a partir de una imagen. |
| `docker run -d -p 8080:80 <imagen>` | Ejecuta en segundo plano (*detached*) mapeando el puerto 8080. |
| `docker ps` | Lista los contenedores actualmente en ejecución. |
| `docker ps -a` | Lista todos los contenedores (incluyendo los detenidos/finalizados). |
| `docker stop <id/nombre>` | Envía señal `SIGTERM` para detener el contenedor de forma ordenada. |
| `docker rm <id/nombre>` | Elimina definitivamente un contenedor detenido y su capa R/W. |
| `docker logs -f <id/nombre>` | Inspecciona y monitoriza los registros de salida estándar (`stdout`/`stderr`). |
| `docker exec -it <nombre> sh` | Abre una sesión de terminal interactiva dentro de un contenedor en ejecución. |
| `docker images` | Lista todas las imágenes almacenadas localmente en disco. |
| `docker rmi <imagen>` | Elimina una imagen local del almacenamiento. |

-----

## Visión Global: Ejemplo de un `Dockerfile`

Un `Dockerfile` define la receta declarativa y automatizada para construir una imagen:

```dockerfile
# 1. Imagen base de partida
FROM python:3.11-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copia de archivos e instalación de dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 4. Metadatos de red y comando de inicio
EXPOSE 8080
CMD ["python", "app.py"]
```

```bash
$ docker build -t mi-app:1.0 .              # Construye la imagen localmente (.)
$ docker run -d -p 8080:8080 mi-app:1.0     # Ejecuta el contenedor
```

-----

## Anatomía del `Dockerfile`: Instrucciones de Estructura

Con el ejemplo en mente, analicemos las instrucciones responsables del sistema de archivos:

  * `FROM <imagen>:<tag>`
      * Especifica la imagen base a partir de la cual se deriva la nueva imagen (ej.: `alpine:3.20`).
  * `WORKDIR <ruta>`
      * Define el directorio de trabajo para las instrucciones siguientes (crea la carpeta si no existe).
  * `COPY <origen> <destino>`
      * Copia archivos y directorios desde el contexto del anfitrión al sistema de archivos de la imagen.
  * `RUN <comando>`
      * Ejecuta comandos durante la construcción y consolida el resultado en una nueva capa inmutable (ej.: `RUN apk add --no-cache curl`).

-----

## Anatomía del `Dockerfile`: Entorno, Puertos & Seguridad

  * `ENV <clave>=<valor>`
      * Define variables de entorno persistentes durante toda la ejecución del contenedor (ej.: `ENV PORT=8080`).
  * `ARG <nombre>=<valor>`
      * Define variables temporales utilizadas exclusivamente durante la compilación de la imagen.
  * `EXPOSE <puerto>`
      * **Metadatos de documentación**: indica los puertos en los que escucha la aplicación (no publica en el anfitrión).
  * `USER <usuario>`
      * Establece el usuario o UID para los procesos siguientes, evitando la ejecución con privilegios de `root`.

-----

## Anatomía del `Dockerfile`: Ejecución (`CMD` & `ENTRYPOINT`)

Para definir el proceso que se inicia al arrancar el contenedor, Docker ofrece dos instrucciones clave:

  * `CMD ["ejecutable", "arg1", ...]`
      * Define el comando y/o argumentos **por omisión** a ejecutar en el arranque.
      * Si se proporcionan argumentos adicionales en `docker run`, toda la instrucción `CMD` se reemplaza.
  * `ENTRYPOINT ["ejecutable", "arg1", ...]`
      * Configura el contenedor para operar como un **ejecutable dedicado y fijo**.
      * Los argumentos proporcionados en `docker run` se añaden como parámetros al ejecutable.

-----

## `CMD` vs. `ENTRYPOINT` en la Práctica: Demostración

Considere dos escenarios representativos construidos sobre Alpine Linux:

**Escenario A: Solo `CMD` (Comando flexible por omisión)**
```dockerfile
FROM alpine:3.20
CMD ["echo", "Mensaje por defecto"]
```
```bash
$ docker run demo-cmd              # Imprime: "Mensaje por defecto"
$ docker run demo-cmd uname -a     # Ejecuta uname -a; sustituye el comando CMD original
```

**Escenario B: `ENTRYPOINT` con `CMD` (Ejecutable fijo + Argumento flexible)**
```dockerfile
FROM alpine:3.20
ENTRYPOINT ["echo", "Entorno:"]
CMD ["Produccion"]
```
```bash
$ docker run demo-ep               # Imprime: "Entorno: Produccion"
$ docker run demo-ep Pruebas       # Imprime: "Entorno: Pruebas" (sustituye el CMD)
```

-----

## El Contexto de Construcción (*Build Context*) y el `.dockerignore`

Al ejecutar el comando de compilación de la imagen:

```bash
$ docker build -t mi-servicio:1.0 .
```

  * **Significado del Argumento de Ruta (`.`):**
      * Define la raíz del **Contexto de Construcción** (*Build Context*).
      * El cliente Docker empaqueta el contenido íntegro de ese directorio y lo transmite al Docker Daemon antes de procesar las instrucciones.
  * **El Archivo `.dockerignore`:**
      * Presenta una semántica análoga a `.gitignore`.
      * Evita que directorios pesados o archivos sensibles se transmitan al demonio:
        ```text
        .git
        node_modules
        .env
        *.log
        ```
      * Reduce la latencia de transferencia al demonio e impide la inclusión accidental de credenciales, claves criptográficas o dependencias locales en las capas de la imagen.

-----

## Ejemplo Integrador: Construcción e Inspección de un Servicio

Considere un `Dockerfile` que compila un servicio de diagnóstico ejecutado bajo un usuario sin privilegios administrativos:

```dockerfile
FROM alpine:3.20
WORKDIR /app
RUN adduser -D -u 1000 appuser
USER appuser
CMD ["sh", "-c", "while true; do echo \"[LOG] Servicio activo en $(date)\"; sleep 5; done"]
```

**Secuencia de Validación en la Terminal:**

```bash
# 1. Compilar la imagen asignando una etiqueta formal
$ docker build -t logging-service:1.0 .

# 2. Iniciar el contenedor en segundo plano
$ docker run -d --name logger logging-service:1.0

# 3. Inspeccionar el entorno de ejecución
$ docker exec -it logger whoami        # Confirma la ejecucion bajo appuser (no-root)
$ docker logs --tail 3 logger          # Consulta las entradas recientes de log
$ docker stop logger && docker rm logger
```

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte V: Orquestación Local con Docker Compose}}
\end{center}

-----

## Motivación y Alcance de Docker Compose

En la arquitectura de sistemas reales, las soluciones rara vez operan como un único contenedor aislado:

  * Una aplicación web típica requiere un servidor web (NGINX), un servidor de aplicaciones (Python/Node) y una base de datos (PostgreSQL).
  * Iniciar esta arquitectura manualmente mediante comandos `docker run` exige:
      * Crear redes privadas manualmente (`docker network create`).
      * Iniciar cada contenedor individualmente con decenas de parámetros de puertos, volúmenes y variables de entorno.
      * Asegurar el orden correcto de inicialización.
  * **Docker Compose:**
      * Es una herramienta declarativa que define y gestiona aplicaciones multi-contenedor mediante un único archivo: `compose.yml`.
      * Toda la infraestructura de la aplicación se describe en código (*Infrastructure as Code*) y se versiona en el repositorio Git del proyecto.

-----

## Anatomía del Archivo `compose.yml`

Un archivo `compose.yml` organiza la topología de los servicios de la aplicación:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"                  # anfitrión:contenedor
    volumes:
      - ./site:/usr/share/nginx/html
    environment:
      - TZ=Europe/Lisbon           # Zona horaria
    restart: unless-stopped        # Politica de recuperacion ante fallos

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secreto  # Variable de inicializacion
    volumes:
      - datos_db:/var/lib/postgresql/data

volumes:
  datos_db:                        # Volumen gestionado por Docker
```

-----

## Comandos de Docker Compose

La orquestación del conjunto de servicios se gestiona de manera centralizada desde el directorio donde reside `compose.yml`:

| Comando | Acción Ejecutada |
| :--- | :--- |
| `docker compose up -d` | Descarga imágenes, crea redes, volúmenes e inicia todos los servicios en segundo plano. |
| `docker compose up --build -d` | Fuerza la reconstrucción de imágenes locales (`build:`) antes de iniciar. |
| `docker compose ps` | Lista el estado y los puertos de todos los servicios de la aplicación. |
| `docker compose logs -f` | Monitoriza la salida combinada de registros de todos los servicios en tiempo real. |
| `docker compose logs -f <servicio>` | Filtra los registros de un único servicio (ej.: `docker compose logs -f web`). |
| `docker compose stop` | Detiene los servicios sin eliminar contenedores ni redes. |
| `docker compose down` | Detiene y elimina contenedores y redes virtuales creadas por Compose. |
| `docker compose down -v` | Detiene los servicios y elimina adicionalmente los volúmenes gestionados persistentes. |

-----

## Patrón Compose 1: Empaquetado de Imagen Personalizada

```yaml
services:
  webserver:
    build: .             # Ubicacion del Dockerfile en el contexto local
    ports:
      - "8080:80"        # Mapeo del puerto 8080 del anfitrion
```

  * **Concepto:** El código fuente se integra en las capas de la imagen durante el proceso de compilación.
  * **Comportamiento:** El contenedor resultante constituye un artefacto autónomo e inmutable, idóneo para validación y despliegue.
  * **Actualización:** Cualquier modificación en el código fuente requiere la recompilación explícita de la imagen (`docker compose up --build -d`).

-----

## Patrón Compose 2: Desarrollo Dinámico con Volúmenes

```yaml
services:
  webserver:
    image: nginx:alpine                  # Imagen oficial de catalogo
    ports:
      - "8080:80"
    volumes:
      - ./my-website:/usr/share/nginx/html # Mapeo dinamico de carpeta local
```

  * **Concepto:** Prescinde de la creación de un `Dockerfile` dedicado, reutilizando directamente la imagen oficial de NGINX.
  * **Montaje Directo:** El directorio local `./my-website` se monta sobre la raíz documental del servidor web.
  * **Ciclo Rápido de Pruebas:** Los cambios realizados en el código fuente en el anfitrión se reflejan al instante en el navegador sin recrear contenedores.

-----

## Patrón Compose 3: Aplicación Multi-Servicio (Web + Base de Datos)

```yaml
services:
  web:
    build: .
    ports:
      - "8080:80"                        # Puerto publico expuesto al anfitrion
    depends_on:
      - db                               # Inicia despues de la base de datos
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secreto
    volumes:
      - datos_db:/var/lib/postgresql/data # Sin puertos expuestos al anfitrion
volumes:
  datos_db:                              # Volumen de persistencia gestionado
```

  * **Comunicación por Nombre:** El servicio `web` accede a `postgres://db:5432`, resuelto automáticamente por el DNS interno.
  * **Aislamiento de Seguridad:** Solo `web` expone un puerto público (`:8080`); la base de datos permanece resguardada en la red interna.
  * **Persistencia con Volumen:** Los datos se graban en `datos_db`, sobreviviendo a paradas y reinicios (`docker compose down`).

-----

## Referencias Técnicas Autorizadas

Documentación oficial y especificaciones técnicas para profundizar en ingeniería de sistemas y computación en la nube:

  * **Docker Documentation:**
      * [Guía Oficial y Referencia de Arquitectura de Docker](https://docs.docker.com/)
      * [Referencia de Dockerfile](https://docs.docker.com/reference/dockerfile/)
      * [Especificación de Compose File (Compose Specification)](https://docs.docker.com/compose/compose-file/)
  * **Open Container Initiative (OCI):**
      * [Especificaciones Oficiales OCI Image y Runtime](https://opencontainers.org/)
  * **Podman Documentation:**
      * [Guía de Uso y Arquitectura de Podman](https://docs.podman.io/)
  * **Documentación del Kernel Linux:**
      * [Namespaces de Linux (`namespaces(7)`)](https://man7.org/linux/man-pages/man7/namespaces.7.html)
      * [Control Groups de Linux (`cgroups(7)`)](https://man7.org/linux/man-pages/man7/cgroups.7.html)
