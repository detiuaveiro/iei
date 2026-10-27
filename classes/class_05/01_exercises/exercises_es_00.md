---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Contenedores de Aplicación & Desktop Sandboxing en Linux (Flatpak & AppImage)"
institute: Universidade de Aveiro
date: October 26, 2026
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
Mientras que en la clase anterior exploramos Docker para empaquetar y orquestar servicios de red y servidores en segundo plano (*headless*), en este laboratorio el foco se desplaza hacia el empaquetamiento y distribución de **aplicaciones desktop en Linux**.  

En esta guía de **3 horas**, aprenderá a empaquetar desde scripts simples de línea de comandos hasta una **aplicación gráfica interactiva con ventana y sonido (el Juego de las Tres en Raya / Tic-Tac-Toe en Pygame)**. Explorará cómo **Flatpak** (con su sandbox basada en *bubblewrap*, sockets X11/Wayland y aceleración GPU) y **AppImage** (con la estructura autónoma `AppDir`) permiten entregar aplicaciones portátiles listas para usar, que se integran directamente en los menús del sistema operativo sin requerir privilegios de administración (`sudo`).

\vspace{0.5em}

### Preparación del Directorio de Trabajo

Antes de iniciar los ejercicios, cree y acceda a la carpeta de trabajo dedicada para esta sesión:

```bash
$ mkdir -p ~/IEI/clase05
$ cd ~/IEI/clase05
```

Todos los archivos creados durante la clase (archivos de manifiesto YAML, scripts `AppRun`, aplicaciones Python y metadatos de escritorio) deberán organizarse en subcarpetas dentro de este directorio de trabajo.

> **Nota sobre rutas de archivos:**
> Los comandos de esta guía asumen que la terminal está situada en el directorio de trabajo `~/IEI/clase05`. Cada ejercicio debe desarrollarse en su subcarpeta correspondiente (ej.: `ex1-flatpak`, `ex1-appimage`, `ex2-pytree`, `ex3-flatpak`, etc.).

-----

## 0. Setup: Configurar el Entorno de Desarrollo

> **Nota para usuarios de macOS y Windows:**  
> Flatpak y AppImage son tecnologías exclusivas del ecosistema Linux (requieren el kernel Linux, *namespaces*, *cgroups* y *libfuse2*). Si su ordenador personal ejecuta macOS o Windows, realice todos los ejercicios de esta guía **dentro de su máquina virtual Ubuntu (creada en la Clase 00 mediante UTM o VirtualBox)** o en los puestos de trabajo de los laboratorios del DETI.

Primero, debemos instalar todas las herramientas necesarias para compilar y probar nuestros paquetes de aplicación.

1.  **Actualizar el sistema:** Este comando descarga la lista más reciente de software disponible y actualiza todos los paquetes actualmente instalados a sus versiones más recientes.

<!-- end list -->

```bash
$ sudo apt update && sudo apt full-upgrade -y
```

2.  **Instalar herramientas:** Este comando instala todos los componentes necesarios para nuestra clase.

<!-- end list -->

  * `curl` & `wget`: Utilidades para descargar archivos de internet.
  * `unzip`: Utilidad para descomprimir archivos ZIP.
  * `file`: Utilidad para identificar tipos de archivos.
  * `libfuse2`: Biblioteca necesaria para que AppImage pueda "montar" (mount) el paquete de la aplicación como un sistema de archivos virtual (virtual filesystem).
  * `flatpak`: Herramienta de línea de comandos para ejecutar y gestionar aplicaciones Flatpak.
  * `flatpak-builder`: Herramienta específica utilizada para construir paquetes Flatpak a partir de un archivo de manifiesto (`manifest`).
  * `python3`, `python3-pip`, `python3-venv`, `python3-dev`: El intérprete Python, su gestor de paquetes (`pip`), la herramienta de **entornos virtuales** (`venv`) y las cabeceras de desarrollo (`dev`) necesarias para compilar módulos C.

<!-- end list -->

