---
title: 47138 - Introduction to Computer Engineering
subtitle: "Version Control with Git & Collaborative Platform GitHub"
institute: Universidade de Aveiro
date: November 02, 2026
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

  * **Part I — Version Control Fundamentals & Architecture:**
      * The challenge of code evolution and collaboration, pitfalls of naive approaches (manual copies and cloud sync), VCS taxonomy, comparative matrix (CVCS vs. DVCS), and Git as the de facto industry standard.
  * **Part II — Git Functional Aspects & Local Lifecycle:**
      * Core concepts (`Repository`, `Commit`, `Branch`, `HEAD`), the three operational areas and file states, essential commands (`init`, `clone`, `status`, `add`, `commit`), Conventional Commits standard, `log`, tagging (`tag`), and `.gitignore`.
  * **Part III — Branching, Integration & Conflict Resolution:**
      * Branch pointer model and `HEAD`, merge integration strategies (fast-forward vs. 3-way merge), linearization with `rebase`, comparative matrix, and conflict resolution.
  * **Part IV — Distributed Collaboration & Team Workflows:**
      * Remote repositories (`origin`), network synchronization (`fetch`, `pull`, `push`), collaborative workflows (*GitFlow* vs. *Trunk-Based Development*), *Feature Branches* with *Pull Requests*, and release management (*releases*).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: Version Control Fundamentals \& Architecture}}
\end{center}

-----

## The Challenge of Code Evolution and Team Collaboration

Software engineering is inherently dynamic and collaborative:

  * **Dynamic Nature of Code:**
      * Continuous evolution: bug fixing, feature additions, and refactoring.
      * Dozens or thousands of interdependent files changing concurrently.
  * **Three Core Engineering Dilemmas:**
      * **Traceability:** *What* changed, *when*, *why*, and by *whom*?
      * **Reversibility:** How to test new ideas without breaking stable, working code?
      * **Concurrent Collaboration:** How to work in teams without overwriting each other's work?

\vspace{0.8em}

\begin{center}
\textbf{Faced with these challenges, what were the most common intuitive (and flawed) attempts?}
\end{center}

-----

## Naive Approaches (I): The Chaos of Manual File Copies

::::: columns
::: {.column width="60%"}

The immediate reaction to save old versions and test new ideas is duplicating files:

  * **The Suffix Anti-Pattern:**
      * `project_v1.c`, `project_v2_fixed.c`
      * `project_final.c`, `project_final_REALLY_FINAL.c`
  * **Why Does It Fail?**
      * **Opacity:** File names do not reveal which lines or functions changed.
      * **Missing Context:** The rationale (*why*) behind changes is lost.
      * **Fragile Reversibility:** Reverting one file breaks whole-project consistency.
      * **Unreliable Dates:** OS timestamps are easily corrupted when copying.

\vspace{0.4em}
\textbf{Manual duplication is opaque, error-prone, and unsustainable for real engineering projects.}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.72\textheight,keepaspectratio]{figures/phd_not_final.png}

\vspace{0.2em}
\textit{\tiny "notFinal.doc" --- Jorge Cham (PhD Comics)}
\end{center}

:::
:::::

-----

## Naive Approaches (II): Cloud Synchronization and Email Sharing

To address **team collaboration**, developers instinctively turn to consumer sharing tools:

  * **1. Cloud Shared Folders (Dropbox, Google Drive):**
      * **Wrong Tool:** Built to sync office documents, not source code.
      * **Blind Overwrites (*Last-Write-Wins*):** The last save silently overwrites teammates' work.
      * **Destructive Duplicates:** Concurrent edits create uncoordinated copies (`Conflicted Copy`), without code merging.
  * **2. Emailing Compressed Archives (.zip):**
      * Exchanging versions (`project_v3_alice.zip` vs. `project_v3_bob.zip`).
      * **Manual Merge Nightmare:** Merging line-by-line via copy-paste is tedious, error-prone, and unscalable.

\vspace{0.8em}

\begin{center}
\textbf{File synchronization $\neq$ Version control. Collaboration requires structured code reconciliation.}
\end{center}

-----

## The Solution: Version Control Systems (VCS)

