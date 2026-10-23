---
title: 47138 - Introduction to Computer Engineering
subtitle: "Containers: Architecture, Docker & Docker Compose"
institute: Universidade de Aveiro
date: October 19, 2026
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

  * **Part I — Isolation Fundamentals & Architecture:** The portability challenge, OS-level virtualization, namespaces, cgroups, and non-Linux host execution.
  * **Part II — From Kernel to Tools: Ecosystem & OCI:** Evolution from LXC to Docker, OCI standardization (`runc`, open specifications), and Podman.
  * **Part III — Images, Storage & Networking:** Terminology, tags, lifecycle, layers (Copy-on-Write), volumes, and DNS-enabled networking.
  * **Part IV — Docker in Practice & `Dockerfile` Anatomy:** Essential CLI commands, instructions, exec/shell forms, and `CMD` vs. `ENTRYPOINT`.
  * **Part V — Local Orchestration with Docker Compose:** Syntax of `compose.yml`, management commands, and multi-service architectural patterns.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: Fundamentals \& Architecture}}
\end{center}

-----

## The Software Portability Challenge

Heterogeneous configurations across development, staging, and production environments pose a major software engineering challenge:

  * **Development Environment:**
      * Local configuration with specific interpreter versions (e.g., Python 3.11), dynamic shared libraries, and local environment variables.
  * **Testing or Production Environment:**
      * Operating systems with different versions of system shared libraries or restrictive security policies.
      * Risk of runtime failures caused by dependency incompatibilities (*dependency hell*).

\vspace{1em}

\begin{center}
\textbf{It would be desirable to package the application and all its dependencies into a standardized artifact, ensuring deterministic and reproducible execution.}
\end{center}

-----

## Virtual Machines as a Solution?

The isolation provided by Virtual Machines incurs substantial overhead when running individual applications:

  * **Hardware Virtualization Characteristics:**
      * Full hardware-level isolation via a hypervisor.
      * Dedicated guest kernel and operating system per virtual machine.
  * **Limitations for Application Workloads:**
      * **Overhead:** Static allocation of gigabytes of RAM and disk per instance.
      * **Redundancy:** Duplication of complete guest OS stacks to run a single service.
      * **Latency:** Slow boot times (minutes), hindering dynamic horizontal scaling.

\vspace{1em}

\begin{center}
\textbf{Hardware-level virtualization is disproportionately heavy for isolating and distributing lightweight individual applications.}
\end{center}

-----

## The Solution: Containers

The answer lies in **operating system-level virtualization**:

  * **Container Concept:** A standardized software unit packaging an application and all its dependencies.
  * **Paradigm Shift:**
      * Shares the **host OS kernel**, without virtualizing underlying hardware.
      * Process isolation is enforced directly **by the kernel itself** (via *namespaces* and *cgroups*).
  * **Deterministic Portability:** Identical execution across developer workstations, CI/CD testing runners, or cloud production clusters.

\vspace{1em}

\begin{center}
\textbf{Standard shipping containers decoupled cargo from transportation vehicles (ships, trains, trucks). Software containers decouple applications from host operating systems.}
\end{center}

-----

## Comparative Architecture: VMs vs. Containers

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{vm_vs_container_architecture.png}
\end{center}

-----

## Systematic Comparison: VMs vs. Containers

| Technical Dimension | Virtual Machines (VMs) | Containers |
| :--- | :--- | :--- |
| **Abstraction Level** | **Hardware Virtualization** | **OS Virtualization** (Processes) |
| **System Kernel** | Dedicated guest kernel per VM | **Shared host OS kernel** |
| **Memory Footprint (RAM)** | High (static allocation to guest OS) | **Minimal** (only what the app consumes) |
| **Image Size** | Gigabytes (GB) | Megabytes (MB) |
| **Startup Time** | Tens of seconds to minutes | **Milliseconds to seconds** |
| **Performance Overhead** | Low to moderate (hypervisor trap latency) | **Near-native** (no hardware mediation) |
| **Isolation Boundary** | Very strong (hardware / CPU rings) | Strong (kernel isolation mechanisms) |
| **Typical Use Case** | Multi-OS environments, strict isolation | Backends, Microservices, APIs, Kubernetes |

