---
title: Contenedores
subtitle: Introducción a la Ingeniería Informática
institute: Universidade de Aveiro
date: October 19, 2026
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

# Guía Práctica de Laboratorio

**Contexto & Objetivos:**  
En la ingeniería de software contemporánea, los contenedores Docker constituyen el estándar de la industria para empaquetar y gestionar **aplicaciones backend, APIs web, bases de datos y arquitecturas orientadas a microservicios**, sirviendo como base directa para la orquestación a escala en la nube (como clústeres de Kubernetes). En esta sesión práctica de laboratorio de **3 horas**, explorará el ciclo de vida de los contenedores, transformará código de aplicación en servicios autónomos y orquestará topologías multi-capa mediante Docker y Docker Compose:

* **Parte 1 — Instalación & Configuración de Docker:** Configuración del repositorio oficial de Docker y permisos de ejecución sin privilegios de root.
* **Parte 2 — Ejercicio 1: Fundamentos de la CLI de Docker & Construcción Manual de Imágenes:** Exploración del ciclo de vida de contenedores (`run`, `ps`, `logs`, `exec`, `stop`, `rm`), registro local vs. remoto y compilación manual de imágenes mediante `Dockerfile` y `docker build`.
* **Parte 3 — Ejercicio 2: "Hello, World" con Docker Compose:** Estructura fundamental de un archivo `compose.yml` y ciclo de vida automatizado de contenedores.
* **Parte 4 — Ejercicio 3: Construcción de Imágenes Personalizadas con Compose:** Creación de un `Dockerfile` integrado con Compose para empaquetar una aplicación web NGINX.
* **Parte 5 — Ejercicio 4: Desarrollo en Tiempo Real con Volúmenes:** Montaje dinámico en vivo (*bind mounts*) de archivos locales del anfitrión en contenedores sin reconstrucción de imágenes.
* **Parte 6 — Ejercicio 5: Arquitectura Multi-Servicio con Varnish Cache & NGINX:** Orquestación de múltiples servicios, red interna con resolución DNS de Docker y almacenamiento en caché de alto rendimiento con proxy inverso.
* **Parte 7 — Ejercicio 6: Despliegue de Aplicaciones del Mundo Real:** Despliegue autónomo de servicios de producción (ej.: Jellyfin) configurando variables de entorno (`PUID`, `PGID`, `TZ`), volúmenes persistentes y mapeo de puertos.

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Antes de comenzar los ejercicios, cree y acceda a la carpeta de trabajo dedicada para esta sesión:

```bash
$ mkdir -p ~/IEI/clase04
$ cd ~/IEI/clase04
```

Todos los archivos creados durante la clase (archivos `compose.yml`, `Dockerfile`, páginas web y configuraciones) deberán organizarse en subcarpetas dentro de este directorio de trabajo.

> **Nota sobre rutas de archivos:**
> Los comandos de esta guía asumen que el terminal se encuentra en el directorio de trabajo `~/IEI/clase04`. Cada ejercicio debe desarrollarse en su respectiva subcarpeta (ej.: `ex1-cli`, `ex2-helloworld`, `ex3-build`, etc.).

-----

## Parte 1: Instalación y Configuración de Docker