A **VCS** is an engineering tool that systematically records the historical evolution of a project:

  * **Full Traceability:** Records *who*, *when*, and *why* (commit messages).
  * **Reversibility (*Time Machine*):** Instant rollback to any verified, stable prior state.
  * **Differential Analysis:** Line-by-line inspection of changes (*diffs*) between arbitrary versions.
  * **Safe Collaboration:** Parallel development across teams with structured conflict reconciliation.

\vspace{0.8em}

\begin{center}
\textbf{A VCS transforms software development into a secure, auditable, and reproducible process.}
\end{center}

-----

## VCS Taxonomy: Centralized vs. Distributed

\begin{center}
\includegraphics[width=\linewidth,height=0.80\textheight,keepaspectratio]{figures/vcs_centralized_vs_distributed.png}
\end{center}

-----

## Comparative Matrix: CVCS vs. DVCS

| Comparison Vector | Centralized VCS (e.g., SVN / Perforce) | Distributed VCS (e.g., Git / Mercurial) |
| :--- | :--- | :--- |
| **Local Repository & History** | Only the current working copy | **Complete clone with full project history** |
| **Offline Operation** | Limited (only editing and `diff` against current base) | **Full (`commit`, `branch`, `log`, `merge` 100% local)** |
| **Fault Tolerance (SPOF)** | Low (central server downtime halts submissions) | **High (every full clone acts as a complete backup)** |
| **Operation Speed** | Constrained by network latency to server | **Near instantaneous (local disk/memory I/O)** |
| **Version Identification** | Global sequential numbers (`r1`, `r2`, `r3`...) | **Distributed cryptographic hashes (SHA)** |
| **Branching & Merging** | Heavyweight (server directories; historically slow merges) | **Lightweight & instant (local pointers; fast merging)** |
| **Large Binaries & Locking** | **Excellent (central *file locking* and partial checkouts)** | Weak natively (bloats history; no offline lock; needs *Git LFS*) |
| **Access Control (Security)** | **Granular (read/write permissions per folder/file)** | Repository-wide (cloning grants access to entire tree) |

-----

## Git: The De Facto Industry Standard

::::: columns
::: {.column width="66%"}

  * **Universal Adoption ($>90\%$ of the Industry):**
      * **Open-source** tool that has become the undisputed standard and the lingua franca of contemporary software engineering.
  * **Pragmatic Origin (2005):**
      * Created by **Linus Torvalds** for the **Linux Kernel**, requiring a free, fast distributed system capable of scaling to thousands of developers.
  * **Why Did It Conquer the Industry?**
      * **Local Performance:** Operations execute directly on local disk (in native C), free from network latency penalties.
      * **Lightweight Branching ($O(1)$):** Creating branches simply writes lightweight pointers, enabling frictionless parallel work.
      * **Cryptographic Integrity:** History structured by SHA hashes (impossible to tamper with or corrupt data **undetected**).

:::
::: {.column width="34%"}

\begin{center}
\includegraphics[width=0.65\linewidth,keepaspectratio]{figures/git_logo.png}

\vspace{0.4em}
\includegraphics[width=0.95\linewidth,keepaspectratio]{figures/git_branching_illustration.png}

\vspace{0.3em}
{\scriptsize \href{https://git-scm.com/}{\texttt{git-scm.com}}}
\end{center}

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part II: Git Functional Aspects \& Local Lifecycle}}
\end{center}

-----

## Core Git Concepts: The Mental Model

::::: columns
::: {.column width="55%"}

  * **1. Repository (*Repository* / `.git/`):**
      * Local database storing the complete history and metadata.
  * **2. Commit (*Snapshot*):**
      * Immutable restoration point recording code evolution.
      * Identified by a **SHA Hash** (e.g., \texttt{98ca9c2}).
  * **3. Branch:**
      * Represents an independent line of code evolution.
      * Lightweight, movable pointer to a commit (`main`, `feature`).
  * **4. `HEAD` Pointer:**
      * Indicator pointing to the currently checked-out branch and commit.

:::
::: {.column width="45%"}

\vspace{0.3em}

