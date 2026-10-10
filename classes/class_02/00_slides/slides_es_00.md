---
title: 47138 - Introducción a la Ingeniería Informática
subtitle: "Linux II: Gestión de Entornos, Automatización e IA en la Ingeniería de Software"
institute: Universidade de Aveiro
date: September 28, 2026
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
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Parte I: Gestión de Entornos Linux y Automatización

Tópicos abordados en esta primera parte:

  * **Variables de Entorno:**
      * Variables locales vs. globales (`export`) y herencia en subprocesos y scripts.
  * **Inspección y Gestión del Entorno:**
      * Comandos `printenv`, `env` y eliminación con `unset`.
  * **Persistencia y Seguridad:**
      * Configuración en `~/.bashrc`, recarga con `source` y protección con `chmod 600`.
  * **Archivado y Copias de Seguridad:**
      * Empaquetado y compresión de proyectos con la utilidad `tar`.

-----

## De la Sesión Anterior: Las Variables de Entorno del Sistema

En la sesión anterior utilizamos variables de contexto proporcionadas por la *shell*:

  * **`$USER`:** El usuario con sesión activa (`echo $USER`).
  * **`$HOME`:** La ruta absoluta al directorio personal (`echo $HOME`).
  * **`$PATH`:** El catálogo de directorios donde la *shell* busca programas ejecutables (`echo $PATH`).

**¿De dónde surgen estas variables?**

  * No son propiedades mágicas del terminal: son **variables de entorno globales** ya configuradas por el sistema al iniciar la sesión.
  * Al residir en el entorno, cualquier comando o script (`ls`, `python`, `./mi_script.sh`) puede leer su valor.

-----

## Variables en la Shell: Locales vs. Globales

En la *shell*, una variable es una asociación entre un identificador y un valor para almacenamiento y reutilización en tiempo de ejecución.

  * **Variables Locales:**
      * Creadas mediante una asignación simple (`NOMBRE="valor"`).
      * Existen **estrictamente en la ventana/sesión de comandos actual** (privadas).
      * No se transmiten a programas, comandos o scripts instanciados desde esa sesión.

      ```bash
      $ CURSO="LEI"
      ```

  * **Variables de Entorno (Globales):**
      * Creadas o promovidas explícitamente con el comando **`export`**.
      * Quedan registradas en la tabla de entorno del sistema de la sesión activa.
      * Se propagan y comparten con **todos los comandos y scripts** que ejecutamos.

      ```bash
      $ export CURSO="LEI"
      ```

-----

## Herencia de Variables en la Shell: La Frontera del Script

Al ejecutar un script (ej.: `./saludo.sh`), la *shell* inicia un **proceso hijo** independiente:

  * El proceso hijo **no hereda** las variables locales de la *shell* progenitora.
  * El proceso hijo **recibe una copia** de todas las variables promovidas con `export` (globales).

```bash
# Contenido del script 'saludo.sh' (creado con permisos chmod +x):
# echo "Bienvenido al curso: $CURSO"

# 1. Con variable local: el script no tiene acceso al valor
$ CURSO="LEI"
$ ./saludo.sh
Bienvenido al curso:

# 2. Promoviendo la variable con export: el script hereda el valor
$ export CURSO="LEI"
$ ./saludo.sh
Bienvenido al curso: LEI
```

-----

## Inspección y Gestión de Variables de Entorno (Globales)

Los comandos `printenv` y `env` son utilidades externas que **solo consultan variables de entorno globales (exportadas)**; ignoran variables locales de la *shell*:

  * **`printenv [CLAVE]` (Consulta Rápida):** Inspecciona una variable de entorno específica (o lista todas):

    ```bash
    $ printenv USER          # Devuelve el usuario actual
    $ printenv CURSO         # Devuelve "LEI" (si está exportada; vacío si es local)
    ```

  * **`env` (Entorno y Ejecución Controlada):** Muestra todas las variables exportadas o ejecuta comandos con variables temporales:

    ```bash
    $ env                    # Lista todas las variables exportadas activas
    $ env PORT=8080 comando  # Aplica PORT estrictamente durante la ejecución del comando
    ```

  * **`unset` (Eliminar de la Sesión):** Elimina la variable (local o exportada) de la sesión activa:

    ```bash
    $ unset CURSO
    $ printenv CURSO         # No devuelve nada (ya no existe)
    ```

-----

## Persistencia de Entorno: Archivos de Inicialización de la Shell

