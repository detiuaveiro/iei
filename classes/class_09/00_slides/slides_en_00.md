---
title: 47138 - Introduction to Computer Engineering
subtitle: "Web Pages & Deployment"
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

## Session Overview

  * **Part I — Web Foundations & HTML5 Structure:**
      * Static web pages, tag anatomy, the **DOM** tree, visual content elements, and **HTML5 semantic tags**.
  * **Part II — Styling and Layout with CSS:**
      * Separation of structure/style, selectors, **Cascade/Specificity**, integration methods, and **CSS Box Model**.
  * **Part III — Deployment with Docker/Nginx & Reverse Proxy:**
      * **Nginx + Docker Compose** server, end-to-end HTTP request flow, and **Reverse Proxy** architecture.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: Web Foundations \& HTML5 Structure}}
\end{center}

-----

## What is a "Static" Web Page?

  * **Direct delivery:** Files served to the *browser* **exactly as stored** on the server.
  * **Fixed content:** Every user sees the exact same document (like a digital brochure).
  * **Server role (e.g., Nginx):** Locate the requested file (`GET /index.html`) and return it via HTTP.
  * **Core technologies:** **HTML** (structure and meaning) + **CSS** (style and layout).

\vspace{2em}

\begin{center}
\includegraphics[width=0.76\linewidth]{figures/static-website.png}
\end{center}

-----

## HTML: *HyperText Markup Language* & Tag Anatomy

  * **HyperText:** Text containing hyperlinks (*links*) connecting documents across the Web.
  * **Markup Language:** *Not* a programming language (no logic/loops); uses **tags** to structure content.

\vspace{0.4em}

\begin{center}
\begin{tikzpicture}[
    box/.style={rectangle, rounded corners=2pt, thick, font=\scriptsize\ttfamily, inner sep=4pt, minimum height=0.60cm},
    lbl/.style={font=\tiny\bfseries, align=center},
    arr/.style={-{Latex[length=1.4mm]}, thick}
]
% Elemento Normal
\node[font=\scriptsize\bfseries, anchor=west] at (-0.2, 2.10) {1. Element with Content:};

\node[box, draw=blue!75!black, fill=blue!8] (open) at (0.6, 1.35) {<a};
\node[box, draw=orange!80!black, fill=orange!10, right=2pt of open] (attr) {href="https://ua.pt"};
\node[box, draw=blue!75!black, fill=blue!8, right=2pt of attr] (openclose) {>};
\node[box, draw=uagreen!75!black, fill=uagreen!12, right=2pt of openclose] (content) {Universidade de Aveiro};
\node[box, draw=red!75!black, fill=red!8, right=2pt of content] (close) {</a>};

\node[lbl, color=blue!75!black] (l_open) at (0.6, 0.35) {Opening\\Tag};
\node[lbl, color=orange!85!black] (l_attr) at (2.5, 0.35) {Attribute\\(\texttt{name="value"})};
\node[lbl, color=uagreen!65!black] (l_cont) at (5.85, 0.35) {Visible\\Content};
\node[lbl, color=red!75!black] (l_close) at (8.3, 0.35) {Closing\\Tag (\texttt{</...>})};

\draw[arr, color=blue!75!black] (l_open.north) -- (open.south);
\draw[arr, color=orange!85!black] (l_attr.north) -- (attr.south);
\draw[arr, color=uagreen!65!black] (l_cont.north) -- (content.south);
\draw[arr, color=red!75!black] (l_close.north) -- (close.south);

% Elemento Vazio
\node[font=\scriptsize\bfseries, anchor=west] at (-0.2, -0.45) {2. Void / Empty Element (no closing tag):};
\node[box, draw=purple!75!black, fill=purple!8, anchor=west] at (0.2, -1.05) {<img src="logo.png" alt="UA Logo">};
\node[font=\tiny, color=black!70, anchor=west] at (5.7, -1.05) {(E.g.: \texttt{<img>}, \texttt{<meta>}, \texttt{<link>})};
\end{tikzpicture}
\end{center}

-----

## HTML5 Skeleton & The DOM Tree

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

  * **`<!DOCTYPE html>`:** Activates HTML5 standards mode in the *browser*.
  * **`<head>` (Invisible on page):** Document metadata (e.g., `<title>` in the *browser* tab).
  * **`<body>` (Visible in window):** Contains all elements rendered on screen (`<h1>`, `<p>`, images, etc.).
  * **DOM Tree (*Document Object Model*):** Hierarchical tree of nodes built in memory by the *browser* to display and manipulate the page.

-----

## Visual Content Elements I: Typography, Text & Hyperlinks

