---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Páginas Web & Publicação"
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

## Visão Geral da Sessão

  * **Parte I — Fundamentos da Web & Estrutura HTML5:**
      * Páginas estáticas, anatomia de tags, árvore **DOM**, elementos visuais e **tags semânticas HTML5**.
  * **Parte II — Estilização e Layout com CSS:**
      * Separação estrutura/estilo, seletores, **Cascata/Especificidade**, integração e **CSS Box Model**.
  * **Parte III — Publicação com Docker/Nginx & Reverse Proxy:**
      * Servidor **Nginx + Docker Compose**, fluxo HTTP fim-a-fim e arquitetura de **Reverse Proxy**.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos da Web \& Estrutura HTML5}}
\end{center}

-----

## O que é uma Página Web "Estática"?

  * **Entrega direta:** Ficheiros enviados ao *browser* **exatamente como estão guardados** no servidor.
  * **Conteúdo fixo:** Todos os utilizadores veem o mesmo documento (como uma brochura digital).
  * **Papel do servidor (ex.: Nginx):** Localizar o ficheiro pedido (`GET /index.html`) e devolvê-lo via HTTP.
  * **Tecnologias base:** **HTML** (estrutura e significado) + **CSS** (estilo e layout).

\vspace{2em}

\begin{center}
\includegraphics[width=0.76\linewidth]{figures/static-website.png}
\end{center}

-----

## HTML: *HyperText Markup Language* & Anatomia de uma Tag

  * **HyperText (Hipertexto):** Texto com hiperligações (*links*) que interligam documentos na Web.
  * **Markup Language (Marcação):** *Não* é programação (sem lógica/ciclos); usa **tags** para estruturar conteúdo.

\vspace{0.4em}

\begin{center}
\begin{tikzpicture}[
    box/.style={rectangle, rounded corners=2pt, thick, font=\scriptsize\ttfamily, inner sep=4pt, minimum height=0.60cm},
    lbl/.style={font=\tiny\bfseries, align=center},
    arr/.style={-{Latex[length=1.4mm]}, thick}
]
% Elemento Normal
\node[font=\scriptsize\bfseries, anchor=west] at (-0.2, 2.10) {1. Elemento com Conteúdo:};

\node[box, draw=blue!75!black, fill=blue!8] (open) at (0.6, 1.35) {<a};
\node[box, draw=orange!80!black, fill=orange!10, right=2pt of open] (attr) {href="https://ua.pt"};
\node[box, draw=blue!75!black, fill=blue!8, right=2pt of attr] (openclose) {>};
\node[box, draw=uagreen!75!black, fill=uagreen!12, right=2pt of openclose] (content) {Universidade de Aveiro};
\node[box, draw=red!75!black, fill=red!8, right=2pt of content] (close) {</a>};

\node[lbl, color=blue!75!black] (l_open) at (0.6, 0.35) {Tag de\\Abertura};
\node[lbl, color=orange!85!black] (l_attr) at (2.5, 0.35) {Atributo\\(\texttt{nome="valor"})};
\node[lbl, color=uagreen!65!black] (l_cont) at (5.85, 0.35) {Conteúdo\\Visível};
\node[lbl, color=red!75!black] (l_close) at (8.3, 0.35) {Tag de Fecho\\(\texttt{</...>})};

\draw[arr, color=blue!75!black] (l_open.north) -- (open.south);
\draw[arr, color=orange!85!black] (l_attr.north) -- (attr.south);
\draw[arr, color=uagreen!65!black] (l_cont.north) -- (content.south);
\draw[arr, color=red!75!black] (l_close.north) -- (close.south);

% Elemento Vazio
\node[font=\scriptsize\bfseries, anchor=west] at (-0.2, -0.45) {2. Elemento Vazio (sem tag de fecho):};
\node[box, draw=purple!75!black, fill=purple!8, anchor=west] at (0.2, -1.05) {<img src="logo.png" alt="Logótipo da UA">};
\node[font=\tiny, color=black!70, anchor=west] at (5.7, -1.05) {(Ex.: \texttt{<img>}, \texttt{<meta>}, \texttt{<link>})};
\end{tikzpicture}
\end{center}

-----

## O Esqueleto Base do HTML5 & A Árvore DOM

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

  * **`<!DOCTYPE html>`:** Ativa o modo standard HTML5 no *browser*.
  * **`<head>` (Invisível na página):** Metadados do documento (p.ex. `<title>` na aba do *browser*).
  * **`<body>` (Visível na janela):** Contém todos os elementos renderizados no ecrã (`<h1>`, `<p>`, imagens, etc.).
  * **Árvore DOM (*Document Object Model*):** Árvore hierárquica de nós construída pelo *browser* em memória para exibir e manipular a página.

-----

## Elementos de Conteúdo Visual I: Tipografia, Texto e Hiperligações