Al cerrar una sesión de terminal, la memoria volátil se descarta. La persistencia de variables y configuraciones se gestiona mediante archivos de arranque de la *shell*:

  * **Ciclo de Inicialización de la Shell Interactiva:**
      * Al iniciar una nueva sesión, la *shell* procesa el archivo de configuración en `$HOME`:
        * En **Linux (Bash)**: procesa el archivo **`~/.bashrc`**.
        * En **macOS (Zsh)**: procesa el archivo **`~/.zshrc`**.
      * Cualquier definición exportada aquí queda disponible en todas las sesiones interactivas subsiguientes.

  * **Registro de Variables Persistentes:**

    ```bash
    # Registro en el archivo personal (~/.bashrc en Linux o ~/.zshrc en Mac)
    $ echo 'export GEMINI_API_KEY="AIzaSy..."' >> ~/.bashrc  # o ~/.zshrc
    ```

  * **Arquitectura Modular de Configuración:**
      * Por organización y seguridad, las credenciales deben residir en archivos dedicados (ej.: `~/.api_keys`), importados en el archivo de la *shell*:

        ```bash
        [ -f ~/.api_keys ] && source ~/.api_keys
        ```

-----

## Recargar el Entorno con source y Seguridad con chmod 600

  * **El Comando `source`:**
      * Ejecuta las instrucciones del archivo especificado **en el contexto de la *shell* activa**, sin instanciar un nuevo subproceso.
      * Permite actualizar el estado de variables sin necesidad de reiniciar la sesión de terminal.

        ```bash
        $ source ~/.bashrc   # o: source ~/.zshrc
        ```

  * **Seguridad en Entornos Multiusuario:**
      * Los permisos predeterminados (ej.: `644`) autorizan la lectura de archivos a cualquier usuario del sistema.
      * Los archivos con credenciales o claves criptográficas exigen restricción estricta de lectura y escritura únicamente al propietario.

        ```bash
        $ chmod 600 ~/.api_keys
        $ ls -l ~/.api_keys
        -rw------- 1 alumno alumno 52 Sep 28 10:00 /home/alumno/.api_keys
        ```

-----

## Archivado y Compresión de Datos con tar

La utilidad **`tar`** (*Tape Archive*) representa el estándar POSIX para empaquetar árboles de directorios y archivos en un único archivo comprimido:

  * **Creación de un archivo comprimido (`.tar.gz`):**

    ```bash
    $ tar -czvf backup_proyecto.tar.gz ~/IEI/mi_proyecto/
    ```

    * `-c` : Creación de un nuevo archivo (*create*).
    * `-z` : Compresión mediante el algoritmo **gzip**.
    * `-v` : Listado detallado de los archivos procesados (*verbose*).
    * `-f` : Especificación del nombre del archivo de salida (*file*).

  * **Inspección de integridad y contenido sin descomprimir:**

    ```bash
    $ tar -tf backup_proyecto.tar.gz
    ```

  * **Extracción a un directorio de destino específico (`-C`):**

    ```bash
    $ tar -xzvf backup_proyecto.tar.gz -C /tmp/restauracion/
    ```

-----

## Parte II: Inteligencia Artificial en la Ingeniería de Software

Tópicos abordados en esta segunda parte:

  * **Fundamentos y Mecánica de LLMs:**
      * Inferencia estadística, tokens, ventanas de contexto y mitigación de alucinaciones.
  * **Consumo y Gestión de Costes:**
      * Paradigmas de interacción, consumo de APIs vía `curl` y control de costes (*FinOps*).
  * **Ingeniería de Contexto:**
      * Formulación técnica directa, delimitación de contexto y calibración con ejemplos (Few-Shot).
  * **Agentes Autónomos y Seguridad:**
      * Arquitectura con `AGENTS.md`, Skills, protocolo MCP y salvaguardas rígidas (*hard guardrails*).

-----

## La Postura de la Ingeniería Informática frente a la IA

> *"En ingeniería, no tratamos a la inteligencia artificial como un oráculo mágico, sino como un componente computacional con entradas, salidas, costes medibles y modos de fallo."*

\vspace{0.8em}

::::: columns
::: {.column width="70%"}

  * **El Cambio de Paradigma en la Industria:**
      * Los Modelos de Lenguaje de Gran Escala (LLMs) han evolucionado de asistentes de conversación a **piezas estructurales en la automatización y construcción de software**.
  * **La Postura del Ingeniero Informático:**
      * El consumidor común se maravilla pasivamente con el texto generado.
      * El ingeniero necesita **comprender** el motor, **controlar** el determinismo de las respuestas y **validar** críticamente los resultados.

:::
::: {.column width="30%"}

\begin{center}
\includegraphics[width=0.95\linewidth,height=0.48\textheight,keepaspectratio]{ai_engineering_concept.jpg}
\end{center}

:::
:::::

-----

## Cómo Funcionan los LLMs: De la Estadística a las Representaciones Internas