::::: {.columns align=center}
::: {.column width="48%"}

```html
<h1>Main Heading (H1)</h1>
<h2>Page Subsection (H2)</h2>

<p>
  Text with <strong>importance</strong>
  and with <em>emphasis</em>.
</p>

<p>
  Visit <a href="https://www.ua.pt">UA</a>
  or contact
  <a href="mailto:student@ua.pt">student@ua.pt</a>.
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
\node[font=\normalsize\bfseries, anchor=west] at (0.25, 3.25) {Main Heading (H1)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 3.25) {<h1>};

\node[font=\footnotesize\bfseries, anchor=west] at (0.25, 2.65) {Page Subsection (H2)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.65) {<h2>};

\node[font=\scriptsize, align=left, text width=4.3cm, anchor=north west] at (0.25, 2.25) {Text with \textbf{importance} and with \textit{emphasis}.};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.00) {<p>};

\node[font=\scriptsize, align=left, text width=4.3cm, anchor=north west] at (0.25, 1.35) {Visit \textcolor{blue}{\underline{UA}} or contact \textcolor{blue}{\underline{student@ua.pt}}.};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 1.10) {<a>};

\draw[dashed, color=black!25] (0.2, 0.45) -- (5.3, 0.45);
\node[font=\tiny\itshape, color=black!60] at (2.75, 0.22) {Native Browser Rendering (without CSS)};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<h1>`–`<h6>`:** Heading hierarchy (use only one main `<h1>` per page).
  * **`<p>`:** Paragraph block with automatic vertical spacing.
  * **`<strong>` / `<em>`:** Semantic emphasis (bold and italic).
  * **`<a href="...">`:** Hyperlink to URLs, local files, or emails (`mailto:`).

-----

## Visual Content Elements II: Lists & Tables

::::: {.columns align=center}
::: {.column width="48%"}

```html
<!-- Unordered and Ordered Lists -->
<ul>
  <li>HTML5 (Structure)</li>
  <li>CSS3 (Style)</li>
</ul>
<ol>
  <li>Create index.html</li>
  <li>Deploy on Nginx</li>
</ol>

<!-- Data Table -->
<table>
  <thead>
    <tr><th>Service</th><th>Port</th></tr>
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
\node[font=\tiny\ttfamily, color=black!65, anchor=west] at (1.15, 4.42) {http://localhost:8080/lists.html};

% Lista ul
\node[font=\scriptsize, anchor=west] at (0.4, 3.72) {$\bullet$ HTML5 (Structure)};
\node[font=\scriptsize, anchor=west] at (0.4, 3.38) {$\bullet$ CSS3 (Style)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 3.55) {<ul> / <li>};

\draw[dotted, color=black!25] (0.25, 3.10) -- (5.25, 3.10);

% Lista ol
\node[font=\scriptsize, anchor=west] at (0.4, 2.75) {1. Create index.html};
\node[font=\scriptsize, anchor=west] at (0.4, 2.40) {2. Deploy on Nginx};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.57) {<ol> / <li>};

\draw[dotted, color=black!25] (0.25, 2.10) -- (5.25, 2.10);

% Tabela renderizada
\draw[thick, draw=black!60, fill=black!8] (0.4, 1.45) rectangle (2.1, 1.85);
\draw[thick, draw=black!60, fill=black!8] (2.1, 1.45) rectangle (3.4, 1.85);
\node[font=\scriptsize\bfseries] at (1.25, 1.65) {Service};
\node[font=\scriptsize\bfseries] at (2.75, 1.65) {Port};

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

\node[font=\tiny\itshape, color=black!60] at (2.75, 0.25) {Lists and tables rendered in Browser};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<ul>` / `<ol>`:** Unordered (bullet) and ordered (numbered) lists, with `<li>` items.
  * **`<table>`:** Tabular layout split into header (`<thead>` / `<th>`) and body (`<tbody>` / `<td>`), organized by rows (`<tr>`).

-----

## Native HTML5 Media: `<img>`, `<figure>`, `<audio>` & `<video>`

::::: {.columns align=center}
::: {.column width="50%"}

