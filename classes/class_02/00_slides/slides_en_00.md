---
title: 47138 - Introduction to Computer Engineering
subtitle: "Linux II: Environment Management, Automation & AI in Software Engineering"
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
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Part I: Linux Environment Management and Automation

Topics covered in this first part:

  * **Environment Variables:**
      * Local vs. global variables (`export`) and inheritance in subprocesses and scripts.
  * **Inspection and Management:**
      * The `printenv`, `env` commands and cleanup with `unset`.
  * **Persistence and Security:**
      * Configuration via `~/.bashrc`, reloading with `source`, and protection with `chmod 600`.
  * **Archiving and Backups:**
      * Packaging and compressing project directories with `tar`.

-----

## Revisiting Session I: System Environment Variables

In the previous session, we used contextual session variables provided by the *shell*:

  * **`$USER`:** The user currently authenticated (`echo $USER`).
  * **`$HOME`:** The absolute path to the personal directory (`echo $HOME`).
  * **`$PATH`:** The directory catalog where the *shell* searches for executable programs (`echo $PATH`).

**Where do these variables originate?**

  * They are not fixed terminal properties: they are **global environment variables** pre-configured by the system upon session startup.
  * Because they reside in the environment, any command or script (`ls`, `python`, `./my_script.sh`) can access their values.
  * **Today's Goal:** Learn how to define our **own variables** and control whether they remain private to our current window or are shared with external programs.

-----

## Shell Variables: Local vs. Global

In the shell, a variable is an association between an identifier and a value for runtime storage and reuse.

  * **Local Variables:**
      * Defined with a simple assignment (`NAME="value"`).
      * Exist **strictly within the current shell session** (private).
      * Are not passed to external programs, commands, or scripts spawned from this session.

      ```bash
      $ COURSE="LEI"
      ```

  * **Environment Variables (Global):**
      * Defined or promoted explicitly using the **`export`** command.
      * Registered in the active session's system environment table.
      * Propagated to and shared with **all commands and scripts** executed from this session.

      ```bash
      $ export COURSE="LEI"
      ```

-----

## Process Inheritance: The Script Boundary

When executing a script (e.g., `./greeting.sh`), the *shell* spawns an independent **child process**:

  * The child process **never inherits** local variables from the parent shell.
  * The child process **inherits a copy** of all variables promoted via `export`.

```bash
# Contents of 'greeting.sh' (executable via chmod +x):
# echo "Welcome to course: $COURSE"

# 1. With local variable: the script cannot access the value
$ COURSE="LEI"
$ ./greeting.sh
Welcome to course:

# 2. Promoting the variable with export: the script inherits the value
$ export COURSE="LEI"
$ ./greeting.sh
Welcome to course: LEI
```

-----

## Inspecting and Managing Environment Variables (Global)

The `printenv` and `env` commands are external utilities that **only access global (exported) environment variables**; they ignore local shell variables:

  * **`printenv [KEY]` (Quick Query):** Inspects a specific environment variable (or lists all):

    ```bash
    $ printenv USER          # Returns current user
    $ printenv COURSE        # Returns "LEI" (if exported; empty if local)
    ```

  * **`env` (Environment and Controlled Execution):** Displays active environment variables or runs commands with temporary variables:

    ```bash
    $ env                    # Lists all active exported variables
    $ env PORT=8080 command  # Applies PORT strictly during command execution
    ```

  * **`unset` (Delete from Session):** Deletes the variable (local or exported) from the active session:

    ```bash
    $ unset COURSE
    $ printenv COURSE        # Returns nothing (no longer exists)
    ```

-----

## Environment Persistence: Shell Startup Files