Un **LLM** se fundamenta en la arquitectura **Transformer** y en el cálculo de probabilidad condicional:

  * **Mecanismo Autorregresivo Fundamental:**
      * Entrenado para estimar la distribución de probabilidad del siguiente elemento de texto: $P(w_t \mid w_1, \dots, w_{t-1})$.
  * **Modelos Internos y Semántica:**
      * Predecir con rigor texto humano complejo exige más que memorización superficial: en las capas intermedias de la red emergen **representaciones geométricas de conceptos**, relaciones de causalidad y estructuras lógicas abstractas.
  * **Inferencia de Intención y Deliberación (Post-Entrenamiento y RL):**
      * El alineamiento mediante aprendizaje por refuerzo especializa al modelo para **deducir la meta e intención del usuario**, permitiendo a los modelos contemporáneos deliberar internamente (*reasoning tokens*) antes de responder.

-----

## Falibilidad de los LLMs: El Fenómeno de las Alucinaciones

> A pesar de su sofisticación actual, **los LLMs siguen siendo sistemas probabilísticos** carentes de **verificación factual formal**, manteniendo la propensión a generar respuestas sintácticamente impecables pero falsas (**alucinaciones**).

\vspace{1em}

\begin{center}
\includegraphics[width=0.68\linewidth,height=0.42\textheight,keepaspectratio]{ai_hallucination_pizza_glue.jpg}\\
\vspace{0.2em}
\textit{\tiny Caso real (Google AI Overviews, 2024): ingestión de sátira de Reddit recomendando pegamento no tóxico para fijar el queso a la pizza.}
\end{center}

-----

## Unidad de Procesamiento: Tokens vs. Palabras

Los LLMs no procesan palabras completas ni caracteres aislados:

  * La unidad de procesamiento fundamental es el **Token**.
  * Un token $\Leftrightarrow$ fragmento de texto (subpalabra, signo de puntuación, carácter, etc.).
  * En promedio **100 palabras $\approx 140$ tokens** (en inglés).
    * En español la proporción es ligeramente superior.
  * Descomposición en tokens:
    * `"Terminal"` $\rightarrow$ `["Term", "inal"]` (2 tokens)
    * `"echo 'hola'"` $\rightarrow$ `["echo", " '", "hola", "'"]` (4 tokens)

### Implicaciones:
  1. **Horizonte de Atención:** Volumen total de tokens (instrucciones, historial y respuesta) que el LLM puede correlacionar y mantener en memoria activa en un momento dado.
  2. **Métricas de Consumo:** Utilización de APIs cuantificada y tarifada según el volumen total de tokens procesados.

-----

## Ventana de Contexto e Hiperparámetros

Conceptos y parámetros operativos esenciales asociados a los LLMs:

  * **Ventana de Contexto ($L_{\max}$) vs. Techo de Salida (*Max Output Tokens*):**
      * La ventana total (memoria de trabajo activa) alcanza **1.000.000+ tokens** para lectura/ingestión.
        * La respuesta generada por llamada tiene un techo menor (ej.: **4.096** a **8.192 tokens**).
  * **Higiene de Contexto (*Context Reset*):**
      * **Buena práctica:** Limpiar la ventana de contexto (iniciar nueva sesión o `/clear`) en la transición entre tareas.
      * Las sesiones prolongadas acumulan contexto obsoleto (*context drift*), encarecen cada petición y elevan notablemente el riesgo de alucinaciones.
  * **Temperatura ($\tau$):**
      * **Baja ($\tau = 0.0$ a $0.2$):** Respuestas deterministas y consistentes (**adecuada para código y comandos**).
      * **Alta ($\tau = 0.8$ a $1.2$):** Mayor dispersión estocástica y creatividad (**adecuada para exploración conceptual**).

-----

## Alucinaciones y Validación Crítica en Ingeniería

Riesgos operativos en la generación de instrucciones para la línea de comandos con LLMs:

  * El modelo puede sugerir **parámetros y opciones sintácticas inexistentes** (ej.: `tar -z --exclude-all-errors`).
  * El modelo puede inducir **comandos con efectos destructivos irreversibles** ante ambigüedades en la instrucción (`rm -rf /tmp/..`).
  * El modelo puede alucinar dependencias y librerías inexistentes en el sistema operativo objetivo.
  * **Deriva de Contexto (*Context Drift*):** Mezclar tareas distintas en la misma sesión hace que el modelo se ancle en premisas antiguas y contradictorias.

**La responsabilidad de ejecución y validación técnica recae exclusivamente en el ingeniero.**

-----

## Paradigmas de Interacción con Modelos de IA

\begin{center}
\includegraphics[height=0.68\textheight,keepaspectratio]{ai_interaction_paradigms.jpg}
\end{center}

-----

## Modelos de Consumo: Suscripciones vs. Interfaces de Programación (APIs)