\begin{center}
\begin{tikzpicture}[
    commit/.style={circle, draw=uagreen!80!black, fill=uagreen!15, thick, font=\tiny\bfseries, inner sep=1pt, minimum size=5.5mm},
    branch/.style={rectangle, draw=blue!70!black, fill=blue!10, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, inner sep=2pt},
    head/.style={rectangle, draw=red!70!black, fill=red!10, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, inner sep=2pt},
    arr/.style={-{Latex[length=1.6mm]}, thick, color=black!70},
    repo/.style={draw=black!30, dashed, rounded corners=4pt, fill=black!2}
]
% Enclosure
\draw[repo] (-0.5,-1.65) rectangle (4.6,1.4);
\node[anchor=north west, font=\tiny\bfseries, color=black!60] at (-0.45,1.35) {Repository (.git/)};

% Commits with short SHA hashes
\node[commit] (C1) at (0.2,0) {C1};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (0.2,-0.32) {98ca9c2};

\node[commit] (C2) at (1.3,0) {C2};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (1.3,-0.32) {34ac2e1};

\node[commit] (C3) at (2.4,0.6) {C3};
\node[anchor=south, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (2.4,0.92) {f30ab12};

\node[commit] (C4) at (2.4,-0.6) {C4};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (2.4,-0.92) {7a12dc8};

% Commit arrows (chronological evolution of code)
\draw[arr] (C1) -- (C2);
\draw[arr] (C2) -- (C3);
\draw[arr] (C2) -- (C4);

% Branches
\node[branch] (main) at (3.7,0.6) {main};
\draw[arr, color=blue!70!black] (main) -- (C3);

\node[branch] (feat) at (3.7,-0.6) {feature};
\draw[arr, color=blue!70!black] (feat) -- (C4);

% HEAD pointing to active branch (feature)
\node[head] (head) at (3.7,-1.25) {HEAD};
\draw[arr, color=red!70!black] (head) -- (feat);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## The Three Operational Areas of Git

Locally, files in a Git repository move across three distinct operational areas:

  * **1. Working Tree / Directory:**
      * The visible local directory where developers inspect, create, and edit files using their standard editors.
      * Files are extracted from the Git database for direct manipulation.
  * **2. Staging Area / Index:**
      * Intermediate selection layer (recorded in `.git/index`).
      * Allows surgically choosing which specific changes will be included in the next commit, rather than committing everything at once.
  * **3. Local Repository (`.git`):**
      * The database where Git permanently and compactly records all project commits (*snapshots*).

-----

## Operational Flow and File States

\vspace{0.4em}

\begin{center}
\begin{tikzpicture}[
    box/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\scriptsize, minimum width=2.6cm, minimum height=1.1cm},
    arr/.style={-{Latex[length=2.2mm]}, thick, color=black!75},
    arrback/.style={-{Latex[length=2.2mm]}, dashed, thick, color=red!70!black}
]
\node[box] (WT) {\textbf{Working Tree}\\\textit{Local Disk Files}};
\node[box, right=1.2cm of WT] (SA) {\textbf{Staging Area}\\\textit{Index / Prepared State}};
\node[box, right=1.2cm of SA] (RP) {\textbf{Local Repository (.git)}\\\textit{Permanent Snapshots}};

\draw[arr] (WT.north east) -- node[above, font=\tiny\ttfamily] {git add} (SA.north west);
\draw[arr] (SA.north east) -- node[above, font=\tiny\ttfamily] {git commit} (RP.north west);

\draw[arrback] (SA.south west) -- node[below, font=\tiny\ttfamily] {git restore --staged} (WT.south east);
\draw[arrback] (RP.south) to[bend left=25] node[below, font=\tiny\ttfamily] {git checkout / switch} (WT.south);
\end{tikzpicture}
\end{center}

\vspace{0.3em}

As files move across these areas, each file assumes one of **four states**:

  * **Untracked:** New file in the *Working Tree* not yet monitored by Git.
  * **Modified:** Tracked file whose content on disk differs from the latest commit.
  * **Staged:** Modification indexed in the *Staging Area* (`git add`), ready for the next commit.
  * **Unmodified:** File recorded in the *Repository* (`git commit`), with no pending local edits.

-----

## Repository Initialization and Cloning

There are two ways to establish a local Git repository:

  * **1. Initialize a New Repository (`git init`):**
      * Converts an existing local folder into a Git repository:
        ```bash
        mkdir my-project && cd my-project
        git init
        # Initialized empty Git repository in /path/my-project/.git/
        ```
  * **2. Clone an Existing Repository (`git clone`):**
      * Downloads a full copy of a remote repository (history, branches, and tags):
        ```bash
        git clone https://github.com/user/my-project.git
        ```