When closing a terminal session, volatile memory allocations are discarded. Variable and configuration persistence is handled by shell startup scripts:

  * **Interactive Shell Initialization:**
      * Upon spawning an interactive session, the shell processes configuration scripts in `$HOME`:
        * On **Linux (Bash)**: reads and executes **`~/.bashrc`**.
        * On **macOS (Zsh)**: reads and executes **`~/.zshrc`**.
      * Definitions exported here become available in all subsequent interactive sessions.

  * **Persisting Variables:**

    ```bash
    # Append export directive to user configuration file (~/.bashrc on Linux or ~/.zshrc on Mac)
    $ echo 'export GEMINI_API_KEY="AIzaSy..."' >> ~/.bashrc  # or ~/.zshrc
    ```

  * **Modular Configuration Architecture:**
      * For isolation and security, credentials should reside in a separate file (e.g., `~/.api_keys`), sourced conditionally within the shell startup file:

        ```bash
        [ -f ~/.api_keys ] && source ~/.api_keys
        ```

-----

## Reloading the Environment with source and Security with chmod 600

Operational principles for managing and protecting system configurations:

  * **The `source` Command (equivalent to `.`):**
      * Executes commands from a target file **within the context of the active shell**, without spawning a child process.
      * Applies configuration modifications immediately without requiring terminal restarts:

        ```bash
        $ source ~/.bashrc   # or: source ~/.zshrc
        ```

  * **Security in Multi-User Environments:**
      * On shared servers or university workstations, default permissions (e.g., `644`) allow file reading by other system users.
      * Restrict authentication credentials and private key files strictly to owner read and write:

        ```bash
        $ chmod 600 ~/.api_keys
        $ ls -l ~/.api_keys
        -rw------- 1 student student 52 Sep 28 10:00 /home/student/.api_keys
        ```

      *Only the file owner possesses read and write permissions (`rw-------`).*

-----

## Archiving and Data Compression with tar

The **`tar`** (*Tape Archive*) utility is the standard POSIX mechanism to consolidate and distribute directory hierarchies into a single compressed archive:

  * **Creating a compressed archive (`.tar.gz`):**

    ```bash
    $ tar -czvf project_backup.tar.gz ~/IEI/my_project/
    ```

    * `-c` : Create a new archive.
    * `-z` : Compress using the **gzip** algorithm.
    * `-v` : Verbose mode (list processed files).
    * `-f` : Specify the archive file name.

  * **Inspecting archive contents without extracting:**

    ```bash
    $ tar -tf project_backup.tar.gz
    ```

  * **Extracting to a specified target directory (`-C`):**

    ```bash
    $ tar -xzvf project_backup.tar.gz -C /tmp/restore/
    ```

-----

## Part II: Artificial Intelligence in Software Engineering

Topics covered in this second part:

  * **LLM Foundations and Mechanics:**
      * Statistical inference, tokens, context windows, and hallucination mitigation.
  * **Consumption and Cost Governance:**
      * Interaction paradigms, API consumption via `curl`, and cost controls (*FinOps*).
  * **Context Engineering:**
      * Direct technical tasking, structured delimitation, and few-shot calibration.
  * **Autonomous Agents and Safety:**
      * Architecture with `AGENTS.md`, Skills, MCP protocol, and strict hard guardrails.

-----

## Software Engineering Stance on AI

> *"In software engineering, we treat artificial intelligence not as a mystical oracle, but as a computational component with inputs, outputs, measurable costs, and failure modes."*

\vspace{0.8em}

::::: columns
::: {.column width="60%"}

  * **Industry Paradigm Shift:**
      * Large Language Models (**LLMs**) have transitioned from conversational chat tools into foundational components for software construction and automation.
  * **The Software Engineer's Stance:**
      * General users passively marvel at generated text; software engineers must **understand the underlying engine**, enforce output determinism, and rigorously validate results.

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=0.95\linewidth,height=0.48\textheight,keepaspectratio]{ai_engineering_concept.jpg}
\end{center}

:::
:::::

-----

## How LLMs Work: From Statistical Prediction to Internal Representations