::::: {.columns align=center}
::: {.column width="48%"}

```html
<h1>Título Principal (H1)</h1>
<h2>Subsecção da Página (H2)</h2>

<p>
  Texto com <strong>importância</strong>
  e com <em>ênfase</em>.
</p>

<p>
  Visite a <a href="https://www.ua.pt">UA</a>
  ou contacte
  <a href="mailto:aluno@ua.pt">aluno@ua.pt</a>.
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

\node[font=\footnotesize\bfseries, anchor=west] at (0.25, 2.65) {Subsecção da Página (H2)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.65) {<h2>};

\node[font=\scriptsize, align=left, text width=4.3cm, anchor=north west] at (0.25, 2.25) {Texto com \textbf{importância} e com \textit{ênfase}.};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.00) {<p>};

\node[font=\scriptsize, align=left, text width=4.3cm, anchor=north west] at (0.25, 1.35) {Visite a \textcolor{blue}{\underline{UA}} ou contacte \textcolor{blue}{\underline{aluno@ua.pt}}.};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 1.10) {<a>};

\draw[dashed, color=black!25] (0.2, 0.45) -- (5.3, 0.45);
\node[font=\tiny\itshape, color=black!60] at (2.75, 0.22) {Renderização nativa no Browser (sem CSS)};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<h1>`–`<h6>`:** Hierarquia de títulos (usar apenas um `<h1>` principal por página).
  * **`<p>`:** Bloco de parágrafo com espaçamento vertical automático.
  * **`<strong>` / `<em>`:** Destaque semântico (negrito e itálico).
  * **`<a href="...">`:** Hiperligação para URLs, ficheiros locais ou emails (`mailto:`).

-----

## Elementos de Conteúdo Visual II: Listas e Tabelas

::::: {.columns align=center}
::: {.column width="48%"}

```html
<!-- Lista Não Ordenada e Ordenada -->
<ul>
  <li>HTML5 (Estrutura)</li>
  <li>CSS3 (Estilo)</li>
</ul>
<ol>
  <li>Criar index.html</li>
  <li>Publicar no Nginx</li>
</ol>

<!-- Tabela de Dados -->
<table>
  <thead>
    <tr><th>Serviço</th><th>Porta</th></tr>
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
\node[font=\scriptsize, anchor=west] at (0.4, 3.72) {$\bullet$ HTML5 (Estrutura)};
\node[font=\scriptsize, anchor=west] at (0.4, 3.38) {$\bullet$ CSS3 (Estilo)};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 3.55) {<ul> / <li>};

\draw[dotted, color=black!25] (0.25, 3.10) -- (5.25, 3.10);

% Lista ol
\node[font=\scriptsize, anchor=west] at (0.4, 2.75) {1. Criar index.html};
\node[font=\scriptsize, anchor=west] at (0.4, 2.40) {2. Publicar no Nginx};
\node[font=\tiny\ttfamily, color=red!75!black, anchor=east] at (5.35, 2.57) {<ol> / <li>};

\draw[dotted, color=black!25] (0.25, 2.10) -- (5.25, 2.10);

% Tabela renderizada
\draw[thick, draw=black!60, fill=black!8] (0.4, 1.45) rectangle (2.1, 1.85);
\draw[thick, draw=black!60, fill=black!8] (2.1, 1.45) rectangle (3.4, 1.85);
\node[font=\scriptsize\bfseries] at (1.25, 1.65) {Serviço};
\node[font=\scriptsize\bfseries] at (2.75, 1.65) {Porta};

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

\node[font=\tiny\itshape, color=black!60] at (2.75, 0.25) {Listas e tabelas renderizadas no Browser};
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{2em}

  * **`<ul>` / `<ol>`:** Listas não ordenadas (*bullets*) e ordenadas (numeradas), com itens `<li>`.
  * **`<table>`:** Estrutura tabular dividida em cabeçalho (`<thead>` / `<th>`) e corpo (`<tbody>` / `<td>`), organizada por linhas (`<tr>`).

-----

## Multimédia Nativa no HTML5: `<img>`, `<figure>`, `<audio>` e `<video>`

::::: {.columns align=center}
::: {.column width="50%"}

```html
<!-- Imagem com Legenda -->
<figure>
  <img src="images/profile.jpg"
       alt="Foto de perfil" width="150">
  <figcaption>Fig 1. Aluno de IEI.</figcaption>
</figure>

<!-- Áudio e Vídeo Nativos -->
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
\node[font=\tiny\itshape, color=black!75] at (1.4, 3.03) {Fig 1. Aluno de IEI.};

