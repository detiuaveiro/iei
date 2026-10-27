---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Contenedores de Aplicación & Desktop Sandboxing en Linux"
institute: Universidade de Aveiro
date: October 26, 2026
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

  * **Parte I — Dependencias y Requisitos de Confinamiento:**
      * Docker en la infraestructura vs. limitaciones en el escritorio, *dependency hell*, modelos alternativos (Windows, macOS, venv) y requisitos de confinamiento.
  * **Parte II — Paradigmas de Contenedorización Desktop:**
      * Análisis conceptual y comparativo de **AppImage**, **Snap** y **Flatpak** (arquitectura, seguridad y distribución).
  * **Parte III — Empaquetamiento con AppImage y Flatpak:**
      * Construcción práctica de artefactos: jerarquía `AppDir`, manifiestos YAML, integración gráfica (Pygame) y `flatpak-builder`.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Dependencias y Requisitos de Confinamiento}}
\end{center}

-----

## Docker y OCI en la Infraestructura vs. Limitaciones en el Escritorio

El ecosistema Docker y los estándares OCI fueron diseñados para servicios de infraestructura:

  * **Contenedores de Infraestructura (Docker & OCI):**
      * **Servicios *Headless*:** Optimizados para procesos de servidor (APIs, bases de datos) sin interfaz gráfica.
      * **Red y Orquestación:** Redes virtuales privadas (*bridge*), mapeo de puertos y orquestación en clúster.
      * **Privilegios:** Gestión mediante daemon centralizado con privilegios de administración (`dockerd` en `root`).

  * **Limitaciones para Aplicaciones Desktop:**
      * **Gráficos y Audio:** Sin soporte nativo para Wayland/X11, aceleración 3D (`/dev/dri`) o PipeWire.
      * **Integración en el Sistema:** Sin accesos directos en menús/dock, notificaciones nativas o asociación de archivos.
      * **Seguridad y Archivos:** Sin delegación dinámica de accesos; los *bind mounts* exponen carpetas sin mediación.

-----

## Gestión de Dependencias Dinámicas (*Dependency Hell*)

La distribución de aplicaciones desktop afronta el reto de las dependencias compartidas:

  * **Arquitectura Tradicional en Linux:**
      * Uso compartido global de bibliotecas dinámicas (`.so` en `/usr/lib`).
  * **Conflicto de Versiones:**
      * La Aplicación A requiere `libXYZ v1.0` vs. la Aplicación B requiere `libXYZ v2.0`.
  * **Limitación de los Gestores de Paquetes (`apt`, `dnf`):**
      * Admiten únicamente una versión global de cada biblioteca en el sistema.
      * Instalar o actualizar la Aplicación B rompe la Aplicación A (*breaking changes*).
  * **Fragmentación del Ecosistema:**
      * Exige compilación y empaquetamiento específico por distribución (Debian, Fedora, Arch).

-----

## El Problema de las Dependencias Compartidas

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{dependency_hell.png}
\end{center}

-----

## Otros Sistemas Operativos: El Modelo de Bundling (Windows y macOS)

Estrategias de empaquetamiento autónomo para sortear conflictos globales de bibliotecas:

  * **Microsoft Windows (Carga Local de DLLs):**
      * Cada aplicación incluye sus bibliotecas (`.dll`) en su propia carpeta (`Program Files`).
      * **Ventaja:** Evita colisiones en el sistema global de archivos.
      * **Compromiso:** Elevada duplicación en disco; ausencia de sandbox por defecto.
  * **Apple macOS (Paquetes Autocontenidos .app):**
      * Estructura de directorio unificada que agrupa binario ejecutable, recursos y bibliotecas (`.dylib`).
      * **Ventaja:** Modelo desacoplado y fácil de transportar por el usuario.
      * **Compromiso:** Duplicación de archivos; depende de una plataforma de SO uniforme y propietaria.

-----

## Aislamiento a Nivel de Lenguaje: El Caso de Python (venv)