A **Large Language Model (LLM)** is fundamentally rooted in the **Transformer** architecture and conditional probability estimation:

  * **Core Autoregressive Mechanism:**
      * Trained to model probability distributions over subsequent text tokens: $P(w_t \mid w_1, \dots, w_{t-1})$.
  * **Emergence of Internal World Models and Semantics:**
      * Accurately predicting complex human language requires far more than surface-level n-gram matching: intermediate network layers develop **geometric representations of concepts**, causal relationships, and logical structures.
  * **Intent Inference and Deliberation (Post-Training & RL):**
      * Reinforcement learning trains the model to **infer user operational intent**, enabling modern models to deliberate internally (*reasoning tokens*) before responding.

-----

## Fallibility of LLMs: The Phenomenon of Hallucinations

> Despite their sophistication, **LLMs remain probabilistic systems** lacking **formal factual verification**, remaining susceptible to syntactically flawless yet completely false outputs (**hallucinations**).

\vspace{-0.2em}
\begin{center}
\includegraphics[width=0.68\linewidth,height=0.42\textheight,keepaspectratio]{ai_hallucination_pizza_glue.jpg}\\
\vspace{0.2em}
\textit{\tiny Real-world case (Google AI Overviews, 2024): ingestion of Reddit satire recommending non-toxic glue to stick cheese to pizza.}
\end{center}

-----

## Processing Unit: Tokens vs. Words

Language models do not operate directly on whole words or isolated characters; the fundamental operational unit is the **Token**.

  * A token represents a text fragment (sub-word, punctuation mark, or control symbol).
  * Statistical ratio: **100 words $\approx$ 130 to 140 tokens** in English.
  * Token decomposition:
    * `"Terminal"` $\rightarrow$ `["Term", "inal"]` (2 tokens)
    * `"echo 'hello'"` $\rightarrow$ `["echo", " '", "hello", "'"]` (4 tokens)

### Engineering Implications:
  1. **Attention Horizon (Context Window):** Total token volume (instructions, history, and active response) that the Transformer can concurrently correlate and maintain in active working memory.
  2. **API Consumption and Metering:** Commercial APIs meter and bill usage based on total processed tokens (with distinct rates for input vs. output tokens).

-----

## Context Window and Hyperparameters

Critical runtime parameters associated with LLMs:

  * **Context Window ($L_{\max}$) vs. Max Output Tokens:**
      * The total window (active memory holding history + prompt) reaches **1,000,000+ tokens** for reading/ingestion; generated output per call is capped much lower (e.g., **4,096** to **8,192 tokens**).
  * **Context Hygiene (Context Reset):**
      * **Best practice:** Clear the context window (start a new session or run `/clear`) when switching tasks.
      * Extended sessions accumulate stale history (*context drift*), inflate token costs, and substantially increase the risk of hallucinations.
  * **Sampling Temperature ($\tau$):**
      * **Low Temperature ($\tau = 0.0$ to $0.2$):** Deterministic, focused, and reproducible outputs (**mandatory for commands and code**).
      * **High Temperature ($\tau = 0.8$ to $1.2$):** Higher stochastic variance and creativity.

-----

## Hallucinations and Critical Engineering Verification

Operational vulnerabilities in model-generated command-line instructions:

  * The model may propose **non-existent flags and syntax options** (e.g., `tar -z --exclude-all-errors`).
  * Ambiguous prompts may elicit **irreversible destructive commands** (`rm -rf /tmp/..`).
  * The model may hallucinate libraries and packages absent from the host operating system.
  * **Context Pollution (Context Drift):** Mixing distinct tasks in the same session causes the model to anchor onto obsolete, conflicting premises.

### Operational Principle:
> **The generative model acts as an assistive mechanism; technical validation and execution responsibility rest solely with the engineer.**
> Reset context between distinct tasks and never execute commands without prior inspection (`man` or `--help`).

-----

## AI Interaction Paradigms in Software Engineering

From general-purpose browser chat to developer terminal automation:

\begin{center}
\includegraphics[height=0.68\textheight,keepaspectratio]{ai_interaction_paradigms.jpg}
\end{center}

-----

## Consumption Models: User Subscriptions vs. Programming Interfaces (APIs)