-----

## Kernel Mechanisms: Linux Namespaces

**Linux Namespaces** restrict what a process can **see** within the operating system:

  * **PID (Process ID):** Isolates the process table (application runs as **PID 1** inside the container).
  * **NET (Network):** Private virtual network interfaces (`eth0`), routing tables, and independent port namespaces.
  * **MNT (Mount):** Isolated mount points with a dedicated root filesystem (`/`).
  * **UTS (Hostnames):** Independent hostname and domain name assignments.
  * **USER:** User ID mappings (e.g., `root` inside the container maps to an unprivileged user on the host).
  * **IPC (Inter-Process Communication):** Isolates shared memory segments and message queues between processes.

-----

## Isolation in Action: Namespaces Mapping

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{linux_namespaces_isolation.png}
\end{center}

-----

## Kernel Mechanisms: Control Groups (cgroups)

**Control Groups (cgroups)** allow the kernel to enforce strict hardware resource limits on containers:

  * **CPU:** Limits processor time share or dedicated core counts (e.g., maximum of 1.5 vCPUs).
  * **Memory (RAM):** Imposes a hard memory ceiling (e.g., 512 MB). If exceeded, the kernel terminates the process (*Out Of Memory Killer - OOM*).
  * **Block I/O:** Prevents a noisy container from starving disk bandwidth with heavy read/write operations.
  * **PID Control (pids cgroup):** Limits the total number of child processes to protect the host against *fork bombs*.

\vspace{1em}

\begin{center}
\textbf{While \textit{namespaces} define visibility boundaries and logical isolation, \textit{cgroups} enforce quantitative resource quotas and fair-share guarantees.}
\end{center}

-----

## Linux Containers Outside Linux: macOS and Windows

Because they rely on the Linux kernel (*namespaces* and *cgroups*), running **Linux containers** on macOS or Windows requires a lightweight support virtual machine (managed by tools like **Docker Desktop** or **Podman**):

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{docker_desktop_architecture.png}
\end{center}

-----

## Linux Containers Outside Linux: macOS and Windows

  * **On Linux (Native Execution):**
      * Direct execution over the host kernel with native performance.
      * No hypervisors and zero virtualization overhead.
  * **On macOS and Windows (Docker Desktop, Podman, etc.):**
      * Host kernels (Darwin / NT) cannot execute Linux binaries natively.
      * Tools run a lightweight **micro-VM Linux** (*Virtualization.framework* / *WSL2*) shared across containers.
      * *(Note: Windows supports native Windows containers, but nearly all industry deployments use Linux images).*
  * **Operational Impact:**
      * Dedicated RAM and CPU resources reserved for the support virtual machine.
      * Higher I/O latency when sharing host filesystems (*bind mounts*) across VM boundaries.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part II: From Kernel to Tools: Ecosystem \& OCI}}
\end{center}

-----

## The Evolution: Linux Containers (LXC) vs. Docker

Container technology did not originate with Docker:

  * **LXC (Linux Containers, 2008):**
      * The first comprehensive solution integrating cgroups and namespaces in the Linux kernel.
      * Focused on **system containers**: operating like lightweight VMs running a full `init` system (systemd), multiple processes, and background daemons.
  * **The Docker Revolution (2013):**
      * Docker initially leveraged LXC as its execution backend, adding a superior abstraction layer.
      * Popularized **application / microservice containers**: each container runs **a single primary process**.
      * Introduced layered image format (`Dockerfile`) and global image registry (Docker Hub), revolutionizing modern software engineering.

-----

## Standardization and Open Standards: The OCI