```bash
$ sudo apt install curl wget unzip file libfuse2 flatpak \
flatpak-builder python3 python3-pip python3-venv python3-dev
```

3.  **Añadir Flathub:** Este comando añade el repositorio **Flathub** a la configuración de Flatpak de su sistema, pero únicamente para su usuario local (`--user`). Un "repositorio" (o "remote") es un servidor que aloja aplicaciones y `runtimes` de Flatpak. Flathub es el repositorio más grande y común, y lo necesitamos para descargar los SDKs (Software Development Kits) necesarios para la compilación.

<!-- end list -->

```bash
$ flatpak --user remote-add --if-not-exists \
flathub https://flathub.org/repo/flathub.flatpakrepo
```

4.  **Instalar `appimagetool`:** Esto descarga el programa `appimagetool`, encargado de comprimir un directorio `AppDir` en un único archivo ejecutable AppImage. Le otorgamos permisos de ejecución (`chmod +x`) y lo movemos a `~/.local/bin`, un directorio estándar para programas instalados por el usuario.

<!-- end list -->

```bash
$ mkdir -p ~/.local/bin
$ wget -O appimagetool \
"https://github.com/AppImage/AppImageKit/\
releases/download/continuous/appimagetool-x86_64.AppImage"
$ chmod +x appimagetool
$ mv appimagetool ~/.local/bin/
```

5.  **Aplicar el cambio al PATH:** El `PATH` es una variable de entorno que indica a su `shell` (como `bash`) en qué directorios buscar programas ejecutables. Por defecto, `~/.local/bin` no siempre está en el `PATH`. Editamos `~/.bashrc` (un archivo que se ejecuta cada vez que abre una nueva terminal) para añadir este directorio al `PATH`. Esto hace que `appimagetool` sea ejecutable desde cualquier ubicación.

    Puede usar `nano` para editar el archivo: `nano ~/.bashrc`.
    Añada la siguiente configuración a la *última* línea del archivo:

<!-- end list -->

```bash
export PATH=${HOME}/.local/bin${PATH:+:${PATH}}
```

6.  **Cierre la sesión e inicie nuevamente (Log out y log back in).** Esto recarga su archivo `~/.bashrc` y aplica la modificación al `PATH`. Para verificar que funciona correctamente, abra una nueva terminal e introduzca el siguiente comando. Debería visualizar la información de versión de la herramienta.

<!-- end list -->

```bash
$ appimagetool --version
```

-----

## 1. "Hello World" 🌍

Vamos a empaquetar un script de shell sencillo.

### 1.A: Flatpak "Hello World"

Flatpak utiliza un archivo de manifiesto (en formato YAML) para definir todo lo relativo a la aplicación y cómo compilarla.

1.  Cree un directorio para este ejercicio:

<!-- end list -->

```bash
$ mkdir ex1-flatpak && cd ex1-flatpak
```

2.  Cree el script de la aplicación, llamado `hello.sh`.
    Puede crearlo con cualquier editor; una posibilidad es usar `nano`: `nano hello.sh`

<!-- end list -->

```bash
#!/bin/sh
echo "Hello from a Flatpak Sandbox!"
```

3.  Cree el archivo de manifiesto, `pt.ua.deti.iei.HelloWorld.yml`. Este archivo define:

    * `app-id`: Un identificador único, en formato DNS inverso, para su aplicación.
    * `runtime` / `sdk`: El sistema base sobre el cual su aplicación se ejecutará y compilará.
    * `command`: El programa a ejecutar cuando arranque la aplicación.
    * `modules`: La lista de pasos de compilación. Aquí, definimos un módulo que instala nuestro script `hello.sh` en la ruta ejecutable de la sandbox (`/app/bin/`).

<!-- end list -->

