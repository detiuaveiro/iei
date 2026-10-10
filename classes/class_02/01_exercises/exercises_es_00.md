---
title: "Linux II: Gestión de Entornos, Automatización e IA en la Ingeniería de Software"
subtitle: Introducción a la Ingeniería Informática
institute: Universidade de Aveiro
date: September 28, 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guía Práctica de Laboratorio

Esta guía fue diseñada para una sesión de **3 horas** y se divide en dos partes fundamentales y una sección de extensión autónoma:

* **Parte I — Gestión de Entornos y Copias de Seguridad (Ejercicios 1 y 2):** Consolidación de variables de sistema, fronteras de procesos y empaquetado con `tar`.
* **Parte II — Ingeniería de IA, Contexto y Agentes en la CLI (Ejercicios 3 a 8):** Llamadas a APIs en la línea de comandos, buenas prácticas de seguridad de secretos, Ingeniería de Contexto, creación de archivos `AGENTS.md`, diseño de una *Skill* modular (`safe-cli`), automatización con el asistente `ask_ai.sh` y desafío integrador de diagnóstico de errores (`ai_fix.sh`).
* **Ejercicios Opcionales de Extensión (Ejercicios 9 a 11):** Automatización avanzada de copias con marca temporal dinámica (`backup_auto.sh`), puente preparatorio para Git con generador inteligente de *Conventional Commits* (`skills/git-commit`) y personalización de inicio de la *shell* con panel de bienvenida y atajos globales (`welcome.sh` en `~/.bashrc` / `~/.zshrc`).

\vspace{1em}

> **Consejos de Supervivencia en el Terminal:**
>
> * **Autocompletado con `<Tab>`:** Escriba las primeras letras de una ruta o comando y pulse `<Tab>`. Si pulsa dos veces, el terminal listará todas las opciones disponibles.
> * **Historial con las flechas `↑` y `↓`:** Nunca vuelva a escribir un comando largo por un pequeño error tipográfico; use la flecha arriba para recuperar y editar comandos anteriores.
> * **Cancelar con `Ctrl + C`:** Si un comando o petición de red se bloquea, pulse `Ctrl + C` para interrumpirlo inmediatamente y regresar a la línea de comandos del terminal.
> * **Comillas en Variables:** Al expandir variables en comandos (ej.: `echo "$MI_VAR"`), use siempre comillas dobles para evitar problemas con espacios o caracteres especiales.

\newpage

# Parte I: Gestión de Entornos y Copias de Seguridad

## Ejercicio 1: Variables de Entorno, Subprocesos y Secretos

En este ejercicio explorará la diferencia entre variables locales de la *shell* y variables exportadas al entorno global, comprendiendo cómo los subprocesos heredan datos y cómo proteger credenciales en el desarrollo de software.

1. **Crear el Directorio de la Clase:**
   Cree una carpeta de trabajo para la sesión de hoy dentro de su directorio personal:
   ```bash
   $ mkdir -p ~/IEI/clase02
   $ cd ~/IEI/clase02
   ```

2. **Crear una Variable Local:**
   Defina una variable simple en su sesión interactiva:
   ```bash
   $ CURSO="LEI_UA"
   $ echo "Mi curso es: $CURSO"
   ```
   *(Pruebe a ejecutar `printenv CURSO`: confirme que no devuelve nada, ya que `printenv` solo consulta variables de entorno).*

3. **Comprobar la Frontera de Procesos con un Script:**
   Cree un script simple para verificar si otros programas pueden acceder a su variable:
   ```bash
   $ echo 'echo "Dentro del script el curso es: $CURSO"' > probar_curso.sh
   $ chmod +x probar_curso.sh
   $ ./probar_curso.sh
   ```
   *¿Qué ocurrió?* El script imprimió `Dentro del script el curso es: ` (vacío). El script se ejecuta como un programa independiente (proceso hijo) y **no tiene acceso** a las variables locales de su ventana.

4. **Promover la Variable con `export`:**
   Promueva la variable al entorno global del sistema y vuelva a ejecutar el script:
   ```bash
   $ export CURSO="LEI_UA"
   $ ./probar_curso.sh
   ```
   *Resultado:* El script ahora puede leer `LEI_UA`, porque los programas y scripts que ejecutamos heredan una copia de todas las variables exportadas.

5. **Inspeccionar y Limpiar el Entorno:**
   Utilidades como `printenv` y `env` consultan exclusivamente variables promovidas con `export`:
   ```bash
   $ printenv CURSO
   $ env | grep CURSO
   ```
   *(Ambos devuelven `CURSO=LEI_UA`).*

   A continuación, elimine la variable de la memoria de la sesión con `unset` y confirme que ya no existe:
   ```bash
   $ unset CURSO
   $ printenv CURSO
   ```

6. **Persistencia de Entorno (`~/.bashrc` / `~/.zshrc`) y Seguridad con `chmod 600`:**
   Si cierra el terminal o reinicia el equipo, todas las variables exportadas en la sesión desaparecerán. Para hacer permanentes las configuraciones y claves entre sesiones de forma modular y segura:

   * **Identificar su Shell activa:**
     Compruebe cuál es el intérprete predeterminado en su terminal:
     ```bash
     $ echo "$SHELL"
     ```
     * En **Linux (Ubuntu/Debian)**: el estándar es Bash (`/bin/bash`), que utiliza el archivo de inicialización **`~/.bashrc`**.
     * En **macOS**: el estándar es Zsh (`/bin/zsh`), que utiliza el archivo de inicialización **`~/.zshrc`**.

   * **Crear un archivo personal de credenciales (`~/.api_keys`):**
     En su carpeta personal, cree un archivo dedicado para claves y variables persistentes:
     ```bash
     $ echo 'export IEI_PERSISTENTE="Hola_IEI"' > ~/.api_keys
     ```

   * **Proteger contra otros usuarios con `chmod 600`:**
     En sistemas multiusuario (como servidores compartidos y puestos de laboratorio), otros usuarios podrían inspeccionar su archivo si los permisos fueran permisivos (`644`). Aplique el principio de mínimo privilegio restringiendo la lectura y escritura exclusivamente a su usuario:
     ```bash
     $ chmod 600 ~/.api_keys
     $ ls -l ~/.api_keys
     ```
     *(Confirme que el permiso sea `-rw-------`: únicamente el propietario puede acceder).*

   * **Configurar la carga automática en el archivo de su Shell:**
     Añada la instrucción de importación al archivo correspondiente a su sistema operativo:

     * *En Linux (Bash):*
       ```bash
       $ echo '[ -f ~/.api_keys ] && source ~/.api_keys' >> ~/.bashrc
       $ source ~/.bashrc
       ```

     * *En macOS (Zsh):*
       ```bash
       $ echo '[ -f ~/.api_keys ] && source ~/.api_keys' >> ~/.zshrc
       $ source ~/.zshrc
       ```

   * **Confirmar la persistencia en la sesión actual:**
     ```bash
     $ echo "$IEI_PERSISTENTE"
     ```
     *(El terminal imprime `Hola_IEI`, confirmando que la variable se cargó en esta ventana).*

   * **La Prueba Definitiva (Abrir un Nuevo Terminal):**
     Para comprobar que la configuración es verdaderamente permanente e independiente de esta ventana:
     1. Abra una **nueva ventana o pestaña de terminal**.
     2. En el nuevo terminal, sin ejecutar ningún comando previo de carga, pruebe:
        ```bash
        $ echo "$IEI_PERSISTENTE"
        ```
     3. Confirme que el valor `Hola_IEI` se imprime inmediatamente, demostrando que la *shell* cargó automáticamente sus credenciales durante el ciclo de arranque.
     4. Cierre esta nueva ventana de prueba (ejecutando `exit` o cerrando la pestaña) y **regrese al terminal original** para continuar con los ejercicios.