To prevent vendor lock-in to a single company, the industry established the **Open Container Initiative (OCI)**:

  * **Image Specification (Image Spec):**
      * Defines the exact binary layout of container image layers and configuration manifests.
      * An image built by Docker adheres to the OCI spec and runs identically on Podman, containerd, CRI-O, or Kubernetes.
  * **Runtime Specification (Runtime Spec):**
      * Defines the kernel interface for launching container processes.
      * The open-source reference implementation is **`runc`**, universally utilized by both Docker and Podman.

-----

## Podman and Container Security

**Podman** (developed by Red Hat) was designed to address traditional Docker security and architectural challenges:

  * **Daemonless Architecture:**
      * Docker relies on a centralized background daemon (`dockerd`) running persistently as `root`. If the daemon fails, all container management is impacted.
      * Podman is completely daemonless: each container is a direct child process of the user who launched it.
  * **Rootless by Design:**
      * Allows unprivileged users (without `sudo`) to pull, build, and run containers on Linux using *User Namespaces*.
  * **Complete CLI Compatibility:**
      * CLI syntax is identical to Docker:
        ```bash
        $ alias docker=podman
        $ docker run -d -p 8080:80 nginx:alpine
        ```

\vspace{1em}

\begin{center}
\textbf{Both tools share the same commands and OCI standards; mastering the Docker CLI provides universal skills across the entire cloud container ecosystem.}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: Images, Storage \& Networking}}
\end{center}

-----

## Core Terminology: Image vs. Container

Three fundamental concepts define the container model:

  * **1. Container Image:**
      * An immutable, read-only template packaging the filesystem, binaries, libraries, and runtime metadata.
      * **Analogy:** Equivalent to a **Class** in Object-Oriented Programming (static blueprint).
  * **2. Container:**
      * A runnable, isolated instance of an image executed by the kernel.
      * **Analogy:** Equivalent to an **Object** (multiple container instances can derive from the same image).
  * **3. Registry:**
      * A centralized service for storing, versioning, and distributing images (e.g., Docker Hub, GitHub Packages).

-----

## The Docker Lifecycle

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{docker_lifecycle.png}
\end{center}

-----

## Image Identification and Naming Convention

Images are identified following a standardized syntax:

$$\texttt{[registry/][repository/]name\textbf{:}tag}$$

  * **Official Repositories:** Official Docker Hub images omit registry and user prefixes (e.g., `nginx`, `alpine`, `ubuntu`).
  * **Role of the Tag:** Specifies the version or variant; defaults to `:latest` if omitted.
  * **Examples:**
      * `nginx:alpine` $\rightarrow$ NGINX based on minimalist Alpine Linux (~20 MB).
      * `python:3.11-slim` $\rightarrow$ Python 3.11 without heavy build tools.
      * `lscr.io/linuxserver/jellyfin:latest` $\rightarrow$ Image sourced from an external registry (`lscr.io`).
  * **Digest (SHA-256):** A unique cryptographic hash guaranteeing absolute image integrity and immutability.

-----

## Image Anatomy: Layers & Copy-on-Write (CoW)

A Docker image is not a monolithic archive, but rather a **stack of immutable read-only layers**:

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{container_layers_cow.png}
\end{center}

-----

## Copy-on-Write (CoW) Mechanism: Efficiency & Immutability

  * **Disk Layer Sharing:**
      * Common base layers (e.g., `alpine:3.20`) are stored on disk **only once**.
      * Substantial savings in network download bandwidth and local storage capacity.
  * **Layer Immutability (Read-Only):**
      * The underlying image layers are never altered or corrupted by running containers.
  * **Container Writable Layer (Read-Write Layer):**
      * A thin temporary layer added on top of the image stack when a container starts.
      * **Read:** Files are read directly from underlying shared image layers.
      * **Modify (CoW):** When modifying an existing file, it is copied to the R/W layer before editing.
      * **Destruction:** When the container is deleted, only this ephemeral R/W layer is discarded.

-----

## Data Persistence: Storage Types

