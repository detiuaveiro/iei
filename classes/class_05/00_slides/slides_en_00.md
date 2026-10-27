---
title: 47138 - Introduction to Computer Engineering
subtitle: "Application Containers & Desktop Sandboxing in Linux"
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

## Session Overview

  * **Part I — Dependencies & Sandboxing Requirements:**
      * Docker in infrastructure vs. desktop limitations, *dependency hell*, alternative models (Windows, macOS, venv), and confinement requirements.
  * **Part II — Desktop Containerization Paradigms:**
      * Conceptual and comparative analysis of **AppImage**, **Snap**, and **Flatpak** (architecture, security, and distribution).
  * **Part III — Packaging with AppImage and Flatpak:**
      * Practical artifact construction: `AppDir` hierarchy, YAML manifests, Pygame integration, and `flatpak-builder`.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: Dependencies and Sandboxing Requirements}}
\end{center}

-----

## Docker and OCI in Infrastructure vs. Desktop Limitations

The Docker and OCI ecosystem was designed for infrastructure services:

  * **Infrastructure Containers (Docker & OCI):**
      * **Headless Services:** Optimized for background server processes (APIs, databases) without graphical interfaces.
      * **Networking & Orchestration:** Private virtual networks (*bridge*), port mapping, and cluster orchestration.
      * **Privileges:** Managed via a centralized daemon with administrative privileges (`dockerd` as `root`).

  * **Desktop Application Limitations:**
      * **Graphics & Audio:** No native support for Wayland/X11, 3D acceleration (`/dev/dri`), or PipeWire.
      * **System Integration:** No menu/dock shortcuts, native notifications, or file associations.
      * **Security & File Access:** No dynamic access delegation; bind mounts expose host folders without mediation.

-----

## Dynamic Dependency Management (*Dependency Hell*)

Desktop application distribution faces the challenge of shared dynamic dependencies:

  * **Traditional Linux Architecture:**
      * Global sharing of dynamic libraries (`.so` files in `/usr/lib`).
  * **Version Conflict Scenario:**
      * Application A requires `libXYZ v1.0` vs. Application B requires `libXYZ v2.0`.
  * **Package Manager Limitations (`apt`, `dnf`):**
      * Only a single global version of each library is allowed in system paths.
      * Installing or upgrading Application B breaks Application A (*breaking changes*).
  * **Ecosystem Fragmentation:**
      * Requires dedicated packaging and compilation per distribution (Debian, Fedora, Arch).

-----

## The Shared Dependencies Problem

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{dependency_hell.png}
\end{center}

-----

## Other Operating Systems: The Bundling Model (Windows & macOS)

Self-contained packaging strategies to avoid global shared library conflicts:

  * **Microsoft Windows (Local DLL Loading):**
      * Each application bundles dynamic libraries (`.dll`) directly within its installation folder (`Program Files`).
      * **Advantage:** Prevents global filesystem conflicts.
      * **Trade-off:** High disk space duplication; no process sandbox by default.
  * **Apple macOS (Self-Contained .app Bundles):**
      * Unified directory structure grouping the binary executable, assets, and shared libraries (`.dylib`).
      * **Advantage:** Decoupled, portable bundle model for end users.
      * **Trade-off:** Redundant storage footprint; relies on a proprietary, uniform OS platform.

-----

## Language-Level Isolation: The Case of Python (venv)

Why not solve desktop application distribution using only language virtual environments?

  * **What `venv` Solves:**
      * Creates a local directory (`.venv`) isolating Python packages and modules (`site-packages`).
      * Ensures Python package reproducibility via `requirements.txt`.
  * **Why It Falls Short for Desktop Applications:**
      * **No Confinement:** Code runs with full user account privileges (no sandbox).
      * **Host OS Dependency:** Requires a pre-installed Python interpreter and **does not bundle system C libraries** (e.g., SDL2, libGL, and audio required by Pygame).
      * **No Desktop Integration:** Does not create application menu entries, manage windowing permissions, or register MIME types.

-----

## Isolation and Confinement Requirements (*Sandboxing*)

Given the limitations of traditional models, desktop Linux requires three fundamental guarantees:

  * **Deterministic Portability (*Run Anywhere*):**
      * Identical and reproducible execution across any Linux distribution.
  * **Stability and Non-Interference:**
      * Installing, upgrading, or removing an application leaves the host system intact.
  * **Security Confinement (*Sandboxing*):**
      * No unauthorized access to personal files (`$HOME`, `~/.ssh`), credentials, or hardware peripherals (camera, microphone).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part II: Desktop Containerization Paradigms}}