Dos modelos de consumo de LLMs:

  * **Suscripciones de Usuario (Tarifa Plana / Flat-Rate):**
      * Ejemplos: Claude Pro, Copilot, Antigravity, ChatGPT Plus.
      * Coste periódico fijo por credencial de usuario, con soporte para interfaces web, IDEs y herramientas de terminal.
      * Consumo basado en **cuotas temporales**: el agotamiento temporal suspende peticiones adicionales sin generar cargos financieros imprevistos.

  * **APIs de Desarrollador (Pago por Consumo / Pay-as-you-go):**
      * Facturación calculada estrictamente por millón de tokens (entrada y salida), autenticada mediante **Claves de API (*API Keys*)**.
      * Estándar obligatorio para **pipelines de CI/CD**, servicios autónomos y **automatización de sistemas**.
      * **Riesgo Operativo:** No dispone de límites de consumo preestablecidos por defecto; **las iteraciones descontroladas incurren en cobros directos y continuos de costes operativos.**

-----

## Gestión de Costes en APIs y el Efecto Multiplicador de Agentes

El desarrollo de agentes y scripts de automatización exige gobernanza financiera estricta (**FinOps**):

  * **El Efecto Multiplicador en Agentes Autónomos:**
      * En un flujo de deliberación iterativo de 30 pasos, en cada ciclo el agente retransmite **el historial conversacional acumulado y la totalidad de los archivos leídos**.
      * Un repositorio con 50.000 tokens ejecutado en 30 iteraciones suma **1.500.000 tokens de entrada** en una única validación.
  * **Riesgo de Bucles Infinitos (*Infinite Retry Loops*):**
      * Deficiencias en las condiciones de parada en scripts de automatización provocan invocaciones continuas de la API con consumo financiero acelerado.

-----

## Gestión de Costes en APIs: Salvaguardas y Buenas Prácticas

  1. **Límites Rígidos de Gasto (*Hard Spend Limits*):** Configurar un techo financiero estricto en la consola de gestión de la API (suspensión inmediata del servicio al alcanzar el importe).
  2. **Alertas de Facturación (*Budget Alerts*):** Activar siempre como buena práctica de monitorización; no obstante, ser conscientes de su latencia (varias horas), impidiendo frenar consumos descontrolados en tiempo real.
  3. **Control en el Código (*Loop Cap* y `max_output_tokens`):** Imponer límites máximos de iteraciones en scripts (`MAX_RETRIES=5`) y acotar los tokens de respuesta en la petición JSON.
  4. **Protección de Claves de API:** Jamás incrustar claves (*hardcoding*) en archivos de código o scripts guardados en repositorios; utilizar siempre variables de entorno, almacenes de secretos (*vaults*) y controles de acceso rigurosos.
  5. **Uso de Niveles Gratuitos (*Free Tiers*):** Utilizar, por ejemplo, Google AI Studio (Free Tier), que impone cuotas estrictas por minuto (15 RPM) sin requerir tarjeta de crédito, eliminando cualquier pasivo financiero.

-----

## La Interfaz de Línea de Comandos en el Ecosistema de IA

Propiedades técnicas que fundamentan la preferencia por el terminal en la integración de LLMs:

  * **Composabilidad Operativa:** La respuesta generada por un LLM puede redirigirse directamente a archivos, compiladores o scripts mediante tuberías (*pipes*, `|`).
  * **Ejecución Desatendida (*Headless*) y Automatización:** Procesos programados (*cron*) o pipelines de integración continua (CI/CD) se comunican con LLMs sin dependencia de interfaces gráficas.
  * **Interoperabilidad REST:** Mediante la utilidad `curl`, cualquier sistema POSIX puede establecer comunicación con LLMs.

-----

## Integración con APIs vía curl en el Terminal

Consumo directo de modelos generativos desde la línea de comandos mediante peticiones HTTP POST con payload JSON a la moderna **Gemini Interactions API**:

```bash
$ curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.5-flash-lite",
    "input": "Explica en 1 frase el comando: tar -czvf arq.tar.gz dir/"
  }'
```

  * **`-s` :** Modo silencioso (omisión de barras de progreso y descarga).
  * **`-X POST` :** Método HTTP para envío de datos de inferencia.
  * **`-H "x-goog-api-key: $GEMINI_API_KEY"` :** Autenticación segura en cabecera HTTP (evita exponer el secreto en la URL).
  * **`-H "Content-Type: application/json"` :** Especificación del tipo MIME del cuerpo de la petición.
  * **`model` e `input` :** Especificación del modelo (`gemini-3.5-flash-lite`) e instrucción a procesar.

-----

## Formulación de Instrucciones: El Mito de las Personas

Al interactuar con LLMs, ya sea mediante interfaces de chat, herramientas de consola o APIs, surge la pregunta central: *¿cómo formular instrucciones técnicas efectivas?*

### En la Fase Inicial de Difusión de la Tecnología

  * Se popularizó el recurso a roles figurativos: **Actúa como un ingeniero Linux sénior con 30 años de experiencia y responde...**