Distinguishing account-based access from direct programmatic consumption:

  * **User Account Subscriptions (Flat-Rate):**
      * Examples: Claude Pro, Copilot, Antigravity, ChatGPT Plus.
      * Fixed periodic fee associated with a user identity, supporting web interfaces, IDE extensions, and CLI environments via OAuth workflows.
      * Rate limiting enforced via **time-window request quotas**: quota exhaustion temporarily pauses requests with zero unexpected financial liability.

  * **Developer and Cloud APIs (Pay-as-you-go / Metered Consumption):**
      * Usage metered strictly per million tokens (input and output), authenticated via **API Keys**.
      * Standard requirement for headless automation, CI/CD pipelines, and shell scripts.
      * **Operational Risk:** No pre-configured maximum consumption ceilings by default; runaway loops incur continuous, direct financial charges.

-----

## API Cost Management and the Agent Multiplier Effect

Autonomous agents and automated scripts require rigorous financial discipline (**FinOps**):

  * **The Multiplier Effect in Multi-Step Agents:**
      * Across a 30-step reasoning trace, an agent transmits the **entire accumulated conversation history plus all ingested files** on every turn.
      * A 50,000-token repository executed across 30 iterations totals **1,500,000 input tokens** in a single test evaluation.
  * **The Hazard of Infinite Retry Loops:**
      * Faulty termination conditions in automation scripts trigger continuous, rapid API invocations, resulting in severe financial liabilities within minutes.

-----

## API Cost Management: Safeguards and Precautions

Essential safeguards and engineering best practices:

  1. **Hard Spend Limits:** Establish an unbreachable expenditure ceiling in the API console to immediately sever service access upon budget exhaustion.
  2. **Budget Alerts:** Always configure for consumption visibility as a best practice; however, be mindful of multi-hour processing latency—they inform reactively without halting ongoing execution in real time.
  3. **Code-Level Safeguards (*Loop Cap* & `max_output_tokens`):** Enforce strict iteration bounds in scripts (`MAX_RETRIES=5`) and limit output tokens in API payloads.
  4. **Unintentional API Key Exposure:** Avoid hardcoding keys directly into source code or scripts stored in repositories; always leverage environment variables and `chmod 600` permissions.
  5. **Free Tier Utilization in Educational Settings:** Google AI Studio (Free Tier) enforces strict per-minute rate limits (15 RPM) without credit card requirements.

-----

## The Command-Line Interface in the AI Ecosystem

Technical advantages underpinning shell adoption for generative model integration:

  * **Operational Composability:** Model outputs can be redirected directly into files, compilers, or analysis scripts via pipes (`|`).
  * **Headless Execution and Automation:** Scheduled background jobs (*cron*) or CI/CD pipelines communicate with models without GUI overhead.
  * **Native REST Interoperability:** Using `curl`, POSIX systems can query frontier foundation models with minimal latency.

-----

## API Integration via curl in the Terminal

Querying foundation models directly from the command-line interface using HTTP POST requests with JSON payloads to the modern **Gemini Interactions API**:

```bash
$ curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.5-flash-lite",
    "input": "Explain in 1 sentence: tar -czvf archive.tar.gz folder/"
  }'
```

  * **`-s` :** Silent mode (suppresses transfer meters).
  * **`-X POST` :** HTTP method for transmitting payload data.
  * **`-H "x-goog-api-key: $GEMINI_API_KEY"` :** Secure HTTP header authentication (prevents secret exposure in URL logs).
  * **`-H "Content-Type: application/json"` :** Header defining body content type.
  * **`model` and `input` :** Target model specification (`gemini-3.5-flash-lite`) and prompt payload.

-----

## Formulating Instructions: The Myth of Personas

When interacting with LLMs — whether through chat interfaces, terminal agents, or API payloads —, the central question arises: *how should effective technical instructions be formulated?*
In the early days of the technology, theatrical role assignment became widespread:
> *"Act as a world-class senior Linux systems engineer with 30 years of experience and answer..."*

