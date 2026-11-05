---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Control de Versiones con Git & Plataforma Colaborativa GitHub"
institute: Universidade de Aveiro
date: November 02, 2026
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

  * **Parte I — Fundamentos del Control de Versiones & Arquitectura:**
      * El desafío de la evolución del código y la colaboración, fallos de los enfoques ingenuos (copias manuales y nube), taxonomía de VCS, matriz comparativa (CVCS vs. DVCS) y Git como estándar de facto de la industria.
  * **Parte II — Aspectos Funcionales de Git & Ciclo de Vida Local:**
      * Conceptos fundamentales (`Repositorio`, `Commit`, `Branch`, `HEAD`), las tres zonas operativas y estados de los archivos, comandos esenciales (`init`, `clone`, `status`, `add`, `commit`), estándar Conventional Commits, `log`, etiquetado (`tag`) y `.gitignore`.
  * **Parte III — Ramificación, Integración & Resolución de Conflictos:**
      * El paradigma de ramas (*branches*) y puntero `HEAD`, estrategias de integración (`merge` *fast-forward* vs. *3-way*), linealización con `rebase`, comparación arquitectural y resolución de conflictos.
  * **Parte IV — Colaboración Distribuida & Flujos de Trabajo en Equipo:**
      * Repositorios remotos (`origin`), sincronización (`fetch`, `pull`, `push`), modelos colaborativos (*GitFlow* vs. *Trunk-Based Development*), *Feature Branches* con *Pull Requests* y publicación de versiones (*releases*).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos del Control de Versiones \& Arquitectura}}
\end{center}

-----

## El Desafío de la Evolución del Código y la Colaboración en Software

El desarrollo de software es intrínsecamente dinámico y colaborativo:

  * **Naturaleza Dinámica del Código:**
      * Evolución continua: corrección de *bugs*, nuevas funcionalidades y refactorización.
      * Múltiples archivos interdependientes cambiando simultáneamente.
  * **Tres Dilemas Centrales de la Ingeniería:**
      * **Trazabilidad:** ¿*Qué* cambió, *cuándo*, *por qué* y por *quién*?
      * **Reversibilidad:** ¿Cómo probar nuevas ideas sin romper el código funcional?
      * **Colaboración Concurrente:** ¿Cómo trabajar en equipo sin sobrescribir trabajo ajeno?

\vspace{0.8em}

\begin{center}
\textbf{Ante estos desafíos, ¿cuáles fueron las soluciones intuitivas (y erróneas) más comunes?}
\end{center}

-----

## Enfoques Ingenuos (I): El Caos de las Copias Manuales

::::: columns
::: {.column width="60%"}

La primera reacción para guardar versiones antiguas y probar ideas es duplicar archivos:

  * **Anti-Patrón de los Sufijos:**
      * `proyecto_v1.c`, `proyecto_v2_corregido.c`
      * `proyecto_final.c`, `proyecto_final_AHORA_SI.c`
  * **¿Por Qué Fracasa?**
      * **Opacidad:** El nombre no revela qué líneas o funciones cambiaron.
      * **Sin Contexto:** Se pierde el motivo (*por qué*) de cada alteración.
      * **Reversibilidad Frágil:** Revertir un archivo quebra la coherencia global.
      * **Fechas Inciertas:** Los metadatos del SO se alteran con facilidad al copiar.

\vspace{0.4em}
\textbf{La duplicación manual es opaca, propensa a errores e inviable en proyectos reales.}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.72\textheight,keepaspectratio]{figures/phd_not_final.png}

\vspace{0.2em}
\textit{\tiny "notFinal.doc" --- Jorge Cham (PhD Comics)}
\end{center}

:::
:::::

-----

## Enfoques Ingenuos (II): Sincronización en la Nube y Correo Electrónico

Para resolver la **colaboración en equipo**, se recurre habitualmente a canales comunes de compartición:

  * **1. Carpetas Compartidas en la Nube (Dropbox, Google Drive):**
      * **Herramienta Inadecuada:** Diseñadas para documentos, no para código fuente.
      * **Sobrescritura Ciega (*Last-Write-Wins*):** El último en guardar borra silenciosamente el trabajo ajeno.
      * **Conflictos Destructivos:** Ediciones simultáneas generan copias ciegas (`Copia Conflictiva`), sin fusión de código.
  * **2. Intercambio de Archivos Comprimidos (.zip) por Correo:**
      * Circulación de versiones (`proyecto_v3_mario.zip` vs. `proyecto_v3_ana.zip`).
      * **Pesadilla del Merge Manual:** Fusionar cambios línea por línea copiando y pegando es insostenible y genera fallos.

\vspace{0.8em}

\begin{center}
\textbf{Sincronización de archivos $\neq$ Control de versiones. Colaborar exige fusión estructurada de código.}
\end{center}

-----

## La Solución: Sistemas de Control de Versiones (VCS)

