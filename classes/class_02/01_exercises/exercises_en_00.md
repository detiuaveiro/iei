---
title: "Linux II: Environment Management, Automation & AI in Software Engineering"
subtitle: Introduction to Computer Engineering
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

# Practical Lab Guide

This lab guide is designed for a **3-hour** session and is organized into two fundamental parts and an independent extension section:

* **Part I — Environment Management and Backups (Exercises 1 and 2):** Core Linux concepts, process boundaries, subshells, and archiving with `tar`.
* **Part II — AI Engineering, Context and Agents on the CLI (Exercises 3 to 8):** Consuming LLM APIs from the terminal, secrets security best practices, Context Engineering, building an `AGENTS.md` repository constitution, designing a modular `Skill` (`safe-cli`), building an automated CLI assistant in Bash, and an integrating error-fixing challenge (`ai_fix.sh`).
* **Optional Extension Exercises (Exercises 9 to 11):** Advanced backup automation with dynamic timestamps (`backup_auto.sh`), preparatory bridge to Git with an intelligent *Conventional Commits* generator (`skills/git-commit`), and shell startup customization with a welcome dashboard and global aliases (`welcome.sh` in `~/.bashrc` / `~/.zshrc`).

\vspace{1em}

> **Terminal Survival Tips:**
>
> * **Auto-completion with `<Tab>`:** Type the first few characters of a command or path and press `<Tab>`. Double `<Tab>` displays all available choices.
> * **Command History with `↑` and `↓` arrows:** Never retype a long command because of a typo; press the up arrow to recall and edit previous commands.
> * **Cancel with `Ctrl + C`:** If a command or network call blocks or loops, press `Ctrl + C` to abort immediately and return to the prompt.
> * **Quote Your Variables:** When expanding variables in scripts or commands (e.g., `echo "$MY_VAR"`), always wrap them in double quotes to avoid issues with whitespace or special characters.

\newpage

# Part I: Environment Management and Backups

## Exercise 1: Shell Variables, Subprocesses, and Secrets

In this exercise you will explore the difference between local shell variables and exported global environment variables, understand how child processes inherit data, and learn how to manage secrets securely in modern software projects.

1. **Create the Lab Directory:**
   Create a dedicated workspace folder inside your home directory for today's session:
   ```bash
   $ mkdir -p ~/IEI/class02
   $ cd ~/IEI/class02
   ```

2. **Define a Local Variable:**
   Assign a simple variable in your interactive shell:
   ```bash
   $ COURSE="LEI_UA"
   $ echo "My course is: $COURSE"
   ```
   *(Try running `printenv COURSE`: confirm that it returns nothing, since `printenv` only checks environment variables).*

3. **Test the Process Boundary with a Script:**
   Create a simple script to test whether other programs can access your variable:
   ```bash
   $ echo 'echo "Course in script: $COURSE"' > test_course.sh
   $ chmod +x test_course.sh
   $ ./test_course.sh
   ```
   *What happened?* The script printed `Inside the script the course is: ` (empty). The script runs as an independent child process and **has no access** to local variables in your current shell window.

4. **Promote the Variable with `export`:**
   Promote the variable to the system environment table and run the script again:
   ```bash
   $ export COURSE="LEI_UA"
   $ ./test_course.sh
   ```
   *Result:* The script now successfully reads `LEI_UA`, because programs and scripts inherit a copy of all exported variables.

5. **Inspect and Clean Up the Environment:**
   Utilities like `printenv` and `env` query only variables promoted with `export`:
   ```bash
   $ printenv COURSE
   $ env | grep COURSE
   ```
   *(Both return `COURSE=LEI_UA`).*

   Then remove the variable from session memory using `unset` and confirm it is gone:
   ```bash
   $ unset COURSE
   $ printenv COURSE
   ```

6. **Environment Persistence (`~/.bashrc` / `~/.zshrc`) and Security with `chmod 600`:**
   When you close a terminal window or reboot your machine, all session-exported variables vanish. To make configurations and API keys persistent across sessions in a modular and secure way:

   * **Identify your Active Shell:**
     Check the default shell interpreter used by your terminal:
     ```bash
     $ echo "$SHELL"
     ```
     * On **Linux (Ubuntu/Debian)**: the standard is Bash (`/bin/bash`), using the **`~/.bashrc`** startup file.
     * On **macOS**: the standard since macOS Catalina is Zsh (`/bin/zsh`), using the **`~/.zshrc`** startup file.

   * **Create a Dedicated Credentials File (`~/.api_keys`):**
     Inside your home directory, create a personal file for persistent environment variables and secrets:
     ```bash
     $ echo 'export IEI_PERSISTENT="Hello_IEI"' > ~/.api_keys
     ```

   * **Protect Against Other Users with `chmod 600`:**
     In multi-user environments (such as university servers or shared lab stations), other users could inspect files in your home folder if permissions are permissive (`644`). Enforce the principle of least privilege by restricting read/write permissions strictly to your user:
     ```bash
     $ chmod 600 ~/.api_keys
     $ ls -l ~/.api_keys
     ```
     *(Confirm that permissions read `-rw-------`: only the owner can access).*

   * **Configure Automatic Sourcing in your Shell's Startup File:**
     Append an import instruction to the startup script corresponding to your operating system:

     * *On Linux (Bash):*
       ```bash
       $ echo '[ -f ~/.api_keys ] && source ~/.api_keys' >> ~/.bashrc
       $ source ~/.bashrc
       ```

     * *On macOS (Zsh):*
       ```bash
       $ echo '[ -f ~/.api_keys ] && source ~/.api_keys' >> ~/.zshrc
       $ source ~/.zshrc
       ```

   * **Confirm Persistence in the Active Session:**
     ```bash
     $ echo "$IEI_PERSISTENT"
     ```
     *(The terminal outputs `Hello_IEI`, confirming the variable was loaded in the current window).*

   * **The Definitive Test (Open a New Terminal):**
     To prove that persistence is truly permanent and independent of the active session:
     1. Open a **new terminal window or tab**.
     2. In the new terminal, without running any preliminary setup commands, run:
        ```bash
        $ echo "$IEI_PERSISTENT"
        ```
     3. Confirm that `Hello_IEI` prints immediately, proving that the shell automatically imported your environment during its startup sequence.
     4. Close this temporary window (`exit` or close the tab) and **return to your original terminal** to proceed with the remaining exercises.