-----

## Ejercicio 2: Copias de Seguridad y Paquetes con `tar`

La utilidad `tar` (*Tape Archive*) es el mecanismo fundamental en el mundo Linux para empaquetar directorios enteros y crear copias de seguridad comprimidas.

1. **Preparar Archivos de Prueba:**
   Dentro de la carpeta `~/IEI/clase02`, cree un directorio de simulación de proyecto con algunos archivos de prueba:
   ```bash
   $ mkdir -p ~/IEI/clase02/proyecto_ejemplo
   $ echo "# Proyecto Ejemplo IEI" > ~/IEI/clase02/proyecto_ejemplo/README.md
   $ echo "echo 'Hola Mundo'" > ~/IEI/clase02/proyecto_ejemplo/app.sh
   $ chmod +x ~/IEI/clase02/proyecto_ejemplo/app.sh
   $ date > ~/IEI/clase02/proyecto_ejemplo/timestamp.txt
   ```

2. **Crear un Archivo Comprimido (`.tar.gz`):**
   Estando en la carpeta `~/IEI/clase02`, empaquete la carpeta `proyecto_ejemplo` en un único archivo comprimido con las opciones clásicas `-czvf`:
   ```bash
   $ tar -czvf backup_proyecto.tar.gz proyecto_ejemplo
   ```
   *Comprender las 4 opciones fundamentales:*
   * `-c` : **Create** — Crea un nuevo archivo de empaquetado.
   * `-z` : **Zip (gzip)** — Comprime los datos para reducir notablemente el espacio ocupado.
   * `-v` : **Verbose** — Muestra en pantalla la lista de archivos a medida que se procesan.
   * `-f` : **File** — Especifica el nombre del archivo de salida (`backup_proyecto.tar.gz`). Debe ser siempre la última opción antes del nombre del archivo.

3. **Inspeccionar el Archivo:**
   Compruebe el tamaño y liste el contenido empaquetado sin descomprimir:
   ```bash
   $ ls -lh backup_proyecto.tar.gz
   $ tar -tf backup_proyecto.tar.gz
   ```
   *(La opción `-t` lista el índice de archivos contenidos en el paquete).*

4. **Simular la Restauración en otra Carpeta con `-C`:**
   Por defecto, `tar` extrae los archivos exactamente en el directorio donde nos encontramos. Para extraer en un destino diferente sin tener que cambiar de carpeta con `cd`, usamos la opción **`-C`** (*Change directory*):
   ```bash
   $ mkdir -p /tmp/restauracion_iei
   $ tar -xzvf backup_proyecto.tar.gz -C /tmp/restauracion_iei/
   $ ls -la /tmp/restauracion_iei/proyecto_ejemplo/
   ```
   * *El papel de `-C`:* Indica a `tar` que cambie temporalmente al directorio `/tmp/restauracion_iei` y descomprima allí, manteniendo limpio su directorio de trabajo.
   * Confirme que el archivo `app.sh` preservó su permiso de ejecución (`x`).

5. **Limpieza:**
   Elimine la carpeta de prueba temporal:
   ```bash
   $ rm -rf /tmp/restauracion_iei
   ```

\newpage

# Parte II: Ingeniería de IA, Contexto y Agentes en la CLI

## Ejercicio 3: La Primera Llamada a la LLM vía `curl`

En este ejercicio se comunicará directamente con un modelo de lenguaje de última generación a través del terminal, consumiendo una API REST con la utilidad `curl`.

> **Prerrequisito del Sistema (`python3`):**
> La manipulación de datos JSON en la línea de comandos se realiza con la
> utilidad `python3` y su módulo nativo `json` (sin necesidad de
> instalar bibliotecas de terceros).
>
> * **Verificar si está instalado:** `$ python3 --version`
> * **Linux (Ubuntu/Debian — si no estuviera instalado):**
>   `$ sudo apt update && sudo apt install -y python3`
> * **macOS (si no estuviera instalado):**
>   `$ xcode-select --install`