Un **VCS** es la herramienta que registra metódicamente la evolución temporal de un proyecto:

  * **Trazabilidad Total:** Registro de *quién*, *cuándo* y *por qué* (mensajes de commit).
  * **Reversibilidad (*Time Machine*):** Recuperación instantánea de cualquier estado anterior estable.
  * **Análisis Diferencial:** Comparación precisa línea por línea (*diffs*) entre versiones.
  * **Colaboración Segura:** Trabajo paralelo de varios desarrolladores con fusión controlada de cambios.

\vspace{0.8em}

\begin{center}
\textbf{El VCS convierte el desarrollo en un proceso seguro, auditable y reproducible.}
\end{center}

-----

## Taxonomía de VCS: Centralizado vs. Distribuido

\begin{center}
\includegraphics[width=\linewidth,height=0.80\textheight,keepaspectratio]{figures/vcs_centralized_vs_distributed.png}
\end{center}

-----

## Matriz Comparativa: CVCS vs. DVCS

| Vector de Comparación | CVCS (ej.: Subversion / Perforce) | DVCS (ej.: Git / Mercurial) |
| :--- | :--- | :--- |
| **Repositorio e Historial Local** | Solo la copia de trabajo actual (*working copy*) | **Clon completo con todo el historial del proyecto** |
| **Operación sin Red (Offline)** | Limitada (solo edición y `diff` de la versión actual) | **Total (`commit`, `branch`, `log`, `merge` 100% locales)** |
| **Tolerancia a Fallos (SPOF)** | Baja (si el servidor central falla, nadie envía cambios) | **Elevada (cada clon completo actúa como respaldo)** |
| **Velocidad de Operaciones** | Penalizada por la latencia de red hacia el servidor | **Casi instantánea (lectura/escritura en disco local)** |
| **Identificación de Versiones** | Números secuenciales globales (`r1`, `r2`, `r3`...) | **Hashes criptográficos distribuidos (SHA)** |
| **Ramificación (*Branching*) y *Merge*** | Pesada (carpetas en servidor; fusiones históricamente lentas) | **Ligera e instantánea (punteros locales; fusión rápida)** |
| **Archivos Binarios y *Locking*** | **Excelente (soporta *file locking* central y *checkouts* parciales)** | Débil nativamente (infla el historial; sin *lock* offline; requiere *Git LFS*) |
| **Control de Acceso (Seguridad)** | **Granular (permisos de lectura/escritura por carpeta/archivo)** | Global al repositorio (quien clona accede a todo el árbol) |

-----

## Git: El Estándar de Facto de la Industria

::::: columns
::: {.column width="66%"}

  * **Adopción Universal ($>90\%$ de la Industria):**
      * Herramienta **open-source** que se convirtió en el estándar indiscutible y la «lengua franca» de la ingeniería de software contemporánea.
  * **Origen Pragmático (2005):**
      * Creado por **Linus Torvalds** para el **Kernel Linux**, exigiendo un sistema distribuido libre, rápido y capaz de escalar a miles de desarrolladores.
  * **¿Por qué Conquistó la Industria?**
      * **Rendimiento Local:** Operaciones ejecutadas directamente en disco local (en C nativo), sin penalización de latencia de red.
      * **Ramificación Ligera ($O(1)$):** Crear ramas (*branches*) se reduce a crear punteros ligeros, habilitando el trabajo paralelo sin fricciones.
      * **Integridad Criptográfica:** Historial estructurado mediante hashes SHA (imposible alterar o corromper datos **sin detección**).

:::
::: {.column width="34%"}

\begin{center}
\includegraphics[width=0.65\linewidth,keepaspectratio]{figures/git_logo.png}

\vspace{0.4em}
\includegraphics[width=0.95\linewidth,keepaspectratio]{figures/git_branching_illustration.png}

\vspace{0.3em}
{\scriptsize \href{https://git-scm.com/}{\texttt{git-scm.com}}}
\end{center}

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Aspectos Funcionales de Git \& Ciclo de Vida Local}}
\end{center}

-----

## Conceptos Fundamentales de Git: El Modelo Mental

::::: columns
::: {.column width="55%"}

  * **1. Repositorio (*Repository* / `.git/`):**
      * Base de datos local que almacena todo el historial y metadatos.
  * **2. *Commit* (*Snapshot*):**
      * Punto de restauración inmutable que registra la evolución del código.
      * Identificado por un **Hash SHA** (ej.: \texttt{98ca9c2}).
  * **3. Rama (*Branch*):**
      * Representa una línea independiente de evolución del código.
      * Puntero móvil y ligero hacia un commit (`main`, `feature`).
  * **4. Puntero `HEAD`:**
      * Indicador que apunta a la rama y al commit activos en el momento.

:::
::: {.column width="45%"}

\vspace{0.3em}