### Comportamiento en Modelos Contemporáneos

  * En tareas formales de lógica, computación e ingeniería, la asignación de personas no muestra mejoras estadísticas en el rendimiento.
    * Con frecuencia induce respuestas prolijas y preámbulos conversacionales innecesarios.
  * Los modelos de frontera ya poseen conocimiento técnico consolidado; la precisión depende del **contexto suministrado sobre el sistema** y de la **claridad de las restricciones impuestas**.

-----

## Transición: De la Ingeniería de Prompts a la Ingeniería de Contexto

El enfoque operativo ha evolucionado de la redacción empírica a la **Ingeniería de Contexto**:

\vspace{0.8em}
\begin{center}
\begin{tikzpicture}[
    box/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\footnotesize},
    boxemp/.style={draw=black!40, fill=black!5, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\footnotesize},
    arr/.style={-{Latex[length=2.5mm]}, dashed, thick, color=uagreen!80!black}
]
\node[boxemp] (P) {\textbf{Enfoque Empírico}\\\scriptsize(Personas y Trucos Textuales)};
\node[box, right=2.0cm of P] (C) {\textbf{Ingeniería de Contexto}\\\scriptsize(Límites, Restricciones y Datos)};
\draw[arr] (P) -- node[above, font=\scriptsize, text=black!70] {Evolución de la Práctica} (C);
\end{tikzpicture}
\end{center}
\vspace{0.6em}

La parametrización del modelo se fundamenta en principios deterministas:

  1. Especificación formal y directa del objetivo a cumplir.
  2. Suministro delimitado de los datos de entrada (archivos, esquemas y registros).
  3. Estipulación de restricciones negativas inequívocas (operaciones prohibidas).
  4. Definición del formato estructural obligatorio de la respuesta.

-----

## Los Cuatro Pilares de la Ingeniería de Contexto

Ejemplo: Estructuración de peticiones para integración determinista en entornos de terminal (*shell*):

| Componente | Objetivo | Ejemplo Técnico |
| :--- | :--- | :--- |
| **1. Tarea (Task)** | Enunciado directo del objetivo técnico | *"Genera el comando Bash para listar archivos modificados en las últimas 24 horas."* |
| **2. Contexto (Context)** | Entorno de ejecución y datos | *"Entorno Linux POSIX (Ubuntu 24.04), intérprete Bash, ruta /var/log."* |
| **3. Restricciones (Constraints)**| Límites formales de ejecución | *"No utilizar intérpretes externos (awk, python). Utilizar estrictamente la utilidad find."* |
| **4. Formato (Format)** | Estructura sintáctica de la respuesta | *"Devolver exclusivamente el comando en una sola línea, sin bloques markdown ni preámbulos."* |

-----

## Delimitación Estructurada de Contexto

Al transmitir archivos o registros (*logs*) a un modelo, es imperativo separar formalmente **instrucciones** de **datos** utilizando delimitadores inequívocos (ej.: etiquetas XML o bloques de formato):

```markdown
Analiza el registro de errores a continuacion e identifica el servicio afectado.

<error_log>
Sep 28 10:14:02 srv1 nginx[1420]: bind() to 0.0.0.0:80 failed (98: Address already in use)
Sep 28 10:14:02 srv1 systemd[1]: nginx.service: Failed with result 'exit-code'.
</error_log>

Responde en el formato:
Servicio: <nombre>
Causa: <motivo>
```

**La delimitación estructurada clarifica el rol de cada bloque y mitiga el riesgo de que el modelo interprete datos o errores como nuevas instrucciones (*prompt injection*).**

-----

## Calibración mediante Ejemplos: Zero-Shot vs. Few-Shot

A diferencia de la instrucción directa (**Zero-Shot**), el enfoque **Few-Shot** incorpora ejemplos resueltos en el *prompt* para que el modelo deduzca la estructura y campos por analogía (*in-context learning*), prescindiendo de reglas exhaustivas:

```text
Analiza el incidente y devuelve el diagnostico estructurado.

[Ejemplo 1]
Entrada: El disco /dev/sda1 alcanzo 98% de ocupacion en la carpeta /var.
Salida:
  Severidad:  ALTA
  Componente: Almacenamiento (/var)
  Accion:     Purgar logs y archivos temporales

[Ejemplo 2]
Entrada: Tres intentos fallidos de autenticacion SSH para root.
Salida:
  Severidad:  MEDIA
  Componente: Seguridad (SSH)
  Accion:     Inspeccionar logs y bloquear IP de origen

[Nueva Peticion a Procesar]
Entrada: El proceso de backup consumio 95% de CPU durante 40 min.
Salida:
  Severidad:  ALTA                                   <-- [CAMPOS
  Componente: Procesador (Backup)                    <--  GENERADOS
  Accion:     Ajustar prioridad del proceso.         <--  POR LA IA]
```