% Imagem partida (fallback alt)
\draw[dashed, draw=red!60!black, fill=red!4, rounded corners=2pt] (2.75, 2.85) rectangle (5.05, 4.25);
\node[font=\tiny\bfseries, color=red!70!black] at (3.9, 3.98) {Se falhar (Erro 404):};
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

  * **`src` & `alt`:** Caminho do ficheiro e texto alternativo (essencial para acessibilidade e erro 404).
  * **`controls` & `<source>`:** Botões nativos do leitor; o *browser* reproduz o 1.º formato suportado.

-----

## Arquitetura Semântica HTML5: Os 7 Contentores

::::: {.columns align=center}
::: {.column width="62%"}

| Tag | Propósito | Regra / Exemplo |
| :--- | :--- | :--- |
| **`<header>`** | Cabeçalho da página (ou artigo). | Logótipo e `<h1>` (**$\neq$ `<head>`!**). |
| **`<nav>`** | Navegação principal. | Menu principal (`<ul>` com links). |
| **`<main>`** | Conteúdo central da página. | **Apenas um `<main>`** por página. |
| **`<article>`** | Conteúdo **autónomo**. | Post, notícia, cartão (*isolável?*). |
| **`<section>`** | Agrupamento **temático**. | Subcapítulo ("Sobre Mim", com `<h2>`). |
| **`<aside>`** | Conteúdo complementar. | *Sidebar*, links extra, biografia. |
| **`<footer>`** | Rodapé da página/secção. | Copyright (`&copy;`), contactos. |

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

  * **Vantagens:** Facilitam a **Acessibilidade** (leitores de ecrã), o **SEO** e a legibilidade do código.
  * **Nota:** Definem **significado**, não layout — sem CSS, aparecem empilhadas.

-----

## Juntar Tudo: HTML5 Semântico vs. Renderização Sem CSS

::::: columns
::: {.column width="54%"}

```html
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <title>Portfólio IEI</title>
</head>
<body>
  <header>
    <h1>O Meu Portfólio</h1>
    <nav>
      <a href="index.html">Início</a>
      <a href="#projetos">Projetos</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>Sobre Mim</h2>
      <p>Estudante de Engenharia Informática.</p>
    </article>
  </main>
  <aside>
    <h3>Links Rápidos</h3>
    <p>GitHub | LinkedIn</p>
  </aside>
  <footer>
    <p>&copy; 2026 Aluno UA</p>
  </footer>
</body>
</html>
```

:::
::: {.column width="46%"}

\begin{center}
\begin{tikzpicture}
\node[font=\scriptsize\bfseries, color=black!75] at (2.5, 4.85) {No Browser apenas com HTML (Sem CSS):};

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
\node[font=\small\bfseries, anchor=west] at (0.20, 3.68) {O Meu Portfólio};
\node[font=\tiny, color=blue, anchor=west] at (0.20, 3.28) {\underline{Início} \hspace{4pt} \underline{Projetos}};

\node[font=\footnotesize\bfseries, anchor=west] at (0.20, 2.75) {Sobre Mim};
\node[font=\tiny, anchor=west] at (0.20, 2.40) {Estudante de Engenharia Informática.};

\node[font=\scriptsize\bfseries, anchor=west] at (0.20, 1.85) {Links Rápidos};
\node[font=\tiny, anchor=west] at (0.20, 1.52) {GitHub | LinkedIn};

\node[font=\tiny, anchor=west] at (0.20, 0.95) {\copyright\ 2026 Aluno UA};

% Anotações tracejadas
\draw[dashed, color=orange!80!black] (0.12, 3.12) rectangle (4.88, 3.92);
\node[font=\tiny\ttfamily, color=orange!85!black, anchor=east] at (4.85, 3.68) {<header>};

\draw[dashed, color=uagreen!75!black] (0.12, 2.22) rectangle (4.88, 3.00);
\node[font=\tiny\ttfamily, color=uagreen!60!black, anchor=east] at (4.85, 2.75) {<main>};

\draw[dashed, color=purple!75!black] (0.12, 1.35) rectangle (4.88, 2.10);
\node[font=\tiny\ttfamily, color=purple!80!black, anchor=east] at (4.85, 1.85) {<aside>};

\draw[dashed, color=teal!80!black] (0.12, 0.72) rectangle (4.88, 1.22);
\node[font=\tiny\ttfamily, color=teal!80!black, anchor=east] at (4.85, 0.95) {<footer>};

\node[rectangle, draw=orange!80!black, fill=orange!10, rounded corners=2pt, font=\tiny, align=center, inner sep=3pt] at (2.5, 0.08) {Estrutura semântica pronta, mas tudo empilhado $\rightarrow$ falta o \textbf{CSS}!};
\end{tikzpicture}
\end{center}

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Estilização e Layout com CSS}}
\end{center}

-----