\begin{center}
\begin{tikzpicture}[
    commit/.style={circle, draw=uagreen!80!black, fill=uagreen!15, thick, font=\tiny\bfseries, inner sep=1pt, minimum size=5.5mm},
    branch/.style={rectangle, draw=blue!70!black, fill=blue!10, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, inner sep=2pt},
    head/.style={rectangle, draw=red!70!black, fill=red!10, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, inner sep=2pt},
    arr/.style={-{Latex[length=1.6mm]}, thick, color=black!70},
    repo/.style={draw=black!30, dashed, rounded corners=4pt, fill=black!2}
]
% Enclosure
\draw[repo] (-0.5,-1.65) rectangle (4.6,1.4);
\node[anchor=north west, font=\tiny\bfseries, color=black!60] at (-0.45,1.35) {Repositorio (.git/)};

% Commits with short SHA hashes
\node[commit] (C1) at (0.2,0) {C1};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (0.2,-0.32) {98ca9c2};

\node[commit] (C2) at (1.3,0) {C2};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (1.3,-0.32) {34ac2e1};

\node[commit] (C3) at (2.4,0.6) {C3};
\node[anchor=south, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (2.4,0.92) {f30ab12};

\node[commit] (C4) at (2.4,-0.6) {C4};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (2.4,-0.92) {7a12dc8};

% Commit arrows (chronological evolution of code)
\draw[arr] (C1) -- (C2);
\draw[arr] (C2) -- (C3);
\draw[arr] (C2) -- (C4);

% Branches
\node[branch] (main) at (3.7,0.6) {main};
\draw[arr, color=blue!70!black] (main) -- (C3);

\node[branch] (feat) at (3.7,-0.6) {feature};
\draw[arr, color=blue!70!black] (feat) -- (C4);

% HEAD pointing to active branch (feature)
\node[head] (head) at (3.7,-1.25) {HEAD};
\draw[arr, color=red!70!black] (head) -- (feat);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## Las Tres Zonas Operativas de Git

Localmente, los archivos de un repositorio Git se articulan a través de tres zonas distintas:

  * **1. Directorio de Trabajo (*Working Tree / Directory*):**
      * La carpeta visible en el disco donde el desarrollador consulta, crea y edita archivos con sus editores habituales.
      * Los archivos se extraen de la base de datos de Git para su manipulación directa.
  * **2. Área de Preparación (*Staging Area / Index*):**
      * Capa intermedia de selección (registrada en `.git/index`).
      * Permite elegir quirúrgicamente qué modificaciones entrarán en el próximo commit, sin obligar a guardar todo de una vez.
  * **3. Repositorio Local (*Local Repository / .git*):**
      * Base de datos donde Git graba de forma permanente y comprimida todos los commits (*snapshots*) del proyecto.

-----

## Flujo Operativo y Estados de los Archivos

\vspace{0.4em}

\begin{center}
\begin{tikzpicture}[
    box/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\scriptsize, minimum width=2.6cm, minimum height=1.1cm},
    arr/.style={-{Latex[length=2.2mm]}, thick, color=black!75},
    arrback/.style={-{Latex[length=2.2mm]}, dashed, thick, color=red!70!black}
]
\node[box] (WT) {\textbf{Working Tree}\\\textit{Archivos Locales en Disco}};
\node[box, right=1.2cm of WT] (SA) {\textbf{Staging Area}\\\textit{Index / Preparación}};
\node[box, right=1.2cm of SA] (RP) {\textbf{Repositorio (.git)}\\\textit{Snapshots Permanentes}};

\draw[arr] (WT.north east) -- node[above, font=\tiny\ttfamily] {git add} (SA.north west);
\draw[arr] (SA.north east) -- node[above, font=\tiny\ttfamily] {git commit} (RP.north west);

\draw[arrback] (SA.south west) -- node[below, font=\tiny\ttfamily] {git restore --staged} (WT.south east);
\draw[arrback] (RP.south) to[bend left=25] node[below, font=\tiny\ttfamily] {git checkout / switch} (WT.south);
\end{tikzpicture}
\end{center}

\vspace{0.3em}

Al transitar entre estas zonas, cada archivo asume uno de **cuatro estados**:

  * **Untracked (No Rastreado):** Archivo nuevo en el *Working Tree* que Git aún no monitoriza.
  * **Modified (Modificado):** Archivo ya rastreado cuyo contenido en disco difiere del último commit.
  * **Staged (Preparado):** Modificación indexada en la *Staging Area* (`git add`), lista para el próximo commit.
  * **Unmodified (Sin Modificar):** Archivo grabado en el *Repositorio* (`git commit`), sin ediciones locales pendientes.

-----

## Inicialización y Clonación de Repositorios

Existen dos formas de establecer un repositorio Git local:

  * **1. Inicializar un Repositorio Nuevo (`git init`):**
      * Transforma una carpeta local existente en un repositorio Git:
        ```bash
        mkdir mi-proyecto && cd mi-proyecto
        git init
        # Inicializado repositorio Git vacío en /ruta/mi-proyecto/.git/
        ```
  * **2. Clonar un Repositorio Preexistente (`git clone`):**
      * Descarga una copia integral de un repositorio remoto (historial, ramas y etiquetas):
        ```bash
        git clone https://github.com/usuario/mi-proyecto.git
        ```

\vspace{0.3em}

  * En ambos casos se crea el directorio oculto **`.git/`**, que aloja toda la base de datos local.