-----

## Más allá de la Invocación Puntual: Agentes Autónomos

Transición de paradigma: de la **invocación puntual** (pregunta-respuesta estática) a **sistemas autónomos** que operan en bucle cerrado sobre el sistema:

* **Definición Formal de Agente (Ciencias de la Computación e IA):**
    * Una entidad computacional autónoma que **percibe su entorno** mediante sensores, **delibera** en función de objetivos y **actúa sobre el entorno** mediante actuadores en un ciclo continuo (*Perceive $\rightarrow$ Reason $\rightarrow$ Act*).

* **Concreción en Agentes de Ingeniería de Software (Coding Agents):**
    * **Entorno:** El repositorio de código, el sistema de archivos y el terminal / *shell* Linux.
    * **Percepción (Sensores):** Lectura de archivos, inspección de errores de compilación y captura de la salida de comandos (`stdout`/`stderr`).
    * **Razonamiento (Deliberación):** Descomposición de tareas, selección de herramientas y consulta de reglas del proyecto (`AGENTS.md`).
    * **Acción (Actuadores):** Edición de archivos y ejecución de comandos de prueba/compilación en el terminal.
    * **Bucle de Retroalimentación (*Feedback Loop*):** Evaluación de resultados y corrección iterativa hasta alcanzar el objetivo.

-----

## Arquitectura de Control: AGENTS.md, Skills y MCP

El control y extensión de agentes en entornos de ingeniería se sustenta en tres pilares complementarios:

\vspace{0.6em}
\begin{center}
\begin{tikzpicture}[
    agentbox/.style={draw=black!70, fill=black!5, rounded corners=4pt, thick, align=center, inner sep=5pt, font=\small},
    pillar/.style={draw=uagreen!80!black, fill=uagreen!8, rounded corners=3pt, thick, align=center, inner sep=4pt, text width=3.4cm, font=\scriptsize},
    arr/.style={-{Latex[length=2.2mm]}, thick, color=black!70}
]
\node[agentbox] (AGENT) {\textbf{Agente de IA}};
\node[pillar, below=0.7cm of AGENT] (R2) {\textbf{2. Skills}\\\textbf{Playbooks Modulares}\\\textit{\tiny(Conocimiento especializado bajo demanda)}};
\node[pillar, left=0.35cm of R2] (R1) {\textbf{1. AGENTS.md}\\\textbf{Constitución y Reglas}\\\textit{\tiny(Contexto permanente del repositorio)}};
\node[pillar, right=0.35cm of R2] (R3) {\textbf{3. Protocolo MCP}\\\textbf{Conectores de Herramientas}\\\textit{\tiny(Estandarización de herramientas y accesos)}};

\draw[arr] (AGENT.south) -- (R1.north);
\draw[arr] (AGENT.south) -- (R2.north);
\draw[arr] (AGENT.south) -- (R3.north);
\end{tikzpicture}
\end{center}
\vspace{0.4em}

-----

## Especificación del Repositorio: El Archivo AGENTS.md

### Concepto y Propósito:

  * Archivo en formato Markdown ubicado en la raíz del repositorio de código o en subcarpetas específicas a las que el agente tenga acceso.
  * Constituye el documento de referencia y alineación normativa para asistentes y agentes autónomos que operan sobre la base de código.
  * Entornos de desarrollo y agentes autónomos (Antigravity, Cursor, Claude Code, Copilot) cargan este contexto antes de generar código o ejecutar tareas.
  * **Ámbito Jerárquico:** Puede definirse globalmente en la raíz del proyecto o especializarse por subdirectorios (ej.: `frontend/AGENTS.md`, `backend/AGENTS.md`).

-----

## Especificación del Repositorio: El Archivo AGENTS.md

### Objetivos Operativos:
  * Elimina la introducción imprevista de tecnologías y dependencias no contempladas en el proyecto.
  * Garantiza la conformidad con los patrones arquitectónicos, estilo de código y gestión de errores acordados por el equipo.
  * Define directrices operativas explícitas (prohibición de comandos destructivos y obligatoriedad de validación mediante pruebas).

-----

## Estructura Típica de un Archivo AGENTS.md

Ejemplo de especificación normativa para un proyecto académico:

```markdown
# Directrices del Proyecto IEI - Laboratorio

## 1. Stack Tecnológica y Entorno
- Sistema Operativo: Linux POSIX (Ubuntu 24.04 / WSL 2).
- Shell: Bash 5.x. Los scripts deben comenzar con `#!/bin/bash`.

## 2. Comandos Estándar de Ejecución
- Pruebas: ejecutar `make test` antes de enviar cambios.
- Compilación: ejecutar `make all`.