\vspace{0.3em}

  * Both commands create the hidden **`.git/`** directory, which houses the entire local database.

-----

## Local Cycle Commands: `status` and `add`

::::: columns
::: {.column width="45%"}

  * **Inspecting with `git status`:**
      * Reveals file states across local workspaces.
      * **Red:** Unstaged changes (*Untracked* / *Modified*).
      * **Green:** Changes ready in the *Staging Area* (*Staged*).
  * **Staging with `git add`:**
      * Promotes changes into the *Staging Area*:
        ```bash
        git add main.c   # Specific file
        git add src/     # Directory
        git add .        # Current dir
        git add -p       # Interactive hunks
        ```

:::
::: {.column width="55%"}

\vspace{0.4em}
\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/git_status_add_en.png}
\end{center}

:::
:::::

-----

## Recording Snapshots: `git commit`

The `git commit` command consolidates the *Staging Area* content into a new immutable snapshot in the repository:

```bash
git commit -m "feat: implement user authentication credential validator"
```

  * **Operational Mechanics:**
      * Git packages the changes prepared in the *Staging Area*, computes their **SHA Hash**, and links the new commit to its predecessor (*parent*).
      * The active branch (e.g., `main`) and the `HEAD` pointer automatically advance to this new commit.
  * **Principle of Atomicity:**
      * Each commit must represent a **single, cohesive logical unit** of work (avoid mixing formatting cleanups with bug fixes in the same commit).
      * Makes it safe to revert or audit a specific change without unintended side effects.

-----

## Commit Message Best Practices

::::: columns
::: {.column width="50%"}

  * **Core Principle:**
      * Code (`diff`) shows **what** changed; the message must explain **why** it was needed.
  * **Industry 50/72 Convention:**
      * **Imperative Mood:** Write as a command (e.g., `Add`, `Fix`, `Resolve`, not *Added* or *Fixed*).
      * **Subject ($\le 50$ chars):** Concise, capitalized, no trailing period.
      * **Body ($\le 72$ chars/line):** Separated from subject by a **blank line**; explains motivation and impact.

:::
::: {.column width="50%"}

  * **Anti-Pattern (Zero Value):**
    ```bash
    git commit -m "fix stuff and updates"
    ```

  * **Recommended Model (50/72 Rule):**
    ```text
    Fix: Resolve expired session validation

    Prior check ignored Redis TTL timestamps,
    allowing stale tokens to be reused.

    Add strict expiration verification and
    return HTTP 401 Unauthorized.
    ```

:::
:::::

-----

## Standardizing with Conventional Commits (I): Structure and Types

::::: columns
::: {.column width="48%"}

  * **Concept & Anatomy:**
      * Lightweight convention for structured commit messages, readable by humans and tooling.
  * **Canonical Structure:**
    ```text
    <type>[optional scope]: <description>

    [optional body]

    [optional footer]
    ```
  * **Practical Examples:**
    ```bash
    git commit -m \
      "feat(auth): add JWT token support"

    git commit -m \
      "fix(api): resolve login timeout"
    ```

:::
::: {.column width="52%"}

  * **Common Canonical Types:**
      * `feat:` A new feature for the user.
      * `fix:` A bug fix in existing code.
      * `docs:` Documentation-only changes.
      * `refactor:` Code restructuring without functional changes.
      * `test:` Adding or refactoring automated tests.
      * `chore:` Maintenance tasks or dependency updates.
      * `ci:` / `build:` CI/CD pipelines, builds, or tooling.

:::
:::::

-----

## Standardizing with Conventional Commits (II): Automation and Lifecycle

::::: columns
::: {.column width="46%"}

  * **Why Adopt in Engineering?**
      * **Automated Changelogs:**
          * CI/CD tools parse git history to automatically generate categorized release notes.
      * **Semantic Versioning (SemVer):**
          * `fix:` $\rightarrow$ bumps **PATCH** version (`x.y.Z`)
          * `feat:` $\rightarrow$ bumps **MINOR** version (`x.Y.z`)
          * `BREAKING CHANGE:` $\rightarrow$ bumps **MAJOR** (`X.y.z`)
      * **Traceability and Review:**
          * Streamlines *code reviews*, triage, and auditing across teams.

