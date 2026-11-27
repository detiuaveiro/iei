---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Páginas Web y Publicación"
institute: Universidade de Aveiro
date: November 23, 2026
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
 - \usetikzlibrary{positioning,arrows.meta,calc,shapes.geometric}
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \BeforeBeginEnvironment{Shaded}{\vspace{0.5em}}
 - \AfterEndEnvironment{Shaded}{\vspace{0.3em}}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Visión General de la Sesión

  * **Parte I — Fundamentos de la Web y Estructura HTML5:**
      * Páginas estáticas, anatomía de etiquetas, árbol **DOM**, elementos visuales y **etiquetas semánticas HTML5**.
  * **Parte II — Estilización y Diseño con CSS:**
      * Separación estructura/estilo, selectores, **Cascada/Especificidad**, integración y **CSS Box Model**.
  * **Parte III — Publicación con Docker/Nginx y Reverse Proxy:**
      * Servidor **Nginx + Docker Compose**, flujo HTTP extremo a extremo y arquitectura de **Reverse Proxy**.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos de la Web y Estructura HTML5}}
\end{center}

-----

## ¿Qué es una Página Web "Estática"?

  * **Entrega directa:** Archivos enviados al navegador **exactamente tal como están almacenados** en el servidor.
  * **Contenido fijo:** Todos los usuarios ven el mismo documento (como un folleto digital).
  * **Rol del servidor (ej.: Nginx):** Localizar el archivo solicitado (`GET /index.html`) y devolverlo vía HTTP.
  * **Tecnologías base:** **HTML** (estructura y significado) + **CSS** (estilo y diseño).

\vspace{2em}

\begin{center}
\includegraphics[width=0.76\linewidth]{figures/static-website.png}
\end{center}

-----

## HTML: *HyperText Markup Language* y Anatomía de una Etiqueta

  * **HyperText (Hipertexto):** Texto con hipervínculos (*links*) que conectan documentos en la Web.
  * **Markup Language (Marcado):** *No* es programación (sin lógica/bucles); usa **etiquetas (*tags*)** para estructurar contenido.

\vspace{0.4em}

\begin{center}
\begin{tikzpicture}[
    box/.style={rectangle, rounded corners=2pt, thick, font=\scriptsize\ttfamily, inner sep=4pt, minimum height=0.60cm},
    lbl/.style={font=\tiny\bfseries, align=center},
    arr/.style={-{Latex[length=1.4mm]}, thick}
]
% Elemento Normal
\node[font=\scriptsize\bfseries, anchor=west] at (-0.2, 2.10) {1. Elemento con Contenido:};

\node[box, draw=blue!75!black, fill=blue!8] (open) at (0.6, 1.35) {<a};
\node[box, draw=orange!80!black, fill=orange!10, right=2pt of open] (attr) {href="https://ua.pt"};
\node[box, draw=blue!75!black, fill=blue!8, right=2pt of attr] (openclose) {>};
\node[box, draw=uagreen!75!black, fill=uagreen!12, right=2pt of openclose] (content) {Universidade de Aveiro};
\node[box, draw=red!75!black, fill=red!8, right=2pt of content] (close) {</a>};

\node[lbl, color=blue!75!black] (l_open) at (0.6, 0.35) {Etiqueta de\\Apertura};
\node[lbl, color=orange!85!black] (l_attr) at (2.5, 0.35) {Atributo\\(\texttt{nombre="valor"})};
\node[lbl, color=uagreen!65!black] (l_cont) at (5.85, 0.35) {Contenido\\Visible};
\node[lbl, color=red!75!black] (l_close) at (8.3, 0.35) {Etiqueta de Cierre\\(\texttt{</...>})};

\draw[arr, color=blue!75!black] (l_open.north) -- (open.south);
\draw[arr, color=orange!85!black] (l_attr.north) -- (attr.south);
\draw[arr, color=uagreen!65!black] (l_cont.north) -- (content.south);
\draw[arr, color=red!75!black] (l_close.north) -- (close.south);

% Elemento Vazio
\node[font=\scriptsize\bfseries, anchor=west] at (-0.2, -0.45) {2. Elemento Vacío (sin etiqueta de cierre):};
\node[box, draw=purple!75!black, fill=purple!8, anchor=west] at (0.2, -1.05) {<img src="logo.png" alt="Logotipo de la UA">};
\node[font=\tiny, color=black!70, anchor=west] at (5.7, -1.05) {(Ej.: \texttt{<img>}, \texttt{<meta>}, \texttt{<link>})};
\end{tikzpicture}
\end{center}

-----

## El Esqueleto Base de HTML5 y el Árbol DOM

::::: {.columns align=center}
::: {.column width="45%"}

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>My Document</title>
  </head>
  <body>
    <h1>Header</h1>
    <p>Paragraph</p>
  </body>
</html>
```

:::
::: {.column width="55%"}

\begin{center}
\begin{tikzpicture}[
    docnode/.style={rectangle, rounded corners=2.5pt, draw=black!55, fill=black!7, thick, font=\tiny\sffamily, minimum width=1.55cm, minimum height=0.40cm},
    elemnode/.style={rectangle, rounded corners=2.5pt, draw=teal!65!black, fill=teal!10, thick, font=\tiny\sffamily\bfseries, text=teal!50!black, minimum width=1.35cm, minimum height=0.40cm},
    textnode/.style={rectangle, rounded corners=6pt, draw=black!40, fill=black!5, thick, font=\tiny\sffamily, minimum width=1.40cm, minimum height=0.40cm, inner xsep=3.5pt},
    edge/.style={-{Latex[length=1.2mm]}, thick, color=black!60}
]
% Raiz Document
\node[docnode] (doc) at (2.4, 3.30) {Document};

% HTML
\node[elemnode] (html) at (2.4, 2.55) {HTML};

% HEAD e BODY
\node[elemnode] (head) at (0.85, 1.80) {HEAD};
\node[elemnode] (body) at (3.55, 1.80) {BODY};

% TITLE, H1, P
\node[elemnode] (title) at (0.85, 1.05) {TITLE};
\node[elemnode] (h1) at (2.70, 1.05) {H1};
\node[elemnode] (p) at (4.40, 1.05) {P};

% Nós de texto (folhas)
\node[textnode] (t_txt) at (0.85, 0.30) {"My Document"};
\node[textnode] (h1_txt) at (2.70, 0.30) {"Header"};
\node[textnode] (p_txt) at (4.40, 0.30) {"Paragraph"};

% Ligações
\draw[edge] (doc.south) -- (html.north);
\draw[edge] (html.south) -- (head.north);
\draw[edge] (html.south) -- (body.north);
\draw[edge] (head.south) -- (title.north);
\draw[edge] (body.south) -- (h1.north);
\draw[edge] (body.south) -- (p.north);
\draw[edge] (title.south) -- (t_txt.north);
\draw[edge] (h1.south) -- (h1_txt.north);
\draw[edge] (p.south) -- (p_txt.north);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<!DOCTYPE html>`:** Activa el modo estándar HTML5 en el navegador.
  * **`<head>` (Invisible en página):** Metadatos del documento (ej. `<title>` en la pestaña del navegador).
  * **`<body>` (Visible en ventana):** Contiene todos los elementos renderizados en pantalla (`<h1>`, `<p>`, imágenes, etc.).
  * **Árbol DOM (*Document Object Model*):** Árbol jerárquico de nodos construido en memoria por el navegador para mostrar y manipular la página.