## 3. Reglas de Código y Seguridad
- Jamás usar contraseñas o claves de API hardcoded.
- No utilizar librerías externas sin autorización previa.
- Las variables locales en scripts deben usar nombres descriptivos en minúsculas.
```

-----

## Estandarización de AGENTS.md en Proyectos de Software

::::: columns
::: {.column width="60%"}

  * **Comandos de Proyecto (Obligatorio):**
    * Comandos para *build*, *lint*, ejecución y pruebas unitarias.
  * **Estructura de Código (Obligatorio):**
    * Mapa del directorio (`src/api`, `src/core`, `tests/`) para evitar la navegación a ciegas del agente.
  * **Convenciones y Estilo (Recomendado):**
    * Tipado estricto, *docstrings* y patrones de confirmación (*Conventional Commits*).
  * **Fronteras y Restricciones (*Boundaries*):**
    * Archivos y carpetas que el agente tiene **estrictamente prohibido** modificar (ej.: migraciones, secretos).

\vspace{0.3em}
\textit{\tiny Referencia: Addy Osmani, \href{https://addyosmani.com/agents/15-agents-md/}{addyosmani.com/agents/15-agents-md/}}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.74\textheight,keepaspectratio]{agents_md_template_generator.png}
\end{center}

:::
:::::

-----

## Caso de Estudio: AGENTS.md en un Proyecto Real de Producción

Especificación completa para un servicio backend (FastAPI, PostgreSQL y Poetry):

\vspace{0.2em}

::::: columns
::: {.column width="52%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{example_agents_md_part1.png}
\end{center}

:::
::: {.column width="48%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.45\textheight,keepaspectratio]{examples_agents_md_part2.png}
\end{center}

\vspace{0.2em}
\textit{\tiny Fuente: Addy Osmani, \href{https://addyosmani.com/agents/15-agents-md/}{addyosmani.com/agents/15-agents-md/}}

:::
:::::

-----

## Impacto del Contexto en el Comportamiento del Agente

Comparación ante la misma solicitud técnica: *"Genera el script de copia de seguridad del proyecto."*

### Sin `AGENTS.md` (Inferencia no anclada en el repositorio):

```python
# El modelo introduce Python y dependencias externas de cloud
import boto3
s3 = boto3.client('s3')
s3.upload_file('backup.zip', 'mi-bucket', 'backup.zip')
```
*(Incompatible con las restricciones de un proyecto enfocado estrictamente en herramientas Bash nativas)*

### Con `AGENTS.md` (Conformidad con el contrato operativo del proyecto):

```bash
#!/bin/bash
set -euo pipefail
tar -czvf "backup_$(date +%Y%m%d).tar.gz" .
echo "Copia de seguridad generada con exito."
```
*(Total conformidad con el entorno y las convenciones fijadas en el repositorio)*

-----

## Seguridad Rigurosa: Soft vs. Hard Guardrails

Principio fundamental de seguridad en inteligencia artificial:

> **"Los prompts en lenguaje natural no constituyen barreras de seguridad."**

La especificación de prohibiciones en `AGENTS.md` (ej.: *"Nunca ejecutes `rm -rf`"*) representa una **Soft Boundary**:

  * El modelo opera mediante cooperación estadística, pudiendo ser eludido mediante **Prompt Injection** (instrucciones maliciosas embebidas en archivos procesados) o alucinación.

-----

## Seguridad Rigurosa: Soft vs. Hard Guardrails

### Barreras Rígidas de Seguridad (Hard Boundaries Deterministas)
La integridad del sistema exige mecanismos de control deterministas externos al modelo:

  * **Interceptores de Herramientas (*Tool Interceptors / Allowlist*):**
      * Módulos de software que analizan los comandos antes de transmitirlos al sistema operativo, bloqueando patrones no autorizados.
  * **Humano en el Bucle (*Human-in-the-Loop* - HITL):**
      * Obligatoriedad de confirmación manual explícita para cualquier acción susceptible de provocar efectos irreversibles.
  * **Aislamiento en Sandbox (Contenedores Docker):**
      * Ejecución en entornos efímeros sin privilegios administrativos y con los sistemas de archivos del anfitrión montados en modo solo lectura (*read-only*).

-----

## Skills: Procedimientos Modulares bajo Demanda

Mientras que `AGENTS.md` establece la especificación global del repositorio, una **Skill** define el procedimiento técnico detallado para una tarea específica.

  * **Criterio de Eficiencia de Contexto:**
      * La inclusión exhaustiva de todos los procedimientos técnicos en `AGENTS.md` saturaría innecesariamente la ventana de contexto.
  * **Principio Operativo:**
      * Una skill se estructura en un directorio dedicado con un archivo descriptor `SKILL.md`, consumido por el agente estrictamente ante una necesidad funcional.
      * Ejemplos: *Skill de Auditoría de Seguridad de Comandos*, *Skill de Migración de Esquemas SQL*, *Skill de Validación de Accesibilidad*.

-----

## Implementación de una Skill: safe-cli

```markdown
---
name: safe-cli
description: Evalua la seguridad y el nivel de riesgo de comandos UNIX (Linux y macOS).
---

