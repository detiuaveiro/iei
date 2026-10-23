---
title: Containers
subtitle: Introduction to Computer Engineering
institute: Universidade de Aveiro
date: October 19, 2026
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

# Practical Laboratory Guide

**Context & Objectives:**  
In contemporary software engineering, Docker containers are the industry standard for packaging and managing **backend applications, web APIs, databases, and microservice-oriented architectures**, serving as the direct foundation for cloud-scale orchestration (such as Kubernetes clusters). In this **3-hour** practical laboratory session, you will explore the container lifecycle, turn application code into autonomous services, and orchestrate multi-tier topologies using Docker and Docker Compose:

* **Part 1 — Docker Installation & Setup:** Configuring the official Docker repository and non-root execution permissions.
* **Part 2 — Exercise 1: Docker CLI Fundamentals & Manual Image Building:** Exploring the container lifecycle (`run`, `ps`, `logs`, `exec`, `stop`, `rm`), local vs. remote registry, and manual image compilation using `Dockerfile` and `docker build`.
* **Part 3 — Exercise 2: "Hello, World" with Docker Compose:** Core structure of a `compose.yml` file and automated container lifecycle.
* **Part 4 — Exercise 3: Building Custom Images with Compose:** Creating a `Dockerfile` integrated with Compose to package an NGINX web application.
* **Part 5 — Exercise 4: Live Development with Volumes:** Live mounting (*bind mounts*) host files into containers without image rebuilds.
* **Part 6 — Exercise 5: Multi-Service Architecture with Varnish Cache & NGINX:** Orchestrating multiple services, internal Docker DNS networking, and high-performance reverse proxy caching.
* **Part 7 — Exercise 6: Deploying Real-World Applications:** Autonomous deployment of production-grade services (e.g., Jellyfin) configuring environment variables (`PUID`, `PGID`, `TZ`), persistent volumes, and port mappings.

\vspace{0.5em}

### Workspace Directory Setup

Before starting the exercises, create and enter a dedicated workspace directory for this session:

```bash
$ mkdir -p ~/IEI/class04
$ cd ~/IEI/class04
```

All files created during this lab (`compose.yml` files, `Dockerfile` definitions, web pages, and configurations) should be organized into subfolders within this workspace.

> **File path note:**
> Commands in this guide assume the terminal is located in the `~/IEI/class04` workspace. Each exercise should be developed within its respective subfolder (e.g., `ex1-cli`, `ex2-helloworld`, `ex3-build`, etc.).

-----

## Part 1: Installing Docker on Debian / Ubuntu