-----

## Comandos del Ciclo Local: `status` e `add`

::::: columns
::: {.column width="45%"}

  * **Inspección con `git status`:**
      * Revela el estado de los archivos en las zonas de trabajo locales.
      * **Rojo:** Modificaciones no preparadas (*Untracked* / *Modified*).
      * **Verde:** Cambios preparados en la *Staging Area* (*Staged*).
  * **Preparación con `git add`:**
      * Traslada modificaciones hacia la *Staging Area*:
        ```bash
        git add main.c   # Archivo específico
        git add src/     # Directorio
        git add .        # Directorio actual
        git add -p       # Por bloques (hunks)
        ```

:::
::: {.column width="55%"}

\vspace{0.4em}
\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/git_status_add_es.png}
\end{center}

:::
:::::

-----

## Registro Permanente de Cambios: `git commit`

El comando `git commit` consolida el contenido de la *Staging Area* en un nuevo snapshot inmutable en el repositorio:

```bash
git commit -m "feat: implementa validación de credenciales de usuario"
```

  * **Dinámica Operativa:**
      * Git empaqueta los cambios preparados en la *Staging Area*, calcula su **Hash SHA** y enlaza el nuevo commit al commit anterior (*parent*).
      * La rama activa (ej.: `main`) y el puntero `HEAD` avanzan automáticamente hacia este nuevo commit.
  * **Principio de Atomicidad:**
      * Cada commit debe representar una **única unidad lógica y cohesiva** de trabajo (evitar mezclar refactorizaciones estéticas con correcciones de errores en el mismo commit).
      * Permite revertir o auditar un cambio específico sin efectos colaterales en el resto del proyecto.

-----

## Buenas Prácticas en Mensajes de Commit

::::: columns
::: {.column width="50%"}

  * **Principio Central:**
      * El código (`diff`) muestra **qué** cambió; el mensaje debe explicar **el porqué** del cambio.
  * **Convención 50/72 de la Industria:**
      * **Modo Imperativo:** Escribir como instrucción (ej.: `Añade`, `Corrige`, `Fix`, y no *Añadido*).
      * **Asunto ($\le 50$ car.):** Conciso, inicial mayúscula y sin punto final.
      * **Cuerpo ($\le 72$ car./línea):** Separado del asunto por una **línea en blanco**; detalla motivación e impacto.

:::
::: {.column width="50%"}

  * **Anti-Patrón (Información Nula):**
    ```bash
    git commit -m "arreglar errores y cambios"
    ```

  * **Modelo Recomendado (Regla 50/72):**
    ```text
    Fix: Corrige validación de sesión expirada

    La verificación previa ignoraba el TTL en
    Redis, permitiendo reutilizar sesiones.

    Añade validación estricta de expiración
    y devuelve HTTP 401 Unauthorized.
    ```

:::
:::::

-----

## Estandarización con Conventional Commits (I): Estructura y Tipos

::::: columns
::: {.column width="48%"}

  * **Concepto y Anatomía:**
      * Convención ligera para mensajes de commit estructurados, legibles por personas y herramientas.
  * **Estructura Canónica:**
    ```text
    <tipo>[ámbito opcional]: <descripción>

    [cuerpo opcional]

    [pie opcional]
    ```
  * **Ejemplos Prácticos:**
    ```bash
    git commit -m \
      "feat(auth): añade token JWT"

    git commit -m \
      "fix(api): resuelve timeout de login"
    ```

:::
::: {.column width="52%"}

  * **Tipos Canónicos Principales:**
      * `feat:` Nueva funcionalidad para el usuario.
      * `fix:` Corrección de un fallo o error en el código.
      * `docs:` Modificaciones exclusivas en la documentación.
      * `refactor:` Reorganización sin alterar el comportamiento.
      * `test:` Adición o corrección de pruebas automatizadas.
      * `chore:` Tareas de mantenimiento o dependencias.
      * `ci:` / `build:` Integración continua, compilación o empaquetado.

:::
:::::

-----

## Estandarización con Conventional Commits (II): Automatización y Ciclo de Vida

::::: columns
::: {.column width="46%"}

  * **¿Por qué adoptarlo en Ingeniería?**
      * **Generación Automática de *Changelogs*:**
          * Las herramientas de CI/CD analizan el historial y generan notas de lanzamiento categorizadas.
      * **Versionado Semántico (SemVer):**
          * `fix:` $\rightarrow$ incrementa versión **PATCH** (`x.y.Z`)
          * `feat:` $\rightarrow$ incrementa versión **MINOR** (`x.Y.z`)
          * `BREAKING CHANGE:` $\rightarrow$ incrementa **MAJOR** (`X.y.z`)
      * **Trazabilidad y Auditoría:**
          * Facilita *code review*, triaje y auditorías en equipo.

:::
::: {.column width="54%"}

\centering
\includegraphics[width=\linewidth,keepaspectratio]{figures/git_conventional_commits.png}

\vspace{0.4em}