## O Papel do CSS e a Separação de Responsabilidades

  * **CSS (*Cascading Style Sheets*):** Controla cores, fontes, espaçamento e disposição visual (*layout*).
  * **Separação de Responsabilidades (*Separation of Concerns*):**
      * **HTML ("Esqueleto"):** Estrutura e conteúdo $\cdot$ **CSS ("Pele"):** Apresentação visual (`style.css`).

\vspace{0.3em}

\begin{center}
\begin{tikzpicture}[
    card/.style={rectangle, rounded corners=2pt, draw=black!20, fill=white}
]
% --- Lado Esquerdo: Sem CSS ---
\node[font=\scriptsize\bfseries, color=black!70] at (2.1, 3.35) {1. Apenas HTML5 (Sem CSS)};
\draw[thick, draw=black!65, fill=white, rounded corners=3pt] (0, 0) rectangle (4.2, 3.1);
\fill[black!12] (0.02, 2.75) rectangle (4.18, 3.08);
\draw[draw=black!50] (0, 2.75) -- (4.2, 2.75);
\fill[red!70] (0.2, 2.91) circle (0.06);
\fill[orange!80] (0.38, 2.91) circle (0.06);
\fill[uagreen!80!black] (0.56, 2.91) circle (0.06);

\node[font=\scriptsize\bfseries, anchor=west] at (0.15, 2.45) {O Meu Portfólio};
\node[font=\tiny, color=blue, anchor=west] at (0.15, 2.12) {\underline{Início} \hspace{3pt} \underline{Projetos}};
\node[font=\tiny\bfseries, anchor=west] at (0.15, 1.72) {Sobre Mim};
\node[font=\tiny, anchor=west] at (0.15, 1.42) {Estudante de Eng. Informática.};
\node[font=\tiny\bfseries, anchor=west] at (0.15, 1.02) {Links Rápidos};
\node[font=\tiny, anchor=west] at (0.15, 0.75) {GitHub | LinkedIn};
\node[font=\tiny, anchor=west] at (0.15, 0.32) {\copyright\ 2026 Aluno UA};

% Seta central
\draw[-{Latex[length=2.2mm]}, very thick, color=uagreen!80!black] (4.45, 1.55) -- node[above, font=\tiny\ttfamily\bfseries, color=black!80] {+ style.css} (5.55, 1.55);

% --- Lado Direito: Com CSS ---
\node[font=\scriptsize\bfseries, color=uagreen!60!black] at (7.9, 3.35) {2. O Mesmo HTML5 + \texttt{style.css}};
\draw[thick, draw=black!65, fill=black!7, rounded corners=3pt] (5.8, 0) rectangle (10.0, 3.1);
\fill[black!15] (5.82, 2.75) rectangle (9.98, 3.08);
\draw[draw=black!50] (5.8, 2.75) -- (10.0, 2.75);
\fill[red!70] (6.0, 2.91) circle (0.06);
\fill[orange!80] (6.18, 2.91) circle (0.06);
\fill[uagreen!80!black] (6.36, 2.91) circle (0.06);

% Cartão Header centrado
\node[card, minimum width=3.6cm, minimum height=0.58cm] at (7.9, 2.32) {};
\node[font=\scriptsize\bfseries, color=blue!65!black, anchor=west] at (6.22, 2.43) {O Meu Portfólio};
\node[font=\tiny\bfseries, color=blue!55!black, anchor=west] at (6.22, 2.16) {Início \hspace{6pt} Projetos};

% Cartão Main + Aside lado a lado
\node[card, minimum width=2.45cm, minimum height=1.18cm] at (7.32, 1.32) {};
\fill[blue!60!black] (6.42, 1.32) circle (0.22);
\node[font=\tiny\bfseries, color=white] at (6.42, 1.32) {Eu};
\node[font=\tiny\bfseries, color=black!85, anchor=west] at (6.72, 1.62) {Sobre Mim};
\node[font=\tiny, color=black!70, align=left, text width=1.65cm, anchor=west] at (6.72, 1.22) {Estudante de\\Eng. Informática.};

\node[card, minimum width=1.05cm, minimum height=1.18cm] at (9.18, 1.32) {};
\node[font=\tiny\bfseries, color=purple!80!black] at (9.18, 1.62) {Links};
\node[font=\tiny, color=blue!65!black, align=center] at (9.18, 1.18) {GitHub\\LinkedIn};

% Cartão Footer
\node[card, minimum width=3.6cm, minimum height=0.38cm] at (7.9, 0.38) {};
\node[font=\tiny, color=black!55] at (7.9, 0.38) {\copyright\ 2026 Aluno UA --- Contacte-me};
\end{tikzpicture}
\end{center}

-----

## Anatomia de uma Regra CSS e Seletores Fundamentais

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