By default, a container's filesystem is **ephemeral**. To manage persistent data, Docker provides three mechanisms:

  * **1. Writable Layer:**
      * **Lifecycle:** Ephemeral; permanently deleted when the container is removed.
      * **Typical Use:** Temporary scratch files and stateless workloads.
  * **2. Bind Mounts:**
      * **Mechanism:** Mounts a host directory directly into the container (`host:container`).
      * **Typical Use:** **Local development** (source code changes on host reflect live without rebuilding images).
  * **3. Managed Volumes (Named Volumes):**
      * **Mechanism:** Storage managed by the Docker Engine within a dedicated system location.
      * **Typical Use:** **Production persistence** (databases, high-performance I/O, independent of container lifecycle).

-----

## Virtual Networks: Bridge Mode and Port Mapping

By default, every container connects to a private virtual bridge network:

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{docker_network_ports_dns.png}
\end{center}

-----

## Container Networking: Isolation and DNS Resolution

  * **Private Virtual Network (Bridge Network):**
      * Isolates containers from the external network using kernel bridge interfaces and NAT firewall rules.
      * Each container receives an internal dynamic private IP address (e.g., `172.20.0.x`).
  * **Port Mapping (`-p <host_port>:<container_port>`):**
      * Forwards traffic arriving at a host port to the internal container port (e.g., `-p 8080:80`).
      * Allows external access to the containerized service via `http://localhost:8080`.
  * **Embedded DNS Resolution:**
      * Containers in the same custom bridge network resolve peer IP addresses automatically using **service names** (e.g., `postgres://db:5432`).
      * Completely decouples services from dynamic ephemeral IP addresses.
  * **Security Isolation:**
      * Internal services (e.g., database `db`) need no exposed host ports.
      * Kept invisible and protected from direct access from the external network or Internet.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part IV: Docker in Practice \& Dockerfile Anatomy}}
\end{center}

-----

## Essential Docker Commands

The `docker` command-line interface controls the entire container lifecycle:

| Command | Description |
| :--- | :--- |
| `docker run [options] <image>` | Creates and starts a new container from an image. |
| `docker run -d -p 8080:80 <image>` | Runs in background (*detached*) mapping host port 8080. |
| `docker ps` | Lists currently active/running containers. |
| `docker ps -a` | Lists all containers (including stopped and exited ones). |
| `docker stop <id/name>` | Sends `SIGTERM` to gracefully stop a running container. |
| `docker rm <id/name>` | Permanently removes an exited container and its R/W layer. |
| `docker logs -f <id/name>` | Streams and monitors standard output (`stdout`/`stderr`) logs. |
| `docker exec -it <name> sh` | Opens an interactive terminal session inside a running container. |
| `docker images` | Lists all container images stored locally on disk. |
| `docker rmi <image>` | Deletes a local container image from storage. |

-----

## High-Level Overview: `Dockerfile` Example

A `Dockerfile` is a declarative, automated recipe for building container images:

```dockerfile
# 1. Base starting image
FROM python:3.11-slim

# 2. Working directory inside container
WORKDIR /app

# 3. Copy files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 4. Network metadata and startup command
EXPOSE 8080
CMD ["python", "app.py"]
```

```bash
$ docker build -t my-app:1.0 .              # Builds the image from context (.)
$ docker run -d -p 8080:8080 my-app:1.0     # Starts the container
```

-----

## `Dockerfile` Anatomy: Structure Instructions

With the overview in mind, let's explore the core filesystem instructions:

  * `FROM <image>:<tag>`
      * Sets the base image from which the new image is derived (e.g., `alpine:3.20`).
  * `WORKDIR <path>`
      * Sets the active working directory for subsequent instructions (creates folder if missing).
  * `COPY <src> <dest>`
      * Copies files and directories from the host build context into the image filesystem.
  * `RUN <command>`
      * Executes commands during build time and commits the result into a new immutable layer (e.g., `RUN apk add --no-cache curl`).

-----