```yaml
app-id: pt.ua.deti.iei.HelloWorld
runtime: org.freedesktop.Platform
runtime-version: '25.08'
sdk: org.freedesktop.Sdk
command: hello.sh

modules:
  - name: hello-module
    buildsystem: simple
    build-commands:
      # Instala el script en la carpeta /app/bin/ de la sandbox
      - install -Dm755 hello.sh /app/bin/hello.sh
    sources:
      # Indica al builder que busque 'hello.sh' en el directorio del proyecto
      - type: file
        path: hello.sh
```

4.  **Compilar el paquete:** Este comando ejecuta `flatpak-builder` con varias opciones importantes:

      * `--user`: Compila e instala la aplicación únicamente para su usuario, sin requerir `sudo`.
      * `--install`: Instala automáticamente la aplicación tras una compilación exitosa.
      * `--install-deps-from=flathub`: Encuentra e instala automáticamente cualquier SDK o runtime faltante desde Flathub.
      * `--force-clean`: Borra `build-dir` para garantizar una compilación limpia.
      * `build-dir`: El nombre del directorio temporal a utilizar para la compilación.

<!-- end list -->

```bash
$ flatpak-builder --user --install --install-deps-from=flathub \
--force-clean build-dir pt.ua.deti.iei.HelloWorld.yml
```

5.  **Ejecutar y Limpiar:** `flatpak run` ejecuta su aplicación dentro de su sandbox. Tras terminar, use `cd ..` para salir del directorio.

<!-- end list -->

```bash
$ flatpak run pt.ua.deti.iei.HelloWorld
$ flatpak uninstall --user pt.ua.deti.iei.HelloWorld
```

-----

### 1.B: AppImage "Hello World"

AppImage funciona empaquetando un directorio completo estructurado (denominado `AppDir`).

1.  Cree un directorio para este ejercicio:

```bash
$ mkdir ex1-appimage && cd ex1-appimage
```

2.  Cree el `AppDir` y el script principal `AppRun`. El archivo **`AppRun`** es un script especial que actúa como punto de entrada (entrypoint). Es lo *primero* que se ejecuta cuando se abre el AppImage. También creamos un archivo `icon.png` vacío (dummy).

<!-- end list -->

```bash
$ mkdir -p HelloWorld.AppDir
$ echo '#!/bin/sh' > HelloWorld.AppDir/AppRun
$ echo 'echo "Hello from an AppImage!"' >> HelloWorld.AppDir/AppRun
$ chmod +x HelloWorld.AppDir/AppRun
$ touch HelloWorld.AppDir/icon.png
```

3.  Cree un archivo llamado `HelloWorld.AppDir/hello.desktop`. Este es un **archivo `.desktop`**, la especificación estándar para integrar la aplicación en el escritorio Linux (menús de aplicaciones, iconos y accesos directos del sistema). Define el `Name` (Nombre) de la aplicación, el comando a `Exec` (Ejecutar) (nuestro script `AppRun`) y el `Icon` (Icono) a utilizar. La herramienta `appimagetool` *requiere* este archivo obligatoriamente.

<!-- end list -->

```bash
[Desktop Entry]
Name=Hello
Exec=AppRun
Icon=icon
Type=Application
Categories=Utility;
```

4.  **Compilar el paquete:** Ejecutamos `appimagetool` sobre nuestro `AppDir`. Debemos especificar además `ARCH=x86_64` porque la herramienta no puede inferir la arquitectura a partir de un script de shell simple; lo necesita para nombrar el archivo final correctamente. Si utiliza otra arquitectura (como ARM), cambie la variable `ARCH` a `arm64`. Esto generará el archivo `Hello-x86_64.AppImage` o `Hello-arm64.AppImage`.

<!-- end list -->

```bash
$ ARCH=x86_64 appimagetool HelloWorld.AppDir
```

5.  **Ejecutar y Limpiar:** Tras terminar, use `cd ..` para salir del directorio.

```bash
$ chmod +x Hello-x86_64.AppImage
$ ./Hello-x86_64.AppImage

# Limpieza
$ rm -rf Hello-x86_64.AppImage
```

-----

## 2. Aplicación CLI Python: Árbol ASCII 🌳