```html
<!-- Image with Caption -->
<figure>
  <img src="images/profile.jpg"
       alt="Profile photo" width="150">
  <figcaption>Fig 1. IEI Student.</figcaption>
</figure>

<!-- Native Audio and Video -->
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
\node[font=\tiny\itshape, color=black!75] at (1.4, 3.03) {Fig 1. IEI Student.};

% Imagem partida (fallback alt)
\draw[dashed, draw=red!60!black, fill=red!4, rounded corners=2pt] (2.75, 2.85) rectangle (5.05, 4.25);
\node[font=\tiny\bfseries, color=red!70!black] at (3.9, 3.98) {If missing (Error 404):};
\draw[draw=black!50, fill=white] (2.95, 3.50) rectangle (3.30, 3.78);
\node[font=\tiny, color=red!75!black] at (3.12, 3.64) {X};
\node[font=\tiny, align=left, text width=1.55cm, anchor=west] at (3.35, 3.55) {"Profile photo" (\texttt{alt})};

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

  * **`src` & `alt`:** File path and alternative text (essential for accessibility and 404 errors).
  * **`controls` & `<source>`:** Native player buttons; the *browser* plays the first supported format.

-----

## HTML5 Semantic Architecture: The 7 Containers

::::: {.columns align=center}
::: {.column width="62%"}

| Tag | Purpose | Rule / Example |
| :--- | :--- | :--- |
| **`<header>`** | Page (or article) header. | Logo and `<h1>` (**$\neq$ `<head>`!**). |
| **`<nav>`** | Main navigation block. | Primary menu (`<ul>` with links). |
| **`<main>`** | Core unique content. | **Only one `<main>`** per page. |
| **`<article>`** | **Standalone** content. | Blog post, news, card (*self-contained?*). |
| **`<section>`** | **Thematic** grouping. | Subsection ("About Me", with `<h2>`). |
| **`<aside>`** | Complementary content. | *Sidebar*, related links, author bio. |
| **`<footer>`** | Page or section footer. | Copyright (`&copy;`), contact links. |

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
\node[font=\tiny\ttfamily\bfseries, color=purple!80!black, align=center] at (6.41, 1.96) {<aside>\\{\tiny (Sidebar)}};

% Footer
\node[blk, draw=teal!80!black, fill=teal!15, minimum width=3.0cm, minimum height=0.50cm] at (5.35, 0.48) {<footer>};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{0.2em}

  * **Benefits:** Improve **Accessibility** (screen readers), **SEO**, and code readability.
  * **Note:** They define **meaning**, not layout — without CSS, containers stack vertically.

-----

## Putting It Together: Semantic HTML5 vs. Unstyled Rendering

::::: columns
::: {.column width="54%"}

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IEI Portfolio</title>
</head>
<body>
  <header>
    <h1>My Portfolio</h1>
    <nav>
      <a href="index.html">Home</a>
      <a href="#projects">Projects</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>About Me</h2>
      <p>Computer Engineering student.</p>
    </article>
  </main>
  <aside>
    <h3>Quick Links</h3>
    <p>GitHub | LinkedIn</p>
  </aside>
  <footer>
    <p>&copy; 2026 UA Student</p>
  </footer>
</body>
</html>
```

:::
::: {.column width="46%"}

\begin{center}
\begin{tikzpicture}
\node[font=\scriptsize\bfseries, color=black!75] at (2.5, 4.85) {In Browser with HTML only (No CSS):};

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
\node[font=\small\bfseries, anchor=west] at (0.20, 3.68) {My Portfolio};
\node[font=\tiny, color=blue, anchor=west] at (0.20, 3.28) {\underline{Home} \hspace{4pt} \underline{Projects}};

\node[font=\footnotesize\bfseries, anchor=west] at (0.20, 2.75) {About Me};
\node[font=\tiny, anchor=west] at (0.20, 2.40) {Computer Engineering student.};

\node[font=\scriptsize\bfseries, anchor=west] at (0.20, 1.85) {Quick Links};
\node[font=\tiny, anchor=west] at (0.20, 1.52) {GitHub | LinkedIn};

\node[font=\tiny, anchor=west] at (0.20, 0.95) {\copyright\ 2026 UA Student};

% Anotações tracejadas
\draw[dashed, color=orange!80!black] (0.12, 3.12) rectangle (4.88, 3.92);
\node[font=\tiny\ttfamily, color=orange!85!black, anchor=east] at (4.85, 3.68) {<header>};

\draw[dashed, color=uagreen!75!black] (0.12, 2.22) rectangle (4.88, 3.00);
\node[font=\tiny\ttfamily, color=uagreen!60!black, anchor=east] at (4.85, 2.75) {<main>};

\draw[dashed, color=purple!75!black] (0.12, 1.35) rectangle (4.88, 2.10);
\node[font=\tiny\ttfamily, color=purple!80!black, anchor=east] at (4.85, 1.85) {<aside>};

\draw[dashed, color=teal!80!black] (0.12, 0.72) rectangle (4.88, 1.22);
\node[font=\tiny\ttfamily, color=teal!80!black, anchor=east] at (4.85, 0.95) {<footer>};