¿Por qué no resolver la distribución desktop únicamente con entornos virtuales de lenguaje?

  * **Lo que `venv` resuelve:**
      * Crea un árbol local (`.venv`) aislando paquetes y módulos Python (`site-packages`).
      * Garantiza la reproducibilidad de dependencias Python mediante `requirements.txt`.
  * **Por qué no es suficiente para Aplicaciones Desktop:**
      * **Sin Confinamiento:** El código se ejecuta con todos los permisos del usuario (sin sandbox).
      * **Dependencia del Sistema Anfitrión:** Requiere Python preinstalado y **no incluye bibliotecas C del sistema** (ej.: SDL2, libGL y audio requeridos por Pygame).
      * **Sin Integración Desktop:** No crea entradas en el menú, no gestiona permisos de ventanas ni asocia tipos MIME.

-----

## Requisitos de Aislamiento y Confinamiento (*Sandboxing*)

Frente a las limitaciones de los modelos tradicionales, el escritorio Linux exige tres garantías:

  * **Portabilidad Determinista (*Run Anywhere*):**
      * Ejecución idéntica y reproducible en cualquier distribución Linux.
  * **Estabilidad y No Interferencia:**
      * Instalar, actualizar o desinstalar una aplicación no afecta al resto del sistema.
  * **Confinamiento de Seguridad (*Sandboxing*):**
      * Sin acceso no autorizado a archivos personales (`$HOME`, `~/.ssh`), credenciales o periféricos (cámara, micrófono).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Paradigmas de Contenedorización Desktop}}
\end{center}

-----

## Contenedores de Aplicación en Linux: Tres Paradigmas

Tres enfoques modernos para la distribución de software en el escritorio Linux:

  * **1. AppImage:**
      * **Archivo único y autónomo (*self-contained*):** "Una aplicación = un archivo".
      * Ejecución directa por el usuario sin instalación ni privilegios de `root`.
  * **2. Snap:**
      * **Paquete universal con sandbox:** Gestionado por un daemon del sistema (`snapd`).
      * Desarrollado por Canonical, profundamente integrado en Ubuntu y utilizado en IoT/servidores.
  * **3. Flatpak:**
      * **Estándar abierto enfocado en el escritorio:** Basado en *Runtimes* compartidos y sandbox estricta.
      * Respaldado por Red Hat, GNOME y KDE; distribuido mediante **Flathub**.

-----

## Arquitecturas Comparadas: Servicios vs. Escritorio

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{desktop_containers_architecture.png}
\end{center}

-----

## Análisis Comparativo: AppImage vs. Snap vs. Flatpak

| Vector de Comparación | AppImage | Snap | Flatpak |
| :--- | :--- | :--- | :--- |
| **Instalación en el Sistema** | **No requiere (ejecución directa)** | Sí (requiere privilegios `sudo` e daemon) | Opcional (instalación por usuario sin `sudo`) |
| **Empaquetamiento de Dependencias** | **100% autónomo (todo en un archivo)** | Dependencias locales + *core snap* base | *Runtimes* compartidos entre aplicaciones |
| **Ocupación en Disco** | Elevada (duplicación total) | Media/Elevada (dependencias por snap) | **Optimizada (amortizada vía *runtimes*)** |
| **Latencia de Arranque** | **Rápida** | Más lenta | **Rápida / casi nativa** |
| **Aislamiento de Seguridad** | Ninguno por defecto | **AppArmor** | **Bubblewrap** |
| **Acceso a Recursos (Red/Archivos)** | Directo y total (hereda del usuario) | Interfaces declarativas (*plugs* / *slots*) | **Declarativo en el manifiesto (permisos)** |
| **Integración en el Escritorio** | Manual (sin accesos directos automáticos) | **Automática (menús e iconos del sistema)** | **Automática (menús e iconos del sistema)** |
| **Modelo de Distribución** | **Descentralizado (descarga directa)** | Centralizado por Canonical (Snap Store) | **Descentralizado y comunitario (Flathub)** |
| **Comunidad & Apoyo** | Comunidad independiente abierta | **Canonical (Ubuntu)** | **Red Hat, GNOME, KDE y comunidad** |
| **Principal Caso de Uso** | **Portabilidad rápida ("memoria USB")** | **Escritorio Ubuntu, servidores e IoT** | **Aplicaciones desktop gráficas y multimedia** |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Empaquetamiento con AppImage y Flatpak}}
\end{center}