-----

## Exercise 2: Project Backups with `tar`

The `tar` (*Tape Archive*) utility is the standard Unix tool to package directories into compressed backup archives.

1. **Prepare Test Files:**
   Inside `~/IEI/class02`, create a mock project folder with several sample files:
   ```bash
   $ mkdir -p ~/IEI/class02/sample_project
   $ echo "# Sample IEI Project" > ~/IEI/class02/sample_project/README.md
   $ echo "echo 'Hello World'" > ~/IEI/class02/sample_project/app.sh
   $ chmod +x ~/IEI/class02/sample_project/app.sh
   $ date > ~/IEI/class02/sample_project/timestamp.txt
   ```

2. **Create a Compressed Archive (`.tar.gz`):**
   From your working directory `~/IEI/class02`, package the `sample_project` directory into a single compressed archive using the classic `-czvf` options:
   ```bash
   $ tar -czvf project_backup.tar.gz sample_project
   ```
   *Understanding the 4 essential options:*
   * `-c` : **Create** — Creates a new archive file.
   * `-z` : **Zip (gzip)** — Compresses data to save disk space.
   * `-v` : **Verbose** — Displays each file as it gets packaged.
   * `-f` : **File** — Specifies the output filename (`project_backup.tar.gz`). Must always be the last option before the filename.

3. **Inspect the Archive:**
   Verify the archive size and list its contents without extracting:
   ```bash
   $ ls -lh project_backup.tar.gz
   $ tar -tf project_backup.tar.gz
   ```
   *(The `-t` option prints the index of files stored in the archive).*

4. **Simulate a Restore to Another Directory with `-C`:**
   By default, `tar` extracts files into the current working directory. To extract into a specific target folder without having to `cd` into it, use the **`-C`** (*Change directory*) option:
   ```bash
   $ mkdir -p /tmp/iei_restore
   $ tar -xzvf project_backup.tar.gz -C /tmp/iei_restore/
   $ ls -la /tmp/iei_restore/sample_project/
   ```
   * *The role of `-C`:* Tells `tar` to temporarily change to `/tmp/iei_restore` and unpack files there, keeping your active workspace uncluttered.
   * Confirm that the executable permission (`x`) on `app.sh` was preserved.

5. **Clean Up:**
   Delete the temporary restoration folder:
   ```bash
   $ rm -rf /tmp/iei_restore
   ```

\newpage

# Part II: AI Engineering, Context and Agents on the CLI

## Exercise 3: Your First LLM Call via `curl`

In this exercise you will communicate directly with a frontier language model from the Linux terminal by querying a REST API using `curl`.

> **System Prerequisite (`python3`):**
> JSON data processing in the terminal is handled with `python3` and
> its built-in `json` module (no third-party packages required).
> * **Verify installation:** `$ python3 --version`
> * **Linux (Ubuntu/Debian — if not installed):**  
>   `$ sudo apt update && sudo apt install -y python3`
> * **macOS (if not installed):**  
>   `$ xcode-select --install`