-----

## Elementos de Contenido Visual I: Tipografía, Texto y Enlaces

::::: {.columns align=center}
::: {.column width="48%"}

```html
<h1>Título Principal (H1)</h1>
<h2>Subsección de Página (H2)</h2>

<p>
  Texto con <strong>importancia</strong>
  y con <em>énfasis</em>.
</p>

<p>
  Visite la <a href="https://www.ua.pt">UA</a>
  o contacte
  <a href="mailto:alumno@ua.pt">alumno@ua.pt</a>.
</p>
```

:::
::: {.column width="52%"}

\begin{center}
\begin{tikzpicture}[scale=0.82, transform shape]
% Moldura do Browser
\draw[thick, draw=black!70, fill=white, rounded corners=3pt] (0, 0) rectangle (5.5, 4.3);
\draw[thick, draw=black!70, fill=black!12, rounded corners=3pt] (0, 3.75) rectangle (5.5, 4.3);
\fill[white] (0.02, 3.73) rectangle (5.48, 3.82);
\draw[draw=black!50] (0, 3.75) -- (5.5, 3.75);

% Botões da janela + Barra de URL
\fill[red!75] (0.25, 4.02) circle (0.08);
\fill[orange!80] (0.50, 4.02) circle (0.08);
\fill[uagreen!80!black] (0.75, 4.02) circle (0.08);
\draw[draw=black!30, fill=white, rounded corners=2pt] (1.05, 3.86) rectangle (5.3, 4.18);
\node[font=\tiny\ttfamily, color=black!65, anchor=west] at (1.15, 4.02) {file:///.../index.html};

% Conteúdo Renderizado
\node[font=\normalsize\bfseries, anchor=west] at (0.25, 3.25) {Título Principal (H1)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 3.25) {<h1>};

\node[font=\footnotesize\bfseries, anchor=west] at (0.25, 2.65) {Subsección de Página (H2)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.65) {<h2>};

\node[font=\scriptsize, align=left, text width=4.3cm, anchor=north west] at (0.25, 2.25) {Texto con \textbf{importancia} y con \textit{énfasis}.};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.00) {<p>};

\node[font=\scriptsize, align=left, text width=4.3cm, anchor=north west] at (0.25, 1.35) {Visite la \textcolor{blue}{\underline{UA}} o contacte \textcolor{blue}{\underline{alumno@ua.pt}}.};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 1.10) {<a>};

\draw[dashed, color=black!25] (0.2, 0.45) -- (5.3, 0.45);
\node[font=\tiny\itshape, color=black!60] at (2.75, 0.22) {Renderizado nativo en el navegador (sin CSS)};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<h1>`–`<h6>`:** Jerarquía de títulos (usar solo un `<h1>` principal por página).
  * **`<p>`:** Bloque de párrafo con espaciado vertical automático.
  * **`<strong>` / `<em>`:** Énfasis semántico (negrita y cursiva).
  * **`<a href="...">`:** Hipervínculo a URLs, archivos locales o correos (`mailto:`).

-----

## Elementos de Contenido Visual II: Listas y Tablas

::::: {.columns align=center}
::: {.column width="48%"}

```html
<!-- Lista No Ordenada y Ordenada -->
<ul>
  <li>HTML5 (Estructura)</li>
  <li>CSS3 (Estilo)</li>
</ul>
<ol>
  <li>Crear index.html</li>
  <li>Publicar en Nginx</li>
</ol>

<!-- Tabla de Datos -->
<table>
  <thead>
    <tr><th>Servicio</th><th>Puerto</th></tr>
  </thead>
  <tbody>
    <tr><td>HTTP</td><td>80</td></tr>
    <tr><td>HTTPS</td><td>443</td></tr>
  </tbody>
</table>
```

:::
::: {.column width="52%"}

\begin{center}
\begin{tikzpicture}[scale=0.80, transform shape]
% Moldura do Browser
\draw[thick, draw=black!70, fill=white, rounded corners=3pt] (0, 0) rectangle (5.5, 4.7);
\draw[thick, draw=black!70, fill=black!12, rounded corners=3pt] (0, 4.15) rectangle (5.5, 4.7);
\fill[white] (0.02, 4.13) rectangle (5.48, 4.22);
\draw[draw=black!50] (0, 4.15) -- (5.5, 4.15);
\fill[red!75] (0.25, 4.42) circle (0.08);
\fill[orange!80] (0.50, 4.42) circle (0.08);
\fill[uagreen!80!black] (0.75, 4.42) circle (0.08);
\draw[draw=black!30, fill=white, rounded corners=2pt] (1.05, 4.26) rectangle (5.3, 4.58);
\node[font=\tiny\ttfamily, color=black!65, anchor=west] at (1.15, 4.42) {http://localhost:8080/listas.html};

% Lista ul
\node[font=\scriptsize, anchor=west] at (0.4, 3.72) {$\bullet$ HTML5 (Estructura)};
\node[font=\scriptsize, anchor=west] at (0.4, 3.38) {$\bullet$ CSS3 (Estilo)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 3.55) {<ul> / <li>};

\draw[dotted, color=black!25] (0.25, 3.10) -- (5.25, 3.10);

% Lista ol
\node[font=\scriptsize, anchor=west] at (0.4, 2.75) {1. Crear index.html};
\node[font=\scriptsize, anchor=west] at (0.4, 2.40) {2. Publicar en Nginx};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.57) {<ol> / <li>};

\draw[dotted, color=black!25] (0.25, 2.10) -- (5.25, 2.10);

% Tabela renderizada
\draw[thick, draw=black!60, fill=black!8] (0.4, 1.45) rectangle (2.1, 1.85);
\draw[thick, draw=black!60, fill=black!8] (2.1, 1.45) rectangle (3.4, 1.85);
\node[font=\scriptsize\bfseries] at (1.25, 1.65) {Servicio};
\node[font=\scriptsize\bfseries] at (2.75, 1.65) {Puerto};

\draw[draw=black!50] (0.4, 1.05) rectangle (2.1, 1.45);
\draw[draw=black!50] (2.1, 1.05) rectangle (3.4, 1.45);
\node[font=\scriptsize] at (1.25, 1.25) {HTTP};
\node[font=\scriptsize] at (2.75, 1.25) {80};

\draw[draw=black!50] (0.4, 0.65) rectangle (2.1, 1.05);
\draw[draw=black!50] (2.1, 0.65) rectangle (3.4, 1.05);
\node[font=\scriptsize] at (1.25, 0.85) {HTTPS};
\node[font=\scriptsize] at (2.75, 0.85) {443};

\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 1.65) {<thead> / <th>};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 1.05) {<tbody> / <td>};

\node[font=\tiny\itshape, color=black!60] at (2.75, 0.25) {Listas y tablas renderizadas en el navegador};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<ul>` / `<ol>`:** Listas no ordenadas (viñetas) y ordenadas (numeradas), con elementos `<li>`.
  * **`<table>`:** Estructura tabular dividida en cabecera (`<thead>` / `<th>`) y cuerpo (`<tbody>` / `<td>`), organizada por filas (`<tr>`).