## `Dockerfile` Anatomy: Environment, Ports & Security

  * `ENV <key>=<value>`
      * Defines environment variables available during build and persistently across container execution (e.g., `ENV PORT=8080`).
  * `ARG <name>=<value>`
      * Defines temporary variables used exclusively during image compilation.
  * `EXPOSE <port>`
      * **Documentation metadata**: specifies the network ports on which the application listens (does not publish to host).
  * `USER <user>`
      * Sets the username or UID for subsequent processes, avoiding running containers with root privileges.

-----

## `Dockerfile` Anatomy: Execution (`CMD` & `ENTRYPOINT`)

To define the process started when a container launches, Docker provides two key instructions:

  * `CMD ["executable", "arg1", ...]`
      * Defines the **default** command and/or arguments executed upon startup.
      * If arguments are passed to `docker run`, the entire `CMD` instruction is overridden.
  * `ENTRYPOINT ["executable", "arg1", ...]`
      * Configures the container to run as a **dedicated, fixed executable**.
      * Arguments supplied to `docker run` are appended as parameters to the executable.

-----

## `CMD` vs. `ENTRYPOINT` in Practice: Demonstration

Consider two representative scenarios built on top of Alpine Linux:

**Scenario A: `CMD` only (Flexible default command)**
```dockerfile
FROM alpine:3.20
CMD ["echo", "Default message"]
```
```bash
$ docker run demo-cmd              # Prints: "Default message"
$ docker run demo-cmd uname -a     # Runs uname -a; overrides the original CMD command
```

**Scenario B: `ENTRYPOINT` with `CMD` (Fixed executable + Flexible argument)**
```dockerfile
FROM alpine:3.20
ENTRYPOINT ["echo", "Environment:"]
CMD ["Production"]
```
```bash
$ docker run demo-ep               # Prints: "Environment: Production"
$ docker run demo-ep Staging       # Prints: "Environment: Staging" (overrides CMD)
```

-----

## The Build Context and `.dockerignore`

When running the image build command:

```bash
$ docker build -t my-service:1.0 .
```

  * **Meaning of the Path Argument (`.`):**
      * Defines the root of the **Build Context**.
      * The Docker client creates an archive of this directory and sends it to the Docker Daemon before processing instructions.
  * **The `.dockerignore` File:**
      * Follows semantics similar to `.gitignore`.
      * Prevents large folders or sensitive files from being transferred to the daemon:
        ```text
        .git
        node_modules
        .env
        *.log
        ```
      * Minimizes build transfer latency and prevents accidental inclusion of credentials, secrets, or local dependencies into image layers.

-----

## Comprehensive Example: Building and Inspecting a Service

Consider a `Dockerfile` packaging a diagnostics service running under an unprivileged user:

```dockerfile
FROM alpine:3.20
WORKDIR /app
RUN adduser -D -u 1000 appuser
USER appuser
CMD ["sh", "-c", "while true; do echo \"[LOG] Service active at $(date)\"; sleep 5; done"]
```

**Validation Sequence in the Terminal:**

```bash
# 1. Build the image with a formal tag
$ docker build -t logging-service:1.0 .

# 2. Run the container in detached background mode
$ docker run -d --name logger logging-service:1.0

# 3. Inspect execution environment and logs
$ docker exec -it logger whoami        # Confirms execution under appuser (non-root)
$ docker logs --tail 3 logger          # Inspects recent standard output log entries
$ docker stop logger && docker rm logger
```

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part V: Local Orchestration with Docker Compose}}
\end{center}

-----

## Motivation and Scope of Docker Compose

In real-world system architecture, applications rarely run as a single isolated container:

  * A typical web application requires a web server (NGINX), an application runtime (Python/Node), and a database (PostgreSQL).
  * Starting this architecture manually with individual `docker run` commands requires:
      * Manually creating virtual networks (`docker network create`).
      * Launching each container individually with dozens of port, volume, and environment parameters.
      * Manually ensuring the correct order of startup.
  * **Docker Compose:**
      * A declarative orchestration tool that defines and manages multi-container applications via a single file: `compose.yml`.
      * Application infrastructure is declared as code (*Infrastructure as Code*) and tracked directly in the project's Git repository.