Vamos a empaquetar una aplicación CLI (Command-Line Interface) sencilla en Python.
Crearemos un script `pytree.py` que lista recursivamente directorios en formato de árbol.

### 2.A: Ejecutar con Entorno Virtual (venv)

Primero, ejecutaremos la aplicación de forma nativa para confirmar su funcionamiento. Usaremos un **entorno virtual de Python** para gestionar dependencias, aunque este script básico no requiera ninguna externa.

Un entorno virtual (`venv`) es una "burbuja" aislada para un proyecto Python. Mantiene su *propio* intérprete Python y paquetes instalados, de modo que los paquetes de este proyecto no entren en conflicto con los de otro.

1.  Cree un directorio de proyecto:

<!-- end list -->

```bash
$ mkdir ex2-pytree && cd ex2-pytree
```

2.  Cree el script `pytree.py` y otórguele permisos de ejecución: `chmod +x pytree.py`.

<!-- end list -->

```python
#!/usr/bin/env python3
import os
import sys

def tree(startpath):
    """Prints a directory tree."""
    for root, dirs, files in os.walk(startpath):
        # Don't visit .venv or __pycache__
        if '.venv' in dirs:
            dirs.remove('.venv')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')

        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        
        print(f'{indent} {os.path.basename(root)}/')
        
        subindent = '│   ' * level + '├── '
        for f in files:
            print(f'{subindent} {f}')

if __name__ == "__main__":
    # Use current directory or a specified path
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    tree(os.path.abspath(path))
```

3.  **Ejecutar la aplicación:** Como esta aplicación no tiene dependencias externas, podemos ejecutarla directamente. Tras terminar, use `cd ..` para salir del directorio.

<!-- end list -->

```bash
$ ./pytree.py
# Probar en otro directorio
$ ./pytree.py /tmp
```

-----

### 2.B: Empaquetar pytree como un Flatpak

1.  Cree un directorio de proyecto:

<!-- end list -->

```bash
$ mkdir ex2-flatpak && cd ex2-flatpak
```

2.  Copie el archivo `pytree.py` del ejercicio anterior:

<!-- end list -->

```bash
$ cp ../ex2-pytree/pytree.py .
```

3.  Cree el manifiesto `pt.ua.deti.iei.pytree.yml`. Utilizamos `org.gnome.Platform` como nuestro `runtime` porque incluye convenientemente un intérprete Python 3, evitando tener que compilar Python manualmente.

<!-- end list -->

```yaml
app-id: pt.ua.deti.iei.pytree
runtime: org.gnome.Platform
runtime-version: '50'
sdk: org.gnome.Sdk
command: pytree.py

modules:
  - name: pytree
    buildsystem: simple
    build-commands:
    - install -Dm755 pytree.py /app/bin/pytree.py
    sources:
    - type: file
      path: pytree.py
```

4.  **Compilar e Instalar:**

<!-- end list -->

```bash
$ flatpak-builder --user --install --install-deps-from=flathub \
--force-clean build-dir pt.ua.deti.iei.pytree.yml
```

5.  **Ejecutar y Limpiar:** Al ejecutarlo por primera vez, únicamente listará los archivos *dentro de su propia sandbox*. Para hacerlo útil, debemos concederle permisos para acceder a los archivos del sistema anfitrión (host). `--filesystem=home` abre un canal en la sandbox, permitiendo a la aplicación acceder a nuestro directorio home. Tras terminar, use `cd ..` para salir del directorio.

<!-- end list -->

```bash
$ flatpak run pt.ua.deti.iei.pytree

# Se ejecuta dentro de una sandbox, ¡por lo que solo se ve a sí mismo!
# Concedemos acceso a nuestro directorio home para probarlo:
$ flatpak run --filesystem=home pt.ua.deti.iei.pytree ~/

$ flatpak uninstall pt.ua.deti.iei.pytree
```

-----

### 2.C: Empaquetar pytree como un AppImage

