---
title: Proyectos 02
subtitle: Introducción a la Ingeniería Informática
author: Luis Moutinho, Joaquim Sousa Pinto
institute: Universidade de Aveiro
date: 24 de Noviembre de 2026
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
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Proyectos

> ### Régimen de Uso de Inteligencia Artificial: IA CONDICIONADA
>
> *En cumplimiento de las directrices institucionales de la Universidade de Aveiro (Referencial para Avaliação das Aprendizagens na Era da Inteligência Artificial):*
>
> * **Desarrollo de Software:** Se permite el uso de sistemas de IA como apoyo técnico para la depuración de errores (*debugging*) o la sugerencia de código repetitivo. La lógica central y la arquitectura de la solución no pueden ser generadas por IA (queda expresamente prohibido el régimen *"one-shot"* para la totalidad del proyecto).
> * **Informe de Proyecto:** Se permite el uso de IA exclusivamente para el apoyo en la revisión lingüística y la mejora de la claridad del texto. La estructura argumentativa, la interpretación de resultados y las conclusiones deben ser fruto del trabajo intelectual y autoral de los estudiantes.
> * **Declaración Obligatoria:** El trabajo debe incluir obligatoriamente en el informe la correspondiente **Declaración de Uso de IA** (ver modelo en el [Anexo](#anexo-modelo-de-declaración-de-uso-de-ia)), acompañada de los extractos de los prompts más relevantes y de la justificación crítica de las sugerencias aceptadas o rechazadas.

Formen grupos de dos o tres estudiantes (excepcionalmente, los proyectos pueden realizarse de forma individual) y seleccionen **uno** de los siguientes proyectos. Todos los proyectos se alojarán en **GitHub**, mediante un repositorio privado creado por cada grupo en una cuenta personal gratuita. Consulten [aquí](#configuración-y-gestión-del-repositorio-en-github) los detalles.

El repositorio debe contener todo el código fuente, scripts relevantes, archivos de configuración (`Dockerfile`, `docker-compose.yml`, etc.), un archivo de licencia *open-source* (`LICENSE`, ej.: MIT) y un `README.md` con instrucciones claras sobre cómo poner el proyecto en marcha.
También debe incluir el **informe del proyecto en formato `PDF`**, **compilado a partir de Markdown (vía Pandoc) o LaTeX**, incluyendo el código fuente correspondiente (`.md`/`.tex`) en el repositorio.

Este es un proyecto de tres semanas (con entrega y **presentación presencial en la última clase del semestre**, en diciembre de 2026). Tienen una semana para notificar a su profesor (por correo electrónico) los miembros de su grupo, la clase y el tema elegido (la lista de temas se encuentra [aquí](#temas)). Tras dicha notificación, los docentes confirmarán el **número de grupo** correspondiente.

No duden en contactar con su profesor ante cualquier duda.
Se podrán añadir instrucciones adicionales.

## Temas

### 1. Servicio Web "Markdown to PDF"
* **Descripción:** Implementar una aplicación web en **Docker Compose** (dos contenedores) que permita editar, previsualizar y convertir documentos Markdown en archivos PDF desde el navegador.
  1. **Backend de Compilación (Python/FastAPI + Pandoc):** Crear un contenedor con Python/FastAPI y **Pandoc** (pudiendo utilizar una imagen base ligera como `pandoc/latex` o Pandoc + `weasyprint` para evitar compilaciones pesadas). La API debe exponer un *endpoint* `POST /api/convert` que reciba un archivo `.md` (o texto Markdown), genere el PDF correspondiente (guardándolo en un **volumen**) y devuelva el archivo para su descarga (o un mensaje de error claro si falla la conversión).
  2. **Frontend Web (HTML5/CSS3/JS en Nginx):** Crear una interfaz web con **editor de texto Markdown y previsualización HTML en tiempo real** (ej.: mediante una biblioteca ligera JS como `marked.js`) y/o carga de archivo `.md`, enviando la petición de conversión vía JavaScript (`fetch`) para descargar el PDF generado.
  3. **Extensiones Opcionales (Creatividad):** Selección de formato de salida (*Informe PDF* vs. *Diapositivas Beamer*), historial de PDFs convertidos o enrutamiento detrás de un **Reverse Proxy Nginx**.
* **Temas Principales:** Docker Compose (multiservicio), APIs REST (FastAPI + CORS), JavaScript asíncrono (`fetch`, manipulación del DOM), compilación de documentos (Markdown, Pandoc y LaTeX), Nginx y `volumes`.

### 2. Dashboard Interactivo de Geo-Datos (Meteorología, Movilidad o Medio Ambiente)
* **Descripción:** Construir un *web dashboard* en **Docker Compose** (dos contenedores) para la visualización de datos georreferenciados en un mapa interactivo (ej.: meteorología, calidad del aire, estaciones de bicicletas o incidencias de tráfico).
  1. **Backend de Datos (Python/FastAPI + Pandas/Polars):** Desarrollar una API que lea un *dataset* real en CSV (con coordenadas `lat`/`lon`, ej.: datos abiertos de `dados.gov.pt`) o consulte una API pública gratuita sin registro complejo (ej.: **Open-Meteo**, con *caché* simple en archivo JSON en un **volumen**). El servicio debe limpiar registros inválidos o valores faltantes y exponer los datos en **JSON** en un *endpoint* REST (ej.: `GET /api/data`), admitiendo al menos un parámetro de filtrado (ej.: categoría o región).
  2. **Frontend Geográfico (HTML5/CSS3/JS + Leaflet en Nginx):** Crear una interfaz web que consuma la API vía `fetch()`, muestre los puntos en un mapa interactivo **Leaflet** (con marcadores y *popups* informativos) y permita filtrar dinámicamente los marcadores visibles en la página.
  3. **Extensiones Opcionales (Creatividad):** Gráfico estadístico complementario (**Matplotlib/Seaborn** o biblioteca JS), agrupación de marcadores o publicación mediante **Reverse Proxy Nginx**.
* **Temas Principales:** Programación Web (HTML5/CSS3/JS, DOM, `fetch`, Leaflet), APIs REST (FastAPI + CORS), limpieza y formateo de datos (CSV/JSON con Pandas/Polars), Nginx y Docker Compose.

### 3. Servicio Web de Análisis y Visualización de CSV (*CSV Data Explorer*)
* **Descripción:** Crear una plataforma web en **Docker Compose** (dos contenedores) que permita cargar cualquier archivo CSV y visualizar automáticamente estadísticas descriptivas y gráficos de sus columnas.
  1. **Backend Analítico (Python/FastAPI + Pandas/Polars + Matplotlib/Seaborn):** Implementar una API con un *endpoint* `POST /api/upload` que reciba un archivo CSV, lo guarde en un **volumen**/directorio temporal, trate valores faltantes y devuelva en JSON el resumen estadístico de las columnas numéricas (`count`, media, mínimo, máximo) y la lista de columnas disponibles. Un segundo *endpoint* (ej.: `GET /api/plot/{columna}`) leerá el CSV guardado y generará la imagen PNG del gráfico correspondiente.
  2. **Frontend Interactivo (HTML5/CSS3/JS en Nginx):** Desarrollar una página web con formulario de carga (`fetch` con `FormData`), tabla dinámica de resumen estadístico generada en el DOM y botones/selectores para abrir y visualizar el gráfico de cada columna sin recargar la página.
  3. **Extensiones Opcionales (Creatividad):** Detección de *outliers* (método **IQR**), matriz de correlación (*heatmap* Seaborn), elección del tipo de gráfico (histograma vs. *boxplot*) o **Reverse Proxy Nginx**.
* **Temas Principales:** Carga de archivos en APIs REST (FastAPI + CORS), análisis de datos (Pandas/Polars), visualización (Matplotlib/Seaborn), manipulación dinámica del DOM (`fetch`), Nginx y Docker Compose.

### 4. Portfolio Dinámico Full-Stack
* **Descripción:** Construir un sitio web de portfolio personal en **Docker Compose** (dos contenedores) que separe totalmente el contenido de la presentación, simulando un *Micro-CMS* moderno con persistencia real.
  1. **Backend REST con Persistencia (Python/FastAPI):** Crear una API que exponga los datos del portfolio en JSON (`GET /api/profile` con nombre, biografía, competencias y lista de proyectos con etiquetas), acepte envíos en **`POST /api/contact`** (validando los campos y guardando los mensajes en un archivo JSON o SQLite en un **volumen** Docker) y proporcione `GET /api/messages` para comprobar los mensajes persistidos durante la demostración.
  2. **Frontend Semántico e Interactivo (HTML5/CSS3/JS en Nginx):** Desarrollar una página en HTML5 semántico y CSS3 (*Box Model*) que cargue dinámicamente los datos de la API vía `fetch()`/`async`/`await`, permita **filtrar proyectos por categoría/etiqueta** en el DOM, incluya alternancia de tema **Dark/Light** (guardada en `localStorage`) y un formulario de contacto con validación *client-side* y confirmación visual de envío.
  3. **Extensiones Opcionales (Creatividad):** Adición/edición dinámica de proyectos vía API, panel visual de mensajes enviados o exposición detrás de un **Reverse Proxy Nginx**.
* **Temas Principales:** JavaScript asíncrono (`fetch`/`async`/`await`, manipulación del DOM, `localStorage`), HTML5 semántico y CSS3, APIs REST con persistencia (FastAPI + CORS), Nginx y Docker Compose.

### 5. Estación de Telemetría en Tiempo Real (MQTT + WebSockets)
* **Descripción:** Desarrollar una arquitectura de telemetría en tiempo real orientada a eventos en **Docker Compose**, integrando recopilación de métricas, protocolo **MQTT** y un *dashboard* web actualizado en directo.
  1. **Broker *Pub/Sub* (Eclipse Mosquitto en Docker):** Configurar el *broker* **Mosquitto** con dos *listeners*: TCP (`1883`) para clientes Python y **WebSockets (`9001`)** para el navegador, utilizando temas jerárquicos claros (ej.: `iei/telemetria/sistema`).
  2. **Agente Publicador (Python + `paho-mqtt` + `psutil`):** Implementar un script (a ejecutar en la máquina anfitriona conectado a `localhost:1883` o en un contenedor dedicado) que recoja periódicamente métricas reales de la máquina (CPU y memoria RAM) — o sensores ambientales simulados — y las publique en **JSON**, incluyendo un mensaje ***Last Will and Testament* (LWT)** para señalar desconexiones abruptas.
  3. **Dashboard Web en Tiempo Real (Nginx + HTML5/CSS3/JS):** Crear una página web que se conecte al *broker* por **WebSockets**, se suscriba a los temas MQTT, actualice valores en el DOM en tiempo real y muestre una alerta visual cuando se supere un umbral (ej.: CPU/RAM $> 80\%$) o cuando llegue un evento LWT.
  4. **Extensiones Opcionales (Creatividad):** Suscriptor Python que guarde histórico en CSV en un volumen y genere gráficos de tendencia con Pandas/Matplotlib.
* **Temas Principales:** *Publish/Subscribe* y MQTT (Mosquitto, temas, QoS, LWT), WebSockets en el navegador, manipulación dinámica del DOM, telemetría (`psutil`), Nginx y Docker Compose.

## Criterios de Evaluación

El proyecto se evaluará en una escala de **0 a 20 puntos**, distribuidos en seis vectores fundamentales:

| Vector de Evaluación | Peso | Puntuación | Descripción Principal |
| :------------------------ | :--------: | :---------: | :---------------------------------------------------- |
| **1. Implementación Técnica y Requisitos** | 30% | 6.0 pts | Cumplimiento riguroso de los requisitos funcionales del tema, arquitectura multiservicio sin errores, buenas prácticas de red/configuración (Nginx, FastAPI, MQTT, Docker). |
| **2. Informe Técnico (Markdown/LaTeX) y Doc.** | 15% | 3.0 pts | Informe conciso en PDF compilado desde Markdown/LaTeX (con fuente en el repo), arquitectura, pruebas/resultados, archivo `LICENSE` y `README.md` reproducible. |
| **3. Presentación y Demostración del Proyecto** | 15% | 3.0 pts | Presentación oral y demostración funcional en vivo en la última clase del semestre; claridad expositiva, gestión del tiempo y dominio técnico individual en las preguntas. |
| **4. Uso Crítico y Transparente de IA** | 20% | 4.0 pts | Ingeniería de contexto (`AGENTS.md`, *skills*), relevancia de los prompts, justificación crítica de aceptación/rechazo y Declaración de IA. |
| **5. Creatividad y Funcionalidades Adicionales** | 10% | 2.0 pts | Innovación más allá del mínimo (ej.: extensiones opcionales sugeridas, Reverse Proxy, pruebas automatizadas, diseño adaptable móvil o pulido UX/UI). |
| **6. Flujo Colaborativo y Gestión de Proyecto** | 10% | 2.0 pts | Uso de GitHub Issues/Tareas, flujo con ramas y Pull Requests con revisiones cruzadas, historial de commits atómico y contribución equilibrada. |

---

### Detalle de los Vectores de Evaluación

#### 1. Implementación Técnica y Requisitos (6.0 puntos)
* El sistema cumple íntegramente los requisitos base descritos en el enunciado del tema elegido.
* Ausencia de errores de ejecución, bloqueos de CORS no tratados o dependencias rotas.
* Uso correcto de Docker Compose, `volumes`, variables de entorno y configuración limpia de los servicios.

#### 2. Informe Técnico (Markdown/LaTeX) y Reproducibilidad (3.0 puntos)
* El informe (en formato **PDF**, **compilado a partir de Markdown con Pandoc o LaTeX**, con los archivos fuente versionados en el repositorio) debe ser **conciso y estructurado (sugerencia: 4 a 6 páginas, sin anexos)**:
  * **Introducción y Contexto:** Descripción del problema, objetivos y tecnologías utilizadas.
  * **Arquitectura de la Solución:** Diagrama conceptual (contenedores, puertos, flujos HTTP/MQTT y volúmenes) y justificación de las decisiones técnicas.
  * **Pruebas y Resultados:** Demostración empírica del funcionamiento (capturas de pantalla, ejemplos de respuestas JSON/gráficos obtenidos).
  * **Dificultades y Conclusiones:** Reflexión honesta sobre obstáculos técnicos superados y lecciones aprendidas.
* El archivo `README.md` en la raíz del repositorio debe permitir a cualquier evaluador clonar el proyecto y ponerlo en marcha con instrucciones directas y reproducibles, acompañado de un archivo `LICENSE`.

#### 3. Presentación y Demostración del Proyecto (3.0 puntos)
* Realizada obligatoriamente en la **última clase del semestre** por todos los miembros del grupo:
  * **Exposición y Soporte Visual:** Presentación clara, objetiva y estructurada del problema, la arquitectura implementada y los principales resultados (con gestión rigurosa del tiempo asignado).
  * **Demostración Funcional en Vivo:** Ejecución práctica de la solución (en contenedores Docker) evidenciando el funcionamiento de los requisitos principales y la respuesta del sistema ante casos de prueba.
  * **Dominio Técnico y Discusión (Preguntas):** Capacidad de cada miembro del grupo para explicar las decisiones arquitectónicas, el código entregado y responder críticamente a las preguntas de los docentes.

#### 4. Uso Crítico y Condicionado de Inteligencia Artificial (4.0 puntos)

La Inteligencia Artificial Generativa (ej.: Gemini, ChatGPT, Claude) se permite como **herramienta de apoyo** al aprendizaje, bajo reglas estrictas de transparencia, intervención humana y buenas prácticas de ingeniería:

* **Usos Permitidos:** Apoyo en el diseño de arquitecturas, ayuda en la depuración de errores de sintaxis o configuración (Nginx, FastAPI, CORS, JS, LaTeX), mejora de redacción en el informe y *brainstorming* para casos de prueba.
* **Usos Estrictamente Prohibidos:** Generación en régimen *"one-shot"* del proyecto completo o del informe sin comprensión ni validación humana. Queda expresamente prohibida la entrega de código que los miembros del equipo no puedan justificar o explicar en detalle.
* **Buenas Prácticas de Ingeniería de Contexto y Agentes:**
  Se valorará positivamente la continuidad y evolución de las técnicas introducidas en la **Clase 02**:
  * **Archivo `AGENTS.md`:** Creación y mantenimiento de un archivo `AGENTS.md` en la raíz del repositorio que defina el contexto del proyecto, convenciones de código, arquitectura y límites de seguridad.
  * **Definición de *Skills* y Guardrails:** Reglas modulares que condicionen las sugerencias de la IA a comandos verificables y seguros.
  * **Ingeniería de Prompts Estructurados:** Demostración de prompts iterativos con contexto delimitado, frente a peticiones vagas o ingenuas.
* **Sección Obligatoria en el Informe ("Declaración de Uso de IA"):**
  El informe debe incluir obligatoriamente la declaración institucional estructurada (ver [Anexo](#anexo-modelo-de-declaración-de-uso-de-ia)), acompañada de los extractos de los prompts más relevantes y de la fundamentación crítica de por qué **aceptaron, adaptaron o rechazaron** las sugerencias de la IA (ej.: *"la IA sugirió configurar `Access-Control-Allow-Origin: *` en FastAPI, pero lo restringimos al origen de nuestro frontend en `localhost:8080`"*).

#### 5. Creatividad y Funcionalidades Adicionales (2.0 puntos)

Este vector premia a los grupos que van más allá de los requisitos mínimos y demuestran autonomía técnica:

* **Ejemplos de valoración:**
  * Implementación de las **extensiones opcionales** indicadas en el tema elegido (ej.: **Reverse Proxy Nginx** unificando `/` y `/api/`, detección de *outliers* IQR, *heatmap* de correlación o historial persistente).
  * Pruebas automatizadas de API (ej.: `pytest` / scripts `curl`) y *healthchecks* en `docker-compose.yml`.
  * Pulido visual superior, accesibilidad (*a11y*) y diseño adaptable para dispositivos móviles.
  * Automatización de la compilación del informe (ej.: `Makefile` o *GitHub Actions* para generar el PDF).

#### 6. Flujo Colaborativo, Gestión de Tareas y Git (2.0 puntos)

* **Gestión de Tareas e Issues:** Uso activo de **GitHub Issues** (y opcionalmente GitHub Projects/Kanban) para planificar, asignar y seguir el progreso del equipo.
* **Flujo con Ramas y Pull Requests:** Desarrollo en *feature branches* e integración en `main` mediante **Pull Requests** revisados y aprobados por otro miembro del equipo.
* **Trazabilidad y Reparto de Trabajo:** Asociación de commits y PRs a los issues correspondientes (ej.: `closes #4`), con contribución equilibrada entre todos los integrantes.
* **Higiene del Repositorio:** Mensajes de commit atómicos y descriptivos (ej.: *Conventional Commits*), `.gitignore` riguroso (sin `node_modules`, `__pycache__`, `.venv`, credenciales ni archivos temporales) y presencia del archivo `LICENSE`.

## Configuración y Gestión del Repositorio en GitHub

Estas son las instrucciones para configurar el repositorio privado de su equipo en GitHub para el Proyecto 02.

### 1. Creación del Repositorio (Solo UN miembro del grupo)

Una vez que los docentes confirmen el equipo y asignen el **número de grupo**:

1. **Acceder a GitHub:** Iniciar sesión en [github.com](https://github.com).
2. **Crear Nuevo Repositorio:** Hacer clic en el botón **New** (o en el menú `+` en la esquina superior derecha).
3. **Nombre del Repositorio:** Utilizar obligatoriamente la siguiente convención (en minúsculas):
   `iei-2026-p2-[clase]-g[grupo]`
   *(Ejemplo para la clase TP1 y grupo 3: `iei-2026-p2-tp01-g03`)*
4. **Visibilidad:** Seleccionar obligatoriamente la opción **Private** (Privado).
5. **Inicialización:** Pueden marcar la creación de `README.md`, seleccionar el `.gitignore` adecuado (ej.: Python) y elegir una licencia *open-source* (`LICENSE`, ej.: MIT License).
6. **Crear:** Hacer clic en **Create repository**.

-----

### 2. Añadir Colaboradores (Miembros del Equipo y Docentes)

Como el repositorio es **privado**, deben conceder acceso al resto de compañeros del grupo y a los docentes de la asignatura para su seguimiento y evaluación:

1. En el repositorio creado, acceder a la pestaña **Settings** (Configuración).
2. En el menú lateral izquierdo, hacer clic en **Collaborators**.
3. Hacer clic en el botón verde **Add people**.
4. **Añadir a los compañeros de equipo:** Introducir el nombre de usuario de GitHub o correo electrónico de cada miembro y enviar la invitación con permisos de escritura (*Write*).
5. **Añadir a los docentes:** Introducir los nombres de usuario de GitHub de los docentes de la asignatura (indicados en clase y en Moodle) y enviar la invitación.
6. Todos los invitados deben aceptar la invitación recibida por correo o directamente en su página de inicio de GitHub.

-----

### 3. Clave SSH para Acceso (Si no se configuró en el Proyecto 01)

Si ya configuraron la clave SSH en su cuenta de GitHub durante el Proyecto 01, pueden pasar directamente a `git clone`. En caso contrario:

1. **Comprobar o generar una clave SSH:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Si el archivo no existe, generen una nueva clave y lean la clave pública generada:
   ```bash
   ssh-keygen -q -t ed25519 -N ''
   cat ~/.ssh/id_ed25519.pub
   ```
2. **Añadir a la cuenta de GitHub:** Vayan a **Settings $\rightarrow$ SSH and GPG keys $\rightarrow$ New SSH key**, asignen un título descriptivo (ej.: `Portatil-IEI`), peguen la clave pública con el tipo **Authentication Key** y pulsen **Add SSH key**.

-----

## Anexo: Modelo de Declaración de Uso de IA

*(Este modelo debe completarse con la identificación de todos los miembros del grupo e integrarse obligatoriamente en el Informe del Proyecto en PDF. La inclusión de los nombres y números mecanográficos constituye la suscripción formal del compromiso de integridad académica por el grupo, sin necesidad de firma manuscrita ni digital).*

---

### Declaración de Uso de Inteligencia Artificial

* **Clase:** [ej.: TP01] | **Grupo:** [ej.: g03]
* **Miembros del Grupo:**
  * [Nombre del Estudiante 1] (NMec: [Número])
  * [Nombre del Estudiante 2] (NMec: [Número])
  * [Nombre del Estudiante 3] (NMec: [Número])

1. **Herramienta(s) utilizada(s):**
   [Indicar los sistemas y modelos utilizados, ej.: Gemini, ChatGPT, Claude, GitHub Copilot. En caso de no haber utilizado herramientas de IA, indicar explícitamente "Ninguna".]

2. **Tareas apoyadas:**
   [Detallar en qué aspectos se utilizó la IA, ej.: apoyo en la depuración de reglas en `nginx.conf`, sugerencias de casos de prueba en la API FastAPI, revisión gramatical del informe.]

3. **Verificación Humana:**
   El código, las configuraciones, los análisis de datos y el texto entregados han sido íntegramente probados, revisados y validados manualmente por el grupo, garantizando su fidelidad a los requisitos técnicos y su correcto funcionamiento.

4. **Responsabilidad y Autoría:**
   Los autores declaran que comprenden y dominan la totalidad de la solución presentada, asumiendo la responsabilidad académica íntegra por el código y contenido del informe, y que ningún componente ha sido generado en régimen *one-shot* sin verificación.