-----

## Multimedia Nativa en HTML5: `<img>`, `<figure>`, `<audio>` y `<video>`

::::: {.columns align=center}
::: {.column width="50%"}

```html
<!-- Imagen con Leyenda -->
<figure>
  <img src="images/profile.jpg"
       alt="Foto de perfil" width="150">
  <figcaption>Fig 1. Alumno de IEI.</figcaption>
</figure>

<!-- Audio y Vídeo Nativos -->
<audio controls>
  <source src="song.ogg" type="audio/ogg">
  <source src="song.mp3" type="audio/mpeg">
</audio>

<video controls width="100%">
  <source src="clip.webm" type="video/webm">
  <source src="clip.mp4" type="video/mp4">
</video>
```

:::
::: {.column width="50%"}

\begin{center}
\begin{tikzpicture}[scale=0.78, transform shape]
% Moldura do Browser
\draw[thick, draw=black!70, fill=white, rounded corners=3pt] (0, 0) rectangle (5.3, 4.95);
\draw[thick, draw=black!70, fill=black!12, rounded corners=3pt] (0, 4.45) rectangle (5.3, 4.95);
\fill[white] (0.02, 4.43) rectangle (5.28, 4.50);
\draw[draw=black!50] (0, 4.45) -- (5.3, 4.45);
\fill[red!75] (0.25, 4.70) circle (0.07);
\fill[orange!80] (0.48, 4.70) circle (0.07);
\fill[uagreen!80!black] (0.71, 4.70) circle (0.07);
\node[font=\tiny\ttfamily, color=black!65, anchor=west] at (0.95, 4.70) {http://localhost:8080/media.html};

% 1. Imagem carregada (<figure>) vs Imagem falhada (alt)
\draw[draw=black!35, fill=black!3, rounded corners=2pt] (0.25, 2.85) rectangle (2.55, 4.25);
\fill[blue!20] (0.45, 3.25) rectangle (2.35, 4.10);
\fill[blue!55!black] (1.4, 3.78) circle (0.18);
\fill[blue!55!black] (1.05, 3.30) rectangle (1.75, 3.55);
\node[font=\tiny\itshape, color=black!75] at (1.4, 3.03) {Fig 1. Alumno de IEI.};

% Imagem partida (fallback alt)
\draw[dashed, draw=red!60!black, fill=red!4, rounded corners=2pt] (2.75, 2.85) rectangle (5.05, 4.25);
\node[font=\tiny\bfseries, color=red!70!black] at (3.9, 3.98) {Si falla (Error 404):};
\draw[draw=black!50, fill=white] (2.95, 3.50) rectangle (3.30, 3.78);
\node[font=\tiny, color=red!75!black] at (3.12, 3.64) {X};
\node[font=\tiny, align=left, text width=1.55cm, anchor=west] at (3.35, 3.55) {"Foto de perfil" (\texttt{alt})};

% 2. Audio Player
\node[font=\tiny\ttfamily\bfseries, color=black!70, anchor=west] at (0.25, 2.58) {<audio controls>};
\draw[draw=black!50, fill=black!8, rounded corners=6pt] (0.25, 1.95) rectangle (5.05, 2.40);
\fill[black!80] (0.48, 2.10) -- (0.48, 2.25) -- (0.62, 2.175) -- cycle;
\node[font=\tiny\ttfamily, color=black!75] at (1.18, 2.17) {0:14 / 2:45};
\draw[thick, color=black!30] (1.85, 2.17) -- (4.30, 2.17);
\draw[very thick, color=uagreen!75!black] (1.85, 2.17) -- (2.65, 2.17);
\fill[uagreen!80!black] (2.65, 2.17) circle (0.07);
\node[font=\tiny, color=black!75] at (4.70, 2.17) {Vol};

% 3. Video Player
\node[font=\tiny\ttfamily\bfseries, color=black!70, anchor=west] at (0.25, 1.70) {<video controls>};
\draw[draw=black!70, fill=black!85, rounded corners=2pt] (0.25, 0.20) rectangle (5.05, 1.52);
\draw[fill=white!20, draw=white] (2.65, 0.95) circle (0.25);
\fill[white] (2.59, 0.85) -- (2.59, 1.05) -- (2.76, 0.95) -- cycle;
% Barra de controlo do vídeo
\fill[black!95] (0.25, 0.20) rectangle (5.05, 0.48);
\fill[white] (0.43, 0.28) -- (0.43, 0.40) -- (0.55, 0.34) -- cycle;
\draw[thick, color=white!40] (0.80, 0.34) -- (4.10, 0.34);
\draw[very thick, color=uagreen] (0.80, 0.34) -- (2.10, 0.34);
\node[font=\tiny\ttfamily, color=white] at (4.60, 0.34) {[  ]};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`src` y `alt`:** Ruta del archivo y texto alternativo (esencial para accesibilidad y error 404).
  * **`controls` y `<source>`:** Botones nativos del reproductor; el navegador reproduce el 1.º formato soportado.

-----

## Arquitectura Semántica HTML5: Los 7 Contenedores

::::: {.columns align=center}
::: {.column width="62%"}

| Etiqueta | Propósito | Regla / Ejemplo |
| :--- | :--- | :--- |
| **`<header>`** | Cabecera de página (o artículo). | Logotipo y `<h1>` (**$\neq$ `<head>`!**). |
| **`<nav>`** | Navegación principal. | Menú principal (`<ul>` con enlaces). |
| **`<main>`** | Contenido central exclusivo. | **Solo un `<main>`** por página. |
| **`<article>`** | Contenido **autónomo**. | Entrada de blog, noticia (*¿aislable?*). |
| **`<section>`** | Agrupación **temática**. | Subcapítulo ("Sobre Mí", con `<h2>`). |
| **`<aside>`** | Contenido complementario. | *Sidebar*, enlaces extra, biografía. |
| **`<footer>`** | Pie de página o sección. | Copyright (`&copy;`), contactos. |

:::
::: {.column width="38%"}

\begin{center}
\begin{tikzpicture}[
    blk/.style={rectangle, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, align=center}
]
\draw[draw=uagreen!75!black, fill=uagreen!4, rounded corners=3pt, thick] (3.7, 0.1) rectangle (7.0, 4.15);

% Header + Nav
\draw[blk, draw=orange!80!black, fill=orange!15] (3.85, 3.22) rectangle (6.85, 4.00);
\node[font=\tiny\ttfamily\bfseries, color=orange!85!black, anchor=north west] at (3.90, 3.98) {<header>};
\node[blk, draw=orange!90!black, fill=orange!30, minimum width=2.7cm, minimum height=0.34cm] at (5.35, 3.46) {<nav>};

% Main + Article + Section
\draw[blk, draw=uagreen!75!black, fill=uagreen!15] (3.85, 0.85) rectangle (5.85, 3.08);
\node[font=\tiny\ttfamily\bfseries, color=uagreen!55!black, anchor=north west] at (3.90, 3.05) {<main>};

\draw[blk, draw=blue!75!black, fill=blue!12] (3.98, 0.98) rectangle (5.72, 2.62);
\node[font=\tiny\ttfamily\bfseries, color=blue!80!black, anchor=north west] at (4.02, 2.60) {<article>};
\node[blk, draw=blue!60!black, fill=white, minimum width=1.48cm, minimum height=0.42cm] at (4.85, 1.92) {<section> 1};
\node[blk, draw=blue!60!black, fill=white, minimum width=1.48cm, minimum height=0.42cm] at (4.85, 1.34) {<section> 2};

% Aside
\draw[blk, draw=purple!75!black, fill=purple!12] (5.98, 0.85) rectangle (6.85, 3.08);
\node[font=\tiny\ttfamily\bfseries, color=purple!80!black, align=center] at (6.41, 1.96) {<aside>\\{\tiny (Lateral)}};

% Footer
\node[blk, draw=teal!80!black, fill=teal!15, minimum width=3.0cm, minimum height=0.50cm] at (5.35, 0.48) {<footer>};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{0.2em}

  * **Ventajas:** Facilitan la **Accesibilidad** (lectores de pantalla), el **SEO** y la legibilidad del código.
  * **Nota:** Definen **significado**, no diseño — sin CSS, se muestran apiladas.

-----

## Uniendo Todo: HTML5 Semántico vs. Renderizado Sin CSS

::::: columns
::: {.column width="54%"}

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Portfolio IEI</title>
</head>
<body>
  <header>
    <h1>Mi Portfolio</h1>
    <nav>
      <a href="index.html">Inicio</a>
      <a href="#proyectos">Proyectos</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>Sobre Mí</h2>
      <p>Estudiante de Ingeniería Informática.</p>
    </article>
  </main>
  <aside>
    <h3>Enlaces Rápidos</h3>
    <p>GitHub | LinkedIn</p>
  </aside>
  <footer>
    <p>&copy; 2026 Alumno UA</p>
  </footer>
</body>
</html>
```

:::
::: {.column width="46%"}

\begin{center}
\begin{tikzpicture}
\node[font=\scriptsize\bfseries, color=black!75] at (2.5, 4.85) {En el Navegador solo con HTML (Sin CSS):};

% Moldura do Browser
\draw[thick, draw=black!70, fill=white, rounded corners=3pt] (0, 0.45) rectangle (5.0, 4.55);
\draw[thick, draw=black!70, fill=black!12, rounded corners=3pt] (0, 4.05) rectangle (5.0, 4.55);
\fill[white] (0.02, 4.03) rectangle (4.98, 4.10);
\draw[draw=black!50] (0, 4.05) -- (5.0, 4.05);
\fill[red!75] (0.22, 4.30) circle (0.07);
\fill[orange!80] (0.44, 4.30) circle (0.07);
\fill[uagreen!80!black] (0.66, 4.30) circle (0.07);
\node[font=\tiny\ttfamily, color=black!65, anchor=west] at (0.90, 4.30) {file:///.../index.html};

% Tudo empilhado à esquerda
\node[font=\small\bfseries, anchor=west] at (0.20, 3.68) {Mi Portfolio};
\node[font=\tiny, color=blue, anchor=west] at (0.20, 3.28) {\underline{Inicio} \hspace{4pt} \underline{Proyectos}};

\node[font=\footnotesize\bfseries, anchor=west] at (0.20, 2.75) {Sobre Mí};
\node[font=\tiny, anchor=west] at (0.20, 2.40) {Estudiante de Ingeniería Informática.};

\node[font=\scriptsize\bfseries, anchor=west] at (0.20, 1.85) {Enlaces Rápidos};
\node[font=\tiny, anchor=west] at (0.20, 1.52) {GitHub | LinkedIn};

\node[font=\tiny, anchor=west] at (0.20, 0.95) {\copyright\ 2026 Alumno UA};

% Anotações tracejadas
\draw[dashed, color=orange!80!black] (0.12, 3.12) rectangle (4.88, 3.92);
\node[font=\tiny\ttfamily, color=orange!85!black, anchor=east] at (4.85, 3.68) {<header>};

\draw[dashed, color=uagreen!75!black] (0.12, 2.22) rectangle (4.88, 3.00);
\node[font=\tiny\ttfamily, color=uagreen!60!black, anchor=east] at (4.85, 2.75) {<main>};

\draw[dashed, color=purple!75!black] (0.12, 1.35) rectangle (4.88, 2.10);
\node[font=\tiny\ttfamily, color=purple!80!black, anchor=east] at (4.85, 1.85) {<aside>};

\draw[dashed, color=teal!80!black] (0.12, 0.72) rectangle (4.88, 1.22);
\node[font=\tiny\ttfamily, color=teal!80!black, anchor=east] at (4.85, 0.95) {<footer>};

\node[rectangle, draw=orange!80!black, fill=orange!10, rounded corners=2pt, font=\tiny, align=center, inner sep=3pt] at (2.5, 0.08) {Estructura semántica lista, pero todo apilado $\rightarrow$ falta \textbf{CSS}!};
\end{tikzpicture}
\end{center}

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Estilización y Diseño con CSS}}
\end{center}

-----

## El Papel de CSS y la Separación de Responsabilidades

  * **CSS (*Cascading Style Sheets*):** Controla colores, fuentes, espaciado y disposición visual (*layout*).
  * **Separación de Responsabilidades (*Separation of Concerns*):**
      * **HTML ("Esqueleto"):** Estructura y contenido $\cdot$ **CSS ("Piel"):** Presentación visual (`style.css`).

\vspace{0.3em}

\begin{center}
\begin{tikzpicture}[
    card/.style={rectangle, rounded corners=2pt, draw=black!20, fill=white}
]
% --- Lado Esquerdo: Sem CSS ---
\node[font=\scriptsize\bfseries, color=black!70] at (2.1, 3.35) {1. Solo HTML5 (Sin CSS)};
\draw[thick, draw=black!65, fill=white, rounded corners=3pt] (0, 0) rectangle (4.2, 3.1);
\fill[black!12] (0.02, 2.75) rectangle (4.18, 3.08);
\draw[draw=black!50] (0, 2.75) -- (4.2, 2.75);
\fill[red!70] (0.2, 2.91) circle (0.06);
\fill[orange!80] (0.38, 2.91) circle (0.06);
\fill[uagreen!80!black] (0.56, 2.91) circle (0.06);

\node[font=\scriptsize\bfseries, anchor=west] at (0.15, 2.45) {Mi Portfolio};
\node[font=\tiny, color=blue, anchor=west] at (0.15, 2.12) {\underline{Inicio} \hspace{3pt} \underline{Proyectos}};
\node[font=\tiny\bfseries, anchor=west] at (0.15, 1.72) {Sobre Mí};
\node[font=\tiny, anchor=west] at (0.15, 1.42) {Estudiante de Ing. Informática.};
\node[font=\tiny\bfseries, anchor=west] at (0.15, 1.02) {Enlaces Rápidos};
\node[font=\tiny, anchor=west] at (0.15, 0.75) {GitHub | LinkedIn};
\node[font=\tiny, anchor=west] at (0.15, 0.32) {\copyright\ 2026 Alumno UA};

% Seta central
\draw[-{Latex[length=2.2mm]}, very thick, color=uagreen!80!black] (4.45, 1.55) -- node[above, font=\tiny\ttfamily\bfseries, color=black!80] {+ style.css} (5.55, 1.55);

% --- Lado Direito: Com CSS ---
\node[font=\scriptsize\bfseries, color=uagreen!60!black] at (7.9, 3.35) {2. El Mismo HTML5 + \texttt{style.css}};
\draw[thick, draw=black!65, fill=black!7, rounded corners=3pt] (5.8, 0) rectangle (10.0, 3.1);
\fill[black!15] (5.82, 2.75) rectangle (9.98, 3.08);
\draw[draw=black!50] (5.8, 2.75) -- (10.0, 2.75);
\fill[red!70] (6.0, 2.91) circle (0.06);
\fill[orange!80] (6.18, 2.91) circle (0.06);
\fill[uagreen!80!black] (6.36, 2.91) circle (0.06);

% Cartão Header centrado
\node[card, minimum width=3.6cm, minimum height=0.58cm] at (7.9, 2.32) {};
\node[font=\scriptsize\bfseries, color=blue!65!black, anchor=west] at (6.22, 2.43) {Mi Portfolio};
\node[font=\tiny\bfseries, color=blue!55!black, anchor=west] at (6.22, 2.16) {Inicio \hspace{6pt} Proyectos};

% Cartão Main + Aside lado a lado
\node[card, minimum width=2.45cm, minimum height=1.18cm] at (7.32, 1.32) {};
\fill[blue!60!black] (6.42, 1.32) circle (0.22);
\node[font=\tiny\bfseries, color=white] at (6.42, 1.32) {Yo};
\node[font=\tiny\bfseries, color=black!85, anchor=west] at (6.72, 1.62) {Sobre Mí};
\node[font=\tiny, color=black!70, align=left, text width=1.65cm, anchor=west] at (6.72, 1.22) {Estudiante de\\Ing. Informática.};

\node[card, minimum width=1.05cm, minimum height=1.18cm] at (9.18, 1.32) {};
\node[font=\tiny\bfseries, color=purple!80!black] at (9.18, 1.62) {Enlaces};
\node[font=\tiny, color=blue!65!black, align=center] at (9.18, 1.18) {GitHub\\LinkedIn};

% Cartão Footer
\node[card, minimum width=3.6cm, minimum height=0.38cm] at (7.9, 0.38) {};
\node[font=\tiny, color=black!55] at (7.9, 0.38) {\copyright\ 2026 Alumno UA --- Contacto};
\end{tikzpicture}
\end{center}

-----

## Anatomía de una Regla CSS y Selectores Fundamentales

\begin{center}
\begin{tikzpicture}[
    box/.style={rectangle, rounded corners=2pt, thick, font=\scriptsize\ttfamily, inner sep=4pt, minimum height=0.52cm},
    lbl/.style={font=\tiny\bfseries, align=center},
    arr/.style={-{Latex[length=1.3mm]}, thick}
]
\node[box, draw=purple!80!black, fill=purple!10] (sel) at (0.8, 0.9) {header h1};
\node[box, draw=black!60, fill=black!5, right=3pt of sel] (b1) {\{};
\node[box, draw=blue!75!black, fill=blue!10, right=3pt of b1] (prop) {color:};
\node[box, draw=uagreen!75!black, fill=uagreen!15, right=3pt of prop] (val) {\#004a8c;};
\node[box, draw=blue!75!black, fill=blue!10, right=6pt of val] (prop2) {font-size:};
\node[box, draw=uagreen!75!black, fill=uagreen!15, right=3pt of prop2] (val2) {24px;};
\node[box, draw=black!60, fill=black!5, right=3pt of val2] (b2) {\}};

\node[lbl, color=purple!80!black] (lsel) at (0.8, 0.08) {Selector ("Quién")};
\node[lbl, color=blue!75!black] (lprop) at (3.0, 0.08) {Propiedad};
\node[lbl, color=uagreen!65!black] (lval) at (4.5, 0.08) {Valor};
\node[lbl, color=black!70] (ldec) at (7.3, 0.08) {Declaración (\texttt{propiedad: valor;})};

\draw[arr, color=purple!80!black] (lsel.north) -- (sel.south);
\draw[arr, color=blue!75!black] (lprop.north) -- (prop.south);
\draw[arr, color=uagreen!65!black] (lval.north) -- (val.south);
\draw[arr, color=black!70] (ldec.north) -- (prop2.south);
\end{tikzpicture}
\end{center}

\vspace{-0.3em}

| Tipo de Selector | Sintaxis CSS | Ejemplo HTML | Objetivo Seleccionado |
| :--- | :--- | :--- | :--- |
| **Elemento (Tag)** | `p { ... }` | `<p>...</p>` | Todas las etiquetas `<p>`. |
| **Clase** | `.tarjeta { ... }` | `<article class="tarjeta">` | Todos los elementos con `class="tarjeta"`. |
| **ID** | `#inicio { ... }` | `<header id="inicio">` | El **único** elemento con `id="inicio"`. |
| **Descendiente** | `header h1 { ... }` | `<header><h1>...` | Etiquetas `<h1>` dentro de `<header>`. |
| **Agrupación** | `header, main, footer` | `<header>`, `<main>`... | Aplica el estilo a los 3 elementos. |
| **Pseudo-clase** | `a:hover { ... }` | `<a href="...">` | Enlace `<a>` al pasar el cursor por encima. |

-----

## La "C" de CSS: La Cascada y la Especificidad

::::: {.columns align=center}
::: {.column width="46%"}

**Orden de desempate:**

1. **Origen:** Tu `style.css` prevalece sobre el estilo por defecto del navegador.
2. **Especificidad:** El selector más específico gana.
3. **Orden:** A igual peso, gana la **última** regla.

:::
::: {.column width="54%"}

\begin{center}
\begin{tikzpicture}[scale=0.82, transform shape,
    tier/.style={trapezium, trapezium angle=72, draw=black!70, thick, align=center, font=\tiny\bfseries, minimum height=0.62cm, inner sep=2pt}
]
\node[font=\scriptsize\bfseries] at (0, 3.35) {Pirámide de Especificidad CSS};

% Nível 1: Inline
\node[tier, fill=red!20, draw=red!75!black, minimum width=2.2cm] at (0, 2.55) {1. Estilo Inline (\texttt{style="..."})\\{\tiny Peso: 1000}};

% Nível 2: ID
\node[tier, fill=orange!20, draw=orange!80!black, minimum width=3.2cm] at (0, 1.75) {2. Selector de ID (\texttt{\#mi-id})\\{\tiny Peso: 100}};

% Nível 3: Classe / Pseudo-classe
\node[tier, fill=uagreen!25, draw=uagreen!75!black, minimum width=4.2cm] at (0, 0.95) {3. Clase / Pseudo-clase (\texttt{.clase}, \texttt{:hover})\\{\tiny Peso: 10}};

% Nível 4: Elemento
\node[tier, fill=blue!15, draw=blue!75!black, minimum width=5.1cm] at (0, 0.15) {4. Elemento / Tag (\texttt{p}, \texttt{h1}, \texttt{header})\\{\tiny Peso: 1}};

\draw[-{Latex[length=1.8mm]}, very thick, color=red!75!black] (2.75, 0.0) -- node[right, font=\tiny\bfseries, align=left] {Mayor\\Prioridad} (2.75, 2.75);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{0.2em}

```css
/* ¿Cuál es el color final de <p id="intro" class="destacado">? */
#intro     { color: gold; }   /* ¡GANA! (ID = peso 100) */
.destacado { color: green; }  /* Clase = peso 10 */
p          { color: blue; }
p          { color: red; }    /* Gana a 'blue' por orden en el archivo (peso 1) */
```

-----

## Métodos de Integración CSS: Externo vs. Interno vs. En Línea

| Método | Sintaxis | Ventajas | Desventajas |
| :--- | :--- | :--- | :--- |
| **1. Externo (Recomendado)** | `<link rel="stylesheet" href="css/style.css">` en `<head>` | **Reutilizable** en todo el sitio, fácil mantenimiento y guardado en **caché**. | 1 petición HTTP extra en la 1.ª visita. |
| **2. Interno (*Embedded*)** | `<style> ... </style>` en `<head>` | Útil para pruebas rápidas en un único archivo. | No reutilizable en otras páginas. |
| **3. En Línea (*Inline* — ¡Evitar!)** | `<p style="color: red;">` | Solo para cambios dinámicos puntuales vía JS. | **Mezcla HTML y CSS**; difícil de mantener (peso 1000). |

\vspace{0.3em}

```html
<!-- Buena Práctica: Enlazar archivo externo en <head> -->
<head>
  <meta charset="UTF-8">
  <title>Mi Portfolio</title>
  <link rel="stylesheet" href="css/style.css">
</head>
```

-----

## El Modelo de Caja (*CSS Box Model*)

::::: {.columns align=center}
::: {.column width="50%"}

\begin{center}
\begin{tikzpicture}[scale=0.88, transform shape]
% Margin
\draw[dashed, thick, draw=orange!85!black, fill=orange!12, rounded corners=2pt] (0, 0) rectangle (5.4, 3.85);
\node[font=\tiny\bfseries, color=orange!85!black, anchor=north west] at (0.12, 3.78) {Margin (Espacio exterior transparente)};

% Border
\draw[very thick, draw=black!80, fill=black!15, rounded corners=4pt] (0.55, 0.45) rectangle (4.85, 3.30);
\node[font=\tiny\bfseries, color=black!85, anchor=north west] at (0.65, 3.24) {Border (Borde + \texttt{border-radius})};

% Padding
\draw[dashed, thick, draw=uagreen!70!black, fill=uagreen!18] (0.95, 0.80) rectangle (4.45, 2.75);
\node[font=\tiny\bfseries, color=uagreen!50!black, anchor=north west] at (1.03, 2.69) {Padding (Espacio interior con fondo)};

% Content
\draw[thick, draw=blue!75!black, fill=white] (1.38, 1.15) rectangle (4.02, 2.20);
\node[font=\scriptsize\bfseries, color=blue!80!black, align=center] at (2.70, 1.68) {Content (Contenido)\\{\tiny Texto / Imágenes (\texttt{width} $\times$ \texttt{height})}};

% Setas de margem horizontal
\draw[<->, >=Latex, thick, color=orange!85!black] (0, 1.68) -- node[above, font=\tiny\ttfamily] {auto} (0.55, 1.68);
\draw[<->, >=Latex, thick, color=orange!85!black] (4.85, 1.68) -- node[above, font=\tiny\ttfamily] {auto} (5.4, 1.68);
\end{tikzpicture}
\end{center}

:::
::: {.column width="50%"}

```css
.tarjeta {
  box-sizing: border-box; /* Incluye padding/border */
  max-width: 600px;       /* Anchura máxima */
  padding: 20px;          /* Espacio interior */
  border: 2px solid #ccc; /* Borde visible */
  border-radius: 8px;     /* Esquinas redondeadas */
  margin: 20px auto;      /* 'auto' centra bloque */
  background-color: #fff;
}
```

:::
:::::

\vspace{0.25em}

  * **Content & Padding:** El contenido y su espaciado interior (ambos heredan `background-color`).
  * **Border & Margin:** El marco visible de la caja y el espacio exterior transparente que separa elementos (`margin: 20px auto` centra horizontalmente).
  * **Buena Práctica (`box-sizing: border-box`):** Garantiza que `width`/`max-width` incluya `padding` y `border` (evita cajas más grandes de lo esperado).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Publicación con Docker/Nginx y Reverse Proxy}}
\end{center}

-----

## Publicar un Sitio Estático con Nginx y Docker Compose

::::: {.columns align=center}
::: {.column width="42%"}

```text
mi-portfolio/
├── docker-compose.yml
└── src/
    ├── index.html
    ├── css/style.css
    └── images/profile.jpg
```

**`docker-compose.yml`:**

```yaml
services:
  webserver:
    image: nginx:alpine
    container_name: portfolio_site
    ports:
      - "8080:80"
    volumes:
      - ./src:/usr/share/nginx/html:ro
```

:::
::: {.column width="58%"}

\begin{center}
\begin{tikzpicture}[scale=0.92, transform shape,
    box/.style={rectangle, rounded corners=3pt, thick, align=center},
    arr/.style={-{Latex[length=1.6mm]}, thick}
]
% Máquina Host
\draw[box, draw=black!70, fill=black!3] (0, 0) rectangle (6.80, 4.15);
\node[font=\scriptsize\bfseries, anchor=north west] at (0.15, 4.08) {Máquina Anfitriona (Host Linux / WSL)};

% Browser (alinhado com Nginx)
\node[box, draw=blue!75!black, fill=blue!10, font=\tiny\bfseries, minimum width=2.20cm, minimum height=0.62cm] (br) at (1.30, 2.55) {Navegador\\\texttt{http://localhost:8080}};

% Pasta Local ./src (alinhada com Pasta no Contentor)
\node[box, draw=orange!85!black, fill=orange!12, font=\tiny\ttfamily, minimum width=2.20cm, minimum height=1.10cm] (src) at (1.30, 0.95) {\textbf{Carpeta Local \texttt{./src}}\\\texttt{index.html}\\\texttt{css/style.css}\\\texttt{images/...}};

% Contentor Docker
\draw[box, draw=uagreen!75!black, fill=uagreen!10] (3.95, 0.25) rectangle (6.60, 3.68);
\node[font=\tiny\bfseries, color=uagreen!55!black] at (5.28, 3.48) {Contenedor Docker};
\node[font=\tiny\ttfamily, color=black!70] at (5.28, 3.22) {(nginx:alpine)};

% Porta 80 Nginx
\node[box, draw=uagreen!80!black, fill=white, font=\tiny\ttfamily\bfseries, minimum width=2.10cm, minimum height=0.55cm] (ngx) at (5.28, 2.55) {Nginx (:80)};

% Pasta dentro do contentor
\node[box, draw=orange!80!black, fill=white, font=\tiny\ttfamily, minimum width=2.10cm, minimum height=0.95cm] (cdir) at (5.28, 0.95) {\textbf{En Contenedor (:ro)}\\\texttt{/usr/share/}\\\texttt{nginx/html}};

% Ligações com espaço livre no corredor central
\draw[arr, color=blue!75!black] (br.east) -- node[above=2pt, pos=0.42, font=\tiny\ttfamily\bfseries] {8080:80} (ngx.west);
\draw[<->, >=Latex, very thick, dashed, color=orange!85!black] (src.east) -- node[above=2pt, pos=0.42, font=\tiny\bfseries] {Volumen} (cdir.west);
\draw[arr, color=uagreen!70!black] (cdir.north) -- node[right=2pt, font=\tiny] {Lee archivos} (ngx.south);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{1em}

  * **Ejecutar:** `docker compose up -d` (arranca el servidor web en segundo plano).
  * **Acceder:** Abrir `http://localhost:8080` en el navegador.
  * **Volumen `:ro` (*read-only*):** Mapea `./src` dentro del contenedor en modo solo lectura (buena práctica de seguridad).

-----

## Cómo Accede un Navegador a una Página (Flujo Extremo a Extremo)

\begin{center}
\begin{tikzpicture}[
    stepbox/.style={rectangle, rounded corners=3pt, draw=black!70, thick, font=\tiny, align=left, inner sep=3.5pt, minimum height=1.55cm},
    arr/.style={-{Latex[length=1.6mm]}, very thick, color=uagreen!80!black}
]
\node[stepbox, fill=blue!8, text width=2.15cm] (s1) at (0, 0) {
  \textbf{1. DNS y Conexión}\\
  $\bullet$ DNS: dominio $\rightarrow$ IP.\\
  $\bullet$ \textit{Handshake} TCP (:80/:443) + TLS si HTTPS.
};

\node[stepbox, fill=orange!10, text width=2.20cm, right=0.25cm of s1] (s2) {
  \textbf{2. Petición HTTP}\\
  $\bullet$ Navegador envía \texttt{GET /}.\\
  $\bullet$ Tráfico llega a \textbf{Nginx} (ej.: puerto Docker).
};

\node[stepbox, fill=uagreen!12, text width=2.25cm, right=0.25cm of s2] (s3) {
  \textbf{3. Respuesta HTTP}\\
  $\bullet$ Nginx lee \texttt{index.html} (volumen \texttt{./src}).\\
  $\bullet$ Devuelve \texttt{200 OK} + HTML.
};

\node[stepbox, fill=purple!10, text width=2.30cm, right=0.25cm of s3] (s4) {
  \textbf{4. DOM y Render}\\
  $\bullet$ Construye el árbol \textbf{DOM}.\\
  $\bullet$ Pide \texttt{style.css} e \texttt{<img>}, y dibuja la página.
};

\draw[arr] (s1.east) -- (s2.west);
\draw[arr] (s2.east) -- (s3.west);
\draw[arr] (s3.east) -- (s4.west);
\end{tikzpicture}
\end{center}

\vspace{0.2em}

::::: columns
::: {.column width="48%"}
**Petición HTTP (Paso 2):**
```http
GET / HTTP/1.1
Host: example.com
Accept: text/html
```
:::
::: {.column width="52%"}
**Respuesta HTTP (Paso 3):**
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html><html lang="es">...
```
:::
:::::

\vspace{0.2em}

  * **Nota (DevTools $\rightarrow$ *Network*):** Abrir 1 página genera **múltiples peticiones HTTP** (1 para HTML + 1 por cada archivo CSS, imagen o vídeo).

-----

## Arquitectura de Red: Forward Proxy vs. Reverse Proxy

¿Cómo exponer varios servicios web en la misma máquina usando solo el puerto público `80`/`443`?

\begin{center}
\begin{tikzpicture}[
    nodebox/.style={rectangle, rounded corners=3pt, draw=black!75, thick, font=\tiny\bfseries, align=center, inner sep=3.5pt},
    zone/.style={rectangle, rounded corners=4pt, dashed, thick},
    arr/.style={-{Latex[length=1.4mm]}, thick}
]
% --- Forward Proxy ---
\node[font=\scriptsize\bfseries, color=blue!75!black] at (2.4, 3.55) {1. Forward Proxy (Oculta al Cliente)};
\draw[zone, draw=blue!60!black, fill=blue!4] (0, 0.35) rectangle (3.1, 3.25);
\node[font=\tiny\itshape, color=blue!75!black] at (1.55, 0.55) {Red Interna (Escuela / Empresa)};

\node[nodebox, fill=white] (fc1) at (0.75, 2.55) {Cliente A};
\node[nodebox, fill=white] (fc2) at (0.75, 1.35) {Cliente B};
\node[nodebox, fill=blue!20, draw=blue!80!black, minimum height=1.5cm] (fp) at (2.35, 1.95) {Forward\\Proxy};
\node[nodebox, fill=black!10, minimum height=1.2cm] (fint) at (4.35, 1.95) {Internet\\{\tiny (ej.: Google)}};

\draw[arr, color=blue!75!black] (fc1.east) -- (fp.west);
\draw[arr, color=blue!75!black] (fc2.east) -- (fp.west);
\draw[arr, color=blue!75!black] (fp.east) -- (fint.west);

\node[font=\tiny, align=center, text width=4.8cm] at (2.4, -0.10) {Filtra tráfico de salida; Internet solo ve la IP del Proxy.};

\draw[dotted, thick, color=black!35] (5.35, 3.7) -- (5.35, -0.35);

% --- Reverse Proxy ---
\node[font=\scriptsize\bfseries, color=uagreen!60!black] at (8.2, 3.55) {2. Reverse Proxy (Oculta los Servidores)};
\node[nodebox, fill=black!10, minimum height=1.2cm] (rc) at (6.3, 1.95) {Clientes\\en Internet};

\draw[zone, draw=uagreen!75!black, fill=uagreen!6] (7.4, 0.35) rectangle (10.85, 3.25);
\node[font=\tiny\itshape, color=uagreen!55!black] at (9.12, 0.55) {Red Privada Docker};

\node[nodebox, fill=uagreen!25, draw=uagreen!80!black, minimum height=1.6cm] (rp) at (8.15, 1.95) {Reverse\\Proxy\\{\tiny (Nginx :80)}};
\node[nodebox, fill=white] (rs1) at (9.95, 2.60) {Sitio Estático\\{\tiny (HTML :80)}};
\node[nodebox, fill=white] (rs2) at (9.95, 1.30) {API FastAPI\\{\tiny (Clase 08 :8000)}};

\draw[arr, color=uagreen!70!black] (rc.east) -- (rp.west);
\draw[arr, color=uagreen!70!black] (rp.east) -- node[above, sloped, font=\tiny\ttfamily] {/} (rs1.west);
\draw[arr, color=orange!85!black] (rp.east) -- node[below, sloped, font=\tiny\ttfamily] {/api/} (rs2.west);

\node[font=\tiny, align=center, text width=5.2cm] at (8.2, -0.10) {El cliente habla solo con el Proxy; contenedores aislados.};
\end{tikzpicture}
\end{center}

-----

## Funciones del Reverse Proxy y Configuración (Docker + Nginx)

\begingroup\footnotesize

  * **Enrutamiento:** Redirige por ruta (`/`, `/api/`) o dominio en el puerto `80`.
  * **Load Balancing:** Distribuye peticiones entre varias réplicas internas.
  * **SSL & Caching:** Termina HTTPS en la entrada y almacena estáticos en caché.

\endgroup

\vspace{0.4em}

::::: {.columns align=T}
::: {.column width="54%"}

\begingroup\footnotesize `docker-compose.yml` *(solo el proxy es público):* \endgroup

```yaml
services:
  proxy:
    image: nginx:alpine
    ports: ["80:80"] # Único puerto público
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
  site:
    image: nginx:alpine # Privado (:80)
    volumes:
      - ./src:/usr/share/nginx/html:ro
  api:
    image: mi-api-fastapi # Privado (:8000)
```

:::
::: {.column width="46%"}

\begingroup\footnotesize `nginx.conf` *(enrutamiento):* \endgroup

```nginx
events {}
http {
  server {
    listen 80;
    location /api/ {
      proxy_pass http://api:8000;
    }
    location / {
      proxy_pass http://site:80;
    }
  }
}
```

:::
:::::

-----

## Síntesis Arquitectural y Recursos de Referencia

| Tecnología | Papel | Punto Clave |
| :--- | :--- | :--- |
| **HTML5 Semántico** | Estructura y Significado | `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>` (Accesibilidad y SEO). |
| **CSS3 y Box Model** | Presentación y Diseño | Archivo externo `style.css`; cajas con `content`, `padding`, `border` y `margin`. |
| **Nginx + Docker** | Publicación Web | Mapea puertos (`8080:80`) y monta `./src` en `/usr/share/nginx/html:ro`. |
| **Reverse Proxy** | Red y Arquitectura | Expone múltiples servicios internos (`/` y `/api/`, o varios dominios) en el puerto `80`. |

\vspace{0.4em}

  * **Documentación de Referencia:**
      * **MDN Web Docs (Mozilla):** Referencia oficial HTML, CSS y HTTP — [https://developer.mozilla.org/](https://developer.mozilla.org/)
      * **W3Schools:** Tutoriales y ejemplos interactivos — [https://www.w3schools.com/](https://www.w3schools.com/)
      * **Docker & Nginx Docs:** [https://docs.docker.com/](https://docs.docker.com/) y [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