1. **Obtener la Clave de API Gratuita en Google AI Studio:**
   * Abra el navegador y acceda a **Google AI Studio**: [https://aistudio.google.com/](https://aistudio.google.com/).
   * Inicie sesión con su cuenta personal de Google (**Gmail**). Si es su primer acceso, acepte los términos del servicio.
   * En la **barra lateral izquierda**, haga clic en **"Dashboard"** y a continuación seleccione **"API Keys"**.
   * En la esquina superior derecha de la página, haga clic en el botón azul **"Create key"** (o *"Create API key"*).
   * En la ventana emergente:
     * En **"Name your key"**, introduzca un nombre descriptivo (ej.: `iei-clase02`).
     * En **"Choose an imported project"**, seleccione **"Default Gemini Project"** (o la opción predeterminada disponible).
     * Confirme haciendo clic en **"Create"**.
   * En la pantalla de detalles (**"API key details"**):
     * Haga clic en el botón **"Copy key"** (en la esquina inferior derecha) para copiar la clave generada al portapapeles.
     * *(Observe también el botón **"Copy cURL quickstart"**: la propia Google proporciona un comando `curl` de prueba rápida prediseñado, demostrando cómo `curl` es la herramienta de referencia en la industria para interactuar directamente con APIs de IA desde el terminal).*

   > **!!! Costes de APIs vs. Suscripciones de Cuenta**
   > A diferencia de las suscripciones personales de usuario (como ChatGPT Plus, Claude Pro, GitHub Copilot o Google Antigravity, que cobran una tarifa mensual fija predecible con cuotas temporales de peticiones), las APIs de desarrollador operan en un modelo métrico de pago por consumo (*pay-as-you-go*) por cada millón de tokens. En agentes y herramientas que operan en bucles (*loops*), la totalidad del historial y de los archivos del repositorio se retransmite en cada iteración, provocando cargos financieros imprevistos y elevados si un script entra en un bucle continuo (*infinite retry loop*).
   > En el ámbito profesional, resulta imprescindible configurar **Hard Spend Limits** (techos de gasto estrictos) en la consola de Cloud. Tenga en cuenta que las **Alertas de Facturación (*Budget Alerts*)** a menudo sufren un retraso de cálculo de varias horas, por lo que el presupuesto fijado puede superarse con creces antes de emitirse el aviso. En nuestro laboratorio utilizamos el Free Tier de Google AI Studio, que opera con limitación de tasa (15 RPM) y sin vinculación de medios de pago, garantizando la total ausencia de riesgo financiero.

2. **Configurar la Clave en la Variable de Entorno:**
   En su terminal, exporte la clave a la variable de entorno `GEMINI_API_KEY`:
   ```bash
   $ export GEMINI_API_KEY="PEGUE_AQUI_SU_CLAVE"
   ```
   *Verifique que la variable fue guardada sin revelar la clave completa:*
   ```bash
   $ echo "Clave configurada: ${GEMINI_API_KEY:0:8}..."
   ```
   *(Consejo: para no tener que exportar la clave en cada nueva ventana de terminal, guárdela en su archivo protegido: `echo 'export GEMINI_API_KEY="PEGUE_AQUI_SU_CLAVE"' >> ~/.api_keys`).*

3. **Realizar la Petición HTTP POST con `curl`:**
   Google ofrece la moderna **Interactions API** (`/v1beta/interactions`) para una comunicación unificada con modelos Gemini:
   ```bash
   $ BASE="https://generativelanguage.googleapis.com"
   $ API_URL="${BASE}/v1beta/interactions"
   $ MODEL="gemini-3.5-flash-lite"

   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Explica en 1 frase el comando tar -czvf.\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }"
   ```
   *(Nota de latencia: el parámetro `"thinking_level": "low"` reduce el razonamiento interno a lo esencial, garantizando respuestas rápidas en ~2 segundos).*

4. **Analizar la Respuesta:**
   Observe la respuesta devuelta en el terminal. Fíjese en la estructura JSON devuelta por el servicio, que contiene el estado (`status: "completed"`), métricas de uso (`usage`) y la lista `steps` con los bloques de texto generados (`"type": "model_output"`).

   > [!WARNING]
   > **Aviso de Sobrecarga Temporal (`service_unavailable` / 503):**
   > Si la respuesta contiene un aviso del servidor como:
   > ```json
   > {
   >   "error": {
   >     "message": "... is currently experiencing high demand ...",
   >     "code": "service_unavailable"
   >   }
   > }
   > ```
   > **¡No se trata de un error de sintaxis ni de su clave!** En el nivel gratuito de Google (*Free Tier*), picos puntuales de peticiones globales provocan temporalmente este aviso.
   > - **Solución rápida:** Espere de 5 a 10 segundos y repita el comando.
   > - **Alternativa mediante `$MODEL`:** Si la sobrecarga persiste, cambie de modelo en la *shell* sin modificar ningún comando ni script:
   >   ```bash
   >   $ export MODEL="gemini-3.8-flash-lite"
   >   ```
   >   *(Y vuelva a ejecutar la llamada `curl` con el nuevo `$MODEL`).*

5. **La Utilidad de Extracción (`get_text.py`):**
   Dado que la API devuelve un documento JSON estructurado con metadatos técnicos, y en los ejercicios siguientes querremos evaluar directamente los comandos y textos generados (con saltos de línea reales), usamos el script auxiliar **`get_text.py`** disponible en el repositorio.
   También puede crearlo directamente en su carpeta de trabajo (`~/IEI/clase02/`):
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/get_text.py
   #!/usr/bin/env python3
   import json, sys

   try:
       d = json.load(sys.stdin)
       t = "".join(c.get("text", "") for s in d.get("steps", [])
                   if s.get("type") == "model_output"
                   for c in s.get("content", []) if c.get("type") == "text")
       if not t and "outputs" in d:
           t = "".join(o.get("text", "") for o in d["outputs"]
                       if o.get("type") == "text")
       if t:
           print(f"\n{t.strip()}\n")
       else:
           print(f"\n{d}\n")
   except Exception as e:
       print("Error al procesar JSON:", e)
   EOF
   $ chmod +x ~/IEI/clase02/get_text.py
   ```
   *Pruebe la extracción canalizando la respuesta de `curl`:*
   ```bash
   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Explica en 1 frase el comando tar -czvf.\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }" | ./get_text.py
   ```

-----

## Ejercicio 4: Ingeniería de Contexto en la CLI (De lo Vago a lo Estricto)

Los modelos de lenguaje modernos no necesitan personajes teatrales ("*Actúa como un ingeniero...*"). Necesitan **tareas explícitas, delimitación de contexto y restricciones estrictas**.

1. **El Problema del Prompt Vago:**
   Ejecute una consulta con una formulación genérica y vaga:
   ```bash
   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"¿Como ver archivos modificados en 24h en Linux?\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }" | ./get_text.py
   ```
   *Reflexión:* La respuesta devuelta viene acompañada de saludos, párrafos explicativos y bloques de formato markdown (```bash ... ```). Si intentara redirigir esta salida directamente a un script de automatización, ¡se produciría un error sintáctico inmediato!

2. **Aplicar los 4 Pilares de la Ingeniería de Contexto:**
   Vamos a reestructurar la petición aplicando **Tarea**, **Contexto**, **Restricciones** y **Formato de Salida**, reforzado con ejemplos **Few-Shot**.
   *(Nota: usamos el nombre `USER_PROMPT` porque en Zsh/macOS la variable `PROMPT` está reservada por el sistema para configurar la apariencia de la línea de comandos del terminal).*
   ```bash
   $ USER_PROMPT="Convierte la intencion en un comando Bash de 1 linea.\n\n"
   $ USER_PROMPT="${USER_PROMPT}Ejemplo 1:\n"
   $ USER_PROMPT="${USER_PROMPT}Intencion: Ver espacio en disco\n"
   $ USER_PROMPT="${USER_PROMPT}Comando: df -h\n\n"
   $ USER_PROMPT="${USER_PROMPT}Ejemplo 2:\n"
   $ USER_PROMPT="${USER_PROMPT}Intencion: Listar ocultos\n"
   $ USER_PROMPT="${USER_PROMPT}Comando: ls -la\n\n"
   $ USER_PROMPT="${USER_PROMPT}Instrucciones Estrictas:\n"
   $ USER_PROMPT="${USER_PROMPT}- Devuelve EXCLUSIVAMENTE el comando de 1 linea.\n"
   $ USER_PROMPT="${USER_PROMPT}- No uses bloques markdown ni explicaciones.\n\n"
   $ USER_PROMPT="${USER_PROMPT}Intencion: Archivos .log de hace 24h en /var/log\n"
   $ USER_PROMPT="${USER_PROMPT}Comando:"

   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"${USER_PROMPT}\",
       \"generation_config\": {
         \"temperature\": 0.0
       }
     }" | ./get_text.py
   ```
   *(Fíjese en el parámetro `"generation_config": {"temperature": 0.0}`: tal como se estudió en la teoría, la temperatura cero instruye al modelo a seleccionar deterministamente los tokens de mayor probabilidad, eliminando variaciones creativas y garantizando salidas de comandos consistentes y reproducibles).*

3. **Evaluar la Salida:**
   Observe cómo el modelo generó de inmediato la respuesta limpia y determinista (sin ruido), con la sintaxis exacta: `find /var/log -name "*.log" -mtime -1` (o `-mmin -1440`).

-----

## Ejercicio 5: Concluir el Asistente de Terminal (`ask_ai.sh`)

Hasta ahora hemos realizado peticiones manuales con `curl` y hemos canalizado la respuesta a través de `./get_text.py`. Sin embargo, en el día a día de la ingeniería —donde queremos inyectar archivos de contexto (`AGENTS.md`) o procedimientos especializados (`SKILL.md`)— construir comandos `curl` manualmente en la consola resulta tedioso y repetitivo.

En este ejercicio concluirá su propio asistente de línea de comandos en Bash (**`ask_ai.sh`**). La estructura general (validación de variables de entorno, argumentos de entrada, detección automática de contexto y generación segura del payload JSON) ya está preparada en una plantilla base (*starter template*). Su desafío práctico consiste en **completar la sección del comando `curl`** para realizar la petición HTTP y canalizar la respuesta hacia `get_text.py`.

1. **Obtener o Crear la Plantilla del Script (`ask_ai.sh`):**
   Puede copiar el archivo proporcionado en eLearning o crearlo directamente en su carpeta `~/IEI/clase02/`:
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/ask_ai.sh
   #!/bin/bash
   # ask_ai.sh — Asistente de Consola con Contexto Local
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   BASE="https://generativelanguage.googleapis.com"
   API_URL="${BASE}/v1beta/interactions"
   MODEL="${MODEL:-gemini-3.5-flash-lite}"

   # 1. Validar si la clave de API esta configurada en el entorno
   if [ -z "${GEMINI_API_KEY:-}" ]; then
       echo "Error: GEMINI_API_KEY no definida!" >&2
       echo "Ejecute: export GEMINI_API_KEY=\"su_clave_aqui\"" >&2
       exit 1
   fi

   # 2. Validar argumento de pregunta
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 \"pregunta o instruccion\" [archivo_contexto]" >&2
       exit 1
   fi

   USER_QUERY="$1"
   CONTEXT_FILE="${2:-}"

   # 3. Cargar contexto (del archivo indicado o de AGENTS.md)
   CONTEXT_TEXT=""
   if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
       CONTEXT_TEXT="<contexto>\n$(cat "$CONTEXT_FILE")\n</contexto>\n\n"
       echo "[INFO] Contexto cargado de: $CONTEXT_FILE" >&2
   elif [ -f "AGENTS.md" ]; then
       CONTEXT_TEXT="<project_guidelines>\n"
       CONTEXT_TEXT="${CONTEXT_TEXT}$(cat AGENTS.md)\n"
       CONTEXT_TEXT="${CONTEXT_TEXT}</project_guidelines>\n\n"
       echo "[INFO] Contexto cargado de: AGENTS.md" >&2
   fi

   FULL_INPUT="${CONTEXT_TEXT}Tarea: ${USER_QUERY}"

   # 4. Construir el payload JSON de forma segura con Python
   PAYLOAD=$(python3 -c '
   import json, sys
   print(json.dumps({
       "model": sys.argv[1],
       "input": sys.argv[2],
       "generation_config": {"thinking_level": "low"}
   }))
   ' "$MODEL" "$FULL_INPUT")

   # 5. Ejecutar la peticion via curl y presentar la respuesta limpia
   echo ""
   echo "=== Respuesta de la IA ==="
   # TODO [Desafio]: Complete con la llamada curl (Ejercicios 3 y 4).
   # Requisitos:
   #  - Metodo POST a "$API_URL"
   #  - Cabecera "x-goog-api-key: ${GEMINI_API_KEY}"
   #  - Cabecera "Content-Type: application/json"
   #  - Enviar datos desde "$PAYLOAD"
   #  - Canalizar (|) la salida hacia: python3 "$SCRIPT_DIR/get_text.py"

   # (Escriba aqui su comando curl)

   echo "=========================="
   EOF
   ```