\node[rectangle, draw=orange!80!black, fill=orange!10, rounded corners=2pt, font=\tiny, align=center, inner sep=3pt] at (2.5, 0.08) {Semantic structure ready, but all stacked $\rightarrow$ missing \textbf{CSS}!};
\end{tikzpicture}
\end{center}

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part II: Styling and Layout with CSS}}
\end{center}

-----

## The Role of CSS & Separation of Concerns

  * **CSS (*Cascading Style Sheets*):** Controls colors, fonts, spacing, and visual *layout*.
  * **Separation of Concerns:**
      * **HTML ("Skeleton"):** Structure and content $\cdot$ **CSS ("Skin"):** Visual presentation (`style.css`).

\vspace{0.3em}

\begin{center}
\begin{tikzpicture}[
    card/.style={rectangle, rounded corners=2pt, draw=black!20, fill=white}
]
% --- Lado Esquerdo: Sem CSS ---
\node[font=\scriptsize\bfseries, color=black!70] at (2.1, 3.35) {1. HTML5 Only (No CSS)};
\draw[thick, draw=black!65, fill=white, rounded corners=3pt] (0, 0) rectangle (4.2, 3.1);
\fill[black!12] (0.02, 2.75) rectangle (4.18, 3.08);
\draw[draw=black!50] (0, 2.75) -- (4.2, 2.75);
\fill[red!70] (0.2, 2.91) circle (0.06);
\fill[orange!80] (0.38, 2.91) circle (0.06);
\fill[uagreen!80!black] (0.56, 2.91) circle (0.06);

\node[font=\scriptsize\bfseries, anchor=west] at (0.15, 2.45) {My Portfolio};
\node[font=\tiny, color=blue, anchor=west] at (0.15, 2.12) {\underline{Home} \hspace{3pt} \underline{Projects}};
\node[font=\tiny\bfseries, anchor=west] at (0.15, 1.72) {About Me};
\node[font=\tiny, anchor=west] at (0.15, 1.42) {Computer Engineering student.};
\node[font=\tiny\bfseries, anchor=west] at (0.15, 1.02) {Quick Links};
\node[font=\tiny, anchor=west] at (0.15, 0.75) {GitHub | LinkedIn};
\node[font=\tiny, anchor=west] at (0.15, 0.32) {\copyright\ 2026 UA Student};

% Seta central
\draw[-{Latex[length=2.2mm]}, very thick, color=uagreen!80!black] (4.45, 1.55) -- node[above, font=\tiny\ttfamily\bfseries, color=black!80] {+ style.css} (5.55, 1.55);

% --- Lado Direito: Com CSS ---
\node[font=\scriptsize\bfseries, color=uagreen!60!black] at (7.9, 3.35) {2. Same HTML5 + \texttt{style.css}};
\draw[thick, draw=black!65, fill=black!7, rounded corners=3pt] (5.8, 0) rectangle (10.0, 3.1);
\fill[black!15] (5.82, 2.75) rectangle (9.98, 3.08);
\draw[draw=black!50] (5.8, 2.75) -- (10.0, 2.75);
\fill[red!70] (6.0, 2.91) circle (0.06);
\fill[orange!80] (6.18, 2.91) circle (0.06);
\fill[uagreen!80!black] (6.36, 2.91) circle (0.06);

% Cartão Header centrado
\node[card, minimum width=3.6cm, minimum height=0.58cm] at (7.9, 2.32) {};
\node[font=\scriptsize\bfseries, color=blue!65!black, anchor=west] at (6.22, 2.43) {My Portfolio};
\node[font=\tiny\bfseries, color=blue!55!black, anchor=west] at (6.22, 2.16) {Home \hspace{6pt} Projects};

% Cartão Main + Aside lado a lado
\node[card, minimum width=2.45cm, minimum height=1.18cm] at (7.32, 1.32) {};
\fill[blue!60!black] (6.42, 1.32) circle (0.22);
\node[font=\tiny\bfseries, color=white] at (6.42, 1.32) {Me};
\node[font=\tiny\bfseries, color=black!85, anchor=west] at (6.72, 1.62) {About Me};
\node[font=\tiny, color=black!70, align=left, text width=1.65cm, anchor=west] at (6.72, 1.22) {Computer Eng.\\student.};

\node[card, minimum width=1.05cm, minimum height=1.18cm] at (9.18, 1.32) {};
\node[font=\tiny\bfseries, color=purple!80!black] at (9.18, 1.62) {Links};
\node[font=\tiny, color=blue!65!black, align=center] at (9.18, 1.18) {GitHub\\LinkedIn};