\footnotesize
\textbf{Especificación Oficial:} \href{https://www.conventionalcommits.org/}{\texttt{conventionalcommits.org}}

:::
:::::

-----

## Inspección del Historial: `git log`

La herramienta `git log` permite explorar y filtrar la línea temporal del proyecto:

```bash
# 1. Visualización detallada estándar
git log

# 2. Resumen compacto en una sola línea por commit (Hash corto + Asunto)
git log --oneline

# 3. Representación visual de ramas y fusiones en arte ASCII
git log --graph --oneline --all

# 4. Muestra las diferencias de código introducidas en los últimos 2 commits
git log -p -2

# 5. Estadísticas de archivos modificados, inserciones y eliminaciones
git log --stat
```

-----

## Marcado de Versiones: `git tag`

Una **Tag** es un puntero fijo e inmutable que referencia un commit específico en la historia del proyecto:

::::: columns
::: {.column width="50%"}

  * **Concepto y Propósito:**
      * Funciona como una etiqueta o hito permanente (una versión de lanzamiento).
      * A diferencia de una rama (*branch*), **no se mueve** al crear nuevos commits.
  * **Versionado Semántico ([SemVer](https://semver.org/)):**
      * Formato estandarizado: `vMAJOR.MINOR.PATCH`
        * `v1.0.0` $\rightarrow$ Versión inicial estable
        * `v1.1.0` $\rightarrow$ Nueva funcionalidad compatible
        * `v1.1.1` $\rightarrow$ Corrección de fallos (*patch*)
      * Especificación: \href{https://semver.org/}{\texttt{semver.org}}

:::
::: {.column width="50%"}

  * **Comandos Principales:**
    ```bash
    # 1. Crear una tag en el commit actual (HEAD)
    git tag v1.0.0

    # 2. Crear una tag en un commit anterior
    git tag v0.9.0 9f1a2b3

    # 3. Listar todas las tags existentes
    git tag

    # 4. Visualizar commits con tags
    git log --oneline --decorate
    ```
  * Las tags facilitan recuperar de forma determinista cualquier versión publicada.

:::
:::::

-----

## Archivos No Rastreados: El Rol de `.gitignore`

Ciertos archivos generados durante el desarrollo no deben registrarse en el repositorio:

  * **Archivos a Excluir Obligatoriamente:**
      * Binarios compilados y artefactos de enlace (`*.o`, `*.class`, `*.exe`).
      * Dependencias descargadas (`node_modules/`, `.venv/`).
      * Claves secretas, credenciales y variables de entorno (`.env`).
      * Metadatos transitorios de editores y sistemas operativos (`.DS_Store`, `.vscode/`).
  * **Ejemplo Estructurado de `.gitignore`:**
    ```gitignore
    # Binarios y carpetas de compilación
    bin/
    build/
    *.o

    # Entornos virtuales Python
    .venv/
    __pycache__/

    # Archivos confidenciales y del sistema operativo
    .env
    .DS_Store
    ```

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Ramificación, Integración \& Resolución de Conflictos}}
\end{center}

-----

## El Paradigma de Ramificación (*Branching*) en Git

En muchos sistemas tradicionales, crear una rama implicaba copiar directorios completos de código fuente:

  * **En Git, una Rama es un Puntero Móvil y Ligero:**
      * Consiste en un simple archivo de 41 bytes (40 caracteres del hash SHA-1 + `\n`) que apunta a un commit.
      * **Crear o eliminar** ramas tiene **coste computacional constante ($O(1)$)**; **cambiar** de rama actualiza solo los archivos que difieren en el *Working Tree*.
  * **El Puntero Especial `HEAD` (Referencia Simbólica):**
      * Apunta a la **rama activa** en ese momento (ej.: `HEAD` $\rightarrow$ `main`).
      * Al crear un nuevo commit, el puntero de la rama activa avanza automáticamente hacia el nuevo snapshot (y `HEAD` lo acompaña al apuntar a ella).
  * **Propósito:** Aislar el desarrollo de nuevas funcionalidades o correcciones sin desestabilizar la línea principal (`main`).

-----

## Comandos Esenciales de Gestión de Ramas

Comandos clave para la creación, alternancia y consulta de ramas locales:

```bash
# 1. Crear una nueva rama sin cambiar a ella
git branch feature-login

# 2. Cambiar a una rama existente (sintaxis moderna recomendada)
git switch feature-login

# 3. Crear y cambiar a la rama en un único paso
git switch -c feature-login        # Sintaxis moderna
git checkout -b feature-login      # Sintaxis clásica equivalente

# 4. Listar ramas locales y de seguimiento remoto
git branch -a

# 5. Eliminar una rama local ya integrada (merge realizado)
git branch -d feature-login
```

-----

## Visualización Estructural de Ramas

\begin{center}
\includegraphics[width=0.85\linewidth,keepaspectratio]{figures/git_branch_00.png}
\end{center}

  * **Rama Principal (`main`):** Línea cronológica de código estable y validado.
  * **Ramas de Funcionalidad (*Feature Branches*):** Bifurcaciones temporales donde el código evoluciona aisladamente.
  * La culminación del trabajo desemboca en la integración (*merge*) de regreso a la línea principal.

-----

## Estrategias de Integración: `git merge`

\begin{center}
\includegraphics[width=\linewidth,height=0.36\textheight,keepaspectratio]{figures/git_merge_types_es.png}
\end{center}

\vspace{-0.6em}

::::: columns
::: {.column width="45%"}

  * **Secuencia de Comandos en Terminal:**
    ```bash
    # 1. Cambiar a la rama de destino
    git switch main

    # 2. Integrar la rama de trabajo
    git merge feature-login
    ```

:::
::: {.column width="55%"}

  * **1. Fusión *Fast-Forward* (Lineal):**
      * `main` avanza directamente ($O(1)$) hasta `feature` (**sin nuevos commits**).
  * **2. Fusión *3-Way Merge* (Divergente):**
      * Reconcilia el ancestro común y ambas puntas en un nuevo **Commit de Fusión**.

:::
:::::

-----

## El Desafío de los Merges Repetidos: Historial Complejo

\begin{center}
\includegraphics[width=\linewidth,height=0.46\textheight,keepaspectratio]{figures/git_messy_history.png}
\end{center}

\vspace{-0.4em}

::::: columns
::: {.column width="50%"}

  * **El Problema ("Grafo *Spaghetti*"):**
      * Sincronizaciones repetidas con `git merge` generan decenas de *merge commits* redundantes (*"Merge branch 'main' into..."*).
      * El historial queda sepultado por ruido administrativo en lugar de código con valor funcional.

:::
::: {.column width="50%"}

  * **Impacto y Alternativa:**
      * **Trazabilidad Dificultosa:** Dificulta la lectura con `git log` e inutiliza la depuración con `git bisect`.
      * **Solución:** ¿Cómo mantener las ramas al día con un historial limpio y lineal? $\rightarrow$ `git rebase`!

:::
:::::

-----

## Linealización del Historial con `git rebase`

::::: columns
::: {.column width="48%"}

  * **Concepto y Mecanismo:**
      * "Desprende" los commits de `feature` y los vuelve a aplicar secuencialmente sobre la punta de `main`.
      * Genera nuevos commits (`E'`, `F'`, `G'`) con nuevos hashes SHA, logrando un grafo rectilíneo.

  * **Flujo Recomendado de Trabajo:**
    ```bash
    # 1. Actualizar main con el remoto
    git switch main
    git pull --rebase

    # 2. Reaplicar feature sobre main
    git switch feature-login
    git rebase main
    ```

  * **La Regla de Oro del Rebase:**
      * **NUNCA** ejecutar rebase sobre ramas públicas compartidas. Reescribir historial público rompe la sincronización del equipo.

:::
::: {.column width="52%"}

\centering
\includegraphics[width=\linewidth,height=0.82\textheight,keepaspectratio]{figures/git_merge_vs_rebase_bytebytego.jpg}

:::
:::::

-----

## Matriz Comparativa: `git merge` vs. `git rebase`

| Criterio | `git merge` | `git rebase` |
| :--- | :--- | :--- |
| **Topología del Historial** | No lineal (preserva bifurcaciones y uniones) | **Estrictamente lineal (secuencia única continua)** |
| **Inmutabilidad de Hashes** | **Conserva los hashes SHA originales** | Reescribe y recalcula todos los hashes |
| **Commit de Fusión** | Genera un commit específico (salvo *fast-forward*) | **No genera commits de fusión adicionales** |
| **Fidelidad Cronológica** | Refleja con exactitud la línea temporal real | Reorganiza los commits sobre una nueva base |
| **Seguridad en Equipo** | **Completamente seguro en ramas compartidas** | **Peligroso si se aplica en ramas públicas** |
| **Caso de Uso Primario** | Incorporación formal de código en `main` | Limpieza local de ramas antes de un Pull Request |

-----

## Detección y Resolución de Conflictos de Merge

Un **conflicto de fusión (*merge conflict*)** surge cuando dos ramas modifican **las mismas líneas del mismo archivo** de forma contradictoria:

  * Git interrumpe la operación de merge e inyecta marcadores visuales en el archivo afectado:
    ```text
    <<<<<<< HEAD (estado en la rama actual main)
    int timeout_ms = 5000;
    =======
    int timeout_ms = 10000;
    >>>>>>> feature-login (estado en la rama que se integra)
    ```
  * **Protocolo Riguroso de Resolución:**
      1. Abrir el archivo en conflicto y definir el código correcto unificado.
      2. Eliminar los marcadores de conflicto (`<<<<<<<`, `=======`, `>>>>>>>`).
      3. Añadir el archivo resuelto a la Staging Area: `git add archivo.c`.
      4. Concluir la transacción de fusión ejecutando `git commit`.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Colaboración Distribuida \& Flujos de Trabajo en Equipo}}