If you are using a Linux host (Debian or Ubuntu), follow these steps in your terminal to install the latest version of Docker Engine and Docker Compose plugin, based on the [official instructions](https://docs.docker.com/engine/install/debian/). *(On Windows or macOS, install [Docker Desktop](https://docs.docker.com/desktop/)).*

1.  **Set up Docker's `apt` repository:**
    ```bash
    # Remove non-official docker packages
    sudo apt remove docker.io docker-doc \
    docker-compose podman-docker containerd runc
    
    # Update package index and install prerequisites
    sudo apt update
    sudo apt install ca-certificates curl

    # Add Docker’s official GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg \
    -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
      https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    ```
2.  **Install the Docker packages:**
    ```bash
    sudo apt install docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
    ```
3.  **Manage Docker as a non-root user (Recommended):**
    To run `docker` commands without `sudo`, add your user to the `docker` group.
    ```bash
    sudo usermod -aG docker $USER
    ```
    **Important:** You must log out and log back in for this change to take effect.

-----

## Exercise 1: Docker CLI Fundamentals & Manual Image Building

**Goal:** Practice essential Docker CLI commands (`run`, `ps`, `logs`, `exec`, `stop`, `rm`, `build`), understand the distinction between local and remote registries (Docker Hub), and manually build your first custom image from a `Dockerfile`.

1.  **Exploring Local Registry & Pulling Images (`docker images` and `docker pull`):**
    * Create a directory for this exercise and enter it:
      ```bash
      $ mkdir -p ex1-cli && cd ex1-cli
      ```
    * Inspect the images stored locally on your machine:
      ```bash
      $ docker images
      ```
      *(If this is a fresh installation, the list will be empty).*
    * Pull the official image of the minimalist **Alpine Linux** distribution directly from Docker Hub (the default remote public registry):
      ```bash
      $ docker pull alpine:3.20
      ```
    * List local images again (`docker images`) and verify that `alpine:3.20` is now on disk (notice its ultralight footprint of only ~8 MB!).

2.  **Running an Interactive Container & Understanding Lifecycle (`run -it`, `ps`, `ps -a` and `rm`):**
    * Create and start an interactive container running a shell session (`sh`):
      ```bash
      $ docker run -it --name my-terminal alpine:3.20 sh
      ```
    * Notice how your shell prompt changed to `/ #`. You are now running commands inside the container's isolated process space and root filesystem! Try:
      ```sh
      / # cat /etc/os-release   # Inspect the container distribution
      / # hostname              # View the unique hostname assigned to the container
      / # exit                  # Terminate the session and exit the container
      ```
    * Back on your host terminal, check running containers:
      ```bash
      $ docker ps
      ```
      *(The container is not listed because its primary process `sh` has finished).*
    * List **all** containers (including stopped/exited ones):
      ```bash
      $ docker ps -a
      ```
      You will see container `my-terminal` still exists on disk in state `Exited (0)`.
    * Remove the container and its temporary writable layer permanently:
      ```bash
      $ docker rm my-terminal
      ```

3.  **Background Web Service, Port Mapping & Logs (`run -d -p`, `logs` and `exec`):**
    * Start an NGINX web server in the background (*detached* mode, `-d` flag) mapping host port 8080 to container port 80 (`-p` flag):
      ```bash
      $ docker run -d --name my-server -p 8080:80 nginx:alpine
      ```
      *(Since `nginx:alpine` was not cached locally, Docker automatically pulled it before running).*
    * Confirm that the container is actively running with the mapped port:
      ```bash
      $ docker ps
      ```
    * Open your web browser at `http://localhost:8080`. You should see the *"Welcome to nginx!"* default page.
    * Return to your terminal and view the HTTP access logs generated by your browser request:
      ```bash
      $ docker logs my-server
      ```
    * Open a live terminal session inside the running container to modify the served webpage on the fly:
      ```bash
      $ docker exec -it my-server sh
      / # echo "<h1>Ola do container</h1>" > /usr/share/nginx/html/index.html
      / # exit
      ```
    * Refresh `http://localhost:8080` in your browser and confirm the live modification.
    * Stop and remove the container:
      ```bash
      $ docker stop my-server
      $ docker rm my-server
      ```

4.  **Creating your First `Dockerfile` Manually and Building (`docker build`):**
    * Inside the `ex1-cli` directory, create an `index.html` file with custom content:
      ```html
      <!DOCTYPE html>
      <html>
      <body>
          <h1>My first custom image built with Dockerfile!</h1>
      </body>
      </html>
      ```
    * Create the declarative recipe file named `Dockerfile` (no extension):
      ```dockerfile
      FROM nginx:alpine
      COPY index.html /usr/share/nginx/html/index.html
      ```
    * Build the image with a tag (`-t`) using the current directory context (`.`):
      ```bash
      $ docker build -t my-manual-site:1.0 .
      ```
    * Inspect your local registry with `docker images`. Your image `my-manual-site:1.0` is now ready to run and distribute!
    * Run a container from your newly built custom image:
      ```bash
      $ docker run -d --name manual-site -p 8080:80 my-manual-site:1.0
      ```
    * Access `http://localhost:8080` in your browser to verify the result.
    * Clean up the container:
      ```bash
      $ docker stop manual-site && docker rm manual-site
      ```
    * Return to the lab root folder to proceed to Docker Compose:
      ```bash
      $ cd ~/IEI/class04
      ```

-----

## Exercise 2: "Hello, World" with Docker Compose

**Goal:** Understand the basic structure of a `compose.yml` file and run a pre-built image.

1.  Create a new folder for this exercise (e.g., `ex2-helloworld`).
2.  Inside the folder, create a new file named `compose.yml` with the following content:
    ```yaml
    services:
      hello:
        image: hello-world
    ```
3.  Open your terminal in this folder and run the application.
    ```bash
    $ docker compose up
    ```
4.  Observe the output. The `hello-world` container will start, print its message, and then exit.
5.  Clean up the created container.
    ```bash
    $ docker compose down
    ```

-----

## Exercise 3: Building a Custom Web Server Image

**Goal:** Use a `Dockerfile` with Docker Compose to create a self-contained application image.

1.  Create a new folder (`ex3-build`) and a subfolder inside it named `my-website`.
2.  Inside `my-website`, create a file named `index.html`:
    ```html
    <!DOCTYPE html>
    <html>
    <body>
        <h1>This page was built into the Docker image!</h1>
    </body>
    </html>
    ```
3.  In the root of the `ex3-build` folder, create a `Dockerfile`:
    ```dockerfile
    FROM nginx:alpine
    COPY ./my-website /usr/share/nginx/html
    ```
4.  Finally, create your `compose.yml` file:
    ```yaml
    services:
      webserver:
        build: .
        ports:
          - "8080:80"
    ```
5.  Build and start the service. The `-d` flag runs it in the background.
    ```bash
    $ docker compose up --build -d
    ```
6.  Open your browser to `http://localhost:8080`. You should see your custom webpage.

-----

## Exercise 4: Live Development with Volumes

**Goal:** Understand how volumes allow you to change your website's content without rebuilding the image.

1.  Create a new folder (`ex4-volumes`) with the same `my-website/index.html` structure as the previous exercise.
2.  Create a `compose.yml` file. This time, we will use the standard `nginx:alpine` image and mount our local folder as a volume. **No `Dockerfile` is needed.**
    ```yaml
    services:
      webserver:
        image: nginx:alpine
        ports:
          - "8080:80"
        volumes:
          - ./my-website:/usr/share/nginx/html
    ```
3.  Start the service: `docker compose up -d`.
4.  Open your browser to `http://localhost:8080` to confirm it's working.
5.  **Live Update:** While the container is running, **edit the `index.html` file** on your host machine. Change the heading to `<h1>Live update with a Volume!</h1>`.
6.  Save the file and **refresh your browser**. The change appears instantly\!

-----

## Exercise 5: Caching Rich Content with Varnish & NGINX

**Goal:** Build a two-tier web application with a Varnish cache serving a rich webpage from an NGINX backend.

1.  **Create the File Structure:**
      * Create a new folder (e.g., `ex5-varnish-cache`).
      * Inside, create two subfolders: `varnish` and `my-dynamic-website`.
2.  **Create the Web Content:**
      * Find a fun animated GIF online and save it inside `my-dynamic-website` as `animation.gif`.
      * Inside `my-dynamic-website`, create an `index.html` file to display the GIF:
        ```html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Varnish Cache Test</title>
            <style> body { font-family: sans-serif; text-align: center; } </style>
        </head>
        <body>
            <h1>This page is being cached by Varnish!</h1>
            <img src="animation.gif" alt="Cached animation">
        </body>
        </html>
        ```
3.  **Create the Varnish Configuration:**
      * Inside the `varnish` folder, create a file named `default.vcl`. This tells Varnish where to find the NGINX server.
        ```vcl
        vcl 4.1;
        backend default {
            .host = "nginx";
            .port = "80";
        }
        ```
4.  **Create the Compose File:**
      * In the root of your `ex5-varnish-cache` folder, create the `compose.yml`:
        ```yaml
        services:
          cache:
            image: varnish:stable
            volumes:
              - ./varnish:/etc/varnish
            ports:
              - "8080:80"
            depends_on:
              - nginx

          nginx:
            image: nginx:alpine
            volumes:
              - ./my-dynamic-website:/usr/share/nginx/html
        ```
5.  **Run and Verify:**
      * Start the services: `docker compose up -d`.
      * Open your browser to `http://localhost:8080`. You should see your webpage with the GIF. The key here is that **Varnish** served you the page, not NGINX directly.
      * **See the cache in action:** Check the NGINX logs for the first request.
        ```bash
        $ docker compose logs nginx
        ```
      * Now, refresh your browser page several times. Check the `nginx` logs again. You should see **no new log entries**, because Varnish is serving the content from its cache without contacting the NGINX backend.

-----

## Exercise 6: Deploying a Real-World Application

**Goal:** Learn to read official documentation and deploy a complex, self-hosted service of your choice.

1.  **Choose a Service:** Create a new directory for this exercise (e.g., `ex6-jellyfin` or `ex6-realworld`). Go to [LinuxServer.io](https://www.linuxserver.io/) and browse their list of popular images. Choose one that interests you, for example:

      * **Jellyfin:** A media server for your movies and music.
      * **Nextcloud:** A personal cloud for files, contacts, and calendars.
      * **Home Assistant:** An open-source home automation platform.

2.  **Read the Documentation:** On the page for your chosen image, find the "Docker Compose" section. Read it carefully, paying close attention to the required **volumes** and **environment variables**.

      * **Volumes (`- ./config:/config`):** This is where the application's configuration will be stored on your host.
      * **Environment Variables (`PUID`, `PGID`, `TZ`):** These are critical. `TZ` sets your timezone (e.g., `Europe/Lisbon`). `PUID` and `PGID` ensure that files created by the container have the correct ownership. On Linux/macOS, find your ID by running the `id` command in your terminal. A common value is `1000`.

3.  **Create Your `compose.yml`:** Based on the documentation, create the file. Here is an example for **Jellyfin**:

    ```yaml
    services:
      jellyfin:
        image: lscr.io/linuxserver/jellyfin:latest
        container_name: jellyfin
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=Europe/Lisbon
        volumes:
          - ./config:/config
          - ./tvshows:/data/tvshows
          - ./movies:/data/movies
        ports:
          - "8096:8096"
        restart: unless-stopped
    ```

4.  **Prepare and Deploy:**

      * Create the local folders you defined in your volumes (e.g., `mkdir config tvshows movies`).
      * Run the application: `docker compose up -d`.

5.  **Explore:** Check the documentation for the default port number. For Jellyfin, it's `8096`. Open your browser to `http://localhost:8096` and follow the setup wizard for your new service\!