2. **Completar el Comando `curl` en el Editor:**
   Abra el script con el editor de texto de su preferencia (por ejemplo, `nano ~/IEI/clase02/ask_ai.sh` o en VS Code).
   Localice la sección `# 5` e inserte el código que falta para que el script quede funcional.

3. **Asignar Permisos de Ejecución:**
   Haga el script ejecutable:
   ```bash
   $ chmod +x ~/IEI/clase02/ask_ai.sh
   ```

4. **Probar el Asistente con Preguntas Básicas:**
   Plantee preguntas técnicas directamente a su nuevo comando:
   ```bash
   $ cd ~/IEI/clase02
   $ ./ask_ai.sh "¿Diferencia entre variable local y exportada?"
   $ ./ask_ai.sh "¿Como ver puertos abiertos en Linux o macOS?"
   ```

-----

## Ejercicio 6: Anclaje Arquitectónico con `AGENTS.md`

El archivo **`AGENTS.md`** es el estándar moderno adoptado en proyectos de software para proporcionar a agentes y asistentes de IA (Antigravity, Cursor, Claude Code, Copilot) el contexto arquitectónico, las convenciones y los límites del repositorio.

1. **Crear el `AGENTS.md`:**
   En la carpeta `~/IEI/clase02`, cree el archivo `AGENTS.md` con la especificación de su proyecto:
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/AGENTS.md
   # Directrices de Ingenieria: Proyecto IEI

   ## 1. Entorno & Stack
   - Sistema Operativo: Linux Ubuntu / Debian POSIX.
   - Interprete de Scripts: Bash (#!/bin/bash).
   - Todos los scripts deben usar las opciones de seguridad
     set -euo pipefail.

   ## 2. Convenciones de Codigo
   - Foco en utilidades nativas del sistema operativo.
   - Queda expresamente PROHIBIDO sugerir dependencias externas
     para tareas basicas de sistema.
   - Las variables deben escribirse en MAYUSCULAS
     y delimitarse entre comillas dobles.

   ## 3. Seguridad & Restricciones
   - NUNCA sugerir comandos que eliminen datos sin confirmacion
     (ej: prohibir rm -rf).
   - NUNCA exponer contrasenas o tokens hardcoded.
   EOF
   ```

2. **Experimentar el Efecto del Contexto con el Asistente:**
   Realice una consulta utilizando su asistente. Como el archivo `AGENTS.md` existe en la carpeta actual, el asistente lo detecta y lo inyecta automáticamente como contexto de la instrucción:
   ```bash
   $ ./ask_ai.sh "Genera un script para comprobar si cron esta activo."
   ```
   *(Observe el mensaje informativo `[INFO] Contexto cargado de: AGENTS.md` emitido por el script).*

3. **Verificación Crítica:**
   Compruebe cómo la IA acató rigurosamente las reglas definidas en `AGENTS.md`: incluyó `#!/bin/bash`, incorporó la salvaguarda `set -euo pipefail` y utilizó herramientas nativas como `systemctl is-active cron` o `pgrep cron`, sin recurrir a dependencias externas.

4. **Desafío Práctico: Modificar el `AGENTS.md` y Evaluar la Reacción de la IA:**
   Abra su archivo `AGENTS.md` en el editor de texto (`nano ~/IEI/clase02/AGENTS.md` o en VS Code) y agregue una nueva directriz a su contrato.
   Por ejemplo, elija una de las siguientes ideas (o cree su propia regla):
   * **Restricción de Herramientas:** Añada una regla que prohíba expresamente la utilidad `systemctl`, exigiendo que la verificación de procesos use exclusivamente `pgrep` o `/etc/init.d/`.
   * **Formato y Registro:** Añada una regla que obligue a que todos los mensajes impresos en la consola por el script contengan un prefijo de fecha/hora en formato `[YYYY-MM-DD hh:mm:ss]`.
   * **Gestión de Señales:** Añada una regla que obligue a que cualquier script implemente una función `cleanup()` y registre un comando `trap` para interceptar `SIGINT` (`Ctrl+C`).

   Guarde los cambios y vuelva a ejecutar el asistente con **la misma pregunta**:
   ```bash
   $ ./ask_ai.sh "Genera un script para comprobar si cron esta activo."
   ```
   **¿Qué cambió?** Compare la nueva respuesta con la anterior. ¡Observe cómo, sin cambiar una sola letra en la pregunta enviada, el modelo adaptó la arquitectura del código para cumplir con la nueva especificación del proyecto!

-----

## Ejercicio 7: Diseñar y Probar una Skill Modular (`safe-cli`)

Una **Skill** es un procedimiento especializado de conocimiento modular, diseñado para activarse bajo demanda para una tarea específica.

En este ejercicio creará la skill **`safe-cli`**, concebida para auditar la seguridad de comandos de terminal en entornos UNIX (**Linux y macOS**, abarcando intérpretes **Bash y Zsh**) antes de ejecutarlos.

> **Nota para usuarios de macOS / Zsh:**
> En macOS, la *shell* predeterminada es Zsh (`/bin/zsh`). La sintaxis de variables, redirecciones y ejecución de esta guía es totalmente compatible. La skill que vamos a diseñar debe ser agnóstica o consciente de las especificidades de cada sistema operativo (ej.: `apt` vs. `brew`, `systemctl` vs. `launchctl`, `/var/www/html` vs. `/Library/WebServer/Documents`, y utilidades específicas como `diskutil`).

1. **Crear la Estructura de la Skill:**
   Cree la carpeta de la skill:
   ```bash
   $ mkdir -p ~/IEI/clase02/skills/safe-cli
   ```

2. **Definir el Procedimiento Operativo (`SKILL.md`):**
   Cree el archivo con las directrices de auditoría para entornos Linux y macOS:
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/skills/safe-cli/SKILL.md
   ---
   name: safe-cli
   description: Analizador de seguridad para comandos UNIX (Linux y macOS).
   ---

   # Procedimiento Operativo de la Skill safe-cli:
   Al recibir un comando para inspeccionar, sigue estos 4 pasos:
   1. [Nivel de Riesgo]: Clasifica como [SEGURO], [ATENCION] o [PELIGROSO].
   2. [Objetivo]: Resume en una frase clara lo que hace el comando.
   3. [Descomposicion]: Explica cada comando, subcomando y flag utilizada.
   4. [Alerta & Alternativa]: Si el comando tiene impacto destructivo
      (ej: rm -rf, dd, chmod -R 777, diskutil), advierte sobre el peligro
      y presenta una alternativa segura con privilegios minimos.
   EOF
   ```

3. **Probar la Skill Pasándola al Asistente:**
   Invoque a su asistente pasando el comando a auditar e indicando el archivo de la skill como segundo argumento:
   ```bash
   $ ./ask_ai.sh "chmod -R 777 ~/" skills/safe-cli/SKILL.md
   ```
   *(También puede probar comandos específicos de su entorno, como `chmod -R 777 /var/www/html` en Linux o `sudo chmod -R 777 /Library/WebServer/Documents` en macOS).*

4. **Inspeccionar el Informe de Auditoría:**
   Confirme que la IA clasificó el comando como **PELIGROSO**, explicó el impacto de los permisos `777` recursivos (lectura, escritura y ejecución universal a cualquier usuario o proceso) y sugirió una alternativa con privilegios mínimos (`chmod 755` o `chmod 700`).

5. **Discusión Crítica de Cierre:**
   Observe que el asistente **presenta** sugerencias y auditorías, pero **no las ejecuta automáticamente**.
   *Reflexione:* ¿Por qué motivo, en el diseño de herramientas de ingeniería de software, la ejecución automática de comandos generados por IA sin validación humana previa (*Human-in-the-Loop*) constituye una vulnerabilidad crítica de seguridad?

-----

## Ejercicio 8 [Desafío de Consolidación]: El Médico del Terminal (`ai_fix.sh`)

Durante el aprendizaje de sistemas UNIX, es habitual encontrarse con mensajes de error en la consola (`No such file or directory`, `Permission denied`, `invalid mode`, etc.).
Como desafío final —para realizar al final de la clase o de forma autónoma en casa— creará una herramienta de productividad real: **`ai_fix.sh`**, un script que ejecuta un comando con error, captura su mensaje de fallo y solicita a la IA un diagnóstico estandarizado y su respectiva corrección.

1. **Especificar los Requisitos de la Skill de Diagnóstico (`skills/error-fix/SKILL.md`):**
   A partir de la estructura de *Skills* aprendida en el Ejercicio 7 (cabecera YAML y procedimiento en Markdown), cree el directorio para la nueva skill:
   ```bash
   $ mkdir -p ~/IEI/clase02/skills/error-fix
   ```
   Cree el archivo `~/IEI/clase02/skills/error-fix/SKILL.md`. En lugar de recibir las instrucciones ya hechas, diseñe su propia *Skill* para que el asistente analice un comando con error y devuelva **estrictamente** este formato de salida:
   ```text
   [Causa]: Explicacion concisa del motivo tecnico del fallo.
   [Comando Corregido]: comando exacto listo para ejecutar
   [Consejo]: Recomendacion sobre la flag, sintaxis o permiso corregido.
   ```
   **Requisitos que debe garantizar:**
   * Incluir los metadatos YAML iniciales (`name` y `description`) en la skill.
   * Definir reglas operativas que impidan al modelo añadir saludos, introducciones o texto conversacional superfluo, limitándolo exclusivamente a los tres bloques de diagnóstico indicados.

2. **Consejos Técnicos Esenciales en Bash:**
   Para construir y comprender el script `ai_fix.sh`, analizamos dos conceptos prácticos de la *shell*:
   * **Cómo Recibe Argumentos un Script (`$#` y `$*`):**
     Cuando ejecutamos un script pasando argumentos (ej.: `./ai_fix.sh "chmod 999 app.sh"` o `./ai_fix.sh chmod 999 app.sh`), Bash proporciona variables especiales automáticas:
     * **`$#`**: Contiene el **número de argumentos** pasados. En la plantilla usamos `[ "$#" -eq 0 ]` para verificar si el usuario olvidó indicar el comando y mostrar el mensaje de ayuda (*usage*).
     * **`$*`**: Agrupa **todas las palabras y opciones** suministradas en una sola cadena de texto almacenada en la variable `CMD`, permitiendo que el usuario pase el comando cómodamente con o sin comillas.
   * **Cómo Utilizar el Script:**
     La forma recomendada de uso es pasar el comando a diagnosticar delimitado entre comillas dobles, preservando tuberías (*pipes*) y opciones especiales:
     ```bash
     $ ./ai_fix.sh "comando_con_error --flags"
     ```
   * **Captura Dinámica de Salida y Errores con `eval` y `2>&1`:**
     ```bash
     ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)
     ```
     * `eval "$CMD"`: Evalúa y ejecuta la cadena de texto del comando dinámicamente.
     * `2>&1`: Redirige el canal de errores (*stderr*, descriptor `2`) al canal estándar (*stdout*, descriptor `1`), permitiendo que la sustitución de comandos `$()` capture los mensajes de fallo.
     * `|| true`: Garantiza que, incluso si el comando finaliza con código de error (distinto de 0), el script no aborte abruptamente debido a la opción de seguridad `set -e`.

3. **Obtener la Plantilla del Script (`ai_fix.sh`):**
   Cree el archivo base en su carpeta `~/IEI/clase02/` (o cópielo de eLearning):
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/ai_fix.sh
   #!/bin/bash
   # ai_fix.sh — Diagnostica y sugiere correcciones para comandos con error
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   # 1. Validar si el usuario proporciono un comando
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 \"comando que fallo\"" >&2
       exit 1
   fi

   # Consejo: "$*" agrupa todas las palabras pasadas como argumento
   CMD="$*"

   # 2. Ejecutar el comando y capturar stdout e stderr juntos
   echo "Ejecutando: $CMD ..."
   ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)

   # 3. Formatear la peticion e invocar al asistente con la skill
   # TODO [Desafio]: Construya el prompt con el comando ($CMD) y el error
   # ($ERROR_OUTPUT), e invoque ask_ai.sh pasando la skill:
   # "$SCRIPT_DIR/skills/error-fix/SKILL.md"

   # (Escriba aqui la llamada a ask_ai.sh)

   EOF
   ```

4. **Completar el Script en el Editor:**
   Abra el script `~/IEI/clase02/ai_fix.sh`. En la sección `# 3`, complete el código para construir el prompt utilizando las variables `$CMD` y `$ERROR_OUTPUT`, e invoque al asistente `ask_ai.sh` pasando el archivo de la *Skill* como segundo argumento:
   ```bash
   INVOCAR_ASK_AI.SH "PROMPT_AQUI" "RUTA/HACIA/SKILL.md"
   ```