1. **Obtain a Free API Key from Google AI Studio:**
   * Open your browser and navigate to **Google AI Studio**: [https://aistudio.google.com/](https://aistudio.google.com/).
   * Sign in with your personal Google account (**Gmail**). Accept the terms of service if prompted.
   * In the **left sidebar**, navigate to **"Dashboard"** and then select **"API Keys"**.
   * In the top-right corner of the page, click the **"Create key"** button (or *"Create API key"*).
   * In the modal dialog that appears:
     * Under **"Name your key"**, enter a descriptive identifier (e.g., `iei-class02`).
     * Under **"Choose an imported project"**, select **"Default Gemini Project"** (or the default available option).
     * Confirm by clicking **"Create"**.
   * In the **"API key details"** modal that appears:
     * Click the **"Copy key"** button (in the bottom-right corner) to copy the generated key to your clipboard.
     * *(Notice also the **"Copy cURL quickstart"** button: Google AI Studio itself offers a pre-built `curl` test command, highlighting that `curl` is the universal industry-standard utility for interacting directly with AI APIs from the terminal).*

   > **!!! API Costs vs. Account Subscriptions**
   > Unlike personal user subscriptions (such as ChatGPT Plus, Claude Pro, GitHub Copilot, or Google Antigravity, which operate on predictable flat periodic pricing with rate-limited usage windows), developer and Cloud APIs operate on a metered pay-as-you-go model per million tokens. In multi-step agent workflows, the entire accumulated context and codebase files are retransmitted on every iteration, leading to rapid, unforeseen cost accumulation if a script enters an infinite retry loop.
   > In production engineering, it is imperative to enforce **Hard Spend Limits** directly within the Cloud billing console. Note that **Budget Alerts** often suffer from asynchronous processing delays of several hours, meaning allocated budget thresholds can be substantially exceeded before notifications are dispatched. In this lab, we use Google AI Studio's Free Tier, which enforces a strict rate limit (15 RPM) and operates without associated payment methods, eliminating financial risk.

2. **Configure the Environment Variable:**
   In your terminal, export the key to the `GEMINI_API_KEY` environment variable:
   ```bash
   $ export GEMINI_API_KEY="PASTE_YOUR_API_KEY_HERE"
   ```
   *Confirm the variable is set without leaking the full key:*
   ```bash
   $ echo "Configured key: ${GEMINI_API_KEY:0:8}..."
   ```
   *(Tip: to avoid exporting the key manually in every new terminal window, append it to your protected credentials file: `echo 'export GEMINI_API_KEY="PASTE_YOUR_API_KEY_HERE"' >> ~/.api_keys`).*

3. **Make the HTTP POST Request with `curl`:**
   Google provides the modern **Interactions API** (`/v1beta/interactions`) for unified interaction with Gemini models.
   Instead of exposing the key in the URL, recommended authentication is performed securely via the `x-goog-api-key` header:
   ```bash
   $ BASE="https://generativelanguage.googleapis.com"
   $ API_URL="${BASE}/v1beta/interactions"
   $ MODEL="gemini-3.5-flash-lite"

   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Explain in one sentence what tar -czvf does.\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }"
   ```
   *(Latency note: `"thinking_level": "low"` keeps reasoning overhead minimal, ensuring fast responses in ~2 seconds).*

4. **Analyze the Response:**
   Inspect the JSON response returned in the terminal. Notice fields such as `status: "completed"`, `usage` token metrics, and the `steps` list containing generated text blocks (`"type": "model_output"`).

   > [!WARNING]
   > **Temporary High Demand Notice (`service_unavailable` / 503):**
   > If the response contains a server notice such as:
   > ```json
   > {
   >   "error": {
   >     "message": "... is currently experiencing high demand ...",
   >     "code": "service_unavailable"
   >   }
   > }
   > ```
   > **This is neither a syntax error nor an invalid API key!** On Google's free tier, temporary spikes in global traffic can briefly return this response.
   > - **Quick fix:** Wait 5 to 10 seconds and rerun the `curl` command.
   > - **Immediate fallback via `$MODEL`:** If high demand persists, switch to an alternative model in your shell without changing any script code:
   >   ```bash
   >   $ export MODEL="gemini-3.8-flash"
   >   ```
   >   *(Then rerun your `curl` command or script with the new `$MODEL`).*

5. **The Extraction Utility (`get_text.py`):**
   Because the API returns a structured JSON document with technical metadata, and in the following exercises you will want to directly evaluate generated commands and multi-line scripts (with real line breaks), we provide the helper script **`get_text.py`** in the course repository.
   You can also create it directly in your working directory (`~/IEI/class02/`):
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/get_text.py
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
       print("Error processing JSON:", e)
   EOF
   $ chmod +x ~/IEI/class02/get_text.py
   ```
   *Test output extraction by piping the `curl` response:*
   ```bash
   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Explain in one sentence what tar -czvf does.\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }" | ./get_text.py
   ```

-----

## Exercise 4: Context Engineering on the CLI (From Vague to Strict)

Modern language models do not need theatrical personas ("*Act as an engineer...*"). They need **explicit tasks, delimited context, and strict constraints**.

1. **The Flaw of Vague Prompts:**
   Send a loosely formulated question:
   ```bash
   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"How to find files modified in last 24h in Linux?\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }" | ./get_text.py
   ```
   *Reflection:* The response includes conversational greetings, paragraphs of explanation, and markdown code fences (```bash ... ```). Attempting to pipe this output directly into a script would immediately cause a syntax error!

2. **Applying the 4 Pillars of Context Engineering:**
   Reconstruct the query applying **Task**, **Context**, **Constraints**, and **Output Format**, reinforced with **Few-Shot** examples.
   *(Note: we name the variable `USER_PROMPT` because in Zsh/macOS `PROMPT` is a reserved system variable that defines the terminal's prompt appearance!)*
   ```bash
   $ USER_PROMPT="Translate user intent into a 1-line Bash command.\n\n"
   $ USER_PROMPT="${USER_PROMPT}Example 1:\n"
   $ USER_PROMPT="${USER_PROMPT}Intent: Check disk space\n"
   $ USER_PROMPT="${USER_PROMPT}Command: df -h\n\n"
   $ USER_PROMPT="${USER_PROMPT}Example 2:\n"
   $ USER_PROMPT="${USER_PROMPT}Intent: List hidden files\n"
   $ USER_PROMPT="${USER_PROMPT}Command: ls -la\n\n"
   $ USER_PROMPT="${USER_PROMPT}Strict Constraints:\n"
   $ USER_PROMPT="${USER_PROMPT}- Return EXCLUSIVELY the 1-line command.\n"
   $ USER_PROMPT="${USER_PROMPT}- No markdown code blocks or explanations.\n\n"
   $ USER_PROMPT="${USER_PROMPT}Intent: Find .log files from 24h in /var/log\n"
   $ USER_PROMPT="${USER_PROMPT}Command:"

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
   *(Notice the `"generation_config": {"temperature": 0.0}` parameter: as covered in the lecture slides, setting temperature to zero instructs the model to deterministically select highest-probability tokens, suppressing creative variance and guaranteeing consistent, reproducible command outputs).*

3. **Evaluate the Output:**
   Notice how the model outputs a completely clean, deterministic command with zero fluff: `find /var/log -name "*.log" -mtime -1` (or `-mmin -1440`).

-----

## Exercise 5: Completing the Terminal Assistant (`ask_ai.sh`)