-----

## Anatomy of the `compose.yml` File

A `compose.yml` file organizes application services into a cohesive topology:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"                  # host:container
    volumes:
      - ./site:/usr/share/nginx/html
    environment:
      - TZ=Europe/Lisbon           # Timezone
    restart: unless-stopped        # Restart policy

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secret   # Initialization variable
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:                         # Docker-managed named volume
```

-----

## Docker Compose Commands

Service orchestration is managed centrally from the directory containing `compose.yml`:

| Command | Action Performed |
| :--- | :--- |
| `docker compose up -d` | Pulls images, creates networks and volumes, and starts all services in background. |
| `docker compose up --build -d` | Forces a rebuild of local images (`build:`) before starting. |
| `docker compose ps` | Displays the status and port mappings of all services. |
| `docker compose logs -f` | Streams aggregated logs from all services in real time. |
| `docker compose logs -f <service>` | Filters logs for a specific service (e.g., `docker compose logs -f web`). |
| `docker compose stop` | Halts service containers without removing networks or containers. |
| `docker compose down` | Stops and removes containers and internal networks created by Compose. |
| `docker compose down -v` | Stops services and additionally removes persistent named volumes. |

-----

## Compose Pattern 1: Custom Image Packaging

```yaml
services:
  webserver:
    build: .             # Path to Dockerfile in local context
    ports:
      - "8080:80"        # Host port 8080 mapped to container port 80
```

  * **Concept:** Application source code is baked directly into the image layers during build time.
  * **Behavior:** The resulting container is an autonomous, self-contained, and immutable artifact ready for staging and production.
  * **Updates:** Code modifications require explicitly rebuilding the image (`docker compose up --build -d`).

-----

## Compose Pattern 2: Live Development with Volumes

```yaml
services:
  webserver:
    image: nginx:alpine                  # Standard official image
    ports:
      - "8080:80"
    volumes:
      - ./my-website:/usr/share/nginx/html # Dynamic host folder mount
```

  * **Concept:** Eliminates the need for a custom `Dockerfile`, directly utilizing the official NGINX image.
  * **Direct Mount:** The host directory `./my-website` is mounted over the web server's document root.
  * **Fast Feedback Cycle:** Edits made to host source files reflect instantly in the browser without restarting containers.

-----

## Compose Pattern 3: Multi-Service Architecture (Web + Database)

```yaml
services:
  web:
    build: .
    ports:
      - "8080:80"                        # Public port mapped to host
    depends_on:
      - db                               # Starts after database service
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data # No public host ports exposed
volumes:
  db_data:                               # Managed persistent volume
```

  * **Name Resolution:** The `web` service connects to `postgres://db:5432`, resolved automatically by embedded DNS.
  * **Security Isolation:** Only `web` exposes a public host port (`:8080`); database remains protected on internal network.
  * **Data Persistence:** Data is stored in managed volume `db_data`, surviving service restarts (`docker compose down`).

-----

## Authoritative Technical References

Official documentation and specifications for further study in systems engineering and cloud computing:

  * **Docker Documentation:**
      * [Official Docker Architecture & Guides](https://docs.docker.com/)
      * [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
      * [Compose File Specification](https://docs.docker.com/compose/compose-file/)
  * **Open Container Initiative (OCI):**
      * [Official OCI Image and Runtime Specifications](https://opencontainers.org/)
  * **Podman Documentation:**
      * [Podman User Guide and Architecture](https://docs.podman.io/)
  * **Linux Kernel Documentation:**
      * [Linux Namespaces (`namespaces(7)`)](https://man7.org/linux/man-pages/man7/namespaces.7.html)
      * [Linux Control Groups (`cgroups(7)`)](https://man7.org/linux/man-pages/man7/cgroups.7.html)