-----

## AppImage: La Estructura AppDir

El formato AppImage se basa en un directorio estructurado denominado **`AppDir`**, comprimido en un ejecutable SquashFS:

```text
MeuJogo.AppDir/
├── AppRun               # Punto de entrada ejecutable (Script obligatorio)
├── meujogo.desktop      # Metadados de integración en el menú de escritorio
├── meujogo.png          # Icono de la aplicación
└── usr/                 # Jerarquía estándar Unix
    ├── bin/             # Binarios compilados
    └── lib/             # Bibliotecas dinámicas (.so) y paquetes Python
```

  * **`AppRun` (Obligatorio):** Script ejecutado al arrancar; configura variables de entorno (`PATH`, `PYTHONPATH`) e inicia el programa principal.

-----

## AppImage: Integración con el Escritorio (.desktop)

El archivo `.desktop` integra la aplicación en el menú del sistema:

  * **Contenido típico de `meujogo.desktop`:**
    ```ini
    [Desktop Entry]
    Name=Meu Jogo
    Exec=AppRun
    Icon=meujogo
    Type=Application
    Categories=Game;
    ```
  * **Asociación de Recursos:**
      * `Exec=AppRun`: Invoca el punto de entrada desde la raíz de la imagen.
      * `Icon=meujogo`: Vincula con el archivo `meujogo.png` en la raíz del `AppDir`.

-----

## AppImage: Ejemplo "Hello World"

Creación de la estructura `AppDir` mínima para un script:

```bash
# 1. Crear el directorio de trabajo
mkdir -p HelloWorld.AppDir && cd HelloWorld.AppDir

# 2. Crear el script de arranque ejecutable AppRun
echo '#!/bin/bash' > AppRun
echo 'echo "Hello from an AppImage!"' >> AppRun
chmod +x AppRun

# 3. Crear los metadados de escritorio e icono
echo '[Desktop Entry]' > hello.desktop
echo 'Name=Hello' >> hello.desktop
echo 'Exec=AppRun' >> hello.desktop
echo 'Icon=hello' >> hello.desktop
echo 'Type=Application' >> hello.desktop
touch hello.png
```

-----

## AppImage: Empaquetar con appimagetool

Transformar la carpeta `AppDir` en un único archivo ejecutable y portátil:

```bash
# Regresar al directorio padre
cd ..

# Descargar la herramienta appimagetool (si no está presente en el sistema)
wget https://github.com/AppImage/AppImageKit/releases/\
download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Generar el archivo .AppImage final
ARCH=x86_64 ./appimagetool-x86_64.AppImage HelloWorld.AppDir

# Probar la ejecución del binario autónomo generado
./Hello-x86_64.AppImage
```

-----

## Flatpak: El Manifiesto Declarativo (.yml)

Las aplicaciones Flatpak se construyen a partir de un archivo de manifiesto declarativo (en YAML o JSON):

  * **`app-id`:** Identificador único global en formato DNS inverso (ej.: `pt.ua.deti.iei.HelloWorld`).
  * **`runtime` / `sdk`:** Plataforma base y herramientas de compilación provistas por el repositorio (ej.: `org.freedesktop.Platform`).
  * **`command`:** Binario o script invocado al iniciar la sandbox.
  * **`modules`:** Lista declarativa de componentes a descargar y compilar (fuentes git, paquetes PyPI, scripts locales).

-----

## Flatpak: Ejemplo de Manifiesto (com.example.HelloWorld.yml)

Ejemplo de manifiesto para un script simple:

```yaml
app-id: com.example.HelloWorld
runtime: org.freedesktop.Platform
runtime-version: '25.08'
sdk: org.freedesktop.Sdk
command: hello.sh
modules:
  - name: hello-module
    buildsystem: simple
    build-commands:
      # Instala el script en el directorio de binarios de la sandbox
      - install -Dm755 hello.sh /app/bin/hello.sh
    sources:
      - type: file
        path: hello.sh
```

-----

## Flatpak en el Laboratorio: Juego de las Tres en Raya (Pygame)

En la guía práctica, este patrón se aplica a una aplicación interactiva con interfaz gráfica y audio:

  * **Requisitos Gráficos y Aceleración por Hardware:**
      * Declaración de accesos a periféricos en `finish-args`:
        ```yaml
        finish-args:
          - --share=ipc
          - --socket=x11
          - --socket=wayland
          - --device=dri        # Aceleración gráfica GPU
          - --env=PYTHONPATH=/app/lib/game
        ```
  * **Gestión de Dependencias Python mediante Módulos:**
      * El manifiesto integra el módulo `pygame` descargado de PyPI e instala el código del juego en `/app/lib/game`.
  * **Integración en el Escritorio:**
      * Archivo `.desktop` e icono instalados en las rutas estándar XDG de la sandbox (`/app/share/applications/` y `/app/share/icons/`).

-----

## Flatpak: La Herramienta flatpak-builder

El comando `flatpak-builder` procesa el manifiesto y compila la aplicación en un entorno aislado:

```bash
# 1. Compilar e instalar localmente para el usuario actual
flatpak-builder --user --install --force-clean \
  build-dir com.example.HelloWorld.yml
```

  * **`--user`:** Instala en el perfil del usuario (`~/.local/share/flatpak`), sin necesidad de `sudo`.
  * **`--install`:** Registra la aplicación en el sistema tras una compilación exitosa.
  * **`--force-clean`:** Limpia la carpeta temporal de compilación `build-dir`.

```bash
# 2. Ejecutar la aplicación dentro de la sandbox de Flatpak
flatpak run com.example.HelloWorld
```


-----

## Síntesis y Puntos Clave de la Sesión

  * **Infraestructura vs. Escritorio:** Docker gestiona servicios de backend (*headless*); AppImage, Snap y Flatpak distribuyen aplicaciones interactivas y gráficas en el cliente.
  * **Resolución del *Dependency Hell*:** El empaquetamiento autónomo elimina conflictos de bibliotecas compartidas (`.so`), garantizando una ejecución determinista.
  * **AppImage:** Archivo único y portátil enfocado en la simplicidad, sin sandbox por defecto.
  * **Snap:** Confinamiento obligatorio (AppArmor) y distribución centralizada estrechamente ligada al ecosistema Ubuntu.
  * **Flatpak:** Estándar abierto para aplicaciones desktop, combinando *Runtimes* compartidos con sandbox robusta (*Bubblewrap*).

-----

## Referencias Técnicas Autorizadas

Documentación oficial y especificaciones para profundizar en sistemas desktop y sandboxing:

  * **Flatpak Documentation:**
      * [Manual de Desarrollador y Arquitectura Flatpak](https://docs.flatpak.org/)
      * [Referencia de la Utilidad flatpak-builder](https://docs.flatpak.org/en/latest/flatpak-builder.html)
  * **AppImage Documentation:**
      * [Guía Oficial de Empaquetamiento AppImage](https://docs.appimage.org/)
      * [Especificación del Formato de Archivo AppImage](https://github.com/AppImage/AppImageSpec)
  * **Canonical Snapcraft:**
      * [Documentación de Arquitectura e Interfaces Snap](https://snapcraft.io/docs)
  * **Especificaciones FreeDesktop.org:**
      * [Especificación Desktop Entry (`.desktop`)](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
      * [Especificación XDG Desktop Portals](https://flatpak.github.io/xdg-desktop-portal/)