5. **Asignar Permisos y Probar:**
   Haga el script ejecutable:
   ```bash
   $ chmod +x ~/IEI/clase02/ai_fix.sh
   ```
   Pruebe comandos deliberadamente erróneos:
   ```bash
   $ cd ~/IEI/clase02
   $ ./ai_fix.sh "cat /archivo_que_no_existe.txt"
   $ ./ai_fix.sh "chmod 999 app.sh"
   $ ./ai_fix.sh "tar -czf backup.tar.gz carpeta_fantasma"
   ```
   *¡Observe cómo la IA diagnostica con precisión el motivo del fallo según las 3 etapas de la Skill (Causa, Comando Corregido y Consejo)!*

\newpage

# Ejercicios Opcionales de Práctica y Extensión

Estos ejercicios están destinados a realizarse en el tiempo restante de la clase de laboratorio o de forma autónoma en casa, consolidando técnicas avanzadas de automatización en Bash y explorando nuevas aplicaciones de ingeniería de contexto y skills modulares.

-----

## Ejercicio 9 [Opcional]: Automatización de Copias con Timestamp (`backup_auto.sh`)

En el Ejercicio 2 aprendió a crear archivos comprimidos con `tar -czvf`. Sin embargo, en tareas reales de administración de sistemas e ingeniería de software, una rutina de copia de seguridad nunca debe sobrescribir un archivo existente: debe generar nombres dinámicos con **marca de fecha y hora** (*timestamps*) y excluir archivos temporales prescindibles.