% Cartão Footer
\node[card, minimum width=3.6cm, minimum height=0.38cm] at (7.9, 0.38) {};
\node[font=\tiny, color=black!55] at (7.9, 0.38) {\copyright\ 2026 UA Student --- Contact};
\end{tikzpicture}
\end{center}

-----

## Anatomy of a CSS Rule & Fundamental Selectors

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

\node[lbl, color=purple!80!black] (lsel) at (0.8, 0.08) {Selector ("Who")};
\node[lbl, color=blue!75!black] (lprop) at (3.0, 0.08) {Property};
\node[lbl, color=uagreen!65!black] (lval) at (4.5, 0.08) {Value};
\node[lbl, color=black!70] (ldec) at (7.3, 0.08) {Declaration (\texttt{property: value;})};

\draw[arr, color=purple!80!black] (lsel.north) -- (sel.south);
\draw[arr, color=blue!75!black] (lprop.north) -- (prop.south);
\draw[arr, color=uagreen!65!black] (lval.north) -- (val.south);
\draw[arr, color=black!70] (ldec.north) -- (prop2.south);
\end{tikzpicture}
\end{center}

\vspace{-0.3em}

| Selector Type | CSS Syntax | HTML Example | Matched Target |
| :--- | :--- | :--- | :--- |
| **Element (Tag)** | `p { ... }` | `<p>...</p>` | All `<p>` tags. |
| **Class** | `.card { ... }` | `<article class="card">` | All elements with `class="card"`. |
| **ID** | `#top { ... }` | `<header id="top">` | The **unique** element with `id="top"`. |
| **Descendant** | `header h1 { ... }` | `<header><h1>...` | `<h1>` tags inside `<header>`. |
| **Grouping** | `header, main, footer` | `<header>`, `<main>`... | Applies style to all 3 elements. |
| **Pseudo-class** | `a:hover { ... }` | `<a href="...">` | `<a>` link when hovered by cursor. |

-----

## The "C" in CSS: Cascade & Specificity

::::: {.columns align=center}
::: {.column width="46%"}

**Tie-breaking order:**

1. **Origin:** Your `style.css` overrides default *browser* styles.
2. **Specificity:** The most specific selector wins.
3. **Source Order:** On equal weight, the **last** rule wins.

:::
::: {.column width="54%"}

\begin{center}
\begin{tikzpicture}[scale=0.82, transform shape,
    tier/.style={trapezium, trapezium angle=72, draw=black!70, thick, align=center, font=\tiny\bfseries, minimum height=0.62cm, inner sep=2pt}
]
\node[font=\scriptsize\bfseries] at (0, 3.35) {CSS Specificity Pyramid};

% Nível 1: Inline
\node[tier, fill=red!20, draw=red!75!black, minimum width=2.2cm] at (0, 2.55) {1. Inline Style (\texttt{style="..."})\\{\tiny Weight: 1000}};