1.  Cree un directorio de proyecto:

    ```bash
    $ mkdir ex2-appimage && cd ex2-appimage
    ```

2.  Cree el `AppDir`:

    ```bash
    $ mkdir -p Pytree.AppDir && cd Pytree.AppDir
    ```

3.  **Descargar y extraer Python portable:** Usamos `wget` para descargar una compilación precompilada y portable de Python. Dado que un AppImage es un sistema de archivos comprimido, usamos `--appimage-extract` para desempaquetarlo. Luego movemos su contenido (`mv squashfs-root/* .`) a la raíz de nuestro `AppDir`.

<!-- end list -->

```bash
# Para PC Intel/AMD (x86_64):
$ wget "https://github.com/niess/python-appimage/releases/\
download/python3.15/python3.15.1-cp315-cp315-manylinux_2_28_x86_64.AppImage" \
-O python.AppImage

# O para Apple Silicon Mac / ARM64 (aarch64) en máquina virtual:
# $ wget "https://github.com/niess/python-appimage/releases/\
# download/python3.15/python3.15.1-cp315-cp315-manylinux2014_aarch64.AppImage" \
# -O python.AppImage

$ chmod +x python.AppImage
$ ./python.AppImage --appimage-extract
$ mv squashfs-root/* .
$ rm -rf python* squashfs-root/
```

4.  **Copiar su script:** Copiamos nuestro script al directorio `usr/bin` provisto por el Python portable que acabamos de extraer.

<!-- end list -->

```bash
$ cp ../../ex2-pytree/pytree.py usr/bin/
```

5.  **Actualizar el punto de entrada `AppRun`:** El paquete de Python portable incluye su propio script `AppRun`. Solo necesitamos editar su *última línea* para invocar nuestro script `pytree.py` en lugar de abrir una shell interactiva de Python. Finalmente, asegúrese de que tiene permisos de ejecución: `chmod +x AppRun`.

<!-- end list -->

```bash
#! /bin/bash
# Si se ejecuta desde una imagen extraída, exporta ARGV0 y APPDIR
if [ -z "${APPIMAGE}" ]; then
    export ARGV0="$0"

    self=$(readlink -f -- "$0")
    here="${self%/*}"
    tmp="${here%/*}"
    export APPDIR="${tmp%/*}"
fi

# Resolver el comando invocado preservando enlaces simbólicos
export APPIMAGE_COMMAND=$(command -v -- "$ARGV0")

# Exportar Tcl/Tk
export TCL_LIBRARY="${APPDIR}/usr/share/tcltk/tcl8.6"
export TK_LIBRARY="${APPDIR}/usr/share/tcltk/tk8.6"
export TKPATH="${TK_LIBRARY}"

# Exportar certificados SSL
export SSL_CERT_FILE="${APPDIR}/opt/_internal/certs.pem"

# Invocar Python
"$APPDIR/opt/python3.15/bin/python3.15" "$APPDIR/usr/bin/pytree.py" "$@"
```

6.  Cree un archivo llamado `pytree.desktop` y complételo.
    También creamos un archivo `icon.png` vacío para satisfacer los requisitos de `appimagetool`.

<!-- end list -->

```bash
[Desktop Entry]
Name=PyTree
Exec=AppRun
Icon=icon
Type=Application
Categories=Utility;
```

```bash
$ touch icon.png
```

7.  **Compilar, Ejecutar y Limpiar:** Tras terminar, use `cd ..` para salir del directorio.

<!-- end list -->

```bash
$ cd ..  # Volver al directorio ex2-appimage
$ ARCH=x86_64 appimagetool Pytree.AppDir  # Si utiliza ARM64, use ARCH=arm64

$ chmod +x PyTree-*.AppImage
$ ./PyTree-*.AppImage

# Probar en su directorio home
$ ./PyTree-*.AppImage ~/

$ rm -rf PyTree-*.AppImage
```

-----

## 3. Aplicación GUI Python: Juego de las Tres en Raya 🎮