\node[lbl, color=purple!80!black] (lsel) at (0.8, 0.08) {Seletor ("Quem")};
\node[lbl, color=blue!75!black] (lprop) at (3.0, 0.08) {Propriedade};
\node[lbl, color=uagreen!65!black] (lval) at (4.5, 0.08) {Valor};
\node[lbl, color=black!70] (ldec) at (7.3, 0.08) {Declaração (\texttt{propriedade: valor;})};

\draw[arr, color=purple!80!black] (lsel.north) -- (sel.south);
\draw[arr, color=blue!75!black] (lprop.north) -- (prop.south);
\draw[arr, color=uagreen!65!black] (lval.north) -- (val.south);
\draw[arr, color=black!70] (ldec.north) -- (prop2.south);
\end{tikzpicture}
\end{center}

\vspace{-0.3em}

| Tipo de Seletor | Sintaxe CSS | Exemplo HTML | Alvo Selecionado |
| :--- | :--- | :--- | :--- |
| **Elemento (Tag)** | `p { ... }` | `<p>...</p>` | Todas as tags `<p>`. |
| **Classe** | `.cartao { ... }` | `<article class="cartao">` | Todos os elementos com `class="cartao"`. |
| **ID** | `#topo { ... }` | `<header id="topo">` | O **único** elemento com `id="topo"`. |
| **Descendente** | `header h1 { ... }` | `<header><h1>...` | Tags `<h1>` dentro de `<header>`. |
| **Agrupamento** | `header, main, footer` | `<header>`, `<main>`... | Aplica o estilo aos 3 elementos. |
| **Pseudo-classe** | `a:hover { ... }` | `<a href="...">` | Link `<a>` quando o rato passa por cima. |

-----

## O "C" do CSS: A Cascata e a Especificidade

::::: {.columns align=center}
::: {.column width="46%"}

**Ordem de desempate:**

1. **Origem:** O teu `style.css` sobrepõe-se ao padrão do *browser*.
2. **Especificidade:** O seletor mais específico vence.
3. **Ordem:** Com igual peso, vence a **última** regra.

:::
::: {.column width="54%"}

\begin{center}
\begin{tikzpicture}[scale=0.82, transform shape,
    tier/.style={trapezium, trapezium angle=72, draw=black!70, thick, align=center, font=\tiny\bfseries, minimum height=0.62cm, inner sep=2pt}
]
\node[font=\scriptsize\bfseries] at (0, 3.35) {Pirâmide de Especificidade CSS};

% Nível 1: Inline
\node[tier, fill=red!20, draw=red!75!black, minimum width=2.2cm] at (0, 2.55) {1. Estilo Inline (\texttt{style="..."})\\{\tiny Peso: 1000}};