# Procedimiento de Analisis:
Al recibir un comando para validacion:
1. Clasifica el riesgo: [SEGURO], [ATENCION] o [PELIGROSO].
2. Sintetiza el objetivo del comando en una frase tecnica.
3. Descompone las opciones y argumentos utilizados.
4. Ante operaciones potencialmente destructivas (rm, dd, chmod 777, redireccionamiento >),
   advierte sobre el impacto potencial y propone una alternativa segura.
```

-----

## Model Context Protocol (MCP): Arquitectura de Conectividad

  * **Limitación Histórica:** Cada herramienta desarrollaba conectores propietarios *ad-hoc* para interactuar con bases de datos, repositorios Git o sistemas de archivos.
  * **Arquitectura Cliente-Servidor:**
      * **Servidor MCP:** expone herramientas, recursos y contexto operativo de forma controlada.
      * **Cliente MCP (IDE/Agente):** intermedia entre el modelo y los recursos externos.

\vspace{0.3em}
\begin{center}
\begin{tikzpicture}[
    clientbox/.style={draw=black!70, fill=black!5, rounded corners=4pt, thick, align=center, inner sep=5pt, font=\footnotesize},
    serverbox/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=3pt, text width=3.2cm, font=\scriptsize},
    arr/.style={{Latex[length=2mm]}-{Latex[length=2mm]}, thick, color=uagreen!80!black}
]
\node[clientbox] (IDE) {\textbf{Agente / IDE}\\\scriptsize(Cliente MCP)};
\node[serverbox, right=2.6cm of IDE.center, yshift=1.05cm] (S1) {\textbf{Servidor Git}\\\tiny(commits, ramas, diffs)};
\node[serverbox, right=2.6cm of IDE.center] (S2) {\textbf{Servidor Base de Datos}\\\tiny(consultas SQL, esquemas)};
\node[serverbox, right=2.6cm of IDE.center, yshift=-1.05cm] (S3) {\textbf{Servidor Sistema Archivos}\\\tiny(lectura y escritura de archivos)};

\draw[arr] (IDE.east) -- node[above, sloped, font=\tiny, text=black!70] {Protocolo MCP} (S1.west);
\draw[arr] (IDE.east) -- node[above, font=\tiny, text=black!70] {Protocolo MCP} (S2.west);
\draw[arr] (IDE.east) -- node[below, sloped, font=\tiny, text=black!70] {Protocolo MCP} (S3.west);
\end{tikzpicture}
\end{center}
\vspace{0.2em}

Con MCP, el acceso a recursos externos se realiza bajo permisos explícitos y canales estandarizados.

-----

## MCP en la Práctica: Implementación y Registro de Herramientas

Ejemplo de conectividad local entre procesos vía canales estándar (\texttt{stdio}):

::::: columns
::: {.column width="50%"}

### 1. Servidor MCP (`servidor_git.py`) - expone función:
```python
# SDK para implementar MCP
from mcp.server.fastmcp import FastMCP
import subprocess

# Nombre del servidor MCP
mcp = FastMCP("git-tools")

# Registra la herramienta para el LLM
@mcp.tool()
def git_status() -> str:
    # Descripcion para que el LLM comprenda la funcion
    """Devuelve archivos modificados."""
    return subprocess.check_output(
        # Comando a ejecutar en el sistema operativo
        ["git", "status", "-s"], text=True
    )

if __name__ == "__main__":
    # Inicia el servidor con comunicacion via stdio (JSON-RPC)
    mcp.run()
```

:::
::: {.column width="50%"}

### 2. Registro en el Cliente (IDE / Agente) (`mcp_config.json`):
```json
{
  "mcpServers": {
    "git-tools": {
      "command": "python",
      "args": ["servidor_git.py"]
    }
  }
}
```

:::
:::::

-----

## Referencias y Recursos Técnicos

Documentación de apoyo y normas técnicas para consulta:

  * **Google AI Studio (Acceso y Gestión de Claves de API):**
      * [https://aistudio.google.com/](https://aistudio.google.com/)
  * **Documentación Oficial de la API Google Gemini:**
      * [https://ai.google.dev/docs](https://ai.google.dev/docs)
  * **Especificación del Model Context Protocol (MCP):**
      * [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
  * **Directrices de Context Engineering & Prompts (Anthropic):**
      * [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
  * **Addy Osmani — Building Effective Agents with AGENTS.md:**
      * [https://addyosmani.com/agents/15-agents-md/](https://addyosmani.com/agents/15-agents-md/)