1. **Probar la Generación Dinámica de Fechas:**
   La utilidad `date` permite dar formato a fechas de forma estandarizada para nombres de archivo. Pruebe en el terminal:
   ```bash
   $ date +"%Y%m%d_%H%M%S"
   ```
   *(Devuelve algo como `20261006_143022`, ideal para ordenar cronológicamente copias de seguridad).*

2. **Crear Archivos Temporales en el Proyecto:**
   Para probar la capacidad de exclusión de `tar`, cree algunos archivos temporales en su carpeta de ejemplo:
   ```bash
   $ touch ~/IEI/clase02/proyecto_ejemplo/cache.tmp
   $ touch ~/IEI/clase02/proyecto_ejemplo/debug.log
   ```

3. **Obtener o Crear el Esqueleto del Script (`backup_auto.sh`):**
   Puede copiar el archivo `backup_auto.sh` disponible en eLearning/repositorio o crearlo en la carpeta `~/IEI/clase02/`.
   Observe que la validación de parámetros, la comprobación de existencia de la carpeta con `[ ! -d "$ORIGEN" ]` y el informe final ya están preconstruidos:
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/backup_auto.sh
   #!/bin/bash
   # backup_auto.sh — Crea archivo .tar.gz con timestamp y excluye temporales
   set -euo pipefail

   # 1. Validar si la carpeta de origen fue indicada y si existe
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 <directorio_origen> [directorio_destino]" >&2
       exit 1
   fi

   ORIGEN="$1"
   DESTINO="${2:-.}"

   if [ ! -d "$ORIGEN" ]; then
       echo "Error: ¡El directorio '$ORIGEN' no existe!" >&2
       exit 1
   fi

   NOME_BASE=$(basename "$ORIGEN")

   # 2. Generar timestamp y nombre del archivo de salida
   # TODO [Desafio 1]: Guarde en TIMESTAMP la fecha actual en formato YYYYMMDD_HHMMSS (use date).
   # A continuacion, construya la ruta completa del archivo de destino en NOME_ARQUIVO:
   # "${DESTINO}/backup_${NOME_BASE}_${TIMESTAMP}.tar.gz"

   # (Defina aqui las variables TIMESTAMP y NOME_ARQUIVO)


   echo "Empaquetando '$ORIGEN' en '$NOME_ARQUIVO'..."

   # 3. Crear archivo comprimido (.tar.gz) excluyendo temporales
   # TODO [Desafio 2]: Ejecute la utilidad tar para crear el archivo comprimido
   # en la ruta "$NOME_ARQUIVO" con el contenido de "$ORIGEN".
   # Requisitos:
   #  - Comprimir con gzip (-czf)
   #  - Excluir archivos con extension .tmp (--exclude="*.tmp")
   #  - Excluir archivos con extension .log (--exclude="*.log")

   # (Escriba aqui su comando tar)


   # 4. Mostrar informe de exito y recuento de archivos preservados
   TOTAL_FICH=$(tar -tf "$NOME_ARQUIVO" | wc -l | tr -d ' ')
   TAMANHO=$(ls -lh "$NOME_ARQUIVO" | awk '{print $5}')

   echo "¡Backup completado con exito!"
   echo " - Archivo: $NOME_ARQUIVO"
   echo " - Tamano: $TAMANHO"
   echo " - Archivos preservados: $TOTAL_FICH"
   EOF
   ```

4. **Completar el Script en el Editor:**
   Abra el script (`nano ~/IEI/clase02/backup_auto.sh` o en su editor de código).
   - En el **Desafío 1**, defina `TIMESTAMP=$(date +"%Y%m%d_%H%M%S")` y construya la variable `NOME_ARQUIVO`.
   - En el **Desafío 2**, escriba el comando `tar` con las opciones de exclusión para archivar `$ORIGEN` en `$NOME_ARQUIVO`.

5. **Asignar Permisos y Probar:**
   Haga el script ejecutable:
   ```bash
   $ chmod +x ~/IEI/clase02/backup_auto.sh
   ```
   Ejecute el script y confirme que los archivos `.tmp` y `.log` fueron ignorados con éxito:
   ```bash
   $ cd ~/IEI/clase02
   $ ./backup_auto.sh proyecto_ejemplo
   $ tar -tf backup_proyecto_ejemplo_*.tar.gz
   ```
   *(Confirme que `cache.tmp` y `debug.log` no aparecen en el listado del archivo).*

-----

## Ejercicio 10 [Opcional]: Puente hacia Git — Mensajes de Commit con IA (`skills/git-commit`)

En una próxima sesión de laboratorio comenzará a trabajar con el sistema de control de versiones **Git**. Una de las convenciones más adoptadas en la industria del software es la especificación [*Conventional Commits*](https://www.conventionalcommits.org/), que estandariza el historial del proyecto mediante prefijos semánticos claros (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).

En este ejercicio diseñará una nueva *Skill* especializada y un comando auxiliar (`ai_commit.sh`) para transformar anotaciones informales de cambios en mensajes de *commit* perfectamente formateados.

1. **Crear la Estructura de la Skill:**
   Cree el directorio dedicado:
   ```bash
   $ mkdir -p ~/IEI/clase02/skills/git-commit
   ```

2. **Definir la Skill (`skills/git-commit/SKILL.md`):**
   Cree el archivo de procedimiento con ejemplos calibrados (*Few-Shot*):
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/skills/git-commit/SKILL.md
   ---
   name: git-commit
   description: Generador especializado de mensajes de commit segun la especificacion Conventional Commits.
   ---

   # Procedimiento Operacional:
   A partir de la descripcion de cambios proporcionada por el usuario, genera estrictamente el mensaje de commit en el siguiente formato:

   1. Linea de Encabezado (obligatoria):
      <tipo>: <resumen en imperativo, en minusculas, sin punto final, max. 50 caracteres>

      Tipos validos:
      - feat: Nueva funcionalidad para el usuario
      - fix: Correccion de un error o fallo
      - docs: Cambios exclusivos de documentacion
      - refactor: Reorganizacion de codigo sin alterar el comportamiento
      - test: Adicion o correccion de pruebas

   2. Cuerpo (opcional, separado por una linea en blanco):
      Si hay detalles relevantes, describelos en puntos con guion (-).

   # Reglas Estrictas:
   - Devuelve EXCLUSIVAMENTE el mensaje de commit listo para usar.
   - No uses bloques de formato markdown, ni introducciones, ni explicaciones.

   # Ejemplos:
   Entrada: hice un script backup_auto.sh para guardar copias con fecha y hora
   Salida:
   feat: anadir script de backup con timestamp

   - soporta exclusion automatica de archivos .tmp y .log
   - calcula el tamano y total de archivos preservados
   EOF
   ```