\end{center}

-----

## Arquitectura Distribuida: Repositorios Remotos

En un DVCS, la colaboración entre pares se realiza a través de repositorios remotos (*remotes*):

  * **Concepto de Remote:**
      * Un alias configurado que referencia la ubicación de red (URI SSH o HTTPS) de otro clon del proyecto.
  * **El Nombre Convencional `origin`:**
      * Nombre predeterminado que Git asigna al repositorio remoto desde el cual se clonó el código original.
  * **Comandos de Gestión de Remotos:**
    ```bash
    # Listar remotos vinculados y sus respectivas URLs
    git remote -v

    # Vincular un nuevo repositorio remoto bajo el nombre 'origin'
    git remote add origin https://github.com/ua-deti/iei-repo.git

    # Modificar la URL de red de un remoto existente
    git remote set-url origin git@github.com:ua-deti/iei-repo.git
    ```

-----

## Sincronización Remota: `fetch`, `pull` y `push`

La transferencia bidireccional de commits entre repositorios locales y remotos se articula mediante tres operaciones clave:

  * **1. `git fetch origin`:**
      * Descarga los nuevos commits, ramas y referencias del servidor hacia el repositorio local.
      * **No modifica en absoluto los archivos del Working Tree** ni altera ramas locales activas.
  * **2. `git pull origin main`:**
      * Ejecuta de forma secuencial un `git fetch` seguido inmediatamente de un `git merge` en la rama local activa.
  * **3. `git push origin feature-login`:**
      * Publica los commits generados localmente en el repositorio remoto, actualizando la rama en el servidor.