### 3.A: Ejecutar con Entorno Virtual (venv)

Este paso simula el flujo de un usuario final tradicional: descargar el código fuente, extraerlo y ejecutarlo localmente.

1.  Cree un directorio y descargue el código fuente: Descargamos el código fuente del juego desde el repositorio público en formato ZIP, lo extraemos con `unzip` y movemos los archivos a la carpeta de trabajo.

<!-- end list -->

```bash
$ mkdir ex3-tictactoe && cd ex3-tictactoe

# Asegurar que unzip está instalado
$ sudo apt update && sudo apt install unzip

# Descargar el archivo con el juego desde el repositorio público
$ wget "https://github.com/mariolpantunes/tictactoe/archive/refs/heads/main.zip" \
-O tictactoe.zip

# Descomprimir el archivo ZIP
$ unzip tictactoe.zip

# Mover los archivos a la carpeta de trabajo
$ mv tictactoe-main/* .
$ rm -rf tictactoe-main
```

2.  **Crear y activar el `venv`:** En este caso, crear un entorno virtual es fundamental porque existen dependencias externas. Verá el prefijo `(venv)` en el prompt de su terminal, indicando que su shell utiliza el Python y `pip` aislados en `./venv`. Actualizamos también las herramientas de empaquetado (`pip`, `setuptools`, `wheel`).

<!-- end list -->

```bash
$ python3 -m venv ./venv
$ source venv/bin/activate
$ pip install --upgrade pip setuptools wheel
```

3.  **Instalar dependencias desde el archivo:** El archivo `requirements.txt` enumera todos los paquetes Python requeridos por el proyecto. `pip install -r` lee dicho archivo y los instala (en este caso `pygame`) dentro del entorno virtual *activo*.

<!-- end list -->

```bash
$ pip install -r requirements.txt
```

> **Resolución de problemas (compilación de Pygame):**  
> Si la instalación de `pygame` falla por falta de bibliotecas de desarrollo C/SDL (situación común cuando `pip` compila desde el código fuente en determinadas distribuciones o arquitecturas ARM64/Apple Silicon), instale los paquetes de desarrollo en el sistema antes de repetir el comando `pip install`:
> ```bash
> $ sudo apt install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \
>   libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev libpng-dev
> ```

4.  **Ejecutar el juego:**

<!-- end list -->

```bash
$ python main.py
```

5.  **Desactivar el venv:** Este comando restaura su shell al Python predeterminado del sistema. Tras terminar, use `cd ..` para salir del directorio.

<!-- end list -->

```bash
$ deactivate
```

-----

### 3.B: Empaquetar el Juego de las Tres en Raya como un Flatpak

1.  Cree un nuevo directorio para esta compilación:

<!-- end list -->

```bash
$ mkdir ex3-flatpak && cd ex3-flatpak
```

2.  **Cree el manifiesto `pt.ua.deti.iei.tictactoe.yml`:** Este manifiesto integra componentes avanzados:

      * `finish-args`: Configura `PYTHONPATH` para que el intérprete dentro de la sandbox localice el módulo `minMaxAgent.py`, instalado en `/app/lib/game`. Declara además sockets gráficos (X11, Wayland) y aceleración de hardware (`--device=dri`).
      * Módulo `python-deps`: Especifica manualmente la URL y la suma de verificación (`sha256`) de los fuentes de `pygame`. `flatpak-builder` descarga y compila esta biblioteca desde cero.
      * Módulo `game`: Descarga el código del juego. Las instrucciones de `build-commands` instalan los scripts Python, la carpeta `assets` y los archivos de integración `.desktop` e icono en las rutas del sistema XDG.

<!-- end list -->