:::
::: {.column width="54%"}

\centering
\includegraphics[width=\linewidth,keepaspectratio]{figures/git_conventional_commits.png}

\vspace{0.4em}

\footnotesize
\textbf{Official Specification:} \href{https://www.conventionalcommits.org/}{\texttt{conventionalcommits.org}}

:::
:::::

-----

## Inspecting History: `git log`

The `git log` utility provides deep inspection and filtering across the commit graph:

```bash
# 1. Full standard commit log
git log

# 2. Compact single-line summary (Short SHA + Subject)
git log --oneline

# 3. ASCII visual graph of branches and merge topologies
git log --graph --oneline --all

# 4. Display inline line diffs for the latest 2 commits
git log -p -2

# 5. File modification statistics (files changed, insertions, deletions)
git log --stat
```

-----

## Tagging Commits: `git tag`

A **Tag** is an immutable, static pointer referencing a specific commit in the project history:

::::: columns
::: {.column width="50%"}

  * **Concept & Purpose:**
      * Acts as a permanent milestone or release label.
      * Unlike a branch, a tag **does not move** when new commits are created.
  * **Semantic Versioning ([SemVer](https://semver.org/)):**
      * Standardized format: `vMAJOR.MINOR.PATCH`
        * `v1.0.0` $\rightarrow$ Initial stable release
        * `v1.1.0` $\rightarrow$ Backward-compatible new feature
        * `v1.1.1` $\rightarrow$ Backward-compatible bug fix (*patch*)
      * Specification: \href{https://semver.org/}{\texttt{semver.org}}

:::
::: {.column width="50%"}

  * **Key Commands:**
    ```bash
    # 1. Create a tag at the current commit (HEAD)
    git tag v1.0.0

    # 2. Create a tag at an earlier commit
    git tag v0.9.0 9f1a2b3

    # 3. List all existing tags
    git tag

    # 4. View commits with tags
    git log --oneline --decorate
    ```
  * Tags enable deterministic checkout and auditing of any released version.

:::
:::::

-----

## Excluding Build Artifacts: `.gitignore`

Transient or environment-specific files must never enter the repository database:

  * **Mandatory Exclusions:**
      * Compiled binaries and object files (`*.o`, `*.class`, `*.exe`).
      * Downloaded dependencies (`node_modules/`, `.venv/`).
      * Secrets, API credentials, and local environment configs (`.env`).
      * Operating system and editor caches (`.DS_Store`, `.vscode/`).
  * **Structured `.gitignore` Example:**
    ```gitignore
    # Build directories and artifacts
    bin/
    build/
    *.o

    # Language environments
    .venv/
    __pycache__/

    # Sensitive files and OS metadata
    .env
    .DS_Store
    ```

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: Branching, Integration \& Conflict Resolution}}
\end{center}

-----

## The Git Branching Paradigm

In many traditional version control systems, creating a branch required copying entire source code directories:

  * **In Git, a Branch is a Lightweight Movable Pointer:**
      * Consists of a simple 41-byte file (40-character SHA-1 hash + `\n`) pointing to a commit.
      * **Creating or deleting** branches takes **constant time ($O(1)$)**; **switching** branches only updates the files that differ in the *Working Tree*.
  * **The Special `HEAD` Pointer (Symbolic Reference):**
      * Points to the **active branch** currently checked out (e.g., `HEAD` $\rightarrow$ `main`).
      * When a new commit is created, the active branch pointer automatically moves forward to the new snapshot (and `HEAD` follows by pointing to it).
  * **Purpose:** Isolate new feature development, experiments, or bug fixes without destabilizing the main line (`main`).

-----

## Essential Branch Management Commands

Standard operations for branch creation, inspection, and switching:

```bash
# 1. Create a new branch without switching
git branch feature-auth

# 2. Switch to an existing branch (modern syntax)
git switch feature-auth

# 3. Create and checkout in a single atomic step
git switch -c feature-auth        # Recommended modern syntax
git checkout -b feature-auth      # Equivalent classic syntax

# 4. List all local and tracking remote branches
git branch -a

# 5. Safely delete an already merged branch
git branch -d feature-auth
```

-----

## Structural Visualization of Branches

\begin{center}
\includegraphics[width=0.85\linewidth,keepaspectratio]{figures/git_branch_00.png}
\end{center}

  * **Main Branch (`main`):** Stable, deployable trunk line.
  * **Feature Branches:** Isolated exploratory branches created for individual tasks.
  * Completion culminates in integrating changes back into the mainline via `git merge`.

-----

## Integration Strategies: `git merge`

\begin{center}
\includegraphics[width=\linewidth,height=0.36\textheight,keepaspectratio]{figures/git_merge_types_en.png}
\end{center}

\vspace{-0.6em}

::::: columns
::: {.column width="45%"}

  * **Terminal Command Sequence:**
    ```bash
    # 1. Switch to the target branch
    git switch main

    # 2. Merge the feature branch
    git merge feature-auth
    ```

:::
::: {.column width="55%"}

  * **1. Fast-Forward Merge (Linear):**
      * `main` simply advances ($O(1)$) to `feature` (**creates no new commits**).
  * **2. 3-Way Merge (Divergent):**
      * Reconciles common ancestor and both tips into a new **Merge Commit**.

:::
:::::

-----

## The Challenge of Repeated Merges: Tangled History

\begin{center}
\includegraphics[width=\linewidth,height=0.46\textheight,keepaspectratio]{figures/git_messy_history.png}
\end{center}

\vspace{-0.4em}

::::: columns
::: {.column width="50%"}

  * **The Problem ("Spaghetti Graph"):**
      * Repeated syncing with `git merge` generates dozens of redundant merge commits (*"Merge branch 'main' into..."*).
      * Commit history becomes cluttered with administrative noise rather than meaningful functional changes.

:::
::: {.column width="50%"}

  * **Impact & Alternative:**
      * **Impaired Traceability:** Makes `git log` chaotic and disrupts automated debugging with `git bisect`.
      * **Solution:** How to keep branches up-to-date with a clean, linear history? $\rightarrow$ `git rebase`!

:::
:::::

-----

## Linearizing History with `git rebase`

::::: columns
::: {.column width="48%"}

  * **Concept & Mechanism:**
      * Detaches commits from `feature` and reapplies them sequentially on top of updated `main`.
      * Produces new commits (`E'`, `F'`, `G'`) with new SHA hashes, yielding a strictly linear graph.

  * **Recommended Terminal Workflow:**
    ```bash
    # 1. Update local main with remote
    git switch main
    git pull --rebase

    # 2. Reapply feature on top of main
    git switch feature-auth
    git rebase main
    ```

  * **The Golden Rule of Rebase:**
      * **NEVER** rebase public branches shared with other collaborators. Rewriting public history breaks team synchronization.

:::
::: {.column width="52%"}

\centering
\includegraphics[width=\linewidth,height=0.82\textheight,keepaspectratio]{figures/git_merge_vs_rebase_bytebytego.jpg}

:::
:::::

-----

## Comparative Matrix: `git merge` vs. `git rebase`

| Criterion | `git merge` | `git rebase` |
| :--- | :--- | :--- |
| **History Topology** | Non-linear (preserves branch graph and merges) | **Strictly linear (single continuous line)** |
| **Hash Immutability** | **Preserves original commit SHA hashes** | Rewrites and recalculates all hashes |
| **Merge Commit** | Creates explicit merge commit (unless fast-forward) | **Does not create merge commits** |
| **Chronological Fidelity** | Exactly preserves real-world timeline | Reorders commits onto new base |
| **Team Collaboration Safety**| **Safe on shared public branches** | **Dangerous on public/collaborative branches** |
| **Primary Use Case** | Formal release and mainline feature integration | Local feature branch cleanup before PR |

-----

## Merge Conflict Detection and Resolution

A **merge conflict** occurs when concurrent branches introduce contradictory changes to the **same lines within the same file**:

  * Git pauses the merge operation and injects visible conflict markers:
    ```text
    <<<<<<< HEAD (state in current branch, e.g., main)
    int timeout_ms = 5000;
    =======
    int timeout_ms = 10000;
    >>>>>>> feature-auth (state in branch being merged)
    ```
  * **Standard Resolution Protocol:**
      1. Open the conflicted file and decide upon the correct unified code.
      2. Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
      3. Stage the resolved file with `git add <file>`.
      4. Complete the merge transaction by executing `git commit`.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part IV: Distributed Collaboration \& Team Workflows}}