-----

## Git vs. GitHub: Diferenciación Conceptual Rigurosa

Es habitual confundir el motor de control de versiones con la plataforma en la nube:

| Vector de Comparación | Git | GitHub |
| :--- | :--- | :--- |
| **Naturaleza Primaria** | **Motor de software CLI y protocolo de control** | **Plataforma web de alojamiento y colaboración (SaaS)** |
| **Entorno de Ejecución** | Local en el sistema operativo del usuario | Infraestructura en la nube (servidores de Microsoft) |
| **Licenciamiento** | Software Libre y de Código Abierto (GPLv2) | Servicio comercial propietario |
| **Dependencia de Red** | **100% operativo sin conexión a Internet** | Requiere conectividad a Internet permanente |
| **Funcionalidades Clave** | Commits, snapshots, branches, merge, rebase | Pull Requests, Code Review, Issues, CI/CD Actions |
| **Alternativas del Mercado**| Mercurial, SVN | GitLab, Bitbucket, Gitea, Sourcehut |

-----

## Modelos de Flujo Colaborativo: GitFlow

::::: columns
::: {.column width="56%"}

Modelo clásico ([Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/)) basado en múltiples ramas de larga duración (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`):

  * **Ventajas:**
      * Desarrollo paralelo estructurado.
      * Lanzamientos (*releases*) estables y controlados.
      * Soporta múltiples versiones en producción simultáneamente.
  * **Desventajas:**
      * **Flujo de trabajo altamente complejo** y burocrático.
      * Ciclos de lanzamiento lentos (*slow releases*).
      * **Conflictos de *merge* frecuentes** entre ramas divergentes de larga vida.

:::
::: {.column width="44%"}

\begin{center}
\includegraphics[height=0.74\textheight,keepaspectratio]{figures/git_flow_nvie.png}
\end{center}

:::
:::::

-----

## Modelos de Flujo Colaborativo: Trunk-Based Development

En el modelo [**Trunk-Based Development**](https://trunkbaseddevelopment.com/#one-line-summary) puro, todo el equipo integra pequeños *commits* diarios directamente en una única rama compartida (**`trunk` / `main`**):

\begin{center}
\includegraphics[width=0.72\linewidth,keepaspectratio]{figures/trunk_based_pure.png}
\end{center}

::::: columns
::: {.column width="48%"}

  * **Ventajas:**
      * Reducción drástica de conflictos de *merge*.
      * Complejidad y sobrecarga (*overhead*) mínimas.
      * Mejor colaboración e integración continua real.

:::
::: {.column width="52%"}

  * **Desventajas:**
      * Requiere un **equipo altamente maduro** y disciplinado.
      * Aislamiento limitado para funcionalidades en curso.
      * **Alto riesgo de romper la producción** (`main`).

:::
:::::

-----

## Modelo Propuesto: Trunk-Based Escalado (Feature Branches)

La variante **Scaled Trunk-Based Development** conserva las ventajas del modelo *trunk-based*, ofreciendo **mayor control y seguridad para equipos en crecimiento**:

\begin{center}
\includegraphics[width=0.74\linewidth,keepaspectratio]{figures/trunk_based_scaled.png}
\end{center}

  * ***Short-Lived Feature Branches*:** Ramas creadas desde `main` por **1 persona y con una duración máxima de un par de días** (evitando divergencia prolongada).
  * **Control de Calidad previo a la integración:** El código pasa por un **Pull Request (*Code Review* + pruebas/build automáticos CI)** antes de fusionarse en `main`.

-----

## El Núcleo de la Ingeniería Colaborativa: Pull Requests (PR)

En el modelo *Trunk-Based con Feature Branches*, el **Pull Request (PR)** actúa como puerta de calidad antes de integrar cambios en la rama `main`:

  * **Un PR No es un Comando Git:** Es un mecanismo colaborativo de las plataformas (GitHub / GitLab).
  * **Pilares de un Pull Request Profesional:**
      * **Revisión de Código por Pares (*Code Review*):** Inspección línea a línea del *diff* por compañeros del equipo para detectar *bugs*, fallos de seguridad y mejorar la legibilidad.
      * **Automatización de Build y Pruebas (CI/CD):** Compilación y ejecución automática de pruebas y *linters* — el *merge* solo se permite si la *build* pasa.
      * **Debate Técnico Transparente:** Registro histórico de las decisiones técnicas previas a la fusión en `main`.

-----

## Ejemplo Práctico: Flujo Trunk-Based con Feature Branches

```bash
# 1. Asegurar que la rama 'main' local está sincronizada y crear el feature branch de corta duración
git switch main && git pull --rebase
git switch -c feat/autenticacion-oauth

# 2. Desarrollar iterativamente con commits pequeños y atómicos (Conventional Commits)
git add src/auth.c
git commit -m "feat: añade validación de token OAuth2"

# 3. Antes de enviar, actualizar 'main' y linealizar el feature branch (prevenir conflictos)
git switch main && git pull --rebase
git switch feat/autenticacion-oauth && git rebase main

# 4. Publicar la rama en el repositorio remoto y abrir el Pull Request (Code Review + CI) en GitHub
git push -u origin feat/autenticacion-oauth

# 5. Tras la aprobación y merge del PR en GitHub, actualizar 'main' local y eliminar la rama temporal
git switch main && git pull --rebase
git branch -d feat/autenticacion-oauth
```

-----

## Publicación de Versiones y GitHub Releases

La distribución pública de versiones se fundamenta en el envío de tags y la creación de *Releases*:

::::: columns
::: {.column width="48%"}

  * **Publicación de Tags en el Remoto:**
      * Por defecto, `git push` no envía tags al servidor remoto (`origin`).
      * Deben enviarse explícitamente:
        ```bash
        # Enviar una tag específica
        git push origin v1.0.0

        # Enviar todas las tags locales
        git push origin --tags
        ```
  * Todo el equipo y las pipelines de CI/CD pueden referenciar dicho hito exacto.

:::
::: {.column width="52%"}

  * **GitHub Releases:**
      * Funcionalidad de la plataforma construida sobre una tag del repositorio.
      * **Ventajas en la Distribución:**
          * Asocia notas de versión formateadas (*Release Notes / Changelog*).
          * Permite descargar binarios compilados (instaladores, paquetes `.deb`, archivos `.zip`).
          * Permite marcar versiones preliminares (*pre-releases*).

:::
:::::

-----

## Síntesis y Puntos Clave de la Sesión

  * **Superación del Caos Manual:** Git sustituye la duplicación desordenada por un historial inmutable, auditable y criptográficamente seguro.
  * **Arquitectura Distribuida:** Cada clon contiene el historial completo y autónomo, garantizando resiliencia y operaciones locales instantáneas.
  * **Los Tres Estados Locales:** La disciplina operativa requiere dominar **Working Tree**, **Staging Area** y **Repositorio Local**.
  * **Ramificación Ultraligera:** Las ramas instantáneas ($O(1)$) posibilitan flujos de desarrollo concurrentes sin riesgo de interferencia destructiva.
  * **Git vs. GitHub:** Git es el motor local CLI de control de versiones; GitHub aporta la infraestructura de colaboración social, revisión de código y CI/CD.
  * **Colaboración Ágil y Segura:** El modelo *Trunk-Based Development* con *Feature Branches* de corta duración y *Pull Requests* garantiza integración rápida, revisión por pares y estabilidad continua en `main`.

-----

## Referencias Técnicas Autorizadas

Documentación oficial, estándares y referencias recomendadas para profundizar:

  * **Documentación Oficial de Git & Libro Pro Git:**
      * [Pro Git Book (Scott Chacon & Ben Straub)](https://git-scm.com/book/en/v2) — Obra canónica de consulta abierta
      * [Manual de Referencia Oficial de Git](https://git-scm.com/docs)
  * **Flujos Colaborativos & GitHub:**
      * [Trunk Based Development (Paul Hammant)](https://trunkbaseddevelopment.com/)
      * [Buenas Prácticas de Colaboración con Pull Requests](https://docs.github.com/es/pull-requests)
  * **Normas y Especificaciones de la Industria:**
      * [Especificación Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/)
      * [Especificación Semantic Versioning 2.0.0 (SemVer)](https://semver.org/lang/es/)
  * **Tutoriales y Simuladores Interactivos:**
      * [Learn Git Branching (Simulador Gráfico Interactivo)](https://learngitbranching.js.org/?locale=es_ES)
      * [Atlassian Git Workflows & Tutorials](https://www.atlassian.com/es/git/tutorials)