\end{center}

-----

## Application Containers in Linux: Three Paradigms

Three modern approaches for software distribution on desktop Linux:

  * **1. AppImage:**
      * **Single Self-Contained File:** "One app = one file".
      * Direct execution by the user without installation or `root` privileges.
  * **2. Snap:**
      * **Universal Sandboxed Package:** Managed by a system background daemon (`snapd`).
      * Developed by Canonical, deeply integrated into Ubuntu, and used in IoT/servers.
  * **3. Flatpak:**
      * **Open Standard for Desktop:** Built on shared *Runtimes* and strict sandboxing.
      * Backed by Red Hat, GNOME, and KDE; distributed via **Flathub**.

-----

## Comparative Architectures: Services vs. Desktop

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{desktop_containers_architecture.png}
\end{center}

-----

## Comparative Analysis: AppImage vs. Snap vs. Flatpak

| Comparison Vector | AppImage | Snap | Flatpak |
| :--- | :--- | :--- | :--- |
| **System Installation** | **None required (direct file execution)** | Required (requires `sudo` and daemon) | Optional (per-user install without `sudo`) |
| **Dependency Bundling** | **100% self-contained (all in one file)** | Local dependencies + base *core snap* | Shared *Runtimes* across applications |
| **Disk Footprint** | High (total duplication) | Medium/High (per-snap dependencies) | **Optimized (amortized across *runtimes*)** |
| **Startup Latency** | **Fast** | Slower | **Fast / near-native** |
| **Security Sandboxing** | None by default | **AppArmor** | **Bubblewrap** |
| **Resource Access (Network/Files)** | Direct and unrestricted (inherits user access) | Declarative interfaces (*plugs* / *slots*) | **Declarative manifest permissions** |
| **Desktop Integration** | Manual (no automatic shortcuts) | **Automatic (system menus and icons)** | **Automatic (system menus and icons)** |
| **Distribution Model** | **Decentralized (direct download)** | Centralized by Canonical (Snap Store) | **Decentralized and community-driven (Flathub)** |
| **Community & Backing** | Independent open-source community | **Canonical (Ubuntu)** | **Red Hat, GNOME, KDE, and community** |
| **Primary Use Case** | **Quick portability ("USB drive")** | **Ubuntu desktop, servers, and IoT** | **Graphical desktop and multimedia apps** |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: Packaging with AppImage and Flatpak}}
\end{center}

-----

## AppImage: The AppDir Hierarchy

The AppImage format is structured around an **`AppDir`** directory tree, packaged into an executable SquashFS image:

```text
MeuJogo.AppDir/
├── AppRun               # Executable entrypoint (Mandatory script)
├── meujogo.desktop      # Desktop menu integration metadata
├── meujogo.png          # Application icon
└── usr/                 # Standard Unix hierarchy
    ├── bin/             # Compiled binaries
    └── lib/             # Dynamic libraries (.so) and Python packages
```

  * **`AppRun` (Mandatory):** Entrypoint script executed on launch; configures environment variables (`PATH`, `PYTHONPATH`) and runs the main application.

-----

## AppImage: Desktop Integration (.desktop)

The `.desktop` entry file integrates the application into desktop menus:

  * **Typical content of `meujogo.desktop`:**
    ```ini
    [Desktop Entry]
    Name=Meu Jogo
    Exec=AppRun
    Icon=meujogo
    Type=Application
    Categories=Game;
    ```
  * **Resource Mapping:**
      * `Exec=AppRun`: Invokes the entrypoint script at the image root.
      * `Icon=meujogo`: Links to `meujogo.png` in the `AppDir` root.

-----

## AppImage: "Hello World" Example

Creating the minimal `AppDir` structure for a shell script:

```bash
# 1. Create working directory
mkdir -p HelloWorld.AppDir && cd HelloWorld.AppDir

# 2. Create executable AppRun entrypoint script
echo '#!/bin/bash' > AppRun
echo 'echo "Hello from an AppImage!"' >> AppRun
chmod +x AppRun

# 3. Create desktop metadata and icon
echo '[Desktop Entry]' > hello.desktop
echo 'Name=Hello' >> hello.desktop
echo 'Exec=AppRun' >> hello.desktop
echo 'Icon=hello' >> hello.desktop
echo 'Type=Application' >> hello.desktop
touch hello.png
```