\end{center}

-----

## Distributed Architecture: Remote Repositories

In a DVCS, code sharing operates between peer repositories via networked remotes:

  * **Remote Definition:**
      * A named alias pointing to the network location (SSH or HTTPS URI) of another clone.
  * **The Canonical `origin` Name:**
      * Default conventional name assigned to the remote repository from which a clone originated.
  * **Remote Configuration Commands:**
    ```bash
    # List configured remotes and their network URLs
    git remote -v

    # Associate a new remote under the alias 'origin'
    git remote add origin https://github.com/ua-deti/iei-repo.git

    # Update the network URL of an existing remote
    git remote set-url origin git@github.com:ua-deti/iei-repo.git
    ```

-----

## Remote Synchronization: `fetch`, `pull`, and `push`

Bidirectional network synchronization involves three core operational primitives:

  * **1. `git fetch origin`:**
      * Downloads new commits, branches, and tags from the remote server into local tracking branches (`origin/main`).
      * **Does not alter your working tree or current branches**.
  * **2. `git pull origin main`:**
      * Combines `git fetch` immediately followed by `git merge` into the active local branch.
  * **3. `git push origin feature-auth`:**
      * Uploads local commits to the corresponding remote branch on the server.

-----

## Git vs. GitHub: Architectural Distinction

