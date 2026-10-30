---
title: Proyectos 01
subtitle: Introducción a la Ingeniería Informática
author: Luis Moutinho, Joaquim Sousa Pinto
institute: Universidade de Aveiro
date: 27 de Octubre de 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\small}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Proyectos

> ### Régimen de Uso de Inteligencia Artificial: IA CONDICIONADA
> 
> *En cumplimiento de las directrices institucionales de la Universidade de Aveiro (Referencial para Avaliação das Aprendizagens na Era da Inteligência Artificial):*
> 
> * **Desarrollo de Software:** Se permite el uso de sistemas de IA como apoyo técnico para la depuración de errores (*debugging*) o la sugerencia de código repetitivo. La lógica central y la arquitectura de la solución no pueden ser generadas por IA (queda expresamente prohibido el régimen *"one-shot"* para la totalidad del proyecto).
> * **Informe de Proyecto:** Se permite el uso de IA exclusivamente para el apoyo en la revisión lingüística y la mejora de la claridad del texto. La estructura argumentativa, la interpretación de resultados y las conclusiones deben ser fruto del trabajo intelectual y autoral de los estudiantes.
> * **Declaración Obligatoria:** El trabajo debe incluir obligatoriamente en el informe la correspondiente **Declaración de Uso de IA** (ver modelo en el [Anexo](#anexo-modelo-de-la-declaración-de-uso-de-ia)), acompañada de los extractos de los prompts más relevantes y de la justificación crítica de las sugerencias aceptadas o rechazadas.

Formen grupos de dos o tres estudiantes (excepcionalmente, los proyectos pueden realizarse de forma individual) y seleccionen **uno** de los siguientes proyectos. Todos los proyectos se alojarán en **GitHub**, a través de un repositorio privado creado por cada grupo en una cuenta personal gratuita. Consulten [aquí](#configuración-y-gestión-del-repositorio-en-github) los detalles.

El repositorio debe contener todos los scripts pertinentes, archivos de configuración y un archivo `README.md` con instrucciones detalladas sobre cómo desplegar y ejecutar el proyecto.
También debe contener un informe del proyecto en formato `PDF`.

Este es un proyecto de tres semanas. Tienen una semana para notificar a su profesor (por correo electrónico) los miembros de su grupo, la clase (*turma*) y el tema seleccionado (la lista de temas se encuentra [aquí](#temas)). Tras dicha notificación, los docentes asignarán el correspondiente **número de grupo**.

No duden en ponerse en contacto con su profesor ante cualquier duda.
Podrán añadirse instrucciones adicionales.

## Temas

### 1. Sitio Estático de Alto Rendimiento con Caché
* **Descripción:** Implementar un servicio web de alto rendimiento utilizando **Docker Compose**. Esta arquitectura debe orquestar dos servicios interdependientes en una red interna: un servidor web de backend (como **NGINX**, **Caddy** o **Apache `httpd`**) y una caché de proxy inverso de alto rendimiento al frente (como **Varnish Cache** o **NGINX** en modo proxy cache). El contenido estático del sitio (una página rica con estilos CSS, scripts e imágenes) debe servirse desde un **volumen** montado en el contenedor del servidor web. Solo el puerto del servicio de caché debe exponerse al exterior. Además, se deben realizar pruebas de carga y rendimiento desde la terminal (utilizando herramientas como `ab` — Apache Benchmark o `wrk`), comparando la latencia y el caudal de peticiones (*requests/sec*) con y sin caché activa.
* **Temas Principales:** Docker Compose (multi-servicio), servidores web (NGINX/Caddy/Apache), Varnish Cache, redes privadas de contenedores, `volumes`, pruebas de rendimiento y latencia en CLI (`ab`/`wrk`).

### 2. El Solucionador "Funciona en mi Máquina": Entorno de Desarrollo en Contenedor
* **Descripción:** Crear un entorno de desarrollo hermético y reproducible basado en contenedores para un lenguaje a su elección (ej.: Python, C/C++, Rust o Node.js), eliminando conflictos de dependencias locales.
  1. **Construcción del Entorno:** Crear un `Dockerfile` optimizado con el compilador/intérprete, herramientas de análisis estático (*linters*) y soporte para un usuario no-root (evitando problemas de permisos con archivos generados en el host).
  2. **Desarrollo con Volúmenes:** Utilizar Docker Compose y **volúmenes** (*bind mounts*) para que el código fuente se edite en la máquina anfitriona, mientras que toda la compilación, ejecución y pruebas se realizan de forma aislada dentro del contenedor.
  3. **Automatización y Aplicación de Ejemplo:** Incluir una pequeña aplicación de prueba (con funciones y pruebas unitarias correspondientes) y un script CLI de automatización (o `Makefile`) para compilar, ejecutar las pruebas y generar informes de linting dentro del contenedor con un único comando.
  4. **Integración con IDEs (Opcional / Desafío):** Los grupos pueden adoptar opcionalmente la especificación abierta de [Development Containers (containers.dev)](https://containers.dev), configurando el archivo `.devcontainer/devcontainer.json` para su integración automática con Visual Studio Code.
* **Temas Principales:** `Dockerfile`, aislamiento de entornos de desarrollo, Docker Compose, `volumes`, gestión de dependencias (`apt`), permisos no-root, automatización de pruebas y especificación [containers.dev](https://containers.dev).

### 3. Asistente Desktop Gemini: Aplicación Gráfica con Sandboxing en Flatpak
* **Descripción:** Implementar una aplicación de escritorio con interfaz gráfica (GUI) en Python que permita a los usuarios interactuar con los modelos de lenguaje **Google Gemini mediante API**, empaquetándola y distribuyéndola a través de un contenedor de aplicación **Flatpak**.
  1. **Interfaz Gráfica Minimalista:** La aplicación debe ofrecer una interfaz gráfica sencilla y funcional (desarrollada con la biblioteca nativa **Tkinter**, sin necesidad de estilos complejos, o alternativamente con **CustomTkinter**/**PyGObject**): un campo de entrada para el *prompt*, botón de envío y un área con historial/visualización de la respuesta generada por el modelo.
  2. **Consumo de API y Secretos:** La aplicación debe comunicarse con la API de Gemini (utilizando cabeceras HTTP con la variable de entorno segura `GEMINI_API_KEY` o un diálogo de configuración en la app), gestionando de manera robusta fallos de conectividad y respuestas de error de la API.
  3. **Empaquetado Flatpak y Manifiesto:** Crear el manifiesto Flatpak (`yaml` o `json`) definiendo el runtime/SDK (ej.: `org.gnome.Platform`), los módulos necesarios, metadatos `.desktop` e icono de la aplicación.
  4. **Auditoría de Permisos en el Informe:** Demostrar en el informe el aislamiento estricto de la *sandbox* (bubblewrap) basándose en el principio de mínimo privilegio, documentando el comportamiento de la app con y sin el permiso de red (`--share=network`) y confirmando la imposibilidad de acceder a archivos confidenciales del anfitrión (ej.: `~/.ssh`).
* **Temas Principales:** Interfaz Gráfica (Python/Tkinter), consumo de APIs REST (Gemini), Contenedores de Aplicación (Flatpak), Desktop Sandboxing y Permisos (`finish-args`, `--share=network`, sockets de display), integración en el escritorio (`.desktop`).

### 4. Plataforma Web con Gestión de Estado y Copias de Seguridad Automatizadas
* **Descripción:** Implementar una plataforma web completa respaldada por base de datos (como **WordPress** o **Ghost CMS**) utilizando **Docker Compose**. El proyecto requiere la orquestación segura del contenedor de la aplicación web y del contenedor de base de datos (**MySQL** o **MariaDB**) en una red aislada, con persistencia total en **volúmenes**. Además de configurar y personalizar la plataforma (con publicaciones iniciales), el grupo debe desarrollar un **script Bash de automatización** que realice copias de seguridad consistentes de la base de datos (`mysqldump`) y de los archivos subidos, generando archivos comprimidos `.tar.gz` fechados con rotación automática (mantener las últimas $N$ copias) y un script de restauración (*disaster recovery*).
* **Temas Principales:** Docker Compose (multi-servicio), WordPress/Ghost, bases de datos relacionales, redes internas, `volumes`, variables de entorno (`.env`), scripting Bash de backup y restauración (`mysqldump`, `tar`, `cron`).

### 5. Comparativa de Rendimiento: Máquina Virtual vs. Contenedor
* **Descripción:** Realizar un estudio comparativo riguroso de rendimiento entre virtualización clásica y contenerización. El grupo debe desplegar un servidor web **NGINX** idéntico en dos entornos: 1) dentro de una **Máquina Virtual Debian** (configurada mediante VirtualBox o QEMU) y 2) dentro de un **contenedor Docker**. A continuación, deben ejecutar una batería de pruebas objetivas recopilando métricas del sistema: tiempo de arranque (*boot time* con `systemd-analyze` o cronómetro), consumo de memoria RAM en reposo y bajo carga (`free`, `vmstat`, `docker stats`), uso de espacio en disco (tamaño de la imagen de disco `.vdi`/`.qcow2` vs imagen Docker) y tiempos de respuesta a peticiones HTTP bajo carga con herramientas de benchmark (`ab` o `wrk`). El informe debe incluir tablas, gráficos comparativos y un análisis fundamentado de los resultados.
* **Temas Principales:** Virtualización de sistemas (VirtualBox/QEMU), Contenedores (Docker), monitorización de recursos (`top`, `free`, `df`, `time`), benchmarking de red (`ab`/`wrk`), análisis comparativo de arquitecturas.

### 6. Cockpit de Observabilidad: Monitorización de Contenedores con Prometheus & Grafana
* **Descripción:** Implementar una infraestructura completa de observabilidad y telemetría de contenedores utilizando **Docker Compose**. La arquitectura debe integrar tres servicios orquestados:
  1. **cAdvisor:** Agente que recopila telemetría y métricas de uso de recursos (CPU, RAM, tráfico de red e I/O de disco) directamente del daemon de Docker mediante el montaje del socket `/var/run/docker.sock`.
  2. **Prometheus:** Servidor de base de datos de series temporales configurado para recolectar (*scrape*) periódicamente las métricas ofrecidas por cAdvisor en una red interna privada.
  3. **Grafana:** Panel de visualización web conectado a Prometheus como fuente de datos, siendo el único servicio con puerto expuesto al exterior.
  El grupo debe diseñar un panel (*dashboard*) interactivo en Grafana que muestre el uso de los contenedores del sistema y demostrar su funcionamiento provocando un pico de consumo de CPU/memoria en un contenedor auxiliar de prueba (utilizando herramientas como `stress` o `stress-ng`).
* **Temas Principales:** Docker Compose (multi-servicio), observabilidad y telemetría (Prometheus, Grafana, cAdvisor), redes de contenedores privadas, montaje de sockets del sistema, persistencia de métricas en `volumes`, pruebas de estrés.

## Criterios de Evaluación

El proyecto será evaluado en una escala de **0 a 20 valores**, distribuidos en cinco vectores fundamentales:

| Vector de Evaluación | Peso | Puntuación | Descripción Principal |
| :------------------------ | :--------: | :---------: | :---------------------------------------------------- |
| **1. Implementación Técnica y Requisitos** | 30% | 6.0 val | Cumplimiento riguroso de los requisitos funcionales del tema, funcionamiento correcto sin fallos, arquitectura modular y buenas prácticas (Docker/Compose/Flatpak/Bash). |
| **2. Informe Técnico y Documentación** | 30% | 6.0 val | Claridad, estructura lógica y fundamentación técnica del informe en PDF; calidad de las instrucciones de despliegue y reproducción en el `README.md`. |
| **3. Uso Crítico y Transparente de IA** | 20% | 4.0 val | Ingeniería de contexto (archivo `AGENTS.md`, *skills*), relevancia de los prompts, justificación crítica de aceptación/rechazo y Declaración de IA. |
| **4. Creatividad y Funcionalidades Adicionales** | 10% | 2.0 val | Innovación y extensión más allá de los requisitos mínimos (funcionalidades extra, resiliencia a fallos, refinamiento visual/UX, automatizaciones y scripts complementarios). |
| **5. Flujo Colaborativo y Gestión de Proyecto** | 10% | 2.0 val | Uso de GitHub Issues/Tareas, flujo de trabajo con ramas y Pull Requests con revisiones cruzadas, historial de commits atómico y contribución equilibrada. |

---

### Detalle de los Vectores de Evaluación

#### 1. Implementación Técnica y Requisitos (6.0 valores)
* El sistema cumple íntegramente todos los requisitos descritos en el enunciado del tema elegido.
* Ausencia de comportamientos anómalos o dependencias rotas.
* Uso correcto de volúmenes, redes aisladas, variables de entorno y configuraciones adecuadas de seguridad.

#### 2. Informe Técnico y Reproducibilidad (6.0 valores)
* El informe (en formato PDF) debe contar con una estructura clara:
  * **Introducción y Contextualización:** Descripción del problema y del objetivo del proyecto.
  * **Arquitectura de la Solución:** Diagrama conceptual de la arquitectura y justificación de las decisiones técnicas adoptadas.
  * **Instrucciones y Pruebas:** Demostración empírica del funcionamiento (incluyendo capturas de pantalla o salidas de terminal relevantes).
  * **Dificultades y Conclusiones:** Reflexión honesta sobre los obstáculos técnicos superados y las lecciones aprendidas.
* El archivo `README.md` en el repositorio debe ser una guía directa de inicio para que cualquier evaluador pueda clonar el repositorio y poner el proyecto en funcionamiento con un único comando.

#### 3. Uso Crítico y Condicionado de Inteligencia Artificial (4.0 valores)
La Inteligencia Artificial Generativa (ej.: Gemini, ChatGPT, Claude) está permitida como **herramienta de apoyo** al aprendizaje, pero sujeta a reglas estrictas de transparencia, intervención humana y buenas prácticas de ingeniería:
* **Usos Permitidos:** Apoyo en el diseño de arquitecturas, asistencia en la depuración de sintaxis o configuración, mejora de la redacción del informe y lluvia de ideas para escenarios de prueba.
* **Usos Estrictamente Prohibidos:** Generación en régimen *"one-shot"* del proyecto completo o del informe sin comprensión ni validación humana. Queda expresamente prohibida la entrega de código que los miembros del equipo no puedan justificar o explicar detalladamente.
* **Buenas Prácticas de Ingeniería de Contexto y Agentes:**
  Se valorará positivamente la aplicación de las técnicas introducidas en la **Clase 02**:
  * **Archivo `AGENTS.md`:** Creación y mantenimiento de un archivo `AGENTS.md` en la raíz del repositorio, definiendo el contexto del proyecto, directrices de arquitectura, convenciones de código y límites de seguridad para los asistentes de IA.
  * **Definición de *Skills* y Guardrails:** Creación de *skills* modulares o reglas de ejecución segura (patrón *safe-cli*) que condicionen las respuestas de la IA a comandos verificables y sin riesgo para el entorno.
  * **Ingeniería de Prompts Estructurados:** Demostración de prompts iterativos con contexto delimitado, en contraposición a solicitudes vagas o ingenuas.
* **Sección Obligatoria en el Informe ("Declaración de Uso de IA"):**
  El informe debe contener obligatoriamente la declaración institucional estructurada con los siguientes campos:
  * **Herramienta(s) utilizada(s):** Identificación clara de las herramientas y modelos de IA consultados (ej.: Gemini, ChatGPT, Claude, GitHub Copilot).
  * **Tareas apoyadas:** Detalle de las etapas apoyadas (ej.: depuración de sintaxis en el Dockerfile, sugerencia de estructura de pruebas, revisión gramatical).
  * **Verificación Humana:** Confirmación explícita de que todo el código y texto fueron íntegramente revisados, probados y validados manualmente por los estudiantes.
  * **Responsabilidad:** Declaración inequívoca de que los miembros del grupo asumen la responsabilidad íntegra del contenido final y código entregado.
  * **Extractos de Prompts y Reflexión Crítica:** Presentación de extractos de los prompts más relevantes utilizados y fundamentación crítica de por qué **aceptaron, adaptaron o rechazaron** las sugerencias de la IA (ej.: *"la IA sugirió exponer el puerto 3306 de la base de datos, pero lo rechazamos para mantener la base de datos aislada en la red privada de Docker"*).

#### 4. Creatividad y Funcionalidades Adicionales (2.0 valores)
Este vector premia a los grupos que van más allá de los requisitos mínimos y demuestran iniciativa técnica:
* **Ejemplos de valoración:**
  * Implementación de scripts de pruebas automáticas y comprobaciones de estado (*healthchecks*).
  * Mecanismos de seguridad adicionales (ej.: restricción estricta de capacidades Linux, usuarios no-root, cifrado).
  * Mejoras visuales, interfaces más intuitivas o un acabado superior en la experiencia de usuario.
  * Funcionalidades extra relevantes que enriquezcan la utilidad real de la solución.

#### 5. Flujo de Trabajo Colaborativo, Gestión de Tareas y Git (2.0 valores)
La colaboración y la trazabilidad son competencias esenciales en la ingeniería de software:
* **Gestión de Tareas e Issues:** Uso activo de **GitHub Issues** (y opcionalmente GitHub Projects/Kanban) para planificar, asignar y seguir el progreso de las tareas del equipo.
* **Flujo de Trabajo con Ramas y Pull Requests:** El trabajo debe desarrollarse en ramas de funcionalidad (*feature branches*) e integrarse en `main` mediante **Pull Requests** revisados y aprobados por otro miembro del equipo.
* **Trazabilidad y División de Trabajo:** Vinculación de commits y PRs a los issues correspondientes (ej.: `closes #3`), con una distribución visiblemente equilibrada del esfuerzo entre todos los miembros.
* **Higiene del Repositorio:** Mensajes de commit atómicos y descriptivos (ej.: estándar *Conventional Commits*), uso riguroso de `.gitignore` y garantía absoluta de no versionar credenciales, archivos binarios innecesarios o archivos temporales.

## Configuración y Gestión del Repositorio en GitHub

A continuación se detallan las instrucciones para configurar el repositorio privado de su equipo en GitHub.

### 1. Creación del Repositorio (Solo UN miembro del grupo)

Una vez que los docentes confirmen el equipo y asignen el correspondiente **número de grupo**:

1. **Acceder a GitHub:** Iniciar sesión en [github.com](https://github.com) (o crear una cuenta personal gratuita si aún no disponen de una).
2. **Crear Nuevo Repositorio:** Hacer clic en el botón **New** (o en el menú `+` de la esquina superior derecha).
3. **Nombre del Repositorio:** Utilizar obligatoriamente la siguiente convención (en minúsculas):  
   `iei-2026-p1-[turma]-g[grupo]`  
   *(Ejemplo para la clase TP1 y grupo 3: `iei-2026-p1-tp01-g03`)*
4. **Visibilidad:** Seleccionar obligatoriamente la opción **Private** (Privado).
5. **Inicialización:** Pueden marcar la creación de un archivo `README.md` y seleccionar el `.gitignore` adecuado (ej.: Python).
6. **Crear:** Hacer clic en **Create repository**.

-----

### 2. Añadir Colaboradores (Miembros del Equipo y Docentes)

Al ser un repositorio **privado**, es necesario conceder acceso a los demás compañeros del grupo y a los docentes de la asignatura para su seguimiento y evaluación:

1. En el repositorio creado, acceder a la pestaña **Settings** (Configuración).
2. En el menú lateral izquierdo, hacer clic en **Collaborators**.
3. Hacer clic en el botón verde **Add people**.
4. **Añadir a los compañeros de equipo:** Introducir el nombre de usuario de GitHub o correo electrónico de cada compañero y enviar la invitación con permisos de escritura (*Write*).
5. **Añadir a los docentes:** Introducir los nombres de usuario de GitHub de los docentes de la asignatura (indicados en clase y en Moodle) y enviar la invitación.
6. Todos los invitados deben aceptar la invitación recibida por correo electrónico o directamente en la página principal de GitHub.

-----

### 3. Configurar una Clave SSH para el Acceso

Esto les permitirá clonar (`clone`), descargar (`pull`) y subir (`push`) cambios al repositorio desde la línea de comandos sin necesidad de introducir contraseñas o tokens en cada operación.

1. **Comprobar si ya existe una clave SSH:**  
   Abran la terminal y ejecuten el siguiente comando:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Generar una nueva clave (si no existe):**

   * Si visualizan una clave (que comienza por `ssh-ed25519...`), copien la línea completa y pasen al paso 3.
   * Si obtienen un error como "No such file or directory", ejecuten el siguiente comando para generar una clave moderna:
     ```bash
     ssh-keygen -q -t ed25519 -N ''
     ```
   * A continuación, muestren y copien la nueva clave pública:
     ```bash
     cat ~/.ssh/id_ed25519.pub
     ```

3. **Añadir la clave pública a su cuenta de GitHub:**

   * Accedan a la configuración de su cuenta de GitHub (**Settings** en el menú de perfil, esquina superior derecha).
   * En el menú lateral izquierdo, hagan clic en **SSH and GPG keys**.
   * Hagan clic en el botón **New SSH key**.
   * Asignen un **Title** descriptivo (ej.: "Portatil-IEI").
   * Peguen la clave pública copiada en el campo **Key**.
   * Asegúrense de que el campo "Key type" esté configurado como **Authentication Key**.
   * Hagan clic en **Add SSH key**.

-----

## Anexo: Modelo de la Declaración de Uso de IA

*(Este modelo debe cumplimentarse con la identificación de todos los miembros del grupo e integrarse obligatoriamente en el Informe del Proyecto en PDF. La inclusión de los nombres y números de estudiante constituye la asunción formal del compromiso de integridad académica por parte del grupo, no siendo necesaria firma manuscrita ni digital).*

---

### Declaración de Uso de Inteligencia Artificial

* **Clase (*Turma*):** [ej.: TP01] | **Grupo:** [ej.: g03]
* **Miembros del Grupo:**
  * [Nombre Completo del Estudiante 1] (NMec: [Número])
  * [Nombre Completo del Estudiante 2] (NMec: [Número])
  * [Nombre Completo del Estudiante 3] (NMec: [Número])

1. **Herramienta(s) utilizada(s):**  
   [Indicar los sistemas y modelos utilizados, ej.: Gemini 3.5, ChatGPT 4o, Claude 3.5 Sonnet, GitHub Copilot. En caso de no haber utilizado herramientas de IA, indicar explícitamente "Ninguna".]

2. **Tareas apoyadas:**  
   [Detallar dónde se utilizó la IA, ej.: apoyo en la depuración de sintaxis en el Dockerfile, sugerencias de casos de prueba, revisión gramatical del informe.]

3. **Verificación Humana:**  
   El código, las configuraciones y el texto entregados fueron íntegramente probados, revisados y validados manualmente por el grupo, garantizando su fidelidad a los requisitos técnicos y su correcto funcionamiento.

4. **Responsabilidad y Autoría:**  
   Los autores declaran que comprenden y dominan la totalidad de la solución presentada, asumiendo la responsabilidad académica íntegra sobre el código y contenido del informe, y que ninguna parte fue generada en régimen *one-shot* sin verificación.