-----

## AppImage: Packaging with appimagetool

Transforming the `AppDir` folder into a single portable executable:

```bash
# Return to parent directory
cd ..

# Download appimagetool (if not present on system)
wget https://github.com/AppImage/AppImageKit/releases/\
download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Generate the final .AppImage file
ARCH=x86_64 ./appimagetool-x86_64.AppImage HelloWorld.AppDir

# Test the generated self-contained binary
./Hello-x86_64.AppImage
```

-----

## Flatpak: The Declarative Manifest (.yml)

Flatpak applications are built from a declarative YAML or JSON manifest:

  * **`app-id`:** Globally unique ID in reverse-DNS notation (e.g., `pt.ua.deti.iei.HelloWorld`).
  * **`runtime` / `sdk`:** Base execution platform and development SDK (e.g., `org.freedesktop.Platform`).
  * **`command`:** Binary or script executed when the sandbox starts.
  * **`modules`:** Declarative list of components to fetch and build (git sources, PyPI packages, local scripts).

-----

## Flatpak: Example Manifest (com.example.HelloWorld.yml)

Manifest example for a simple shell script:

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
      # Installs the script into the sandbox binary path
      - install -Dm755 hello.sh /app/bin/hello.sh
    sources:
      - type: file
        path: hello.sh
```

-----

## Flatpak in the Lab: Tic-Tac-Toe (Pygame)

In the lab guide, this pattern packages an interactive graphical game:

  * **Graphics Requirements & Hardware Acceleration:**
      * Peripheral access declared in `finish-args`:
        ```yaml
        finish-args:
          - --share=ipc
          - --socket=x11
          - --socket=wayland
          - --device=dri        # GPU hardware acceleration
          - --env=PYTHONPATH=/app/lib/game
        ```
  * **Python Dependency Management via Modules:**
      * The manifest bundles `pygame` from PyPI and installs game code to `/app/lib/game`.
  * **Desktop Integration:**
      * `.desktop` file and icon installed to standard XDG sandbox paths (`/app/share/applications/` and `/app/share/icons/`).

-----

## Flatpak: The flatpak-builder Tool

The `flatpak-builder` utility parses the manifest and builds the app in an isolated environment:

```bash
# 1. Build and install locally for the current user
flatpak-builder --user --install --force-clean \
  build-dir com.example.HelloWorld.yml
```

  * **`--user`:** Installs into user profile (`~/.local/share/flatpak`), requiring no `sudo`.
  * **`--install`:** Registers the application in the system upon successful build.
  * **`--force-clean`:** Cleans the temporary build directory `build-dir`.

```bash
# 2. Run the application inside the Flatpak sandbox
flatpak run com.example.HelloWorld
```


-----

## Session Summary & Key Takeaways

  * **Infrastructure vs. Desktop:** Docker manages backend server workloads (*headless*); AppImage, Snap, and Flatpak distribute interactive graphical desktop applications.
  * **Solving Dependency Hell:** Self-contained packaging eliminates shared library (`.so`) version conflicts, guaranteeing deterministic execution.
  * **AppImage:** Single portable executable focused on simplicity, without a sandbox by default.
  * **Snap:** Mandatory confinement (AppArmor) and centralized distribution closely tied to Ubuntu.
  * **Flatpak:** Open standard for desktop applications, combining shared *Runtimes* with robust sandboxing (*Bubblewrap*).

-----

## Authoritative Technical References

Official documentation and specifications for further study in desktop systems and sandboxing:

  * **Flatpak Documentation:**
      * [Flatpak Developer Guide and Architecture Reference](https://docs.flatpak.org/)
      * [flatpak-builder Command Reference](https://docs.flatpak.org/en/latest/flatpak-builder.html)
  * **AppImage Documentation:**
      * [Official AppImage Packaging Guide](https://docs.appimage.org/)
      * [AppImage File Format Specification](https://github.com/AppImage/AppImageSpec)
  * **Canonical Snapcraft:**
      * [Snap Architecture and Interfaces Documentation](https://snapcraft.io/docs)
  * **FreeDesktop.org Specifications:**
      * [Desktop Entry Specification (`.desktop`)](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
      * [XDG Desktop Portals Specification](https://flatpak.github.io/xdg-desktop-portal/)