### Empirical Behavior in Contemporary Models:
  * In formal tasks involving logic, computation, and software engineering, persona assignment yields zero statistical accuracy improvement.
  * Instead, it frequently introduces verbose conversational pleasantries and filler text.
  * Frontier models already encode technical knowledge; output precision depends strictly on **system context** and **clarity of operational constraints**.

-----

## Transition: From Prompt Engineering to Context Engineering

Engineering practice has evolved from empirical wording tricks to formal **Context Engineering**:

\vspace{0.8em}
\begin{center}
\begin{tikzpicture}[
    box/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\footnotesize},
    boxemp/.style={draw=black!40, fill=black!5, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\footnotesize},
    arr/.style={-{Latex[length=2.5mm]}, dashed, thick, color=uagreen!80!black}
]
\node[boxemp] (P) {\textbf{Empirical Prompting}\\\scriptsize(Personas \& Rhetorical Framing)};
\node[box, right=2.0cm of P] (C) {\textbf{Context Engineering}\\\scriptsize(Boundaries, Constraints \& Grounding)};
\draw[arr] (P) -- node[above, font=\scriptsize, text=black!70] {Methodological Shift} (C);
\end{tikzpicture}
\end{center}
\vspace{0.6em}

Foundation models are parameterized through deterministic principles:
  1. Unambiguous, direct specification of the target objective.
  2. Formal delimitation of input data (files, schemas, logs).
  3. Explicit negative constraints (prohibited behaviors).
  4. Mandatory structural format definitions for the output.

-----

## The Four Pillars of Context Engineering

Recommended specification structure for deterministic console integration:

| Component | Objective | Technical Example |
| :--- | :--- | :--- |
| **1. Task** | Direct statement of technical goal | *"Generate a Bash command to list files modified in the last 24 hours."* |
| **2. Context** | Runtime environment and input state | *"POSIX Linux environment (Ubuntu 24.04), Bash shell, target path /var/log."* |
| **3. Constraints** | Formal execution boundaries | *"Do not use external scripting interpreters (awk, python). Use find exclusively."* |
| **4. Format** | Structural syntax of the response | *"Return strictly the single-line command without markdown fences or commentary."* |

-----

## Structured Context Delimitation

When passing files or error logs to a model, **instructions** must be strictly isolated from **untrusted data** using unambiguous delimiters (e.g., XML tags or code blocks):

```markdown
Analyze the error log below and identify the affected service.

<error_log>
Sep 28 10:14:02 srv1 nginx[1420]: bind() to 0.0.0.0:80 failed (98: Address already in use)
Sep 28 10:14:02 srv1 systemd[1]: nginx.service: Failed with result 'exit-code'.
</error_log>

Respond in the following format:
Service: <name>
Cause: <reason>
```

Structured delimitation clarifies the boundary between components, reducing the risk of the model misinterpreting raw data or error logs as actionable instructions (*prompt injection*).

-----

## Calibrating with Examples: Zero-Shot vs. Few-Shot

Unlike direct instructions (**Zero-Shot**), **Few-Shot** prompting supplies solved input-output pairs so the model infers structure and fields by analogy (*in-context learning*), avoiding exhaustive rules:

```text
Analyze the technical incident and return a structured diagnosis.

[Example 1]
Input: Disk /dev/sda1 reached 98% capacity on /var partition.
Output:
  Severity:  HIGH
  Component: Storage (/var)
  Action:    Purge old log files and temporary artifacts

[Example 2]
Input: Three failed SSH authentication attempts for user root.
Output:
  Severity:  MEDIUM
  Component: Security (SSH)
  Action:    Inspect audit logs and block source IP address

[New Request to Process]
Input: Backup process consumed 95% CPU for 40 min.
Output:
  Severity:  HIGH                                    <-- [FIELDS
  Component: Processor (Backup)                      <--  GENERATED
  Action:    Adjust process priority (nice)          <--  BY MODEL]
```

-----

## Beyond One-Shot Invocations: Autonomous Agents

Paradigm shift: from **one-shot invocation** (static request-response) to **autonomous systems** operating continuously in closed loops on the environment:

* **Formal Definition of Agent (Computer Science & AI):**
    * An autonomous computational entity that **perceives its environment** via sensors, **deliberates** to pursue defined goals, and **acts upon the environment** via actuators in a closed loop (*Perceive $\rightarrow$ Reason $\rightarrow$ Act*).

* **Instantiation in Software Engineering (Coding Agents):**
    * **Environment:** The source repository, filesystem, and Linux shell environment.
    * **Perception (Sensors):** Reading files, inspecting compiler errors, and capturing command outputs (`stdout`/`stderr`).
    * **Reasoning (Deliberation):** Task decomposition, tool selection, and consultation of repository rules (`AGENTS.md`).
    * **Action (Actuators):** Automated file modifications and execution of build, test, and CLI commands.
    * **Feedback Loop:** Continuous evaluation of command exit codes and test results, iterating until goal criteria are met.

-----

## Control Architecture: AGENTS.md, Skills, and MCP

Controlling and extending autonomous agents in software engineering relies on three complementary pillars:

\vspace{0.6em}
\begin{center}
\begin{tikzpicture}[
    agentbox/.style={draw=black!70, fill=black!5, rounded corners=4pt, thick, align=center, inner sep=5pt, font=\small},
    pillar/.style={draw=uagreen!80!black, fill=uagreen!8, rounded corners=3pt, thick, align=center, inner sep=4pt, text width=3.4cm, font=\scriptsize},
    arr/.style={-{Latex[length=2.2mm]}, thick, color=black!70}
]
\node[agentbox] (AGENT) {\textbf{AI Agent}};
\node[pillar, below=0.7cm of AGENT] (R2) {\textbf{2. Skills}\\\textbf{Modular Playbooks}\\\textit{\tiny(On-demand specialized knowledge)}};
\node[pillar, left=0.35cm of R2] (R1) {\textbf{1. AGENTS.md}\\\textbf{Constitution \& Rules}\\\textit{\tiny(Permanent repository context)}};
\node[pillar, right=0.35cm of R2] (R3) {\textbf{3. MCP Protocol}\\\textbf{Tool Connectors}\\\textit{\tiny(Standardized tool bridge)}};

\draw[arr] (AGENT.south) -- (R1.north);
\draw[arr] (AGENT.south) -- (R2.north);
\draw[arr] (AGENT.south) -- (R3.north);
\end{tikzpicture}
\end{center}
\vspace{0.4em}

Detailed examination of each architectural component:

-----

## Repository Specification: The AGENTS.md File

### Concept and Purpose:

  * Markdown specification file located at the repository root or within specific folders accessible to the agent.
  * Serves as the authoritative reference document and behavioral constitution for AI assistants and autonomous agents operating on the codebase.
  * Development environments and agents (Antigravity, Cursor, Claude Code, Copilot) automatically ingest this context prior to code generation or task execution.
  * **Hierarchical Scope:** Can be declared globally at the project root or scoped to subdirectories (e.g., `frontend/AGENTS.md`, `backend/AGENTS.md`).

-----

## Repository Specification: The AGENTS.md File

### Operational Objectives:
  * Precludes the introduction of unwarranted technologies or unapproved third-party dependencies.
  * Enforces compliance with team coding conventions, architectural standards, and error-handling patterns.
  * Establishes explicit execution boundaries (prohibiting destructive operations and mandating test verification).

-----

## Typical Structure of an AGENTS.md File

Example of a normative specification for a lab project repository:

```markdown
# Engineering Guidelines: IEI Project

## 1. Environment & Technical Stack
- Operating System: POSIX Linux (Ubuntu 24.04 / WSL 2).
- Script Interpreter: Bash 5.x. Scripts must start with `#!/bin/bash`.

## 2. Standard Execution Commands
- Tests: execute `make test` before committing changes.
- Compilation: execute `make all`.