So far, we have executed manual requests using `curl` and piped the response through `./get_text.py`. However, in day-to-day engineering workflows—where we want to inject context files (`AGENTS.md`) or specialized operational procedures (`SKILL.md`)—constructing manual `curl` commands in the terminal becomes repetitive.

In this exercise, you will complete your own Bash command-line assistant (**`ask_ai.sh`**). The general scaffolding (environment variable checks, input arguments, automatic context loading, and safe JSON payload generation) is already prepared in a starter template. Your hands-on challenge is to **complete the `curl` command section** to perform the HTTP request and pipe the response into `get_text.py`.

1. **Obtain or Create the Script Skeleton (`ask_ai.sh`):**
   You can copy the starter file from eLearning or create it directly in `~/IEI/class02/`:
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/ask_ai.sh
   #!/bin/bash
   # ask_ai.sh — Terminal Assistant with Local Context
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   BASE="https://generativelanguage.googleapis.com"
   API_URL="${BASE}/v1beta/interactions"
   MODEL="${MODEL:-gemini-3.5-flash-lite}"

   # 1. Verify that the API key is set in the environment
   if [ -z "${GEMINI_API_KEY:-}" ]; then
       echo "Error: GEMINI_API_KEY is not set!" >&2
       echo "Run: export GEMINI_API_KEY=\"your_key_here\"" >&2
       exit 1
   fi

   # 2. Validate query argument
   if [ "$#" -eq 0 ]; then
       echo "Usage: $0 \"question or instruction\" [context_file]" >&2
       exit 1
   fi

   USER_QUERY="$1"
   CONTEXT_FILE="${2:-}"

   # 3. Load context (from specified file or from AGENTS.md)
   CONTEXT_TEXT=""
   if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
       CONTEXT_TEXT="<context>\n$(cat "$CONTEXT_FILE")\n</context>\n\n"
       echo "[INFO] Context loaded from: $CONTEXT_FILE" >&2
   elif [ -f "AGENTS.md" ]; then
       CONTEXT_TEXT="<project_guidelines>\n"
       CONTEXT_TEXT="${CONTEXT_TEXT}$(cat AGENTS.md)\n"
       CONTEXT_TEXT="${CONTEXT_TEXT}</project_guidelines>\n\n"
       echo "[INFO] Context loaded from: AGENTS.md" >&2
   fi

   FULL_INPUT="${CONTEXT_TEXT}Task: ${USER_QUERY}"

   # 4. Safely assemble the JSON payload with Python
   PAYLOAD=$(python3 -c '
   import json, sys
   print(json.dumps({
       "model": sys.argv[1],
       "input": sys.argv[2],
       "generation_config": {"thinking_level": "low"}
   }))
   ' "$MODEL" "$FULL_INPUT")

   # 5. Send request via curl and display clean response
   echo ""
   echo "=== AI Response ==="
   # TODO [Challenge]: Complete with the curl command from Exercises 3 & 4.
   # Requirements:
   #  - POST method to "$API_URL"
   #  - Header "x-goog-api-key: ${GEMINI_API_KEY}"
   #  - Header "Content-Type: application/json"
   #  - Data payload from "$PAYLOAD"
   #  - Pipe (|) to: python3 "$SCRIPT_DIR/get_text.py"

   # (Write your curl command here)

   echo "==================="
   EOF
   ```

2. **Complete the `curl` Command in Your Editor:**
   Open the script with your preferred text editor (e.g., `nano ~/IEI/class02/ask_ai.sh` or VS Code).
   Locate section `# 5` and insert the missing code to make the script functional.


3. **Grant Execution Permissions:**
   Make the script executable:
   ```bash
   $ chmod +x ~/IEI/class02/ask_ai.sh
   ```

4. **Test the Assistant with Basic Queries:**
   Ask technical questions directly to your new command:
   ```bash
   $ cd ~/IEI/class02
   $ ./ask_ai.sh "Difference between local and exported variable?"
   $ ./ask_ai.sh "How to check open network ports in Linux or macOS?"
   ```

-----

## Exercise 6: Architectural Grounding with `AGENTS.md`

An **`AGENTS.md`** file is the modern standard adopted in software engineering to provide coding agents and AI assistants (Antigravity, Cursor, Claude Code, Copilot) with architectural context, style conventions, and repository boundaries.

1. **Create `AGENTS.md`:**
   In `~/IEI/class02`, create the `AGENTS.md` file specifying your project rules:
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/AGENTS.md
   # Engineering Guidelines: IEI Project

   ## 1. Environment & Tech Stack
   - Operating System: Linux Ubuntu / Debian POSIX.
   - Script Interpreter: Bash (#!/bin/bash).
   - All scripts must enable strict safety modes:
     set -euo pipefail.

   ## 2. Coding Standards
   - Rely strictly on native operating system utilities.
   - It is strictly FORBIDDEN to suggest external dependencies
     for basic system tasks.
   - Variables in scripts must be UPPERCASE
     and enclosed in double quotes.

   ## 3. Safety & Constraints
   - NEVER propose destructive commands that delete data
     without confirmation (e.g., forbid rm -rf).
   - NEVER expose hardcoded passwords or API tokens.
   EOF
   ```

2. **Test Context-Driven Behavior with the Assistant:**
   Execute a query using your assistant. Because `AGENTS.md` exists in the current directory, the assistant automatically detects and injects it as instruction context:
   ```bash
   $ ./ask_ai.sh "Generate a script to check if cron is active."
   ```
   *(Notice the informative message `[INFO] Context loaded from: AGENTS.md` printed by the script).*

3. **Critical Inspection:**
   Observe how the model faithfully followed the rules defined in `AGENTS.md`: it included `#!/bin/bash`, added the `set -euo pipefail` safety check, and used native tools like `systemctl is-active cron` or `pgrep cron` without resorting to external dependencies.

4. **Hands-on Challenge: Modifying `AGENTS.md` and Observing Model Adaptation:**
   Open your `AGENTS.md` file in your text editor (`nano ~/IEI/class02/AGENTS.md` or VS Code) and add a new guideline to your contract.
   For example, choose one of the following ideas (or craft your own rule):
   * **Tool Restrictions:** Add a rule strictly forbidding the `systemctl` utility, requiring process checking to rely exclusively on `pgrep` or `/etc/init.d/`.
   * **Logging / Formatting:** Add a rule requiring all console output messages in the script to include a timestamp prefix formatted as `[YYYY-MM-DD hh:mm:ss]`.
   * **Signal Handling:** Add a rule requiring any generated script to implement a `cleanup()` function registered via `trap` to catch `SIGINT` (`Ctrl+C`).

   Save your changes and re-run the assistant with the **exact same query**:
   ```bash
   $ ./ask_ai.sh "Generate a script to check if cron is active."
   ```
   **What changed?** Compare the new response with the previous one. Notice how, without modifying a single word in your prompt, the AI reshaped its generated code to comply with the updated repository contract!


-----

## Exercise 7: Designing and Testing a Modular Skill (`safe-cli`)

A **Skill** is an on-demand, specialized procedural playbook loaded by an AI agent for a specific task.

In this exercise you will build the **`safe-cli`** skill, designed to audit the safety of terminal commands across UNIX environments (**Linux and macOS**, supporting both **Bash and Zsh** shells) before execution.

> **Note for macOS / Zsh users:**
> On macOS, the default shell is Zsh (`/bin/zsh`). The syntax for variables, redirection, and execution in this guide is fully compatible. The skill we design here is structured to understand nuances across operating systems (e.g., `apt` vs. `brew`, `systemctl` vs. `launchctl`, `/var/www/html` vs. `/Library/WebServer/Documents`, and utilities like `diskutil`).

1. **Create the Skill Directory:**
   ```bash
   $ mkdir -p ~/IEI/class02/skills/safe-cli
   ```

2. **Define the Operational Procedure (`SKILL.md`):**
   Create the audit guideline file for Linux and macOS environments:
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/skills/safe-cli/SKILL.md
   ---
   name: safe-cli
   description: Security analyzer for UNIX commands (Linux & macOS).
   ---

   # Operational Procedure for safe-cli:
   When inspecting a command, strictly follow these 4 steps:
   1. [Risk Level]: Classify as [SAFE], [CAUTION], or [DANGEROUS].
   2. [Goal]: Summarize what the command does in one clear sentence.
   3. [Decomposition]: Explain each command, subcommand, and flag used.
   4. [Warning & Alternative]: If the command has destructive impact
      (e.g., rm -rf, dd, chmod -R 777, diskutil), warn about the danger
      and provide a safer least-privilege alternative.
   EOF
   ```

3. **Test the Skill by Passing It to the Assistant:**
   Invoke your assistant passing the command to audit and specifying the skill file as the second argument:
   ```bash
   $ ./ask_ai.sh "chmod -R 777 ~/" skills/safe-cli/SKILL.md
   ```
   *(You can also test environment-specific commands, such as `chmod -R 777 /var/www/html` on Linux or `sudo chmod -R 777 /Library/WebServer/Documents` on macOS).*

4. **Inspect the Audit Report:**
   Confirm that the AI classified the command as **DANGEROUS**, explained the severe hazard of recursive `777` permissions (read, write, and execute permissions granted to all users and processes), and proposed a safer least-privilege alternative (`chmod 755` or `chmod 700`).

5. **Closing Critical Discussion:**
   Notice that the assistant **presents** suggestions and audits, but **does not execute them automatically**.
   *Reflect:* Why, in the design of software engineering tools, does the automatic, unsupervised execution of AI-generated commands without prior human validation (*Human-in-the-Loop*) represent a critical security vulnerability?

-----

## Exercise 8 [Consolidation Challenge]: The Terminal Doctor (`ai_fix.sh`)

While learning UNIX systems, developers frequently encounter cryptic terminal error messages (`No such file or directory`, `Permission denied`, `invalid mode`, etc.).
As an integrating final challenge—to complete at the end of class or autonomously at home—you will build a real-world productivity tool: **`ai_fix.sh`**, a script that runs a failing command, captures its error output, and asks the AI for a standardized diagnosis and the exact corrected command.

1. **Define Diagnostic Skill Requirements (`skills/error-fix/SKILL.md`):**
   Based on the *Skill* structure learned in Exercise 7 (YAML frontmatter and Markdown procedure), create the directory for the new capability:
   ```bash
   $ mkdir -p ~/IEI/class02/skills/error-fix
   ```
   Create the file `~/IEI/class02/skills/error-fix/SKILL.md`. Rather than receiving pre-written instructions, design your own *Skill* so that the assistant analyzes a failing command and outputs **strictly** this format:
   ```text
   [Root Cause]: Concise technical explanation of why it failed.
   [Corrected Command]: exact working command ready to execute
   [Tip]: Brief advice on the flag, syntax, or permission fixed.
   ```
   **Requirements to enforce:**
   * Include the initial YAML frontmatter (`name` and `description`).
   * Establish operational rules that prevent conversational fluff or pleasantries, strictly restricting the assistant to the three diagnostic blocks above.

2. **Essential Technical Bash Concepts:**
   To build and understand `ai_fix.sh`, we examine two core shell scripting concepts:
   * **How a Script Receives Arguments (`$#` and `$*`):**
     When invoking a script passing instructions on the command line (e.g., `./ai_fix.sh "chmod 999 app.sh"` or `./ai_fix.sh chmod 999 app.sh`), Bash populates special automatic variables:
     * **`$#`**: Holds the **number of arguments** provided. In the skeleton, we check `[ "$#" -eq 0 ]` to see if the user forgot to supply a command and print a usage guide.
     * **`$*`**: Joins **all words and flags** passed into a single string stored in `CMD`, allowing users to conveniently invoke the script with or without surrounding quotes.
   * **How to Use the Script:**
     The recommended usage pattern is enclosing the failing command in double quotes, ensuring flags and special shell symbols are preserved:
     ```bash
     $ ./ai_fix.sh "failing_command --flags"
     ```
   * **Dynamic Execution and Error Capture with `eval` and `2>&1`:**
     ```bash
     ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)
     ```
     * `eval "$CMD"`: Dynamically evaluates and executes the command string at runtime.
     * `2>&1`: Redirects standard error (*stderr*, descriptor `2`) into standard output (*stdout*, descriptor `1`), enabling `$()` command substitution to capture error text.
     * `|| true`: Prevents the non-zero exit code of the failing command from aborting the script prematurely under `set -e`.

3. **Obtain the Script Skeleton (`ai_fix.sh`):**
   Create the starter file in `~/IEI/class02/` (or copy it from eLearning):
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/ai_fix.sh
   #!/bin/bash
   # ai_fix.sh — Diagnoses and suggests fixes for failed commands
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   # 1. Validate query argument
   if [ "$#" -eq 0 ]; then
       echo "Usage: $0 \"failing command\"" >&2
       exit 1
   fi

   # Tip: "$*" joins all arguments passed to the script
   CMD="$*"

   # 2. Run the command and capture stdout and stderr together
   echo "Running: $CMD ..."
   ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)

   # 3. Assemble prompt and invoke assistant with the skill
   # TODO [Challenge]: Assemble the prompt with the command ($CMD)
   # and error ($ERROR_OUTPUT), and invoke ask_ai.sh passing the skill:
   # "$SCRIPT_DIR/skills/error-fix/SKILL.md"

   # (Write the call to ask_ai.sh here)

   EOF
   ```

4. **Complete the Script in Your Editor:**
   Open the script (`nano ~/IEI/class02/ai_fix.sh` or VS Code). In section `# 3`, construct the prompt using variables `$CMD` and `$ERROR_OUTPUT`, and invoke the assistant `ask_ai.sh` passing the *Skill* file as the second argument:
   ```bash
   INVOKE_ASK_AI.SH "PROMPT_HERE" "PATH/TO/SKILL.md"
   ```

5. **Grant Execution Permissions and Test:**
   Make the script executable:
   ```bash
   $ chmod +x ~/IEI/class02/ai_fix.sh
   ```
   Test your terminal doctor with intentional errors:
   ```bash
   $ cd ~/IEI/class02
   $ ./ai_fix.sh "cat /path/to/nonexistent_file.txt"
   $ ./ai_fix.sh "chmod 999 app.sh"
   $ ./ai_fix.sh "tar -czf backup.tar.gz nonexistent_folder"
   ```
   *Notice how accurately the AI diagnoses the technical failure following the 3 Skill sections (Root Cause, Corrected Command, and Tip)!*

\newpage

# Optional Practice and Extension Exercises

These exercises are intended to be completed in the remaining laboratory time or independently at home, consolidating advanced Bash automation techniques and exploring new applications of context engineering and modular skills.

-----

## Exercise 9 [Optional]: Automated Backups with Timestamps (`backup_auto.sh`)

In Exercise 2, you learned how to create compressed archives with `tar -czvf`. However, in real-world systems administration and software engineering, a backup routine should never overwrite an existing file: it must generate dynamic names with **timestamps** and exclude disposable temporary files.

1. **Test Dynamic Date Formatting:**
   The `date` utility allows formatting dates in a standardized way for filenames. Try in your terminal:
   ```bash
   $ date +"%Y%m%d_%H%M%S"
   ```
   *(Returns something like `20261006_143022`, ideal for chronologically sorting backups).*

2. **Create Temporary Files in the Project:**
   To test the exclusion capability of `tar`, create some temporary files in your sample folder:
   ```bash
   $ touch ~/IEI/class02/sample_project/cache.tmp
   $ touch ~/IEI/class02/sample_project/debug.log
   ```

3. **Get or Create the Starter Script (`backup_auto.sh`):**
   You can copy the starter file `backup_auto.sh` provided in eLearning/repository or create it in `~/IEI/class02/`.
   Notice that parameter validation, directory existence verification with `[ ! -d "$ORIGEM" ]`, and the final summary report are already pre-built:
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/backup_auto.sh
   #!/bin/bash
   # backup_auto.sh — Creates .tar.gz archive with timestamp and excludes temporary files
   set -euo pipefail

   # 1. Validate that the source directory was provided and exists
   if [ "$#" -eq 0 ]; then
       echo "Usage: $0 <source_directory> [destination_directory]" >&2
       exit 1
   fi

   ORIGEM="$1"
   DESTINO="${2:-.}"

   if [ ! -d "$ORIGEM" ]; then
       echo "Error: Directory '$ORIGEM' does not exist!" >&2
       exit 1
   fi

   NOME_BASE=$(basename "$ORIGEM")

   # 2. Generate timestamp and output archive path
   # TODO [Challenge 1]: Store the current date in TIMESTAMP formatted as YYYYMMDD_HHMMSS (using date).
   # Then construct the full target path in NOME_ARQUIVO:
   # "${DESTINO}/backup_${NOME_BASE}_${TIMESTAMP}.tar.gz"

   # (Define TIMESTAMP and NOME_ARQUIVO here)


   echo "Archiving '$ORIGEM' to '$NOME_ARQUIVO'..."

   # 3. Create compressed archive (.tar.gz) excluding temporary files
   # TODO [Challenge 2]: Run tar to archive and compress ($ORIGEM)
   # into the target file ($NOME_ARQUIVO).
   # Requirements:
   #  - Compress with gzip (-czf)
   #  - Exclude files ending with .tmp (--exclude="*.tmp")
   #  - Exclude files ending with .log (--exclude="*.log")

   # (Write your tar command here)


   # 4. Display success report and count of preserved files
   TOTAL_FICH=$(tar -tf "$NOME_ARQUIVO" | wc -l | tr -d ' ')
   TAMANHO=$(ls -lh "$NOME_ARQUIVO" | awk '{print $5}')

   echo "Backup completed successfully!"
   echo " - Archive: $NOME_ARQUIVO"
   echo " - Size: $TAMANHO"
   echo " - Preserved files: $TOTAL_FICH"
   EOF
   ```

4. **Complete the Script in the Editor:**
   Open the script (`nano ~/IEI/class02/backup_auto.sh` or in your code editor).
   - In **Challenge 1**, set `TIMESTAMP=$(date +"%Y%m%d_%H%M%S")` and construct the `NOME_ARQUIVO` variable.
   - In **Challenge 2**, write the `tar` command with the exclusion options to archive `$ORIGEM` into `$NOME_ARQUIVO`.

5. **Grant Execution Permissions and Test:**
   Make the script executable:
   ```bash
   $ chmod +x ~/IEI/class02/backup_auto.sh
   ```
   Run the script and confirm that `.tmp` and `.log` files were successfully excluded:
   ```bash
   $ cd ~/IEI/class02
   $ ./backup_auto.sh sample_project
   $ tar -tf backup_sample_project_*.tar.gz
   ```
   *(Confirm that `cache.tmp` and `debug.log` do not appear in the archive listing).*

-----

## Exercise 10 [Optional]: Bridge to Git — Commit Messages with AI (`skills/git-commit`)

In an upcoming laboratory session, you will begin working with the **Git** version control system. One of the most widely adopted standards in the software industry is the [*Conventional Commits*](https://www.conventionalcommits.org/) specification, which standardizes repository history through clear semantic prefixes (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).

In this exercise, you will design a specialized *Skill* and a helper utility (`ai_commit.sh`) to transform informal notes into structured, production-ready commit messages.

1. **Create the Skill Directory:**
   Create the dedicated folder:
   ```bash
   $ mkdir -p ~/IEI/class02/skills/git-commit
   ```

2. **Define the Skill (`skills/git-commit/SKILL.md`):**
   Create the operational playbook with few-shot calibration:
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/skills/git-commit/SKILL.md
   ---
   name: git-commit
   description: Specialized commit message generator following the Conventional Commits specification.
   ---

   # Operational Playbook:
   Based on the change description provided by the user, strictly output the commit message in the following format:

   1. Header Line (mandatory):
      <type>: <imperative summary, lowercase, no trailing period, max. 50 characters>

      Valid types:
      - feat: A new feature for the user
      - fix: A bug fix
      - docs: Documentation-only changes
      - refactor: Code restructuring without changing behavior
      - test: Adding or updating tests

   2. Body (optional, separated by a blank line):
      If there are key technical details, list them as bullet points with hyphens (-).

   # Strict Rules:
   - Output EXCLUSIVAMENTE the commit message ready to use.
   - Do NOT use markdown code blocks, intros, greetings, or explanations.

   # Few-Shot Examples:
   Input: made a backup_auto.sh script to archive folders with timestamps
   Output:
   feat: add timestamped backup automation script

   - supports automatic exclusion of .tmp and .log files
   - computes archive size and total preserved file count
   EOF
   ```

3. **Get or Create the Starter Script (`ai_commit.sh`):**
   The starter script already resolves its directory and includes defensive validation:
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/ai_commit.sh
   #!/bin/bash
   # ai_commit.sh — Generates Conventional Commits messages via CLI assistant
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   # 1. Validate that the user provided a change description
   if [ "$#" -eq 0 ]; then
       echo "Usage: $0 \"briefly describe what changed in your code\"" >&2
       exit 1
   fi

   # Validate that the skill file exists
   SKILL_FILE="${SCRIPT_DIR}/skills/git-commit/SKILL.md"
   if [ ! -f "$SKILL_FILE" ]; then
       echo "Error: Skill file not found at: $SKILL_FILE" >&2
       exit 1
   fi

   # 2. Capture change notes and invoke the assistant with the skill
   # TODO [Challenge]:
   #  - Store all argument words provided by the user in NOTAS (hint: use "$*")
   #  - Invoke "$SCRIPT_DIR/ask_ai.sh" passing as the first argument the prompt:
   #    "Generate the commit message for: $NOTAS"
   #    and as the second argument the skill file: "$SKILL_FILE"

   # (Write the NOTAS capture and ask_ai.sh invocation here)

   EOF
   ```

4. **Complete the Script in the Editor:**
   Open the script `~/IEI/class02/ai_commit.sh`. In section `# 2`, complete the challenge by capturing arguments with `NOTAS="$*"` and invoking `ask_ai.sh` with the formatted prompt and skill path.

5. **Grant Permissions and Test:**
   Make the script executable:
   ```bash
   $ chmod +x ~/IEI/class02/ai_commit.sh
   ```
   Test the tool with various types of changes:
   ```bash
   $ cd ~/IEI/class02
   $ ./ai_commit.sh "fixed permission error on keys file by changing to 600"
   $ ./ai_commit.sh "added python3 installation instructions to the lab guide"
   ```
   *Notice how the AI automatically infers the correct prefix (`fix:` or `docs:`) and outputs a commit message ready to copy for a future `git commit -m "..."`!*

-----

## Exercise 11 [Optional]: Welcome Terminal Dashboard and Global Aliases (`welcome.sh`)

In Exercise 1, you learned how shell startup files (`~/.bashrc` on Linux or `~/.zshrc` on macOS) execute every time you open a new terminal window.
In this exercise, you will build a dynamic *Message of the Day* (MOTD) welcome dashboard and configure **global aliases** to invoke your lab assistants from any directory in the system.

> **Golden Rule of UNIX Portability (`printf` vs. `echo -e`):**
> On Linux (GNU), the `echo -e` command interprets color escape codes. However, on macOS (BSD), `/bin/echo` does not recognize the `-e` flag, printing `-e \033...` literally.
> The **POSIX-standard universal pattern** compatible across both Linux and macOS (and across Bash and Zsh) is using **`printf`**:
> ```bash
> VERDE=$(printf '\033[32m')
> RESET=$(printf '\033[0m')
> printf "%s\n" "${VERDE}[OK] Works on both Linux and macOS!${RESET}"
> ```

1. **Get or Create the Starter Script (`welcome.sh`):**
   Create the welcome script in `~/IEI/class02/` (or copy it from eLearning/repository):
   ```bash
   $ cat << 'EOF' > ~/IEI/class02/welcome.sh
   #!/bin/bash
   # welcome.sh — IEI Workstation Welcome Dashboard (Linux & macOS)
   set -euo pipefail

   # Portable ANSI color definitions compatible with Linux and macOS (POSIX)
   VERDE=$(printf '\033[32m')
   AMARELO=$(printf '\033[33m')
   AZUL=$(printf '\033[34m')
   RESET=$(printf '\033[0m')

   printf "${AZUL}====================================================${RESET}\n"
   printf "${AZUL}    IEI Workstation — Universidade de Aveiro        ${RESET}\n"
   printf "${AZUL}====================================================${RESET}\n"
   printf " User       : ${VERDE}%s${RESET}\n" "$USER"
   printf " System     : %s (%s)\n" "$(uname -s)" "$(uname -m)"
   printf " Date/Time  : %s\n" "$(date +"%Y-%m-%d %H:%M:%S")"

   # 1. Check secrets and Gemini API key status
   # TODO [Challenge]: Verify if the GEMINI_API_KEY environment variable is defined and non-empty.
   # Hint: use [ -n "${GEMINI_API_KEY:-}" ]
   # If defined:
   #    printf " Gemini API : ${VERDE}[OK] Key active${RESET}\n"
   # Otherwise:
   #    printf " Gemini API : ${AMARELO}[WARNING] Missing key (~/.api_keys)${RESET}\n"

   # (Write the if/else condition here)


   # 2. Lab workspace summary
   AULA_DIR="$HOME/IEI/class02"
   if [ -d "$AULA_DIR" ]; then
       TOTAL_FICH=$(find "$AULA_DIR" -maxdepth 1 -type f | wc -l | tr -d ' ')
       printf " Files      : %s files in ~/IEI/class02\n" "$TOTAL_FICH"
   fi

   printf "${AZUL}----------------------------------------------------${RESET}\n"
   printf " Shortcuts  : ${VERDE}ask${RESET} \"question\" | ${VERDE}fix${RESET} \"failing_cmd\"\n"
   printf "${AZUL}====================================================${RESET}\n\n"
   EOF
   ```

2. **Complete the Script in the Editor:**
   Open `~/IEI/class02/welcome.sh` in your text editor. In section `# 1`, complete the conditional check `if [ -n "${GEMINI_API_KEY:-}" ]; then ... else ... fi` to report whether your API key is properly loaded.

3. **Grant Execution Permissions:**
   Make the script executable:
   ```bash
   $ chmod +x ~/IEI/class02/welcome.sh
   ```
   *(You can test it directly by running `./welcome.sh`)*.

4. **Challenge: Register the Script and Aliases in Shell Startup:**
   Using what you learned in **Exercise 1 (step 6)**, configure your shell startup file (`~/.bashrc` on Linux or `~/.zshrc` on macOS) to make these utilities permanent.

   > **How Aliases Work:**
   > The `alias` command creates a short keyword to invoke a longer command or script path from any working directory:
   > ```bash
   > alias my_shortcut="full_command_or_path"
   > ```
   > *(Shell syntax rule: never put spaces before or after the `=` sign; otherwise, the shell will try to run the command instead of creating the alias).*

   **Requirements to fulfill:**
   * **Run dashboard on startup:** Add the command to run `~/IEI/class02/welcome.sh` in every new shell session, using defensive validation with `[ -f ... ]` (to prevent errors if the file is moved or deleted).
   * **Create global aliases:** Define `ask` (pointing to `~/IEI/class02/ask_ai.sh`) and `fix` (pointing to `~/IEI/class02/ai_fix.sh`).
   * **Reload environment:** Reload your startup file in the current window using `source`.

5. **The Final Verification (Open a New Terminal):**
   Open a **new terminal window** (or tab).
   * Confirm that your custom green and blue workstation dashboard displays instantly on startup!
   * From any working directory (e.g., your home folder `cd ~`), test your new shortcut directly:
     ```bash
     $ ask "Explain the difference between echo and printf in POSIX."
     ```
   *(Notice how the assistant runs immediately from any folder, without needing `./` or relative paths!).*