Engineers must maintain a clear conceptual distinction between the engine and the platform:

| Comparison Vector | Git | GitHub |
| :--- | :--- | :--- |
| **Primary Nature** | **CLI version control engine and protocol** | **Cloud collaboration platform and hosting (SaaS)** |
| **Execution Host** | Local workstation / operating system | Distributed cloud infrastructure (Microsoft) |
| **Licensing** | Free & Open Source Software (GPLv2) | Proprietary commercial service |
| **Network Dependence** | **Fully functional offline without Internet** | Requires continuous Internet connectivity |
| **Core Primitives** | Commits, branches, merges, rebases, hashing | Pull Requests, Issues, Actions (CI/CD), Wikis |
| **Industry Alternatives** | Mercurial, SVN | GitLab, Bitbucket, Gitea, Sourcehut |

-----

## Collaborative Workflow Models: GitFlow

::::: columns
::: {.column width="56%"}

Classical branching model ([Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/)) built around multiple long-lived branches (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`):

  * **Advantages:**
      * Structured parallel development.
      * Stable, controlled production releases.
      * Supports multiple versions in the wild simultaneously.
  * **Disadvantages:**
      * **Highly complex workflow** and process overhead.
      * Slow release cycles (*slow releases*).
      * **Frequent merge conflicts** across long-lived diverging branches.

:::
::: {.column width="44%"}

\begin{center}
\includegraphics[height=0.74\textheight,keepaspectratio]{figures/git_flow_nvie.png}
\end{center}

:::
:::::

-----

## Collaborative Workflow Models: Trunk-Based Development

In pure [**Trunk-Based Development**](https://trunkbaseddevelopment.com/#one-line-summary), the entire team streams small daily commits directly into a single shared branch (**`trunk` / `main`**):

\begin{center}
\includegraphics[width=0.72\linewidth,keepaspectratio]{figures/trunk_based_pure.png}
\end{center}

::::: columns
::: {.column width="48%"}

  * **Advantages:**
      * Drastically reduced merge conflicts.
      * Very low complexity and process overhead.
      * Improved collaboration and true continuous integration.

:::
::: {.column width="52%"}

  * **Disadvantages:**
      * Requires a **highly mature and disciplined team**.
      * Limited isolation for work-in-progress features.
      * **High risk of breaking production** (`main`).

:::
:::::

-----

## Proposed Model: Scaled Trunk-Based (Feature Branches)

**Scaled Trunk-Based Development** retains most of the advantages of trunk-based development while providing **better control and safety for growing teams**:

\begin{center}
\includegraphics[width=0.74\linewidth,keepaspectratio]{figures/trunk_based_scaled.png}
\end{center}

  * **Short-Lived Feature Branches:** Created from `main` by **one developer lasting at most a couple of days** (preventing long-lived divergence).
  * **Pre-Integration Quality Gate:** Changes flow through a **Pull Request (Peer Code Review + automated CI build/tests)** before merging into `main`.

-----

## The Core of Collaborative Engineering: Pull Requests (PR)

In *Scaled Trunk-Based Development*, a **Pull Request (PR)** serves as the quality gate before integrating a short-lived feature branch into `main`:

  * **A PR is Not a Git Command:** It is a web platform collaboration mechanism (GitHub / GitLab).
  * **Pillars of a Professional Pull Request:**
      * **Peer Code Review:** Line-by-line inspection of the diff by teammates to catch bugs, security flaws, and readability issues.
      * **Automated Build & Test Verification (CI/CD):** Automatic compilation, unit tests, and linters — merging is blocked unless the build passes.
      * **Transparent Technical Discussion:** Persistent record of architectural decisions prior to merging into `main`.

-----

## Practical Example: Trunk-Based Workflow with Feature Branches

```bash
# 1. Ensure local 'main' is synchronized and create a short-lived feature branch
git switch main && git pull --rebase
git switch -c feat/oauth-authentication

# 2. Develop iteratively with small, atomic commits (Conventional Commits)
git add src/auth.c
git commit -m "feat: add OAuth2 token validation"

# 3. Before submitting, update 'main' and linearize the feature branch (prevent conflicts)
git switch main && git pull --rebase
git switch feat/oauth-authentication && git rebase main

# 4. Push the branch to the remote repository and open a Pull Request (Code Review + CI) on GitHub
git push -u origin feat/oauth-authentication

# 5. Once approved and merged on GitHub, update local 'main' and delete the temporary branch
git switch main && git pull --rebase
git branch -d feat/oauth-authentication
```

-----

## Publishing Releases & GitHub Releases

Distributing official releases relies on pushing tags and creating GitHub Releases:

::::: columns
::: {.column width="48%"}

  * **Pushing Tags to the Remote:**
      * By default, `git push` does not transfer tags to the remote server (`origin`).
      * Tags must be explicitly pushed:
        ```bash
        # Push a specific tag
        git push origin v1.0.0

        # Push all local tags
        git push origin --tags
        ```
  * Once pushed, all collaborators and CI pipelines can reference this exact milestone.

:::
::: {.column width="52%"}

  * **GitHub Releases:**
      * Platform feature layered on top of repository tags.
      * **Distribution Advantages:**
          * Associates formatted release notes and automated changelogs.
          * Attaches pre-compiled binaries (installers, `.deb` packages, `.zip` archives).
          * Supports marking pre-releases (beta/release candidates).

:::
:::::

-----

## Session Summary & Key Takeaways

  * **Eliminating Manual Chaos:** Git replaces error-prone file duplication with a cryptographic, auditable version history.
  * **Distributed Architecture:** Every clone hosts full autonomous history, guaranteeing local execution and resilience without central servers.
  * **Mastering the Three States:** Operational proficiency requires understanding **Working Tree**, **Staging Area**, and the **Local Repository**.
  * **Lightweight Branching:** Inexpensive ($O(1)$) branches enable safe parallel engineering without destructive interference.
  * **Git vs. GitHub:** Git is the local CLI distributed version engine; GitHub provides cloud collaboration, code review, and automation.
  * **Agile & Safe Collaboration:** *Scaled Trunk-Based Development* with short-lived *Feature Branches* and *Pull Requests* ensures fast integration, peer code review, and continuous stability on `main`.

-----

## Authorized Technical References

Official documentation and technical standards for further study:

  * **Official Git Documentation & Pro Git Book:**
      * [Pro Git Book by Scott Chacon and Ben Straub](https://git-scm.com/book/en/v2) — Canonical free text
      * [Official Git Reference Manual](https://git-scm.com/docs)
  * **Collaborative Workflows & GitHub:**
      * [Trunk Based Development (Paul Hammant)](https://trunkbaseddevelopment.com/)
      * [Best Practices for Collaborative Pull Requests](https://docs.github.com/en/pull-requests)
  * **Software Engineering Specifications:**
      * [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/)
      * [Semantic Versioning 2.0.0 (SemVer)](https://semver.org/)
  * **Interactive Tutorials & Learning Resources:**
      * [Learn Git Branching (Interactive Visual Simulator)](https://learngitbranching.js.org/)
      * [Atlassian Git Workflows & Tutorials](https://www.atlassian.com/git/tutorials)