```yaml
app-id: pt.ua.deti.iei.tictactoe
runtime: org.gnome.Platform
runtime-version: '50'
sdk: org.gnome.Sdk
command: game
finish-args:
  - --share=ipc
  - --socket=x11
  - --socket=wayland
  - --device=dri
  - --env=PYTHONPATH=/app/lib/game
modules:
  - name: python-deps
    buildsystem: simple
    build-options:
      env:
        MAKEFLAGS: -j$(nproc)
    build-commands:
      - pip3 install --isolated --no-index
        --find-links="file://${PWD}" --prefix=/app pygame
    sources:
      - type: file
        url: https://pypi.io/packages/source/p/pygame/pygame-2.6.1.tar.gz
        sha256: 56fb02ead529cee00d415c3e007f75e0780c655909aaa8e8bf616ee09c9feb1f
  - name: game
    buildsystem: simple
    build-commands:
      - install -d /app/lib/game/
      - install -Dm644 minMaxAgent.py /app/lib/game/minMaxAgent.py
      - install -d /app/share/game/
      - cp -r assets /app/share/game/
      - install -Dm755 main.py /app/bin/game
      - install -Dm644 pt.ua.deti.iei.tictactoe.desktop
        /app/share/applications/pt.ua.deti.iei.tictactoe.desktop
      - install -Dm644 assets/icon.png
        /app/share/icons/hicolor/128x128/apps/pt.ua.deti.iei.tictactoe.png
    sources:
      - type: archive
        url: https://github.com/mariolpantunes/tictactoe/archive/refs/heads/main.zip
        sha256: 038b54a775c2934cfa17ecced82c5db33a5d9ff15243cd5682ae2a3d07866ba2
```

3.  **Compilar e Instalar:** ¡Tras la instalación, el juego aparecerá directamente en el menú de aplicaciones de su entorno de escritorio!

<!-- end list -->

```bash
$ flatpak-builder --user --install --install-deps-from=flathub \
--force-clean build-dir pt.ua.deti.iei.tictactoe.yml
```

4.  **Ejecutar y Limpiar:** Tras terminar, use `cd ..` para salir del directorio.

<!-- end list -->

```bash
$ flatpak run pt.ua.deti.iei.tictactoe
$ flatpak uninstall pt.ua.deti.iei.tictactoe
```

-----

### 3.C: Empaquetar el Juego de las Tres en Raya como un AppImage

1.  Cree un directorio de compilación:

<!-- end list -->

```bash
$ mkdir ex3-appimage && cd ex3-appimage
```

2.  **Descargar el código fuente del juego:**

<!-- end list -->

```bash
$ wget "https://github.com/mariolpantunes/tictactoe/archive/refs/heads/main.zip" \
-O tictactoe.zip
```

3.  Cree el `AppDir`:

<!-- end list -->

```bash
$ mkdir -p TTT.AppDir && cd TTT.AppDir
```

4.  **Descargar y extraer Python portable:** Idéntico al procedimiento del Ejercicio 2.C.

<!-- end list -->

```bash
# Para PC Intel/AMD (x86_64):
$ wget "https://github.com/niess/python-appimage/releases/\
download/python3.15/python3.15.1-cp315-cp315-manylinux_2_28_x86_64.AppImage" \
-O python.AppImage

# O para Apple Silicon Mac / ARM64 (aarch64) en máquina virtual:
# $ wget "https://github.com/niess/python-appimage/releases/\
# download/python3.15/python3.15.1-cp315-cp315-manylinux2014_aarch64.AppImage" \
# -O python.AppImage

$ chmod +x python.AppImage
$ ./python.AppImage --appimage-extract
$ mv squashfs-root/* .
$ rm -rf python* squashfs-root/
```

5.  **Extraer el código fuente del juego:**

<!-- end list -->

```bash
$ unzip ../tictactoe.zip
$ mv tictactoe-main/* .
$ rm -rf tictactoe-main
```

6.  **Instalar dependencias desde `requirements.txt`:** Utilizamos el gestor `pip` del Python integrado (*bundled*). El parámetro `--target` instruye a `pip` para instalar `pygame` *dentro* de la carpeta `site-packages` de nuestro `AppDir`, sin contaminar el sistema anfitrión.

<!-- end list -->