3. **Obtener o Crear el Esqueleto del Script (`ai_commit.sh`):**
   El script ya incluye la resolución de carpeta y las validaciones defensivas de argumentos y de existencia de la skill:
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/ai_commit.sh
   #!/bin/bash
   # ai_commit.sh — Genera mensajes Conventional Commits mediante asistente
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   # 1. Validar si el usuario indico una descripcion de los cambios
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 \"describa brevemente lo que cambio en el codigo\"" >&2
       exit 1
   fi

   # Validar si el archivo de la skill existe
   SKILL_FILE="${SCRIPT_DIR}/skills/git-commit/SKILL.md"
   if [ ! -f "$SKILL_FILE" ]; then
       echo "Error: Archivo de la skill no encontrado en: $SKILL_FILE" >&2
       exit 1
   fi

   # 2. Capturar las notas de cambios e invocar al asistente con la skill
   # TODO [Desafio]:
   #  - Guarde todas las palabras pasadas por el usuario en la variable NOTAS (pista: use "$*")
   #  - Invoque el script "$SCRIPT_DIR/ask_ai.sh" pasando como primer argumento la peticion:
   #    "Genera el mensaje de commit para: $NOTAS"
   #    y como segundo argumento el archivo de la skill: "$SKILL_FILE"

   # (Escriba aqui la captura de NOTAS y la llamada a ask_ai.sh)

   EOF
   ```

4. **Completar el Script en el Editor:**
   Abra el script `~/IEI/clase02/ai_commit.sh`. En la sección `# 2`, complete el desafío capturando la lista de argumentos con `NOTAS="$*"` e invocando `ask_ai.sh` pasando la instrucción y la ruta de la skill.