% Nível 2: ID
\node[tier, fill=orange!20, draw=orange!80!black, minimum width=3.2cm] at (0, 1.75) {2. Seletor de ID (\texttt{\#meu-id})\\{\tiny Peso: 100}};

% Nível 3: Classe / Pseudo-classe
\node[tier, fill=uagreen!25, draw=uagreen!75!black, minimum width=4.2cm] at (0, 0.95) {3. Classe / Pseudo-classe (\texttt{.classe}, \texttt{:hover})\\{\tiny Peso: 10}};

% Nível 4: Elemento
\node[tier, fill=blue!15, draw=blue!75!black, minimum width=5.1cm] at (0, 0.15) {4. Elemento / Tag (\texttt{p}, \texttt{h1}, \texttt{header})\\{\tiny Peso: 1}};

\draw[-{Latex[length=1.8mm]}, very thick, color=red!75!black] (2.75, 0.0) -- node[right, font=\tiny\bfseries, align=left] {Maior\\Prioridade} (2.75, 2.75);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{0.2em}

```css
/* Qual a cor final de <p id="intro" class="destaque">? */
#intro    { color: gold; }   /* GANHA! (ID = peso 100) */
.destaque { color: green; }  /* Classe = peso 10 */
p         { color: blue; }
p         { color: red; }    /* Ganha a 'blue' pela ordem no ficheiro (peso 1) */
```

-----

## Métodos de Integração CSS: Externo vs. Interno vs. Em Linha

| Método | Sintaxe | Vantagens | Desvantagens |
| :--- | :--- | :--- | :--- |
| **1. Externo (Recomendado)** | `<link rel="stylesheet" href="css/style.css">` no `<head>` | **Reutilizável** em todo o site, fácil manutenção e guardado em **cache**. | 1 pedido HTTP extra na 1.ª visita. |
| **2. Interno (*Embedded*)** | `<style> ... </style>` no `<head>` | Útil para testes rápidos num único ficheiro. | Não reutilizável noutras páginas. |
| **3. Em Linha (*Inline* — Evitar!)** | `<p style="color: red;">` | Apenas para alterações dinâmicas via JS. | **Mistura HTML e CSS**; difícil de manter (peso 1000). |

\vspace{0.3em}

```html
<!-- Boa Prática: Ligar ficheiro externo no <head> -->
<head>
  <meta charset="UTF-8">
  <title>O Meu Portfólio</title>
  <link rel="stylesheet" href="css/style.css">
</head>
```

-----

## O Modelo de Caixa (*CSS Box Model*)

::::: {.columns align=center}
::: {.column width="50%"}

\begin{center}
\begin{tikzpicture}[scale=0.88, transform shape]
% Margin
\draw[dashed, thick, draw=orange!85!black, fill=orange!12, rounded corners=2pt] (0, 0) rectangle (5.4, 3.85);
\node[font=\tiny\bfseries, color=orange!85!black, anchor=north west] at (0.12, 3.78) {Margin (Espaço exterior transparente)};

% Border
\draw[very thick, draw=black!80, fill=black!15, rounded corners=4pt] (0.55, 0.45) rectangle (4.85, 3.30);
\node[font=\tiny\bfseries, color=black!85, anchor=north west] at (0.65, 3.24) {Border (Moldura + \texttt{border-radius})};

% Padding
\draw[dashed, thick, draw=uagreen!70!black, fill=uagreen!18] (0.95, 0.80) rectangle (4.45, 2.75);
\node[font=\tiny\bfseries, color=uagreen!50!black, anchor=north west] at (1.03, 2.69) {Padding (Espaço interior com fundo)};

% Content
\draw[thick, draw=blue!75!black, fill=white] (1.38, 1.15) rectangle (4.02, 2.20);
\node[font=\scriptsize\bfseries, color=blue!80!black, align=center] at (2.70, 1.68) {Content (Conteúdo)\\{\tiny Texto / Imagens (\texttt{width} $\times$ \texttt{height})}};

% Setas de margem horizontal
\draw[<->, >=Latex, thick, color=orange!85!black] (0, 1.68) -- node[above, font=\tiny\ttfamily] {auto} (0.55, 1.68);
\draw[<->, >=Latex, thick, color=orange!85!black] (4.85, 1.68) -- node[above, font=\tiny\ttfamily] {auto} (5.4, 1.68);
\end{tikzpicture}
\end{center}

:::
::: {.column width="50%"}

```css
.cartao {
  box-sizing: border-box; /* Inclui padding/border */
  max-width: 600px;       /* Largura máxima */
  padding: 20px;          /* Espaço interno */
  border: 2px solid #ccc; /* Moldura visível */
  border-radius: 8px;     /* Cantos arredondados */
  margin: 20px auto;      /* 'auto' centra bloco */
  background-color: #fff;
}
```

:::
:::::

\vspace{0.25em}

  * **Content & Padding:** O conteúdo e o seu espaçamento interior (ambos herdam o `background-color`).
  * **Border & Margin:** A moldura visível da caixa e o espaço exterior transparente que a afasta de outros elementos (`margin: 20px auto` centra na horizontal).
  * **Boa Prática (`box-sizing: border-box`):** Garante que `width`/`max-width` já inclui `padding` e `border` (evita caixas maiores do que o esperado).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Publicação com Docker/Nginx \& Reverse Proxy}}
\end{center}

-----

## Publicar um Site Estático com Nginx e Docker Compose

::::: {.columns align=center}
::: {.column width="42%"}

```text
o-meu-portfolio/
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
\node[font=\scriptsize\bfseries, anchor=north west] at (0.15, 4.08) {Máquina Anfitriã (Host Linux / WSL)};

% Browser (alinhado com Nginx)
\node[box, draw=blue!75!black, fill=blue!10, font=\tiny\bfseries, minimum width=2.20cm, minimum height=0.62cm] (br) at (1.30, 2.55) {Browser\\\texttt{http://localhost:8080}};

% Pasta Local ./src (alinhada com Pasta no Contentor)
\node[box, draw=orange!85!black, fill=orange!12, font=\tiny\ttfamily, minimum width=2.20cm, minimum height=1.10cm] (src) at (1.30, 0.95) {\textbf{Pasta Local \texttt{./src}}\\\texttt{index.html}\\\texttt{css/style.css}\\\texttt{images/...}};

% Contentor Docker
\draw[box, draw=uagreen!75!black, fill=uagreen!10] (3.95, 0.25) rectangle (6.60, 3.68);
\node[font=\tiny\bfseries, color=uagreen!55!black] at (5.28, 3.48) {Contentor Docker};
\node[font=\tiny\ttfamily, color=black!70] at (5.28, 3.22) {(nginx:alpine)};

% Porta 80 Nginx
\node[box, draw=uagreen!80!black, fill=white, font=\tiny\ttfamily\bfseries, minimum width=2.10cm, minimum height=0.55cm] (ngx) at (5.28, 2.55) {Nginx (:80)};

% Pasta dentro do contentor
\node[box, draw=orange!80!black, fill=white, font=\tiny\ttfamily, minimum width=2.10cm, minimum height=0.95cm] (cdir) at (5.28, 0.95) {\textbf{No Contentor (:ro)}\\\texttt{/usr/share/}\\\texttt{nginx/html}};

% Ligações com espaço livre no corredor central
\draw[arr, color=blue!75!black] (br.east) -- node[above=2pt, pos=0.42, font=\tiny\ttfamily\bfseries] {8080:80} (ngx.west);
\draw[<->, >=Latex, very thick, dashed, color=orange!85!black] (src.east) -- node[above=2pt, pos=0.42, font=\tiny\bfseries] {Volume} (cdir.west);
\draw[arr, color=uagreen!70!black] (cdir.north) -- node[right=2pt, font=\tiny] {Lê ficheiros} (ngx.south);
\end{tikzpicture}
\end{center}

:::
:::::

\vspace{1em}

  * **Executar:** `docker compose up -d` (arranca o servidor web em segundo plano).
  * **Aceder:** Abrir `http://localhost:8080` no *browser*.
  * **Volume `:ro` (*read-only*):** Mapeia `./src` para dentro do contentor apenas em modo de leitura (boa prática de segurança).

-----

## Como um Browser Acede a uma Página (Fluxo Fim-a-Fim)

\begin{center}
\begin{tikzpicture}[
    stepbox/.style={rectangle, rounded corners=3pt, draw=black!70, thick, font=\tiny, align=left, inner sep=3.5pt, minimum height=1.55cm},
    arr/.style={-{Latex[length=1.6mm]}, very thick, color=uagreen!80!black}
]
\node[stepbox, fill=blue!8, text width=2.15cm] (s1) at (0, 0) {
  \textbf{1. DNS \& Ligação}\\
  $\bullet$ DNS: domínio $\rightarrow$ IP.\\
  $\bullet$ \textit{Handshake} TCP (:80/:443) + TLS se HTTPS.
};

\node[stepbox, fill=orange!10, text width=2.20cm, right=0.25cm of s1] (s2) {
  \textbf{2. Pedido HTTP}\\
  $\bullet$ Browser envia \texttt{GET /}.\\
  $\bullet$ Tráfego chega ao \textbf{Nginx} (ex.: porta Docker).
};

\node[stepbox, fill=uagreen!12, text width=2.25cm, right=0.25cm of s2] (s3) {
  \textbf{3. Resposta HTTP}\\
  $\bullet$ Nginx lê \texttt{index.html} (volume \texttt{./src}).\\
  $\bullet$ Devolve \texttt{200 OK} + HTML.
};

\node[stepbox, fill=purple!10, text width=2.30cm, right=0.25cm of s3] (s4) {
  \textbf{4. DOM \& Render}\\
  $\bullet$ Constrói a árvore \textbf{DOM}.\\
  $\bullet$ Pede \texttt{style.css} e \texttt{<img>}, e desenha a página.
};

\draw[arr] (s1.east) -- (s2.west);
\draw[arr] (s2.east) -- (s3.west);
\draw[arr] (s3.east) -- (s4.west);
\end{tikzpicture}
\end{center}

\vspace{0.2em}

::::: columns
::: {.column width="48%"}
**Pedido HTTP (Passo 2):**
```http
GET / HTTP/1.1
Host: example.com
Accept: text/html
```
:::
::: {.column width="52%"}
**Resposta HTTP (Passo 3):**
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html><html lang="pt">...
```
:::
:::::

\vspace{0.2em}

  * **Nota (DevTools $\rightarrow$ *Network*):** Abrir 1 página gera **vários pedidos HTTP** (1 para o HTML + 1 por cada ficheiro CSS, imagem ou vídeo).

-----

## Arquitetura de Rede: Forward Proxy vs. Reverse Proxy

Como expor vários serviços web na mesma máquina usando apenas a porta pública `80`/`443`?

\begin{center}
\begin{tikzpicture}[
    nodebox/.style={rectangle, rounded corners=3pt, draw=black!75, thick, font=\tiny\bfseries, align=center, inner sep=3.5pt},
    zone/.style={rectangle, rounded corners=4pt, dashed, thick},
    arr/.style={-{Latex[length=1.4mm]}, thick}
]
% --- Forward Proxy ---
\node[font=\scriptsize\bfseries, color=blue!75!black] at (2.4, 3.55) {1. Forward Proxy (Esconde o Cliente)};
\draw[zone, draw=blue!60!black, fill=blue!4] (0, 0.35) rectangle (3.1, 3.25);
\node[font=\tiny\itshape, color=blue!75!black] at (1.55, 0.55) {Rede Interna (Escola / Empresa)};

\node[nodebox, fill=white] (fc1) at (0.75, 2.55) {Cliente A};
\node[nodebox, fill=white] (fc2) at (0.75, 1.35) {Cliente B};
\node[nodebox, fill=blue!20, draw=blue!80!black, minimum height=1.5cm] (fp) at (2.35, 1.95) {Forward\\Proxy};
\node[nodebox, fill=black!10, minimum height=1.2cm] (fint) at (4.35, 1.95) {Internet\\{\tiny (ex.: Google)}};

\draw[arr, color=blue!75!black] (fc1.east) -- (fp.west);
\draw[arr, color=blue!75!black] (fc2.east) -- (fp.west);
\draw[arr, color=blue!75!black] (fp.east) -- (fint.west);

\node[font=\tiny, align=center, text width=4.8cm] at (2.4, -0.10) {Filtra tráfego de saída; a Internet vê apenas o IP do Proxy.};

\draw[dotted, thick, color=black!35] (5.35, 3.7) -- (5.35, -0.35);

% --- Reverse Proxy ---
\node[font=\scriptsize\bfseries, color=uagreen!60!black] at (8.2, 3.55) {2. Reverse Proxy (Esconde os Servidores)};
\node[nodebox, fill=black!10, minimum height=1.2cm] (rc) at (6.3, 1.95) {Clientes\\na Internet};

\draw[zone, draw=uagreen!75!black, fill=uagreen!6] (7.4, 0.35) rectangle (10.85, 3.25);
\node[font=\tiny\itshape, color=uagreen!55!black] at (9.12, 0.55) {Rede Privada Docker};

\node[nodebox, fill=uagreen!25, draw=uagreen!80!black, minimum height=1.6cm] (rp) at (8.15, 1.95) {Reverse\\Proxy\\{\tiny (Nginx :80)}};
\node[nodebox, fill=white] (rs1) at (9.95, 2.60) {Site Estático\\{\tiny (HTML :80)}};
\node[nodebox, fill=white] (rs2) at (9.95, 1.30) {API FastAPI\\{\tiny (Aula 08 :8000)}};

\draw[arr, color=uagreen!70!black] (rc.east) -- (rp.west);
\draw[arr, color=uagreen!70!black] (rp.east) -- node[above, sloped, font=\tiny\ttfamily] {/} (rs1.west);
\draw[arr, color=orange!85!black] (rp.east) -- node[below, sloped, font=\tiny\ttfamily] {/api/} (rs2.west);

\node[font=\tiny, align=center, text width=5.2cm] at (8.2, -0.10) {O cliente fala apenas com o Proxy; contentores ficam isolados.};
\end{tikzpicture}
\end{center}

-----

## Funções do Reverse Proxy & Configuração (Docker + Nginx)

\begingroup\footnotesize

  * **Roteamento:** Encaminha por caminho (`/`, `/api/`) ou domínio na porta `80`.
  * **Load Balancing:** Distribui pedidos por várias réplicas internas.
  * **SSL & Caching:** Termina HTTPS à entrada e serve estáticos em *cache*.

\endgroup

\vspace{0.4em}

::::: {.columns align=T}
::: {.column width="54%"}

\begingroup\footnotesize `docker-compose.yml` *(só o proxy é público):* \endgroup

```yaml
services:
  proxy:
    image: nginx:alpine
    ports: ["80:80"] # Única porta pública
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
  site:
    image: nginx:alpine # Privado (:80)
    volumes:
      - ./src:/usr/share/nginx/html:ro
  api:
    image: minha-api-fastapi # Privado (:8000)
```

:::
::: {.column width="46%"}

\begingroup\footnotesize `nginx.conf` *(encaminhamento):* \endgroup

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

## Síntese Arquitetural & Recursos de Referência

| Tecnologia | Papel | Ponto-Chave |
| :--- | :--- | :--- |
| **HTML5 Semântico** | Estrutura & Significado | `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>` (Acessibilidade e SEO). |
| **CSS3 & Box Model** | Apresentação & Layout | Ficheiro externo `style.css`; caixas com `content`, `padding`, `border` e `margin`. |
| **Nginx + Docker** | Publicação Web | Mapeia portas (`8080:80`) e monta `./src` em `/usr/share/nginx/html:ro`. |
| **Reverse Proxy** | Rede & Arquitetura | Expõe múltiplos serviços internos (`/` e `/api/`, ou vários domínios) numa única porta `80`. |

\vspace{0.4em}

  * **Documentação de Referência:**
      * **MDN Web Docs (Mozilla):** Referência oficial HTML, CSS e HTTP — [https://developer.mozilla.org/](https://developer.mozilla.org/)
      * **W3Schools:** Tutoriais e exemplos interativos — [https://www.w3schools.com/](https://www.w3schools.com/)
      * **Docker & Nginx Docs:** [https://docs.docker.com/](https://docs.docker.com/) e [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