```bash
$ ./usr/bin/python3.15 -m pip install -r ./requirements.txt \
--target ./usr/lib/python3.15/site-packages/
```

7.  **Copiar los archivos del juego:** Movemos los scripts y recursos (`assets`) del juego a `usr/bin/`.

<!-- end list -->

```bash
$ mv main.py minMaxAgent.py assets usr/bin/
```

8.  **Actualizar el punto de entrada `AppRun`:** Se actualiza el script `AppRun` para definir la variable `PYTHONPATH`, indicando al intérprete que busque módulos en dos ubicaciones clave: `site-packages` (para `pygame`) y `usr/bin` (para `minMaxAgent.py`). Finalmente, otórguele permisos de ejecución: `chmod +x AppRun`.

<!-- end list -->

```bash
#! /bin/bash
# Si se ejecuta desde una imagen extraída, exporta ARGV0 y APPDIR
if [ -z "${APPIMAGE}" ]; then
    export ARGV0="$0"

    self=$(readlink -f -- "$0")
    here="${self%/*}"
    tmp="${here%/*}"
    export APPDIR="${tmp%/*}"
fi

# Resolver el comando invocado preservando enlaces simbólicos
export APPIMAGE_COMMAND=$(command -v -- "$ARGV0")

# Exportar Tcl/Tk
export TCL_LIBRARY="${APPDIR}/usr/share/tcltk/tcl8.6"
export TK_LIBRARY="${APPDIR}/usr/share/tcltk/tk8.6"
export TKPATH="${TK_LIBRARY}"

# Exportar certificados SSL
export SSL_CERT_FILE="${APPDIR}/opt/_internal/certs.pem"

# Exportar PYTHONPATH para Pygame y módulos locales
export PYTHONPATH="$APPDIR/usr/lib/python3.15/site-packages:$APPDIR/usr/bin"

# Invocar Python
"$APPDIR/opt/python3.15/bin/python3.15" "$APPDIR/usr/bin/main.py" "$@"
```

9.  **Añadir metadados:** Movemos el archivo `.desktop` y copiamos el icono a la raíz del `AppDir` para que `appimagetool` los localice e integre correctamente.

<!-- end list -->

```bash
$ mv pt.ua.deti.iei.tictactoe.desktop ./tictactoe.desktop
$ cp usr/bin/assets/icon.png ./pt.ua.deti.iei.tictactoe.png
```

10. **Compilar, Ejecutar y Limpiar:**

<!-- end list -->

```bash
$ cd .. # Volver al directorio ex3-appimage
$ ARCH=x86_64 appimagetool TTT.AppDir  # Si utiliza ARM64, use ARCH=arm64

$ chmod +x TicTacToe-*.AppImage
$ ./TicTacToe-*.AppImage

$ rm -rf *.AppImage tictactoe.zip
```

-----

## Conclusión

En estos ejercicios prácticos, ha empaquetado una aplicación Python de dos formas distintas: como un **AppImage** autosuficiente y portátil, y como un **Flatpak** con confinamiento en sandbox.

Aunque ambos métodos alcanzan el objetivo de portabilidad, este laboratorio destaca las ventajas significativas del ecosistema Flatpak para aplicaciones complejas:

1.  **Enfoque Declarativo:** En Flatpak, todas las dependencias, orígenes y permisos se declaran en un único manifiesto YAML reproducible. El proceso AppImage requirió ensamblar manualmente el bundle, gestionar el intérprete portable y configurar scripts de arranque.
2.  **Eficiencia de Runtimes Compartidos:** En lugar de duplicar un entorno Python completo de ~100MB por aplicación, Flatpak amortiza el espacio en disco compartiendo el `runtime` base entre múltiples programas.
3.  **Compilación y Mantenimiento Automatizados:** La herramienta `flatpak-builder` automatiza la descarga, compilación y aislamiento de permisos de forma determinista, simplificando drásticamente el ciclo de vida del software para desarrolladores y usuarios finales.