% Nível 2: ID
\node[tier, fill=orange!20, draw=orange!80!black, minimum width=3.2cm] at (0, 1.75) {2. ID Selector (\texttt{\#my-id})\\{\tiny Weight: 100}};

% Nível 3: Classe / Pseudo-classe
\node[tier, fill=uagreen!25, draw=uagreen!75!black, minimum width=4.2cm] at (0, 0.95) {3. Class / Pseudo-class (\texttt{.class}, \texttt{:hover})\\{\tiny Weight: 10}};

% Nível 4: Elemento
\node[tier, fill=blue!15, draw=blue!75!black, minimum width=5.1cm] at (0, 0.15) {4. Element / Tag (\texttt{p}, \texttt{h1}, \texttt{header})\\{\tiny Weight: 1}};

\draw[-{Latex[length=1.8mm]}, very thick, color=red!75!black] (2.75, 0.0) -- node[right, font=\tiny\bfseries, align=left] {Highest\\Priority} (2.75, 2.75);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{0.2em}

```css
/* What is the final color of <p id="intro" class="highlight">? */
#intro     { color: gold; }   /* WINS! (ID = weight 100) */
.highlight { color: green; }  /* Class = weight 10 */
p          { color: blue; }
p          { color: red; }    /* Beats 'blue' by file order (weight 1) */
```

-----

## CSS Integration Methods: External vs. Internal vs. Inline

| Method | Syntax | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **1. External (Recommended)** | `<link rel="stylesheet" href="css/style.css">` in `<head>` | **Reusable** site-wide, easy to maintain, and **cached**. | 1 extra HTTP request on first visit. |
| **2. Internal (*Embedded*)** | `<style> ... </style>` inside `<head>` | Useful for quick single-file tests. | Not reusable across other pages. |
| **3. Inline (Avoid!)** | `<p style="color: red;">` | Only for isolated dynamic JS tweaks. | **Mixes HTML & CSS**; hard to maintain (weight 1000). |

\vspace{0.3em}

```html
<!-- Best Practice: Link external stylesheet inside <head> -->
<head>
  <meta charset="UTF-8">
  <title>My Portfolio</title>
  <link rel="stylesheet" href="css/style.css">
</head>
```

-----

## The Box Model (*CSS Box Model*)

::::: {.columns align=center}
::: {.column width="50%"}

\begin{center}
\begin{tikzpicture}[scale=0.88, transform shape]
% Margin
\draw[dashed, thick, draw=orange!85!black, fill=orange!12, rounded corners=2pt] (0, 0) rectangle (5.4, 3.85);
\node[font=\tiny\bfseries, color=orange!85!black, anchor=north west] at (0.12, 3.78) {Margin (Transparent outer space)};

% Border
\draw[very thick, draw=black!80, fill=black!15, rounded corners=4pt] (0.55, 0.45) rectangle (4.85, 3.30);
\node[font=\tiny\bfseries, color=black!85, anchor=north west] at (0.65, 3.24) {Border (Frame + \texttt{border-radius})};

% Padding
\draw[dashed, thick, draw=uagreen!70!black, fill=uagreen!18] (0.95, 0.80) rectangle (4.45, 2.75);
\node[font=\tiny\bfseries, color=uagreen!50!black, anchor=north west] at (1.03, 2.69) {Padding (Inner space with background)};

% Content
\draw[thick, draw=blue!75!black, fill=white] (1.38, 1.15) rectangle (4.02, 2.20);
\node[font=\scriptsize\bfseries, color=blue!80!black, align=center] at (2.70, 1.68) {Content\\{\tiny Text / Images (\texttt{width} $\times$ \texttt{height})}};

% Setas de margem horizontal
\draw[<->, >=Latex, thick, color=orange!85!black] (0, 1.68) -- node[above, font=\tiny\ttfamily] {auto} (0.55, 1.68);
\draw[<->, >=Latex, thick, color=orange!85!black] (4.85, 1.68) -- node[above, font=\tiny\ttfamily] {auto} (5.4, 1.68);
\end{tikzpicture}
\end{center}

:::
::: {.column width="50%"}

```css
.card {
  box-sizing: border-box; /* Includes padding/border */
  max-width: 600px;       /* Maximum width */
  padding: 20px;          /* Inner spacing */
  border: 2px solid #ccc; /* Visible border */
  border-radius: 8px;     /* Rounded corners */
  margin: 20px auto;      /* 'auto' centers block */
  background-color: #fff;
}
```

:::
:::::

\vspace{0.25em}

  * **Content & Padding:** The content and its inner spacing (both inherit `background-color`).
  * **Border & Margin:** The box's visible frame and outer transparent space separating elements (`margin: 20px auto` centers horizontally).
  * **Best Practice (`box-sizing: border-box`):** Ensures `width`/`max-width` already includes `padding` and `border` (prevents oversized boxes).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: Deployment with Docker/Nginx \& Reverse Proxy}}
\end{center}

-----

## Deploying a Static Site with Nginx & Docker Compose

::::: {.columns align=center}
::: {.column width="42%"}

```text
my-portfolio/
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
\node[font=\scriptsize\bfseries, anchor=north west] at (0.15, 4.08) {Host Machine (Linux / macOS / WSL)};

% Browser (alinhado com Nginx)
\node[box, draw=blue!75!black, fill=blue!10, font=\tiny\bfseries, minimum width=2.20cm, minimum height=0.62cm] (br) at (1.30, 2.55) {Browser\\\texttt{http://localhost:8080}};

% Pasta Local ./src (alinhada com Pasta no Contentor)
\node[box, draw=orange!85!black, fill=orange!12, font=\tiny\ttfamily, minimum width=2.20cm, minimum height=1.10cm] (src) at (1.30, 0.95) {\textbf{Local Folder \texttt{./src}}\\\texttt{index.html}\\\texttt{css/style.css}\\\texttt{images/...}};

% Contentor Docker
\draw[box, draw=uagreen!75!black, fill=uagreen!10] (3.95, 0.25) rectangle (6.60, 3.68);
\node[font=\tiny\bfseries, color=uagreen!55!black] at (5.28, 3.48) {Docker Container};
\node[font=\tiny\ttfamily, color=black!70] at (5.28, 3.22) {(nginx:alpine)};

% Porta 80 Nginx
\node[box, draw=uagreen!80!black, fill=white, font=\tiny\ttfamily\bfseries, minimum width=2.10cm, minimum height=0.55cm] (ngx) at (5.28, 2.55) {Nginx (:80)};

% Pasta dentro do contentor
\node[box, draw=orange!80!black, fill=white, font=\tiny\ttfamily, minimum width=2.10cm, minimum height=0.95cm] (cdir) at (5.28, 0.95) {\textbf{In Container (:ro)}\\\texttt{/usr/share/}\\\texttt{nginx/html}};

% Ligações com espaço livre no corredor central
\draw[arr, color=blue!75!black] (br.east) -- node[above=2pt, pos=0.42, font=\tiny\ttfamily\bfseries] {8080:80} (ngx.west);
\draw[<->, >=Latex, very thick, dashed, color=orange!85!black] (src.east) -- node[above=2pt, pos=0.42, font=\tiny\bfseries] {Volume} (cdir.west);
\draw[arr, color=uagreen!70!black] (cdir.north) -- node[right=2pt, font=\tiny] {Reads files} (ngx.south);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{1em}

  * **Run:** `docker compose up -d` (starts the web server in the background).
  * **Access:** Open `http://localhost:8080` in the *browser*.
  * **Volume `:ro` (*read-only*):** Mounts `./src` inside the container as read-only (security best practice).

-----

## How a Browser Accesses a Page (End-to-End Flow)

\begin{center}
\begin{tikzpicture}[
    stepbox/.style={rectangle, rounded corners=3pt, draw=black!70, thick, font=\tiny, align=left, inner sep=3.5pt, minimum height=1.55cm},
    arr/.style={-{Latex[length=1.6mm]}, very thick, color=uagreen!80!black}
]
\node[stepbox, fill=blue!8, text width=2.15cm] (s1) at (0, 0) {
  \textbf{1. DNS \& Connect}\\
  $\bullet$ DNS: domain $\rightarrow$ IP.\\
  $\bullet$ TCP \textit{Handshake} (:80/:443) + TLS if HTTPS.
};

\node[stepbox, fill=orange!10, text width=2.20cm, right=0.25cm of s1] (s2) {
  \textbf{2. HTTP Request}\\
  $\bullet$ Browser sends \texttt{GET /}.\\
  $\bullet$ Traffic reaches \textbf{Nginx} (e.g., Docker port).
};

\node[stepbox, fill=uagreen!12, text width=2.25cm, right=0.25cm of s2] (s3) {
  \textbf{3. HTTP Response}\\
  $\bullet$ Nginx reads \texttt{index.html} (volume \texttt{./src}).\\
  $\bullet$ Returns \texttt{200 OK} + HTML.
};

\node[stepbox, fill=purple!10, text width=2.30cm, right=0.25cm of s3] (s4) {
  \textbf{4. DOM \& Render}\\
  $\bullet$ Builds the \textbf{DOM} tree.\\
  $\bullet$ Fetches \texttt{style.css} \& \texttt{<img>}, then paints page.
};

\draw[arr] (s1.east) -- (s2.west);
\draw[arr] (s2.east) -- (s3.west);
\draw[arr] (s3.east) -- (s4.west);
\end{tikzpicture}
\end{center}

\vspace{0.2em}

::::: columns
::: {.column width="48%"}
**HTTP Request (Step 2):**
```http
GET / HTTP/1.1
Host: example.com
Accept: text/html
```
:::
::: {.column width="52%"}
**HTTP Response (Step 3):**
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html><html lang="en">...
```
:::
:::::

\vspace{0.2em}

  * **Note (DevTools $\rightarrow$ *Network*):** Loading 1 page generates **multiple HTTP requests** (1 for HTML + 1 per CSS, image, or video file).

-----

## Network Architecture: Forward Proxy vs. Reverse Proxy

How do we expose multiple web services on the same machine using only public port `80`/`443`?

\begin{center}
\begin{tikzpicture}[
    nodebox/.style={rectangle, rounded corners=3pt, draw=black!75, thick, font=\tiny\bfseries, align=center, inner sep=3.5pt},
    zone/.style={rectangle, rounded corners=4pt, dashed, thick},
    arr/.style={-{Latex[length=1.4mm]}, thick}
]
% --- Forward Proxy ---
\node[font=\scriptsize\bfseries, color=blue!75!black] at (2.4, 3.55) {1. Forward Proxy (Hides the Client)};
\draw[zone, draw=blue!60!black, fill=blue!4] (0, 0.35) rectangle (3.1, 3.25);
\node[font=\tiny\itshape, color=blue!75!black] at (1.55, 0.55) {Internal Network (School / Corp)};

\node[nodebox, fill=white] (fc1) at (0.75, 2.55) {Client A};
\node[nodebox, fill=white] (fc2) at (0.75, 1.35) {Client B};
\node[nodebox, fill=blue!20, draw=blue!80!black, minimum height=1.5cm] (fp) at (2.35, 1.95) {Forward\\Proxy};
\node[nodebox, fill=black!10, minimum height=1.2cm] (fint) at (4.35, 1.95) {Internet\\{\tiny (e.g., Google)}};

\draw[arr, color=blue!75!black] (fc1.east) -- (fp.west);
\draw[arr, color=blue!75!black] (fc2.east) -- (fp.west);
\draw[arr, color=blue!75!black] (fp.east) -- (fint.west);

\node[font=\tiny, align=center, text width=4.8cm] at (2.4, -0.10) {Filters outbound traffic; Internet only sees the Proxy's IP.};

\draw[dotted, thick, color=black!35] (5.35, 3.7) -- (5.35, -0.35);

% --- Reverse Proxy ---
\node[font=\scriptsize\bfseries, color=uagreen!60!black] at (8.2, 3.55) {2. Reverse Proxy (Hides the Servers)};
\node[nodebox, fill=black!10, minimum height=1.2cm] (rc) at (6.3, 1.95) {Clients\\on Internet};

\draw[zone, draw=uagreen!75!black, fill=uagreen!6] (7.4, 0.35) rectangle (10.85, 3.25);
\node[font=\tiny\itshape, color=uagreen!55!black] at (9.12, 0.55) {Private Docker Network};

\node[nodebox, fill=uagreen!25, draw=uagreen!80!black, minimum height=1.6cm] (rp) at (8.15, 1.95) {Reverse\\Proxy\\{\tiny (Nginx :80)}};
\node[nodebox, fill=white] (rs1) at (9.95, 2.60) {Static Site\\{\tiny (HTML :80)}};
\node[nodebox, fill=white] (rs2) at (9.95, 1.30) {FastAPI API\\{\tiny (Class 08 :8000)}};

\draw[arr, color=uagreen!70!black] (rc.east) -- (rp.west);
\draw[arr, color=uagreen!70!black] (rp.east) -- node[above, sloped, font=\tiny\ttfamily] {/} (rs1.west);
\draw[arr, color=orange!85!black] (rp.east) -- node[below, sloped, font=\tiny\ttfamily] {/api/} (rs2.west);

\node[font=\tiny, align=center, text width=5.2cm] at (8.2, -0.10) {Client talks only to Proxy; containers stay isolated.};
\end{tikzpicture}
\end{center}

-----

## Reverse Proxy Functions & Configuration (Docker + Nginx)

\begingroup\footnotesize

  * **Routing:** Forwards requests by path (`/`, `/api/`) or domain on port `80`.
  * **Load Balancing:** Distributes traffic across multiple internal replicas.
  * **SSL & Caching:** Terminates HTTPS at the edge and caches static assets.

\endgroup

\vspace{0.4em}

::::: {.columns align=T}
::: {.column width="54%"}

\begingroup\footnotesize `docker-compose.yml` *(only proxy is public):* \endgroup

```yaml
services:
  proxy:
    image: nginx:alpine
    ports: ["80:80"] # Only public port
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
  site:
    image: nginx:alpine # Private (:80)
    volumes:
      - ./src:/usr/share/nginx/html:ro
  api:
    image: my-fastapi-api # Private (:8000)
```

:::
::: {.column width="46%"}

\begingroup\footnotesize `nginx.conf` *(routing rules):* \endgroup

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

## Architectural Summary & Reference Resources

| Technology | Role | Key Takeaway |
| :--- | :--- | :--- |
| **Semantic HTML5** | Structure & Meaning | `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>` (Accessibility & SEO). |
| **CSS3 & Box Model** | Presentation & Layout | External `style.css`; boxes built from `content`, `padding`, `border`, and `margin`. |
| **Nginx + Docker** | Web Deployment | Maps ports (`8080:80`) and mounts `./src` to `/usr/share/nginx/html:ro`. |
| **Reverse Proxy** | Network & Architecture | Exposes multiple internal services (`/` and `/api/`, or domains) on port `80`. |

\vspace{0.4em}

  * **Reference Documentation:**
      * **MDN Web Docs (Mozilla):** Official reference for HTML, CSS, and HTTP — [https://developer.mozilla.org/](https://developer.mozilla.org/)
      * **W3Schools:** Interactive tutorials and examples — [https://www.w3schools.com/](https://www.w3schools.com/)
      * **Docker & Nginx Docs:** [https://docs.docker.com/](https://docs.docker.com/) and [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
