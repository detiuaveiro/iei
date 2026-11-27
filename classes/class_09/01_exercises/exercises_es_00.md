---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Páginas Web y Publicación"
institute: Universidade de Aveiro
date: 23 de noviembre de 2026
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
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guion Práctico de Laboratorio

**Marco Pedagógico y Objetivos:**
En esta sesión de laboratorio se construye y publica una página web estática desde cero, aplicando los fundamentos de **HTML5 semántico**, **CSS3 (Box Model)** y **publicación en contenedores Docker con Nginx**. El guion se estructura en tres bloques progresivos y un reto opcional:

* **Bloque 1 — Estructuración Semántica en HTML5:** Creación de la estructura base de un documento HTML5, inspección del árbol **DOM**, uso de contenedores semánticos (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`), listas, hipervínculos (`mailto:`) y elementos multimedia nativos (`<figure>`/`<img>` y `<video>`).
* **Bloque 2 — Estilización y Diseño con CSS3:** Separación de responsabilidades mediante una hoja de estilos externa (`css/style.css`), aplicación de selectores, reglas de tipografía y color, y diseño de tarjetas con el **CSS Box Model** (`box-sizing: border-box`, `padding`, `border` y `margin`).
* **Bloque 3 — Publicación con Nginx, Docker Compose e Inspección HTTP:** Separación entre código fuente (`src/`) y configuración de despliegue, ejecución del servidor web `nginx:alpine` con volumen en solo lectura (`:ro`) y análisis del ciclo de peticiones HTTP mediante `curl` y *DevTools*.
* **Reto Opcional — Arquitectura de *Reverse Proxy* con Nginx:** Enrutamiento de peticiones en un único puerto público (`8080`) entre el sitio estático (`/`) y un servicio interno de API (`/api/`) aislados en una red privada Docker.

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Cree el directorio dedicado al proyecto de esta sesión y verifique que Docker Compose se encuentra operativo:

```bash
mkdir -p ~/IEI/clase09/mi-portfolio
cd ~/IEI/clase09/mi-portfolio
docker compose version
```

-----

## Bloque 1: Estructuración Semántica en HTML5

### Paso 1.1: Documento HTML5 Base y Árbol DOM

Cree un archivo llamado `index.html` en la raíz del directorio `mi-portfolio` con la estructura base de un documento HTML5 válido:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1.0">
  <title>Mi Portfolio</title>
</head>
<body>
  <h1>¡Hola, Mundo!</h1>
  <p>Documento HTML5 inicial servido localmente.</p>
</body>
</html>
```

* **`<!DOCTYPE html>`:** Indica al navegador que interprete el documento en el modo estándar HTML5.
* **`<head>`:** Contiene metadatos no renderizados en el área principal de la página (`UTF-8` para la correcta codificación de caracteres, `viewport` para adaptación a pantallas móviles y `<title>` para la pestaña del navegador).
* **`<body>`:** Contiene todos los elementos visibles renderizados en la ventana.

**Verificación:**

1. Abra el archivo `index.html` en su navegador (desde el explorador de archivos o arrastrándolo a una ventana del navegador).
2. Observe la dirección mostrada en la barra de URL — se trata de una ruta local del sistema de archivos (`file:///.../mi-portfolio/index.html`) — y confirme que la pestaña muestra el título *"Mi Portfolio"*.
3. Abra las **Herramientas de Desarrollador (*DevTools*)** (`F12` o *Clic derecho $\rightarrow$ Inspeccionar*) y examine en la pestaña **Elements / Inspector** el árbol **DOM** generado por el navegador.

### Paso 1.2: Contenedores Semánticos, Navegación e Hipervínculos

Sustituya el bloque `<body>` del archivo `index.html` por una estructura semántica compuesta por cabecera (`<header>`), navegación (`<nav>`), contenido principal (`<main>`), artículo autónomo (`<article>`) y pie de página (`<footer>`) con un hipervínculo `mailto:`:

```html
<body>
  <header>
    <h1>Mi Portfolio</h1>
    <nav>
      <ul>
        <li><a href="index.html">Inicio</a></li>
        <li><a href="#sobre">Sobre Mí</a></li>
        <li><a href="#media">Multimedia</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h2>Bienvenido</h2>
    <p>
      Página desarrollada desde cero en <strong>HTML5</strong>
      y <em>CSS3</em> en el marco de IEI.
    </p>

    <article id="sobre">
      <h3>Sobre Mí</h3>
      <p>
        Soy estudiante de 1.º de Ingeniería Informática
        en la Universidade de Aveiro.
      </p>
      <p>
        Mis principales áreas de interés incluyen [Interés 1]
        y [Interés 2].
      </p>
    </article>
  </main>

  <footer>
    <p>
      Contacto: <a href="mailto:tu.correo@ua.pt">tu.correo@ua.pt</a>
    </p>
    <p>&copy; 2026 Tu Nombre</p>
  </footer>
</body>
```

**Tareas:**

1. Sustituya los marcadores `[Interés 1]`, `[Interés 2]`, `tu.correo@ua.pt` y `Tu Nombre` por sus propios datos.
2. Guarde el archivo, actualice el navegador y observe que, aunque la estructura semántica está definida, **todos los bloques aparecen apilados verticalmente sin formato** (comportamiento predeterminado sin CSS).
3. Pruebe el enlace `mailto:` en el pie de página y verifique la navegación interna mediante las anclas `#sobre` y `#media`.

### Paso 1.3: Elementos Multimedia Nativos (`<figure>`/`<img>` y `<video>`)

1. Cree los directorios para almacenar los recursos multimedia:
   ```bash
   mkdir -p images videos
   ```
2. Descargue una imagen de ejemplo en formato JPEG (o copie una fotografía propia a `images/profile.jpg`) y un vídeo corto de prueba en formato MP4:
   ```bash
   curl -L "https://placehold.co/400x400/004a8c/ffffff/jpg?text=IEI" \
     -o images/profile.jpg
   curl -L "https://www.w3schools.com/html/mov_bbb.mp4" \
     -o videos/my-clip.mp4
   ```
3. En el archivo `index.html`, incorpore la imagen con leyenda semántica (`<figure>` y `<figcaption>`) dentro de `<article id="sobre">` y añada una nueva `<section id="media">` dentro de `<main>` (manteniendo el `<article>` existente):

   ```html
   <main>
     <h2>Bienvenido</h2>
     <p>
       Página desarrollada desde cero en <strong>HTML5</strong>
       y <em>CSS3</em> en el marco de IEI.
     </p>

     <article id="sobre">
       <h3>Sobre Mí</h3>
       <figure>
         <img src="images/profile.jpg"
              alt="Fotografía de perfil del autor" width="150">
         <figcaption>Ingeniería Informática — UA</figcaption>
       </figure>
       <p>
         Soy estudiante de 1.º de Ingeniería Informática
         en la Universidade de Aveiro.
       </p>
       <p>
         Mis principales áreas de interés incluyen [Interés 1]
         y [Interés 2].
       </p>
     </article>

     <section id="media">
       <h3>Demostración de Vídeo HTML5</h3>
       <video controls width="100%">
         <source src="videos/my-clip.mp4" type="video/mp4">
         Su navegador no soporta vídeo HTML5.
       </video>
     </section>
   </main>
   ```

4. **Prueba de accesibilidad (`alt`):** Cambie temporalmente el atributo `src` de la imagen a una ruta inexistente (ej.: `images/inexistente.jpg`), actualice el navegador y confirme que se muestra el texto alternativo definido en `alt`. Restaure después la ruta correcta (`images/profile.jpg`).

-----

## Bloque 2: Estilización y Diseño con CSS3

### Paso 2.1: Hoja de Estilos Externa, Tipografía y Colores

Para garantizar la **separación de responsabilidades** entre contenido (HTML) y presentación (CSS), cree un directorio `css` y el archivo `css/style.css`:

```bash
mkdir -p css
```

1. Añada el enlace a la hoja de estilos externa en la sección `<head>` de `index.html`:
   ```html
   <head>
     <meta charset="UTF-8">
     <meta name="viewport"
           content="width=device-width, initial-scale=1.0">
     <title>Mi Portfolio</title>
     <link rel="stylesheet" href="css/style.css">
   </head>
   ```
2. Defina las reglas base de tipografía, colores y selectores en `css/style.css`:
   ```css
   /* Incluye padding y border en el cálculo de width/max-width */
   * {
       box-sizing: border-box;
   }

   body {
       background-color: #f0f0f0;
       font-family: Arial, Helvetica, sans-serif;
       line-height: 1.6;
       color: #333;
       margin: 0;
       padding: 16px;
   }

   header h1 {
       color: #004a8c;
       margin-top: 0;
   }

   a {
       color: #005a9c;
       text-decoration: none;
   }

   a:hover {
       text-decoration: underline;
   }
   ```
3. Guarde ambos archivos y actualice el navegador para confirmar la aplicación de la hoja de estilos externa.

### Paso 2.2: Modelo de Caja (*CSS Box Model*) y Diseño en Tarjetas

Añada al final de `css/style.css` las reglas de espaciado, bordes y disposición en tarjetas centradas:

```css
/* Diseño en tarjetas centradas (CSS Box Model) */
header, main, footer {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}

/* Menú de navegación horizontal */
nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 16px;
}

nav a {
    font-weight: bold;
}

/* Evita que el elemento flotante desborde <article> */
article {
    display: flow-root;
}

article figure {
    float: left;
    margin: 0 20px 10px 0;
    text-align: center;
}

article img {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid #004a8c;
}

figcaption {
    font-size: 0.78em;
    color: #555;
    margin-top: 4px;
}

footer {
    text-align: center;
    font-size: 0.9em;
    color: #666;
}
```

**Verificación:** Actualice el navegador y observe el resultado del **Box Model** (`max-width: 800px` + `margin: 20px auto`), el menú horizontal y el encuadre circular de la imagen de perfil sin superposición con la sección de vídeo.

-----

## Bloque 3: Publicación con Nginx, Docker Compose e Inspección HTTP

### Paso 3.1: Reorganización para Despliegue (`src/`)

En un flujo de trabajo estructurado, se separa el **código fuente público** de la página de la **configuración de despliegue (*deployment*)**. Mueva los archivos del sitio a un subdirectorio `src/`:

```bash
mkdir -p src
mv index.html css images videos src/
```

Verifique que la estructura de directorios corresponde al siguiente esquema:

```text
mi-portfolio/
└── src/
    ├── index.html
    ├── css/
    │   └── style.css
    ├── images/
    │   └── profile.jpg
    └── videos/
        └── my-clip.mp4
```

> **Observación:** Si actualiza la pestaña anterior del navegador (`file:///.../mi-portfolio/index.html`), la carga fallará porque el archivo se ha movido. En el siguiente paso serviremos el sitio mediante el protocolo HTTP.

### Paso 3.2: Configuración del Servidor Web Nginx en Docker Compose

En la raíz de `mi-portfolio` (junto a `src/`), cree el archivo `docker-compose.yml`:

```yaml
services:
  webserver:
    image: nginx:alpine
    container_name: mi_portfolio_site
    ports:
      - "8080:80"
    volumes:
      - ./src:/usr/share/nginx/html:ro
```

* **`image: nginx:alpine`:** Imagen oficial y ligera del servidor web Nginx basada en Alpine Linux.
* **`ports: - "8080:80"`:** Redirige el tráfico del puerto `8080` de la máquina anfitriona (*host*) al puerto `80` del contenedor.
* **`volumes: - ./src:/usr/share/nginx/html:ro`:** Monta el directorio local `./src` en la raíz servida por Nginx en modo solo lectura (*read-only*), evitando modificaciones no autorizadas desde el contenedor.

Inicie el servicio en segundo plano (*detached mode*) y acceda a la dirección en el navegador:

```bash
docker compose up -d
```

Acceda a **`http://localhost:8080`** en el navegador y confirme que el sitio completo (HTML, CSS, imagen y vídeo) se sirve correctamente.

### Paso 3.3: Inspección del Ciclo de Peticiones HTTP (`curl` y *DevTools*)

1. **Inspección de cabeceras desde terminal:** Ejecute `curl -I` para inspeccionar la respuesta HTTP devuelta por Nginx:
   ```bash
   curl -I http://localhost:8080
   curl -I http://localhost:8080/css/style.css
   ```
   Observe el código de estado (`HTTP/1.1 200 OK`), la cabecera `Server: nginx/...` y la diferencia en `Content-Type` (`text/html` frente a `text/css`).

2. **Inspección en el navegador (*DevTools*):**
   * En `http://localhost:8080`, abra las **DevTools** (`F12`) $\rightarrow$ pestaña **Network** (*Red*).
   * Active la opción **Disable cache** (*Desactivar caché*) y recargue la página (`Ctrl+R` / `Cmd+R`).
   * Confirme que la carga de una sola página origina **múltiples peticiones HTTP** individuales (`/` o `index.html`, `style.css`, `profile.jpg` y `my-clip.mp4`).

3. Al finalizar este bloque, detenga y elimine el contenedor:
   ```bash
   docker compose down
   ```

-----

## Reto Opcional: Arquitectura de *Reverse Proxy* con Nginx

**Objetivo:** Reproducir la arquitectura de **Reverse Proxy** vista en teoría, exponiendo **dos servicios internos aislados** a través de un único puerto público (`8080`):
* Peticiones a **`/`** $\rightarrow$ redirigidas al contenedor **`site`** (su portfolio HTML/CSS);
* Peticiones a **`/api/`** $\rightarrow$ redirigidas al contenedor **`api`** (un servicio interno que devuelve datos JSON, simulando la API REST de la Clase 08).

1. En la raíz de `mi-portfolio`, cree un archivo de configuración mínimo `api.conf` para el servicio interno `api`:
   ```nginx
   events {}
   http {
     server {
       listen 8000;
       location / {
         default_type application/json;
         return 200 '{"servicio":"api-iei","estado":"operativo"}';
       }
     }
   }
   ```

2. Cree el archivo `nginx.conf` con las reglas de enrutamiento del **Reverse Proxy**:
   ```nginx
   events {}
   http {
     server {
       listen 80;

       location /api/ {
         proxy_pass http://api:8000/;
       }

       location / {
         proxy_pass http://site:80;
       }
     }
   }
   ```

3. Cree un archivo `docker-compose.proxy.yml` donde **solo el servicio `proxy` expone puertos al exterior**:
   ```yaml
   services:
     proxy:
       image: nginx:alpine
       ports:
         - "8080:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf:ro
       depends_on:
         - site
         - api

     site:
       image: nginx:alpine
       volumes:
         - ./src:/usr/share/nginx/html:ro
       # Sin 'ports': accesible solo en la red privada Docker

     api:
       image: nginx:alpine
       volumes:
         - ./api.conf:/etc/nginx/nginx.conf:ro
       # Reemplazable por su imagen FastAPI de la Clase 08
   ```

4. Inicie la arquitectura completa y valide el enrutamiento en ambas rutas:
   ```bash
   docker compose -f docker-compose.proxy.yml up -d
   curl -i http://localhost:8080/api/
   ```
   * Acceda a **`http://localhost:8080/`** en el navegador (servido por el contenedor `site`).
   * Acceda a **`http://localhost:8080/api/`** (servido por el contenedor `api`, devolviendo JSON).
   * Compruebe con `docker ps` que solo el contenedor `proxy` posee mapeo de puerto hacia el *host* (`0.0.0.0:8080->80/tcp`), manteniendo `site` y `api` aislados en la red interna.

5. Para detener los servicios del reto:
   ```bash
   docker compose -f docker-compose.proxy.yml down
   ```

-----

## Síntesis de Resultados Obtenidos

Al completar este guion práctico, ha ejecutado el flujo completo de desarrollo y publicación de páginas web estáticas:

* Construcción de un documento **HTML5 semántico** válido con navegación, hipervínculos (`mailto:`) y multimedia nativa (`<figure>`/`<img>` y `<video>`).
* Aplicación de **CSS3** externo con separación de responsabilidades, selectores y control de diseño mediante el **CSS Box Model** (`box-sizing: border-box`).
* Empaquetado y publicación del sitio con **Nginx + Docker Compose** en modo solo lectura (`:ro`), validación de peticiones HTTP con `curl` y *DevTools*, y (opcionalmente) configuración de enrutamiento con **Reverse Proxy**.