## 3. Code Conventions & Security
- Never include hardcoded credentials or API keys.
- Do not introduce external dependencies without authorization.
- Local script variables must use descriptive lowercase identifiers.
```

-----

## Standardizing AGENTS.md in Software Projects

::::: columns
::: {.column width="60%"}

  * **Project Commands (Required):**
    * Deterministic commands for build, lint, dev server, and tests.
  * **Code Structure (Required):**
    * Directory layout map (`src/api`, `src/core`, `tests/`) preventing blind agent exploration.
  * **Conventions and Style (Recommended):**
    * Strict typing, docstring formats, and Git commit standards (*Conventional Commits*).
  * **Boundaries & Guardrails (Critical):**
    * Explicit declaration of files and directories the agent **must not modify** (e.g., migrations, secrets).

\vspace{0.3em}
\textit{\tiny Reference: Addy Osmani, \href{https://addyosmani.com/agents/15-agents-md/}{addyosmani.com/agents/15-agents-md/}}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.74\textheight,keepaspectratio]{agents_md_template_generator.png}
\end{center}

:::
:::::

-----

## Case Study: AGENTS.md in a Production Software Project

Complete specification for a backend service (FastAPI, PostgreSQL, and Poetry):

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
\textit{\tiny Source: Addy Osmani, \href{https://addyosmani.com/agents/15-agents-md/}{addyosmani.com/agents/15-agents-md/}}

:::
:::::

-----

## Impact of Context on Agent Behavior

Comparative analysis for the identical technical request: *"Generate the project backup script."*

### Without `AGENTS.md` (Ungrounded inference):

```python
# The model introduces Python and third-party cloud SDKs
import boto3
s3 = boto3.client('s3')
s3.upload_file('backup.zip', 'my-bucket', 'backup.zip')
```
*(Incompatible with the project requirement for native Bash utilities)*

### With `AGENTS.md` (Compliant with repository operational contract):

```bash
#!/bin/bash
set -euo pipefail
tar -czvf "backup_$(date +%Y%m%d).tar.gz" .
echo "Backup completed successfully."
```
*(Strict alignment with the environment and conventions specified for the repository)*

-----

## Rigorous Safety: Soft vs. Hard Guardrails

Fundamental axiom of artificial intelligence systems security:
> **"Natural language prompts do not constitute security boundaries."**

Prohibiting commands within `AGENTS.md` (e.g., *"Never execute `rm -rf`"*) forms a **Soft Boundary**:
  * The model cooperates based on probabilistic instruction adherence, which can be bypassed via **Prompt Injection** (adversarial payloads in processed files) or hallucination.

-----

## Rigorous Safety: Soft vs. Hard Guardrails

### Deterministic Hard Guardrails
System integrity requires deterministic enforcement mechanisms external to the model:

  * **Tool Execution Interceptors / Allowlists:**
      * Deterministic software modules that inspect commands prior to OS invocation, halting execution if unauthorized patterns are detected.
  * **Human-in-the-Loop (HITL):**
      * Mandatory requirement for explicit interactive operator confirmation before executing operations with irreversible side effects.
  * **Containerized Sandboxing (Docker):**
      * Execution within disposable containers lacking administrative privileges, with sensitive host filesystem trees mounted read-only.

-----

## Skills: Modular On-Demand Procedures

While `AGENTS.md` establishes repository-wide operational rules, a **Skill** specifies an in-depth procedure for a specialized task:

  * **Context Efficiency Principle:**
      * Ingesting every operational procedure into `AGENTS.md` would saturate context windows with task-irrelevant instructions.
  * **Operational Model:**
      * A skill is encapsulated in a dedicated directory containing a descriptor `SKILL.md`, loaded into agent context strictly when triggered by functional needs.
      * Examples: *Command Security Audit Skill*, *SQL Schema Migration Skill*, *Accessibility Compliance Skill*.

-----

## Implementation of a Skill: safe-cli


```markdown
---
name: safe-cli
description: Evaluates safety and risk levels of UNIX commands (Linux and macOS).
---