Si está utilizando un anfitrión Linux (Debian o Ubuntu), siga estos pasos en su terminal para instalar la versión más reciente de Docker Engine y del plugin Docker Compose, de acuerdo con las [instrucciones oficiales](https://docs.docker.com/engine/install/debian/). *(En Windows o macOS, instale [Docker Desktop](https://docs.docker.com/desktop/)).*

1.  **Configurar el repositorio `apt` de Docker:**
    ```bash
    # Eliminar paquetes no oficiales de docker
    sudo apt remove docker.io docker-doc \
    docker-compose podman-docker containerd runc

    # Actualizar el índice de paquetes e instalar prerrequisitos
    sudo apt update
    sudo apt install ca-certificates curl

    # Añadir la clave GPG oficial de Docker
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg \
    -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Añadir el repositorio a las fuentes de Apt:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
      https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    ```
2.  **Instalar los paquetes de Docker:**
    ```bash
    sudo apt install docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
    ```
3.  **Gestionar Docker como usuario no-root (Recomendado):**
    Para ejecutar comandos `docker` sin `sudo`, añada su usuario al grupo `docker`.
    ```bash
    sudo usermod -aG docker $USER
    ```
    **Importante:** Debe cerrar sesión y volver a iniciarla para que este cambio surta efecto.

-----

## Ejercicio 1: Fundamentos de la CLI de Docker y Construcción Manual de Imágenes

**Objetivo:** Practicar los comandos esenciales de la CLI de Docker (`run`, `ps`, `logs`, `exec`, `stop`, `rm`, `build`), comprender la distinción entre registro local y remoto (Docker Hub), y crear manualmente la primera imagen personalizada a partir de un `Dockerfile`.

1.  **Explorar el Registro Local y Descargar Imágenes (`docker images` y `docker pull`):**
    * Cree una carpeta para este ejercicio y acceda a ella:
      ```bash
      $ mkdir -p ex1-cli && cd ex1-cli
      ```
    * Inspeccione las imágenes almacenadas localmente en su máquina:
      ```bash
      $ docker images
      ```
      *(Si la instalación es reciente, la lista estará vacía).*
    * Descargue la imagen oficial de la distribución minimalista **Alpine Linux** directamente desde Docker Hub (el registro público oficial):
      ```bash
      $ docker pull alpine:3.20
      ```
    * Vuelva a listar las imágenes locales (`docker images`) y compruebe que `alpine:3.20` está ahora en disco (¡observe su tamaño ultraligero de apenas ~8 MB!).

2.  **Ejecutar un Contenedor Interactivo y Comprender el Ciclo de Vida (`run -it`, `ps`, `ps -a` y `rm`):**
    * Cree e inicie un contenedor interactivo con una sesión de terminal (`sh`):
      ```bash
      $ docker run -it --name mi-terminal alpine:3.20 sh
      ```
    * Observe cómo el indicador de línea de comandos cambia a `/ #`. ¡Ahora está ejecutando comandos dentro del espacio de procesos y sistema de archivos aislado del contenedor! Pruebe:
      ```sh
      / # cat /etc/os-release   # Inspeccionar la distribución del contenedor
      / # hostname              # Ver el identificador único asignado al contenedor
      / # exit                  # Finalizar la sesión y salir del contenedor
      ```
    * De vuelta en el terminal del anfitrión, verifique qué contenedores están en ejecución:
      ```bash
      $ docker ps
      ```
      *(El contenedor no aparece listado porque su proceso principal `sh` ha finalizado).*
    * Liste **todos** los contenedores (incluyendo los detenidos/finalizados):
      ```bash
      $ docker ps -a
      ```
      Constatará que el contenedor `mi-terminal` todavía existe en disco en estado `Exited (0)`.
    * Elimine definitivamente el contenedor y su capa temporal de escritura:
      ```bash
      $ docker rm mi-terminal
      ```

3.  **Servicio en Segundo Plano, Redirección de Puertos y Registros (`run -d -p`, `logs` y `exec`):**
    * Inicie un servidor web NGINX en segundo plano (*detached*, flag `-d`) mapeando el puerto 8080 del anfitrión al puerto 80 del contenedor (flag `-p`):
      ```bash
      $ docker run -d --name mi-servidor -p 8080:80 nginx:alpine
      ```
      *(Como la imagen `nginx:alpine` no existía localmente, Docker realizó el `pull` automático antes de arrancar).*
    * Confirme que el contenedor está en ejecución con el puerto mapeado:
      ```bash
      $ docker ps
      ```
    * Abra su navegador web en `http://localhost:8080`. Deberá visualizar la página de bienvenida *"Welcome to nginx!"*.
    * Regrese al terminal y visualice los registros de acceso HTTP generados por la petición del navegador:
      ```bash
      $ docker logs mi-servidor
      ```
    * Abra una sesión de terminal dentro del contenedor en ejecución para modificar la página servida en vivo:
      ```bash
      $ docker exec -it mi-servidor sh
      / # echo "<h1>Ola do container</h1>" > /usr/share/nginx/html/index.html
      / # exit
      ```
    * Actualice el navegador en `http://localhost:8080` y compruebe la modificación en tiempo real.
    * Detenga el contenedor y elimínelo:
      ```bash
      $ docker stop mi-servidor
      $ docker rm mi-servidor
      ```

4.  **Crear el Primer `Dockerfile` "a Mano" y Compilar (`docker build`):**
    * Dentro de la carpeta `ex1-cli`, cree un archivo `index.html` con un mensaje personalizado:
      ```html
      <!DOCTYPE html>
      <html>
      <body>
          <h1>Mi primera imagen construida con Dockerfile!</h1>
      </body>
      </html>
      ```
    * Cree ahora el archivo de receta declarativa llamado `Dockerfile` (sin extensión):
      ```dockerfile
      FROM nginx:alpine
      COPY index.html /usr/share/nginx/html/index.html
      ```
    * Compile la imagen en el contexto del directorio actual (`.`):
      ```bash
      $ docker build -t mi-sitio-manual:1.0 .
      ```
    * Inspeccione el registro local con `docker images`. ¡Su imagen `mi-sitio-manual:1.0` aparece ahora como una imagen local lista para desplegarse!
    * Inicie un contenedor a partir de su nueva imagen personalizada:
      ```bash
      $ docker run -d --name sitio-manual -p 8080:80 mi-sitio-manual:1.0
      ```
    * Acceda a `http://localhost:8080` en el navegador y verifique el resultado.
    * Concluya limpiando el contenedor:
      ```bash
      $ docker stop sitio-manual && docker rm sitio-manual
      ```
    * Regrese al directorio raíz de la sesión para continuar con Docker Compose:
      ```bash
      $ cd ~/IEI/clase04
      ```

-----

## Ejercicio 2: "Hello, World" con Docker Compose

**Objetivo:** Comprender la estructura básica de un archivo `compose.yml` y ejecutar una imagen preconstruida.

1.  Cree una nueva carpeta para este ejercicio (ej.: `ex2-helloworld`).
2.  Dentro de la carpeta, cree un nuevo archivo llamado `compose.yml` con el siguiente contenido:
    ```yaml
    services:
      hello:
        image: hello-world
    ```
3.  Abra su terminal en esta carpeta y ejecute la aplicación.
    ```bash
    $ docker compose up
    ```
4.  Observe la salida. El contenedor `hello-world` arrancará, imprimirá su mensaje y luego finalizará.
5.  Limpie el contenedor creado por la ejecución.
    ```bash
    $ docker compose down
    ```

-----

## Ejercicio 3: Construir una Imagen de Servidor Web Personalizada

**Objetivo:** Utilizar un `Dockerfile` con Docker Compose para crear una imagen de aplicación autónoma.

1.  Cree una nueva carpeta (`ex3-build`) y una subcarpeta dentro de ella llamada `my-website`.
2.  Dentro de `my-website`, cree un archivo llamado `index.html`:
    ```html
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Esta pagina fue construida dentro de la imagen Docker!</h1>
    </body>
    </html>
    ```
3.  En la raíz de la carpeta `ex3-build`, cree un `Dockerfile`:
    ```dockerfile
    FROM nginx:alpine
    COPY ./my-website /usr/share/nginx/html
    ```
4.  Finalmente, cree su archivo `compose.yml`:
    ```yaml
    services:
      webserver:
        build: .
        ports:
          - "8080:80"
    ```
5.  Construya e inicie el servicio. La flag `-d` lo ejecuta en segundo plano.
    ```bash
    $ docker compose up --build -d
    ```
6.  Abra su navegador en `http://localhost:8080`. Deberá ver su página web personalizada.

-----

## Ejercicio 4: Desarrollo en Tiempo Real con Volúmenes

**Objetivo:** Comprender cómo los volúmenes permiten modificar el contenido de su sitio web sin reconstruir la imagen.

1.  Cree una nueva carpeta (`ex4-volumes`) con la misma estructura `my-website/index.html` del ejercicio anterior.
2.  Cree un archivo `compose.yml`. En esta ocasión, utilizaremos la imagen estándar `nginx:alpine` y montaremos nuestra carpeta local como un volumen. **No se necesita ningún `Dockerfile`.**
    ```yaml
    services:
      webserver:
        image: nginx:alpine
        ports:
          - "8080:80"
        volumes:
          - ./my-website:/usr/share/nginx/html
    ```
3.  Inicie el servicio: `docker compose up -d`.
4.  Abra su navegador en `http://localhost:8080` para confirmar que está funcionando.
5.  **Actualización en Vivo:** Con el contenedor en ejecución, **edite el archivo `index.html`** en su máquina anfitriona. Cambie el encabezado a `<h1>Actualizacion en tiempo real con un Volumen!</h1>`.
6.  Guarde el archivo y **actualice su navegador**. ¡El cambio se refleja instantáneamente\!

-----

## Ejercicio 5: Contenido en Caché con Varnish & NGINX

**Objetivo:** Construir una aplicación web de dos capas con una caché Varnish sirviendo una página web rica desde un backend NGINX.

1.  **Crear la Estructura de Archivos:**
      * Cree una nueva carpeta (ej.: `ex5-varnish-cache`).
      * Dentro de ella, cree dos subcarpetas: `varnish` y `my-dynamic-website`.
2.  **Crear el Contenido Web:**
      * Busque un GIF animado divertido en Internet y guárdelo dentro de `my-dynamic-website` como `animation.gif`.
      * Dentro de `my-dynamic-website`, cree un archivo `index.html` para mostrar el GIF:
        ```html
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Prueba de Cache Varnish</title>
            <style> body { font-family: sans-serif; text-align: center; } </style>
        </head>
        <body>
            <h1>Esta pagina esta siendo servida por la cache de Varnish!</h1>
            <img src="animation.gif" alt="Animacion en cache">
        </body>
        </html>
        ```
3.  **Crear la Configuración de Varnish:**
      * Dentro de la carpeta `varnish`, cree un archivo llamado `default.vcl`. Este archivo indica a Varnish dónde encontrar el servidor NGINX.
        ```vcl
        vcl 4.1;
        backend default {
            .host = "nginx";
            .port = "80";
        }
        ```
4.  **Crear el Archivo Compose:**
      * En la raíz de su carpeta `ex5-varnish-cache`, cree el `compose.yml`:
        ```yaml
        services:
          cache:
            image: varnish:stable
            volumes:
              - ./varnish:/etc/varnish
            ports:
              - "8080:80"
            depends_on:
              - nginx

          nginx:
            image: nginx:alpine
            volumes:
              - ./my-dynamic-website:/usr/share/nginx/html
        ```
5.  **Ejecutar y Verificar:**
      * Inicie los servicios: `docker compose up -d`.
      * Abra su navegador en `http://localhost:8080`. Deberá ver su página web con el GIF. El punto clave es que **Varnish** le ha servido la página, no NGINX directamente.
      * **Observe la caché en acción:** Compruebe los registros de NGINX para la primera petición:
        ```bash
        $ docker compose logs nginx
        ```
      * Ahora, actualice la página del navegador varias veces. Vuelva a consultar los registros de `nginx`. Comprobará que **no aparecen nuevas entradas de registro**, ya que Varnish está sirviendo el contenido directamente desde su memoria caché sin consultar al backend NGINX.

-----

## Ejercicio 6: Desplegar una Aplicación del Mundo Real

**Objetivo:** Aprender a interpretar documentación oficial y desplegar un servicio complejo auto-hospedado a su elección.

1.  **Elija un Servicio:** Cree una nueva carpeta de trabajo (ej.: `ex6-jellyfin` o `ex6-realworld`). Visite [LinuxServer.io](https://www.linuxserver.io/) y explore su catálogo de imágenes populares. Elija una que le resulte de interés, por ejemplo:

      * **Jellyfin:** Servidor multimedia para películas y música.
      * **Nextcloud:** Nube personal para archivos, contactos y calendarios.
      * **Home Assistant:** Plataforma de domótica y automatización del hogar de código abierto.

2.  **Lea la Documentación:** En la página de la imagen seleccionada, localice la sección "Docker Compose". Léala con atención, identificando los **volúmenes** y las **variables de entorno** requeridas.

      * **Volúmenes (`- ./config:/config`):** Es aquí donde se almacenará la configuración de la aplicación en el anfitrión.
      * **Variables de Entorno (`PUID`, `PGID`, `TZ`):** Son críticas. `TZ` establece su zona horaria (ej.: `Europe/Lisbon` o `Europe/Madrid`). `PUID` y `PGID` garantizan que los archivos generados por el contenedor tengan los permisos correctos en el sistema anfitrión. En Linux/macOS, obtenga su ID ejecutando el comando `id` en su terminal. Un valor estándar habitual es `1000`.

3.  **Cree su `compose.yml`:** Tomando como base la documentación oficial, cree el archivo. A continuación se presenta un ejemplo para **Jellyfin**:

    ```yaml
    services:
      jellyfin:
        image: lscr.io/linuxserver/jellyfin:latest
        container_name: jellyfin
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=Europe/Lisbon
        volumes:
          - ./config:/config
          - ./series:/data/tvshows
          - ./peliculas:/data/movies
        ports:
          - "8096:8096"
        restart: unless-stopped
    ```

4.  **Prepare y Despliegue:**

      * Cree las carpetas locales definidas en los volúmenes (ej.: `mkdir config series peliculas`).
      * Ejecute la aplicación: `docker compose up -d`.

5.  **Explore el Servicio:** Consulte la documentación para conocer el puerto por defecto. Para Jellyfin es el `8096`. Abra su navegador en `http://localhost:8096` y siga el asistente de configuración inicial de su nuevo servicio\!