5. **Asignar Permisos y Probar:**
   Haga el script ejecutable:
   ```bash
   $ chmod +x ~/IEI/clase02/ai_commit.sh
   ```
   Pruebe la herramienta con diferentes tipos de tareas:
   ```bash
   $ cd ~/IEI/clase02
   $ ./ai_commit.sh "corregi el error de permisos en el archivo de claves cambiando a 600"
   $ ./ai_commit.sh "anadi instrucciones sobre la instalacion de python3 en la guia"
   ```
   *¡Observe cómo la IA clasifica automáticamente el tipo (`fix:` o `docs:`) y genera el mensaje listo para copiar en un futuro `git commit -m "..."`!*

-----

## Ejercicio 11 [Opcional]: Panel de Bienvenida en el Terminal y Atajos Globales (`welcome.sh`)

En el Ejercicio 1 exploró cómo los archivos de inicio de la *shell* (`~/.bashrc` en Linux o `~/.zshrc` en macOS) se ejecutan cada vez que abre una nueva ventana de terminal.
En este ejercicio construirá un panel de bienvenida (*Message of the Day* / MOTD) dinámico y creará **atajos globales (*aliases*)** para invocar las herramientas desarrolladas en la clase desde cualquier carpeta del sistema.

> **Regla de Oro de la Portabilidad UNIX (`printf` vs. `echo -e`):**
> En Linux (GNU), el comando `echo -e` interpreta códigos de escape de color. Sin embargo, en macOS (BSD), el comando `/bin/echo` no reconoce la opción `-e`, imprimiendo literalmente `-e \033...`.
> El estándar **POSIX universalmente compatible** entre Linux y macOS (y entre intérpretes Bash y Zsh) es utilizar el comando **`printf`**:
> ```bash
> VERDE=$(printf '\033[32m')
> RESET=$(printf '\033[0m')
> printf "%s\n" "${VERDE}[OK] ¡Funciona en Linux y macOS!${RESET}"
> ```

1. **Obtener o Crear el Esqueleto del Script (`welcome.sh`):**
   Cree el archivo de bienvenida en la carpeta `~/IEI/clase02/` (o cópielo de eLearning/repositorio):
   ```bash
   $ cat << 'EOF' > ~/IEI/clase02/welcome.sh
   #!/bin/bash
   # welcome.sh — Panel de Bienvenida de la Workstation IEI (Linux & macOS)
   set -euo pipefail

   # Definicion portable de colores ANSI compatible con Linux y macOS (POSIX)
   VERDE=$(printf '\033[32m')
   AMARELO=$(printf '\033[33m')
   AZUL=$(printf '\033[34m')
   RESET=$(printf '\033[0m')

   printf "${AZUL}====================================================${RESET}\n"
   printf "${AZUL}    IEI Workstation — Universidade de Aveiro        ${RESET}\n"
   printf "${AZUL}====================================================${RESET}\n"
   printf " Usuario    : ${VERDE}%s${RESET}\n" "$USER"
   printf " Sistema    : %s (%s)\n" "$(uname -s)" "$(uname -m)"
   printf " Fecha/Hora : %s\n" "$(date +"%Y-%m-%d %H:%M:%S")"

   # 1. Verificacion de secretos y estado de la API Gemini
   # TODO [Desafio]: Verifique si la variable GEMINI_API_KEY esta definida y no vacia.
   # Pista: use [ -n "${GEMINI_API_KEY:-}" ]
   # Si esta definida:
   #    printf " API Gemini : ${VERDE}[OK] Clave activa${RESET}\n"
   # En caso contrario:
   #    printf " API Gemini : ${AMARELO}[AVISO] Clave ausente (~/.api_keys)${RESET}\n"

   # (Escriba aqui la condicion if/else)


   # 2. Resumen de la carpeta de trabajo del laboratorio
   AULA_DIR="$HOME/IEI/clase02"
   if [ -d "$AULA_DIR" ]; then
       TOTAL_FICH=$(find "$AULA_DIR" -maxdepth 1 -type f | wc -l | tr -d ' ')
       printf " Archivos   : %s archivos en la carpeta ~/IEI/clase02\n" "$TOTAL_FICH"
   fi

   printf "${AZUL}----------------------------------------------------${RESET}\n"
   printf " Atajos: ${VERDE}ask${RESET} \"pregunta\" | ${VERDE}fix${RESET} \"cmd_con_error\"\n"
   printf "${AZUL}====================================================${RESET}\n\n"
   EOF
   ```

2. **Completar el Script en el Editor:**
   Abra el script `~/IEI/clase02/welcome.sh` en su editor de texto. En la sección `# 1`, complete la comprobación condicional `if [ -n "${GEMINI_API_KEY:-}" ]; then ... else ... fi` para informar de si la clave está configurada en el entorno con los colores adecuados.

3. **Asignar Permisos de Ejecución:**
   Haga el script ejecutable:
   ```bash
   $ chmod +x ~/IEI/clase02/welcome.sh
   ```
   *(Puede probarlo directamente en la consola ejecutando `./welcome.sh`)*.

4. **Desafío: Registrar el Script y los Atajos en el Inicio de la Shell:**
   A partir de lo aprendido en el **Ejercicio 1 (paso 6)**, configure el archivo de inicio de su *shell* (`~/.bashrc` en Linux o `~/.zshrc` en macOS) para hacer permanentes estas funciones.

   > **Cómo funcionan los Atajos (*Aliases*):**
   > El comando `alias` permite asociar una palabra corta a un comando largo o a la ruta de un script, permitiendo invocarlo desde cualquier directorio:
   > ```bash
   > alias nombre_del_atajo="comando_o_ruta_completa"
   > ```
   > *(Atención a la regla de sintaxis en Shell: nunca coloque espacios antes ni después del signo `=`, de lo contrario el intérprete intentará ejecutar el comando en lugar de definir el atajo).*

   **Requisitos a cumplir:**
   * **Ejecutar el panel al inicio:** Agregue la instrucción para ejecutar el script `~/IEI/clase02/welcome.sh` en cada nueva sesión, utilizando una comprobación defensiva con `[ -f ... ]` (para evitar mensajes de error si el archivo se mueve o elimina).
   * **Crear atajos globales (*aliases*):** Defina los atajos `ask` (apuntando a la ruta de `~/IEI/clase02/ask_ai.sh`) y `fix` (apuntando a `~/IEI/clase02/ai_fix.sh`).
   * **Recargar el entorno:** Recargue el archivo de inicio en la sesión actual utilizando el comando `source`.

5. **La Prueba Final (Nuevo Terminal Independiente):**
   Abra una **nueva ventana de terminal** (o una nueva pestaña).
   * ¡Verifique el panel con los colores verde y azul mostrado instantáneamente al abrir la consola!
   * Estando en cualquier directorio (por ejemplo, en su carpeta personal `cd ~`), pruebe a usar los nuevos atajos directamente:
     ```bash
     $ ask "Explica la diferencia entre echo y printf en POSIX."
     ```
   *(¡Observe cómo la herramienta funciona de inmediato desde cualquier carpeta, sin necesidad de `./` ni de rutas relativas!).*