# Analysis Procedure:
When receiving a command for inspection:
1. Classify risk level: [SAFE], [CAUTION], or [DANGEROUS].
2. Summarize command intent in a single technical sentence.
3. Decompose and explain each option and argument utilized.
4. If the command involves destructive operations (rm, dd, chmod 777, redirection >),
   highlight the potential hazard and supply a safe alternative.
```

-----

## Model Context Protocol (MCP): Connectivity Architecture

  * **Historical Fragmentation:** Software tools previously developed proprietary *ad-hoc* plugins for database querying, Git inspection, or filesystem access.
  * **Client-Server Architecture:**
      * **MCP Server:** exposes tools, resources, and execution endpoints under defined access controls.
      * **MCP Client (IDE/Agent):** mediates between model inference and tool invocation.

\vspace{0.3em}
\begin{center}
\begin{tikzpicture}[
    clientbox/.style={draw=black!70, fill=black!5, rounded corners=4pt, thick, align=center, inner sep=5pt, font=\footnotesize},
    serverbox/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=3pt, text width=3.2cm, font=\scriptsize},
    arr/.style={{Latex[length=2mm]}-{Latex[length=2mm]}, thick, color=uagreen!80!black}
]
\node[clientbox] (IDE) {\textbf{Agent / IDE}\\\scriptsize(MCP Client)};
\node[serverbox, right=2.6cm of IDE.center, yshift=1.05cm] (S1) {\textbf{Git Server}\\\tiny(commits, branches, diffs)};
\node[serverbox, right=2.6cm of IDE.center] (S2) {\textbf{Database Server}\\\tiny(SQL queries, schema discovery)};
\node[serverbox, right=2.6cm of IDE.center, yshift=-1.05cm] (S3) {\textbf{Filesystem Server}\\\tiny(secure file reads/writes)};

\draw[arr] (IDE.east) -- node[above, sloped, font=\tiny, text=black!70] {MCP Protocol} (S1.west);
\draw[arr] (IDE.east) -- node[above, font=\tiny, text=black!70] {MCP Protocol} (S2.west);
\draw[arr] (IDE.east) -- node[below, sloped, font=\tiny, text=black!70] {MCP Protocol} (S3.west);
\end{tikzpicture}
\end{center}
\vspace{0.2em}

MCP establishes resource access under explicit permissions and standardized wire protocols.

-----

## MCP in Practice: Tool Implementation and Registration

Example of local inter-process connectivity via standard I/O channels (\texttt{stdio}):

::::: columns
::: {.column width="50%"}

### 1. MCP Server (`git_server.py`) - exposes capability:
```python
# SDK to implement MCP
from mcp.server.fastmcp import FastMCP
import subprocess

# MCP server instance name
mcp = FastMCP("git-tools")

# Registers tool for the LLM
@mcp.tool()
def git_status() -> str:
    # Description so the LLM knows what this method does
    """Returns modified working files."""
    return subprocess.check_output(
        # Command to execute in the operating system
        ["git", "status", "-s"], text=True
    )

if __name__ == "__main__":
    # Starts server communicating via stdio (JSON-RPC)
    mcp.run()
```

:::
::: {.column width="50%"}

### 2. Client (IDE / Agent) Registration (`mcp_config.json`):
```json
{
  "mcpServers": {
    "git-tools": {
      "command": "python",
      "args": ["git_server.py"]
    }
  }
}
```

:::
:::::

-----

## Technical References and Resources

Authoritative reference documentation and technical standards:

  * **Google AI Studio (API Key Provisioning and Console):**
      * [https://aistudio.google.com/](https://aistudio.google.com/)
  * **Google Gemini API Official Documentation:**
      * [https://ai.google.dev/docs](https://ai.google.dev/docs)
  * **Model Context Protocol (MCP) Open Specification:**
      * [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
    * **Anthropic Context Engineering and Prompt Design Guides:**
      * [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
  * **Addy Osmani — Building Effective Agents with AGENTS.md:**
      * [https://addyosmani.com/agents/15-agents-md/](https://addyosmani.com/agents/15-agents-md/)
