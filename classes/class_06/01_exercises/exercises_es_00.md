---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Control de Versiones con Git & Plataforma Colaborativa GitHub"
institute: Universidade de Aveiro
date: November 02, 2026
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

**Contexto Pedagógico & Objetivos:**
El control de versiones distribuido con **Git** y la colaboración mediante plataformas en la nube como **GitHub** constituyen la columna vertebral de la ingeniería de software contemporánea. En esta sesión práctica de **3 horas**, aplicará paso a paso todos los conceptos abordados en la presentación teórica, adquiriendo la disciplina operativa para controlar el ciclo de vida del código fuente con trazabilidad, reversibilidad y colaboración segura en equipo:

* **Parte 0 — Configuración del Entorno & Autenticación en GitHub:** Instalación de Git, configuración de identidad (`user.name`, `user.email`) y autenticación criptográfica segura con GitHub mediante clave SSH `ed25519`.
* **Parte 1 — Aspectos Funcionales de Git & Ciclo de Vida Local:** Inicialización de repositorios (`git init`), transición entre las tres zonas operativas (*Working Tree*, *Staging Area* y *Repositorio Local*) y los cuatro estados de los archivos, buenas prácticas (regla 50/72) y estandarización con *Conventional Commits*, inspección detallada con `git log`, marcado local de versiones con `git tag` ([SemVer](https://semver.org/)) y exclusión de artefactos con `.gitignore`.
* **Parte 2 — Ramificación, Integración & Resolución de Conflictos:** El paradigma de ramas como punteros ligeros ($O(1)$) y el puntero simbólico `HEAD`, comandos de gestión (`git branch`, `git switch`, `git switch -c`, `git branch -d`), estrategias de integración con `git merge` (*Fast-Forward* vs. *3-Way Merge*), linealización del historial con `git rebase` y resolución manual de conflictos de *merge*.
* **Parte 3 — Colaboración Distribuida, Flujos de Trabajo & GitHub Releases:** Gestión de repositorios remotos (`origin`), sincronización con `fetch`, `pull` y `push`, ejecución *end-to-end* del modelo **Scaled Trunk-Based Development** (con *Short-Lived Feature Branches* y *Pull Requests* con *Code Review*) y publicación oficial de versiones con **GitHub Releases**.

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Antes de iniciar los ejercicios, cree y acceda a la carpeta de trabajo dedicada para esta sesión de laboratorio:

```bash
$ mkdir -p ~/IEI/clase06
$ cd ~/IEI/clase06
```

Todos los repositorios locales y archivos creados durante la clase deberán organizarse dentro de este directorio de trabajo.

> **Nota sobre rutas de archivos:**
> Los comandos de esta guía asumen que la terminal está posicionada en el directorio de trabajo `~/IEI/clase06`.

-----

## Parte 0: Configuración del Entorno & Autenticación en GitHub

Antes de iniciar el desarrollo, es necesario preparar el cliente Git local y establecer la autenticación segura con la plataforma GitHub.

### Paso 1: Instalación y Verificación de Git

En sistemas basados en Debian/Ubuntu, verifique si Git se encuentra instalado o proceda a su instalación:

```bash
$ sudo apt update && sudo apt install -y git
$ git --version
```

### Paso 2: Configuración Global de Identidad

Git incorpora la identidad del autor de forma inmutable en cada *commit* creado. Configure su nombre completo, su dirección de correo electrónico institucional de la Universidad de Aveiro y el nombre predeterminado de la rama principal (`main`):

```bash
$ git config --global user.name "Su Nombre Completo"
$ git config --global user.email "su.email@ua.pt"
$ git config --global init.defaultBranch main
```

Puede consultar la configuración guardada en `~/.gitconfig` ejecutando:

```bash
$ git config --global --list
```

### Paso 3: Autenticación Segura con GitHub

Para sincronizar código con GitHub (`git push`), la plataforma exige autenticación mediante clave SSH (recomendada) o *Personal Access Token* (PAT).

#### Método Recomendado: Par de Claves SSH (ed25519)

1. Genere un nuevo par de claves SSH utilizando el algoritmo `ed25519`:
   ```bash
   $ ssh-keygen -t ed25519 -C "su.email@ua.pt" -f ~/.ssh/id_ed25519 -N ""
   ```
2. Visualice y copie el contenido íntegro de su **clave pública** (`.pub`):
   ```bash
   $ cat ~/.ssh/id_ed25519.pub
   ```
   *(El contenido debe comenzar por `ssh-ed25519 AAAAC3...` y terminar en su email).*
3. Registre la clave pública en su cuenta de GitHub:
   * Acceda a [GitHub.com](https://github.com/) e inicie sesión.
   * En la esquina superior derecha, haga clic en la foto de perfil $\rightarrow$ **Settings**.
   * En la barra lateral izquierda (sección *Access*), seleccione **SSH and GPG keys**.
   * Haga clic en el botón verde **New SSH key**.
   * Rellene el campo **Title** con un identificador del equipo (ej.: `Portátil Ubuntu IEI`).
   * En el campo **Key**, pegue exactamente el texto copiado de la clave pública y haga clic en **Add SSH key**.
4. Pruebe la conexión segura desde la terminal:
   ```bash
   $ ssh -T git@github.com
   ```
   > En la primera conexión, confirme la huella digital (*fingerprint*) del servidor escribiendo `yes`. Deberá recibir la confirmación:
   > `Hi <usuario>! You've successfully authenticated, but GitHub does not provide shell access.`

#### Método Alternativo: Personal Access Token (PAT)

En caso de no disponer de acceso SSH en la red actual:
1. En GitHub, acceda a **Settings** $\rightarrow$ **Developer settings** $\rightarrow$ **Personal access tokens** $\rightarrow$ **Fine-grained tokens**.
2. Haga clic en **Generate new token**, defina un nombre descriptivo (ej.: `IEI-Token-Clase06`), elija la validez y conceda permiso **Read and write** en **Repository permissions $\rightarrow$ Contents**.
3. Copie inmediatamente el token generado (`github_pat_...`) y utilícelo como contraseña en las operaciones HTTPS.

-----

## Parte 1: Aspectos Funcionales de Git & Ciclo de Vida Local

En esta parte (correspondiente a la **Parte II** de las diapositivas teóricas), operará localmente sobre las tres zonas de Git (**Working Tree**, **Staging Area** y **Repositorio Local**), sin depender de conexión a Internet.

### Ejercicio 1: Inicialización del Repositorio (`git init`) y Estructura `.git/`

1. Cree una carpeta para su proyecto e inicialícela como repositorio Git:
   ```bash
   $ mkdir ~/IEI/clase06/mi-proyecto && cd ~/IEI/clase06/mi-proyecto
   $ git init
   ```
2. Inspeccione el directorio oculto `.git/` creado automáticamente:
   ```bash
   $ ls -la .git/
   $ cat .git/HEAD
   ```
   > **Comprensión Arquitectural:**
   > El directorio `.git/` es la base de datos local que almacena todo el grafo del historial, objetos comprimidos (`objects/`), punteros de ramas (`refs/heads/`) y la referencia simbólica `HEAD` (`ref: refs/heads/main`).

### Ejercicio 2: Las Tres Zonas y Estados de los Archivos (`status`, `add`, `commit`)

Al transitar entre el **Working Tree**, la **Staging Area** y el **Repositorio Local**, cada archivo asume uno de cuatro estados: **Untracked**, **Modified**, **Staged** o **Unmodified**.

1. Cree un archivo `index.html` en su *Working Tree*:
   ```html
   <!DOCTYPE html>
   <html lang="es">
   <head>
       <meta charset="UTF-8">
       <title>Portal IEI - Universidad de Aveiro</title>
   </head>
   <body>
       <h1>Bienvenido al Proyecto de IEI</h1>
       <p>Control de versiones distribuido con Git y GitHub.</p>
   </body>
   </html>
   ```
2. Inspeccione el estado con `git status`:
   ```bash
   $ git status
   ```
   El archivo aparece en rojo como **Untracked** (Git aún no lo monitoriza).
3. Promueva el archivo a la **Staging Area / Index** con `git add`:
   ```bash
   $ git add index.html
   $ git status
   ```
   El archivo aparece ahora en verde en el estado **Staged** (*Changes to be committed*).
4. Consolide el contenido de la *Staging Area* en un snapshot permanente en el **Repositorio Local** usando `git commit`:
   ```bash
   $ git commit -m "feat: añade estructura HTML inicial de la página principal"
   $ git status
   ```
   El archivo se encuentra ahora en el estado **Unmodified** (*nothing to commit, working tree clean*).
5. Edite el archivo `index.html` añadiendo un pie de página antes de `</body>`:
   ```html
       <footer>DETI - Universidad de Aveiro</footer>
   ```
   Ejecute `git status` y verifique que el archivo ya rastreado pasó al estado **Modified** (en rojo, *Changes not staged for commit*).
6. **Prueba de Desindexación (`git restore --staged`):**
   Si prepara un archivo modificado por error (`git add`), puede retirarlo de la *Staging Area* de vuelta al estado *Modified* en el *Working Tree* sin perder sus ediciones en disco:
   ```bash
   $ git add index.html
   $ git restore --staged index.html
   $ git status
   ```

### Ejercicio 3: Buenas Prácticas (50/72), Conventional Commits y Rectificación (`--amend`)

Como se abordó en las diapositivas teóricas, los mensajes de commit estructurados según la especificación [Conventional Commits](https://www.conventionalcommits.org/) (`<tipo>[ámbito opcional]: <descripción>`) facilitan auditorías rápidas, generación automática de *changelogs* y cálculo automático de versiones SemVer.

1. Indexe la modificación realizada en `index.html` y simule un commit con un mensaje descuidado (antipatrón):
   ```bash
   $ git add index.html
   $ git commit -m "cambios en html"
   $ git log --oneline
   ```
2. Corrija el último commit utilizando `git commit --amend`, reemplazándolo por un mensaje que respete la **convención 50/72** (asunto conciso en modo imperativo $\le 50$ caracteres, seguido de cuerpo explicativo separado por una línea en blanco):
   ```bash
   $ git commit --amend -m "feat(ui): añade pie de página institucional en la portada" \
   -m "Incluye identificación oficial del departamento para cumplir la guía de estilo."
   $ git log --oneline
   ```
   > **Nota Técnica:** El comando `--amend` reemplaza el último commit por un nuevo objeto con nuevo hash SHA-1. Solo debe utilizarse en commits locales que **aún no hayan sido compartidos** mediante `push`.
3. Cree un archivo de documentación `README.md` y registre un commit del tipo `docs:`:
   ```bash
   $ cat << 'EOF' > README.md
   # Portal IEI
   Proyecto de laboratorio de la Clase 06 de Introducción a la Ingeniería Informática.
   EOF
   $ git add README.md
   $ git commit -m "docs: añade documentación inicial en el archivo README"
   ```

### Ejercicio 4: Inspección del Historial (`git log`) y Marcado de Versiones (`git tag`)

1. Practique las cinco variantes de inspección del historial estudiadas en las diapositivas teóricas:
   ```bash
   # 1. Presentación detallada estándar (autor, fecha, hash SHA completo y cuerpo)
   $ git log

   # 2. Vista compacta de una línea por commit (Hash corto + Asunto)
   $ git log --oneline

   # 3. Representación visual de la topología en ASCII
   $ git log --graph --oneline --all

   # 4. Visualización de diferencias de código (diff) introducidas en los últimos 2 commits
   $ git log -p -2

   # 5. Resumen estadístico de archivos modificados, inserciones y eliminaciones
   $ git log --stat
   ```
2. **Marcado de Versiones con `git tag` y Versionado Semántico ([SemVer](https://semver.org/)):**
   A diferencia de una rama (*branch*), una **tag** es un puntero fijo e inmutable hacia un commit específico (`vMAJOR.MINOR.PATCH`):
   ```bash
   # 1. Crear una tag ligera en el commit actual (HEAD)
   $ git tag v0.1.0

   # 2. Listar todas las tags existentes en el repositorio
   $ git tag

   # 3. Visualizar los commits con sus respectivas tags y punteros asociados
   $ git log --oneline --decorate
   ```

### Ejercicio 5: Exclusión de Archivos No Rastreados (`.gitignore`)

Binarios compilados (`*.o`), dependencias (`node_modules/`, `.venv/`), secretos locales (`.env`) y metadatos del sistema (`.DS_Store`) nunca deben ser versionados.

1. Simule la presencia de un archivo de credenciales sensibles y de un binario compilado en el *Working Tree*:
   ```bash
   $ echo "API_SECRET_KEY=9988776655" > .env
   $ touch modulo.o
   $ git status
   ```
2. Cree el archivo `.gitignore` con las reglas de exclusión estudiadas:
   ```bash
   $ cat << 'EOF' > .gitignore
   # Binarios y directorios de compilación
   bin/
   build/
   *.o

   # Entornos virtuales Python
   .venv/
   __pycache__/

   # Archivos sensibles y de configuración local
   .env
   .DS_Store
   EOF
   ```
3. Verifique con `git status` que `.env` y `modulo.o` dejaron de aparecer como *Untracked*:
   ```bash
   $ git status
   ```
4. Indexe y consolide `.gitignore` con el tipo `chore:`:
   ```bash
   $ git add .gitignore
   $ git commit -m "chore: configura reglas de exclusión en .gitignore"
   ```

-----

## Parte 2: Ramificación, Integración & Resolución de Conflictos

En esta parte (correspondiente a la **Parte III** de las diapositivas teóricas), explorará el modelo de ramificación en $O(1)$ de Git, comparará los dos tipos de `git merge` (*Fast-Forward* vs. *3-Way Merge*), linealizará el historial con `git rebase` y resolverá conflictos de fusión.

### Ejercicio 6: Paradigma de Ramas ($O(1)$) y Comandos de Gestión

En Git, una rama es simplemente un archivo de **41 bytes** (40 caracteres del hash SHA-1 + `\n`) guardado en `.git/refs/heads/`.

1. Cree y cambie a una nueva rama `feature-login` en un único paso utilizando la sintaxis moderna recomendada (`git switch -c`):
   ```bash
   $ git switch -c feature-login
   ```
   *(Nota: En la sintaxis clásica equivalente se utilizaba `git checkout -b feature-login`).*
2. Verifique cómo representa Git esta rama internamente en `.git/`:
   ```bash
   $ cat .git/HEAD
   $ cat .git/refs/heads/feature-login
   $ wc -c .git/refs/heads/feature-login
   ```
   > **Confirmación Experimental:** ¡El archivo `.git/refs/heads/feature-login` tiene exactamente **41 bytes**! Y `.git/HEAD` apunta simbólicamente a `ref: refs/heads/feature-login`.
3. Liste todas las ramas existentes:
   ```bash
   $ git branch -a
   ```
4. Cree un archivo `login.html` para desarrollar esta funcionalidad de forma aislada:
   ```html
   <!DOCTYPE html>
   <html lang="es">
   <head>
       <meta charset="UTF-8">
       <title>Autenticación - Portal IEI</title>
   </head>
   <body>
       <h1>Iniciar Sesión</h1>
   </body>
   </html>
   ```
5. Indexe y haga commit en la rama `feature-login`:
   ```bash
   $ git add login.html
   $ git commit -m "feat(auth): crea página de autenticación de usuarios"
   ```
6. Cambie de vuelta a `main` y observe el *Working Tree*:
   ```bash
   $ git switch main
   $ ls -la
   ```
   El archivo `login.html` desapareció del directorio de trabajo, pues pertenece exclusivamente a la rama `feature-login`.

### Ejercicio 7: Estrategias de Integración con `git merge` (*Fast-Forward* vs. *3-Way*)

1. **Escenario 1 — Fusión *Fast-Forward* (Lineal):**
   Como la rama `main` no recibió nuevos commits desde la creación de `feature-login`, integre la rama ejecutando la secuencia de comandos estudiada:
   ```bash
   $ git switch main
   $ git merge feature-login
   ```
   Observe el mensaje `Fast-forward`: el puntero `main` simplemente avanzó en $O(1)$ hasta el commit de `feature-login`, **sin crear ningún commit de fusión**.
2. Elimine con seguridad la rama `feature-login` ya integrada:
   ```bash
   $ git branch -d feature-login
   ```
3. **Escenario 2 — Fusión *3-Way Merge* (Ramas Divergentes):**
   Vamos ahora a crear una divergencia real entre `main` y una nueva rama `feature-estilos`:
   ```bash
   # 1. Crear y cambiar a la rama feature-estilos
   $ git switch -c feature-estilos
   $ echo "body { font-family: Arial, sans-serif; }" > style.css
   $ git add style.css
   $ git commit -m "feat(ui): añade hoja de estilos CSS"

   # 2. Regresar a main y realizar un commit independiente en otro archivo
   $ git switch main
   $ echo "Licencia MIT - 2026" > LICENSE
   $ git add LICENSE
   $ git commit -m "docs: añade archivo de licencia MIT"
   ```
4. Ahora las dos historias han divergido a partir de su ancestro común. Integre `feature-estilos` en `main`:
   ```bash
   $ git merge feature-estilos -m "Merge branch 'feature-estilos' into main"
   ```
5. Visualice el grafo resultante y elimine la rama temporal:
   ```bash
   $ git log --graph --oneline --all
   $ git branch -d feature-estilos
   ```
   > **Observación:** ¡Como las ramas habían divergido, Git ejecutó un **3-Way Merge**, creando un nuevo **Commit de Fusión (*Merge Commit*)** con dos padres!

### Ejercicio 8: Linealización del Historial con `git rebase`

Como vimos en las diapositivas teóricas, las sincronizaciones repetidas mediante *3-Way Merge* generan historiales complejos ("grafo *spaghetti*"). `git rebase` resuelve este problema reaplicando los commits de la rama de funcionalidad sobre el extremo actualizado de `main`.

1. Cree una nueva rama `feature-perfil` y registre un commit:
   ```bash
   $ git switch -c feature-perfil
   $ echo "<h1>Perfil del Estudiante</h1>" > perfil.html
   $ git add perfil.html
   $ git commit -m "feat(perfil): añade página de perfil del estudiante"
   ```
2. Regrese a `main` y simule una actualización concurrente en la línea principal:
   ```bash
   $ git switch main
   $ echo "Versión: 0.2.0" >> README.md
   $ git add README.md
   $ git commit -m "docs: registra número de versión en README"
   ```
3. ¡Las ramas `main` y `feature-perfil` han vuelto a divergir! En lugar de usar `git merge` (que crearía una nueva bifurcación), cambie a `feature-perfil` y linealícela sobre `main` con `git rebase`:
   ```bash
   $ git switch feature-perfil
   $ git rebase main
   ```
   > **Mecanismo Interno:** Git "desprendió" el commit de `feature-perfil` y lo reaplicó sobre el extremo más reciente de `main`, generando un nuevo commit (`E'`) con nuevo hash SHA.
4. Ahora regrese a `main` e integre `feature-perfil`:
   ```bash
   $ git switch main
   $ git merge feature-perfil
   $ git branch -d feature-perfil
   ```
5. Inspeccione el historial con `git log --graph --oneline`:
   ```bash
   $ git log --graph --oneline
   ```
   ¡Observe que la integración ocurrió por **Fast-Forward** y la cima del historial se mantuvo **estrictamente lineal**!
   > **Regla de Oro del Rebase:** **NUNCA** ejecute `git rebase` sobre ramas públicas compartidas con compañeros, pues la reescritura de hashes SHA rompe la sincronización del equipo.

### Ejercicio 9: Detección y Resolución de Conflictos de Merge

Un conflicto ocurre cuando dos ramas alteran **las mismas líneas en el mismo archivo** de forma contradictoria.

1. En `main`, cree un archivo de configuración `config.txt`:
   ```bash
   $ echo "timeout_ms = 5000" > config.txt
   $ git add config.txt
   $ git commit -m "chore(config): define timeout por defecto de 5000ms"
   ```
2. Cree una rama `feature-timeout` y cambie el valor a `10000`:
   ```bash
   $ git switch -c feature-timeout
   $ echo "timeout_ms = 10000" > config.txt
   $ git add config.txt
   $ git commit -m "perf(config): aumenta timeout a 10000ms en redes lentas"
   ```
3. Vuelva a `main` y modifique la **misma línea** de `config.txt` a `3000`:
   ```bash
   $ git switch main
   $ echo "timeout_ms = 3000" > config.txt
   $ git add config.txt
   $ git commit -m "perf(config): reduce timeout a 3000ms en la rama principal"
   ```
4. Intente integrar `feature-timeout` en `main`:
   ```bash
   $ git merge feature-timeout
   ```
   Git suspende el merge y emite el aviso:
   ```text
   Auto-merging config.txt
   CONFLICT (content): Merge conflict in config.txt
   Automatic merge failed; fix conflicts and then commit the result.
   ```
5. Inspeccione el contenido de `config.txt` para observar los marcadores visuales inyectados por Git:
   ```bash
   $ cat config.txt
   ```
   ```text
   <<<<<<< HEAD
   timeout_ms = 3000
   =======
   timeout_ms = 10000
   >>>>>>> feature-timeout
   ```
6. **Protocolo de Resolución (4 pasos de las diapositivas teóricas):**
   * **Pasos 1 & 2:** Decida el valor final (ej.: `8000`) y reemplace el contenido del archivo **eliminando todos los marcadores** (`<<<<<<<`, `=======`, `>>>>>>>`):
     ```bash
     $ echo "timeout_ms = 8000" > config.txt
     ```
   * **Paso 3:** Añada el archivo resuelto a la *Staging Area*:
     ```bash
     $ git add config.txt
     ```
   * **Paso 4:** Concluya el merge commit:
     ```bash
     $ git commit -m "fix(config): resuelve conflicto de merge"
     $ git branch -d feature-timeout
     ```

-----

## Parte 3: Colaboración Distribuida, Flujos de Trabajo & GitHub Releases

En esta parte final (correspondiente a la **Parte IV** de las diapositivas teóricas), publicará el proyecto en GitHub, sincronizará cambios remotos (`fetch`, `pull`, `push`), ejecutará el modelo colaborativo propuesto (**Scaled Trunk-Based Development con Feature Branches y Pull Requests**) y publicará una **GitHub Release**.

### Ejercicio 10: Repositorios Remotos (`origin`) y Sincronización (`push`, `fetch`, `pull`)

1. En su navegador, acceda a [GitHub.com](https://github.com/) y cree un **nuevo repositorio vacío**:
   * **Repository name:** `iei-proyecto-git`
   * **Visibility:** Public
   * **Importante:** **NO** seleccione *Add a README file*, `.gitignore` ni *license*. Haga clic en **Create repository**.
2. En su terminal local (`~/IEI/clase06/mi-proyecto`), asocie el repositorio remoto bajo el nombre convencional `origin`:
   ```bash
   # Reemplace <USUARIO> por su username de GitHub
   $ git remote add origin git@github.com:<USUARIO>/iei-proyecto-git.git
   $ git remote -v
   ```
   *(Si utiliza HTTPS/PAT, use `https://github.com/<USUARIO>/iei-proyecto-git.git`).*
3. **Publicar la rama local (`git push`):**
   ```bash
   $ git push -u origin main
   ```
   Actualice la página de GitHub en el navegador y confirme que todo el código e historial están ahora alojados en la nube.
4. **Diferencia práctica entre `git fetch` y `git pull`:**
   * En la interfaz web de GitHub, haga clic en el archivo `README.md`, pulse el icono del lápiz (**Edit this file**), añada una línea al final (`## Equipo de Desarrollo`) y haga clic en **Commit changes...** directamente en el navegador.
   * ¡El servidor remoto (`origin/main`) tiene ahora un commit nuevo que su equipo local desconoce!
   * En la terminal local, ejecute primero `git fetch origin`:
     ```bash
     $ git fetch origin
     $ cat README.md
     $ git log --graph --oneline --all
     ```
     > **Verificación:** Como se estudió en las diapositivas, `git fetch` descargó el nuevo commit del servidor (visible en `origin/main` en `git log`), pero **no alteró los archivos de su Working Tree**!
   * Ahora integre los cambios descargados en su rama `main` local:
     ```bash
     $ git pull --rebase origin main
     $ cat README.md
     ```

### Ejercicio 11: Modelo Propuesto — Flujo Trunk-Based con Feature Branches & Pull Requests

En los proyectos en equipo, adoptamos **Scaled Trunk-Based Development**: creamos *Short-Lived Feature Branches* a partir de `main`, las mantenemos actualizadas con `rebase` y las integramos mediante **Pull Requests (PR)** con **Revisión de Código (*Code Review*)**.

Ejecute la secuencia completa paso a paso (idéntica al ejemplo práctico de las diapositivas teóricas):

```bash
# 1. Asegurar que la rama 'main' local está sincronizada
# y crear el feature branch de corta duración
$ git switch main && git pull --rebase
$ git switch -c feat/autenticacion-oauth
```

2. **Desarrollar de forma iterativa con commits pequeños y atómicos (Conventional Commits):**
   ```bash
   $ echo "<h2>Autenticación Segura vía OAuth2</h2>" >> login.html
   $ git add login.html
   $ git commit -m "feat(auth): añade soporte de autenticación OAuth2"
   ```
3. **Antes de enviar, actualizar `main` y linealizar el feature branch (prevenir conflictos):**
   ```bash
   $ git switch main && git pull --rebase
   $ git switch feat/autenticacion-oauth && git rebase main
   ```
4. **Publicar la rama en el repositorio remoto:**
   ```bash
   $ git push -u origin feat/autenticacion-oauth
   ```
5. **Abrir el Pull Request y realizar *Code Review* en GitHub:**
   * Acceda a la página de su repositorio en GitHub y haga clic en el botón verde **Compare & pull request**.
   * Confirme la dirección de fusión: `base: main` $\leftarrow$ `compare: feat/autenticacion-oauth`.
   * Complete la descripción explicando el objetivo de la funcionalidad y haga clic en **Create pull request**.
   * En la página del Pull Request, haga clic en la pestaña **Files changed**, sitúe el cursor sobre la línea añadida en `login.html`, pulse el icono `+` y añada un comentario de revisión (*Code Review*).
   * Regrese a la pestaña **Conversation** y concluya la integración haciendo clic en **Merge pull request** $\rightarrow$ **Confirm merge**.
6. **Tras la aprobación y merge del PR en GitHub, actualizar `main` local y eliminar la rama temporal:**
   ```bash
   $ git switch main && git pull --rebase
   $ git branch -d feat/autenticacion-oauth
   $ git log --oneline -5
   ```

### Ejercicio 12: Publicación de Versiones y GitHub Releases

Para cerrar el ciclo de desarrollo, etiquetaremos la versión estable `v1.0.0` (tras el merge del Pull Request) y publicaremos una **GitHub Release** oficial:

1. En la terminal (en la rama `main` actualizada), cree la tag ligera `v1.0.0`:
   ```bash
   $ git tag v1.0.0
   ```
2. Como `git push` estándar no transfiere etiquetas al servidor, publique la tag explícitamente en el remoto `origin`:
   ```bash
   $ git push origin v1.0.0
   ```
   *(Nota: Para enviar todas las tags locales de una sola vez, también puede utilizar `git push origin --tags`).*
3. **Crear la Release en la plataforma GitHub:**
   * En la página principal del repositorio en GitHub, localice la sección **Releases** (barra lateral derecha) y haga clic en **Create a new release** (o **Draft a new release**).
   * En **Choose a tag**, seleccione `v1.0.0`.
   * En **Release title**, escriba `v1.0.0 — Primera Versión Estable`.
   * Haga clic en el botón **Generate release notes** (¡para ver cómo GitHub genera automáticamente el *changelog* a partir de sus *Conventional Commits* y *Pull Requests*!) y pulse **Publish release**.

-----

## Parte 4: Desafíos Autónomos de Consolidación

Para consolidar sus competencias, experimente los siguientes desafíos autónomos:

### Desafío A: La "Máquina del Tiempo" y el Estado *Detached HEAD*
1. Consulte el historial compacto: `git log --oneline`.
2. Elija el hash SHA de su primer commit (ej.: `98ca9c2`) y ejecute:
   ```bash
   $ git checkout <HASH_DEL_PRIMER_COMMIT>
   ```
3. Ejecute `git status` y verifique que Git avisa de que está en **Detached HEAD** (el puntero `HEAD` apunta directamente a un commit en lugar de apuntar simbólicamente a una rama).
4. Verifique con `ls` que todos los archivos creados después de ese commit desaparecieron temporalmente del *Working Tree*.
5. Regrese inmediatamente al presente con seguridad mediante:
   ```bash
   $ git switch main
   ```

### Desafío B: Localización Rápida de Cambios con `git log -S`
1. Suponga que desea descubrir exactamente en qué commit se introdujo la expresión `"OAuth2"` en el proyecto:
   ```bash
   $ git log -S "OAuth2" -p
   ```
2. Observe cómo la opción `-S` (*pickaxe*) busca en la historia los commits que añadieron o eliminaron apariciones de esa cadena.

-----

## Síntesis de los Comandos Esenciales Abordados

| Comando | Descripción Operativa |
| :--- | :--- |
| `git init` | Inicializa un nuevo repositorio Git local (`.git/`). |
| `git clone <url>` | Clona un repositorio remoto completo en la máquina local. |
| `git status` | Inspecciona el estado de los archivos en el *Working Tree* y *Staging Area*. |
| `git add <archivo>` | Promueve cambios del *Working Tree* a la *Staging Area*. |
| `git restore --staged <arch>` | Retira un archivo de la *Staging Area* sin alterar el *Working Tree*. |
| `git commit -m "<msg>"` | Registra el contenido de la *Staging Area* en un nuevo snapshot inmutable. |
| `git commit --amend` | Reemplaza el último commit local corrigiendo su mensaje o contenido. |
| `git log --oneline --graph` | Visualiza el historial y la topología de ramas de forma compacta. |
| `git tag v1.0.0` | Crea una etiqueta ligera (*lightweight tag*) en el commit actual (`HEAD`). |
| `git branch -a` | Lista todas las ramas locales y remotas conocidas. |
| `git switch <rama>` | Cambia a una rama existente actualizando el *Working Tree*. |
| `git switch -c <nueva-rama>` | Crea una nueva rama y cambia inmediatamente a ella. |
| `git merge <rama>` | Integra la rama especificada en la rama activa (*Fast-Forward* o *3-Way*). |
| `git rebase main` | Linealiza la rama actual reaplicando sus commits sobre el extremo de `main`. |
| `git branch -d <rama>` | Elimina con seguridad una rama local ya integrada. |
| `git remote add origin <url>` | Registra un servidor remoto bajo el identificador estándar `origin`. |
| `git fetch origin` | Descarga novedades del remoto sin alterar el *Working Tree* local. |
| `git pull --rebase` | Sincroniza la rama local linealizándola sobre el extremo del servidor remoto. |
| `git push -u origin <rama>` | Publica los commits de la rama local en el repositorio remoto. |
| `git push origin v1.0.0` | Publica explícitamente una etiqueta de versión en el servidor remoto. |
