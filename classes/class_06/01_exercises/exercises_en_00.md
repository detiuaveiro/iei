---
title: 47138 - Introduction to Computer Engineering
subtitle: "Version Control with Git & Collaborative Platform GitHub"
institute: Universidade de Aveiro
date: November 02, 2026
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

**Pedagogical Context & Objectives:**  
Distributed version control with **Git** and cloud collaboration through platforms such as **GitHub** form the backbone of contemporary software engineering. In this **3-hour** practical session, you will apply step by step every concept covered in the theoretical presentation, acquiring the operational discipline to manage the source-code lifecycle with full traceability, reversibility, and safe team collaboration:

* **Part 0 — Environment Setup & GitHub Authentication:** Installing Git, configuring committer identity (`user.name`, `user.email`), and setting up secure cryptographic authentication with GitHub via an `ed25519` SSH key pair.
* **Part 1 — Git Functional Aspects & Local Lifecycle:** Initializing repositories (`git init`), moving across the three operational areas (*Working Tree*, *Staging Area*, and *Local Repository*) and the four file states, applying best practices (50/72 rule) and *Conventional Commits*, inspecting history with `git log`, creating local tags with `git tag` ([SemVer](https://semver.org/)), and excluding build artifacts via `.gitignore`.
* **Part 2 — Branching, Integration & Conflict Resolution:** Understanding branches as lightweight $O(1)$ pointers and the symbolic `HEAD` reference, branch management commands (`git branch`, `git switch`, `git switch -c`, `git branch -d`), integration strategies with `git merge` (*Fast-Forward* vs. *3-Way Merge*), history linearization with `git rebase`, and manual merge conflict resolution.
* **Part 3 — Distributed Collaboration, Workflows & GitHub Releases:** Managing remote repositories (`origin`), synchronizing with `fetch`, `pull`, and `push`, executing the end-to-end **Scaled Trunk-Based Development** workflow (using *Short-Lived Feature Branches* and *Pull Requests* with *Code Review*), and publishing official versions with **GitHub Releases**.

\vspace{0.5em}

### Workspace Directory Setup

Before starting the exercises, create and enter the dedicated workspace directory for this laboratory session:

```bash
$ mkdir -p ~/IEI/class06
$ cd ~/IEI/class06
```

All local repositories and files created during the lab should be organized inside this workspace directory.

> **File path note:**  
> Commands in this guide assume your terminal is positioned in the `~/IEI/class06` workspace directory.

-----

## Part 0: Environment Setup & GitHub Authentication

Before starting development, you must configure the local Git client and establish secure authentication with the GitHub platform.

### Step 1: Install and Verify Git

On Debian/Ubuntu-based systems, verify whether Git is installed or install it:

```bash
$ sudo apt update && sudo apt install -y git
$ git --version
```

### Step 2: Configure Global Identity

Git permanently embeds the author's identity into every created commit. Configure your full name, your institutional University of Aveiro email address, and the default primary branch name (`main`):

```bash
$ git config --global user.name "Your Full Name"
$ git config --global user.email "your.email@ua.pt"
$ git config --global init.defaultBranch main
```

You can inspect the global configuration stored in `~/.gitconfig` by running:

```bash
$ git config --global --list
```

### Step 3: Secure Authentication with GitHub

To synchronize code with GitHub (`git push`), the platform requires authentication via SSH keys (recommended) or a *Personal Access Token* (PAT).

#### Recommended Method: SSH Key Pair (ed25519)

1. Generate a new SSH key pair using the `ed25519` algorithm:
   ```bash
   $ ssh-keygen -t ed25519 -C "your.email@ua.pt" -f ~/.ssh/id_ed25519 -N ""
   ```
2. Display and copy the full contents of your **public key** (`.pub`):
   ```bash
   $ cat ~/.ssh/id_ed25519.pub
   ```
   *(The output must start with `ssh-ed25519 AAAAC3...` and end with your email).*
3. Register the public key in your GitHub account:
   * Go to [GitHub.com](https://github.com/) and sign in.
   * In the top-right corner, click your profile picture $\rightarrow$ **Settings**.
   * On the left sidebar (under *Access*), select **SSH and GPG keys**.
   * Click the green **New SSH key** button.
   * Fill in the **Title** field with a machine identifier (e.g., `Ubuntu Laptop IEI`).
   * Paste the copied public key into the **Key** field and click **Add SSH key**.
4. Test the secure connection from your terminal:
   ```bash
   $ ssh -T git@github.com
   ```
   > On the first connection, confirm the server's fingerprint by typing `yes`. You should receive the confirmation message:  
   > `Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.`

#### Alternative Method: Personal Access Token (PAT)

If SSH access is blocked on your current network:
1. On GitHub, go to **Settings** $\rightarrow$ **Developer settings** $\rightarrow$ **Personal access tokens** $\rightarrow$ **Fine-grained tokens**.
2. Click **Generate new token**, set a descriptive name (e.g., `IEI-Token-Class06`), choose an expiration date, and grant **Read and write** access under **Repository permissions $\rightarrow$ Contents**.
3. Copy the generated token (`github_pat_...`) immediately and use it as your password during HTTPS operations.

-----

## Part 1: Git Functional Aspects & Local Lifecycle

In this section (corresponding to **Part II** of the theoretical slides), you will operate locally across Git's three operational areas (**Working Tree**, **Staging Area**, and **Local Repository**) without requiring any Internet connection.

### Exercise 1: Repository Initialization (`git init`) and `.git/` Structure

1. Create a folder for your project and initialize it as a Git repository:
   ```bash
   $ mkdir ~/IEI/class06/my-project && cd ~/IEI/class06/my-project
   $ git init
   ```
2. Inspect the hidden `.git/` directory automatically generated by Git:
   ```bash
   $ ls -la .git/
   $ cat .git/HEAD
   ```
   > **Architectural Understanding:**  
   > The `.git/` directory is the local database that stores the entire history graph, compressed objects (`objects/`), branch pointers (`refs/heads/`), and the symbolic reference `HEAD` (`ref: refs/heads/main`).

### Exercise 2: The Three Areas and File States (`status`, `add`, `commit`)

As a file moves across the **Working Tree**, **Staging Area**, and **Local Repository**, it assumes one of four states: **Untracked**, **Modified**, **Staged**, or **Unmodified**.

1. Create an `index.html` file in your *Working Tree*:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>IEI Portal - University of Aveiro</title>
   </head>
   <body>
       <h1>Welcome to the IEI Project</h1>
       <p>Distributed version control with Git and GitHub.</p>
   </body>
   </html>
   ```
2. Inspect the repository state with `git status`:
   ```bash
   $ git status
   ```
   The file appears in red as **Untracked** (Git is not monitoring it yet).
3. Promote the file to the **Staging Area / Index** with `git add`:
   ```bash
   $ git add index.html
   $ git status
   ```
   The file now appears in green in the **Staged** state (*Changes to be committed*).
4. Record the contents of the *Staging Area* as a permanent snapshot in the **Local Repository** using `git commit`:
   ```bash
   $ git commit -m "feat: add initial HTML structure for homepage"
   $ git status
   ```
   The file is now in the **Unmodified** state (*nothing to commit, working tree clean*).
5. Edit `index.html` by adding a footer right before `</body>`:
   ```html
       <footer>DETI - University of Aveiro</footer>
   ```
   Run `git status` and verify that the tracked file transitioned to the **Modified** state (in red, *Changes not staged for commit*).
6. **Unstaging Test (`git restore --staged`):**  
   If you stage a modified file by mistake (`git add`), you can move it back from the *Staging Area* to the *Modified* state in the *Working Tree* without losing your edits on disk:
   ```bash
   $ git add index.html
   $ git restore --staged index.html
   $ git status
   ```

### Exercise 3: Best Practices (50/72), Conventional Commits, and Amending (`--amend`)

As covered in the theoretical slides, commit messages structured according to [Conventional Commits](https://www.conventionalcommits.org/) (`<type>[optional scope]: <description>`) enable fast auditing, automated *changelogs*, and automatic SemVer version calculation.

1. Stage the modification made to `index.html` and simulate a commit with a careless message (anti-pattern):
   ```bash
   $ git add index.html
   $ git commit -m "html edits"
   $ git log --oneline
   ```
2. Rectify the latest commit using `git commit --amend`, replacing it with a message that follows the **50/72 convention** (concise imperative subject $\le 50$ chars, followed by an explanatory body separated by a blank line):
   ```bash
   $ git commit --amend -m "feat(ui): add institutional footer to homepage" \
                        -m "Include official department identification (DETI - UA) at the bottom of the page to comply with the style guide."
   $ git log --oneline
   ```
   > **Technical Note:** `--amend` replaces the latest commit with a new object and a new SHA-1 hash. Only use it on local commits that **have not yet been shared** via `push`.
3. Create a `README.md` documentation file and record a `docs:` commit:
   ```bash
   $ cat << 'EOF' > README.md
   # IEI Portal
   Laboratory project for Class 06 of Introduction to Computer Engineering.
   EOF
   $ git add README.md
   $ git commit -m "docs: add initial project documentation in README"
   ```

### Exercise 4: Inspecting History (`git log`) and Tagging Versions (`git tag`)

1. Practice the five history inspection variants studied in the theoretical slides:
   ```bash
   # 1. Full standard commit log (author, date, full SHA hash, and message body)
   $ git log

   # 2. Compact single-line summary per commit (Short SHA + Subject)
   $ git log --oneline

   # 3. ASCII visual representation of branch and merge topology
   $ git log --graph --oneline --all

   # 4. Display code diffs introduced in the last 2 commits
   $ git log -p -2

   # 5. Summary statistics of modified files, insertions, and deletions
   $ git log --stat
   ```
2. **Tagging Versions with `git tag` and Semantic Versioning ([SemVer](https://semver.org/)):**  
   Unlike a branch, a **tag** is a fixed, immutable pointer to a specific commit (`vMAJOR.MINOR.PATCH`):
   ```bash
   # 1. Create a lightweight tag at the current commit (HEAD)
   $ git tag v0.1.0

   # 2. List all existing tags in the repository
   $ git tag

   # 3. View commits with their associated tags and branch pointers
   $ git log --oneline --decorate
   ```

### Exercise 5: Excluding Untracked Files (`.gitignore`)

Compiled binaries (`*.o`), dependencies (`node_modules/`, `.venv/`), local secrets (`.env`), and OS metadata (`.DS_Store`) must never be tracked.

1. Simulate the presence of a sensitive credentials file and a compiled object file in your *Working Tree*:
   ```bash
   $ echo "API_SECRET_KEY=9988776655" > .env
   $ touch module.o
   $ git status
   ```
2. Create the `.gitignore` file with the exclusion rules studied in class:
   ```bash
   $ cat << 'EOF' > .gitignore
   # Compiled binaries and build directories
   bin/
   build/
   *.o

   # Python virtual environments
   .venv/
   __pycache__/

   # Sensitive files and local OS metadata
   .env
   .DS_Store
   EOF
   ```
3. Verify with `git status` that `.env` and `module.o` are no longer listed as *Untracked*:
   ```bash
   $ git status
   ```
4. Stage and commit `.gitignore` using the `chore:` type:
   ```bash
   $ git add .gitignore
   $ git commit -m "chore: configure exclusion rules in .gitignore"
   ```

-----

## Part 2: Branching, Integration & Conflict Resolution

In this section (corresponding to **Part III** of the theoretical slides), you will explore Git's $O(1)$ branching model, compare both `git merge` strategies (*Fast-Forward* vs. *3-Way Merge*), linearize history with `git rebase`, and resolve merge conflicts.

### Exercise 6: The Branching Paradigm ($O(1)$) and Management Commands

In Git, a branch is simply a **41-byte** file (40-character SHA-1 hash + `\n`) stored inside `.git/refs/heads/`.

1. Create and switch to a new branch `feature-login` in a single step using the recommended modern syntax (`git switch -c`):
   ```bash
   $ git switch -c feature-login
   ```
   *(Note: The equivalent classic syntax is `git checkout -b feature-login`).*
2. Inspect how Git represents this branch internally inside `.git/`:
   ```bash
   $ cat .git/HEAD
   $ cat .git/refs/heads/feature-login
   $ wc -c .git/refs/heads/feature-login
   ```
   > **Experimental Verification:** `.git/refs/heads/feature-login` is exactly **41 bytes**! And `.git/HEAD` points symbolically to `ref: refs/heads/feature-login`.
3. List all existing branches:
   ```bash
   $ git branch -a
   ```
4. Create a `login.html` file to develop this feature in isolation:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Login - IEI Portal</title>
   </head>
   <body>
       <h1>Sign In</h1>
   </body>
   </html>
   ```
5. Stage and commit on the `feature-login` branch:
   ```bash
   $ git add login.html
   $ git commit -m "feat(auth): create user authentication page"
   ```
6. Switch back to `main` and inspect the *Working Tree*:
   ```bash
   $ git switch main
   $ ls -la
   ```
   `login.html` disappeared from the working directory because it belongs exclusively to `feature-login`.

### Exercise 7: Integration Strategies with `git merge` (*Fast-Forward* vs. *3-Way*)

1. **Scenario 1 — *Fast-Forward* Merge (Linear):**  
   Since `main` received no new commits since `feature-login` was created, merge the branch using the two-step command sequence from the slides:
   ```bash
   $ git switch main
   $ git merge feature-login
   ```
   Observe the `Fast-forward` output: the `main` pointer simply slid forward in $O(1)$ to the `feature-login` commit **without creating a merge commit**.
2. Safely delete the already-merged `feature-login` branch:
   ```bash
   $ git branch -d feature-login
   ```
3. **Scenario 2 — *3-Way Merge* (Divergent Branches):**  
   Let us now create true divergence between `main` and a new branch `feature-styles`:
   ```bash
   # 1. Create and switch to feature-styles
   $ git switch -c feature-styles
   $ echo "body { font-family: Arial, sans-serif; }" > style.css
   $ git add style.css
   $ git commit -m "feat(ui): add base CSS stylesheet"

   # 2. Return to main and make an independent commit on another file
   $ git switch main
   $ echo "MIT License - 2026" > LICENSE
   $ git add LICENSE
   $ git commit -m "docs: add MIT license file"
   ```
4. Now the two histories have diverged from their common ancestor. Merge `feature-styles` into `main`:
   ```bash
   $ git merge feature-styles -m "Merge branch 'feature-styles' into main"
   ```
5. View the resulting graph and delete the temporary branch:
   ```bash
   $ git log --graph --oneline --all
   $ git branch -d feature-styles
   ```
   > **Observation:** Because the branches had diverged, Git performed a **3-Way Merge**, creating a new **Merge Commit** with two parents!

### Exercise 8: Linearizing History with `git rebase`

As shown in the theoretical slides, repeated *3-Way Merges* produce tangled "spaghetti graphs". `git rebase` solves this by detaching feature commits and reapplying them sequentially on top of the updated tip of `main`.

1. Create a new branch `feature-profile` and record a commit:
   ```bash
   $ git switch -c feature-profile
   $ echo "<h1>Student Profile</h1>" > profile.html
   $ git add profile.html
   $ git commit -m "feat(profile): add student profile page"
   ```
2. Switch back to `main` and simulate a concurrent update on the main line:
   ```bash
   $ git switch main
   $ echo "Version: 0.2.0" >> README.md
   $ git add README.md
   $ git commit -m "docs: record version number in README"
   ```
3. `main` and `feature-profile` have diverged again! Instead of running `git merge` (which would create another diamond fork), switch to `feature-profile` and linearize it onto `main` using `git rebase`:
   ```bash
   $ git switch feature-profile
   $ git rebase main
   ```
   > **Internal Mechanism:** Git detached the commit on `feature-profile` and reapplied it directly on top of the latest commit on `main`, generating a new commit (`E'`) with a new SHA hash.
4. Now return to `main` and integrate `feature-profile`:
   ```bash
   $ git switch main
   $ git merge feature-profile
   $ git branch -d feature-profile
   ```
5. Inspect the history with `git log --graph --oneline`:
   ```bash
   $ git log --graph --oneline
   ```
   Notice that the integration occurred via **Fast-Forward** and the top of the history remained **strictly linear**!
   > **The Golden Rule of Rebase:** **NEVER** run `git rebase` on public branches shared with teammates, as rewriting shared SHA hashes breaks team synchronization.

### Exercise 9: Detecting and Resolving Merge Conflicts

A merge conflict occurs when two branches modify **the exact same lines in the same file** in contradictory ways.

1. On `main`, create a `config.txt` configuration file:
   ```bash
   $ echo "timeout_ms = 5000" > config.txt
   $ git add config.txt
   $ git commit -m "chore(config): set default timeout to 5000ms"
   ```
2. Create a branch `feature-timeout` and change the value to `10000`:
   ```bash
   $ git switch -c feature-timeout
   $ echo "timeout_ms = 10000" > config.txt
   $ git add config.txt
   $ git commit -m "perf(config): increase timeout to 10000ms for slow networks"
   ```
3. Switch back to `main` and modify the **exact same line** in `config.txt` to `3000`:
   ```bash
   $ git switch main
   $ echo "timeout_ms = 3000" > config.txt
   $ git add config.txt
   $ git commit -m "perf(config): reduce timeout to 3000ms on main branch"
   ```
4. Attempt to merge `feature-timeout` into `main`:
   ```bash
   $ git merge feature-timeout
   ```
   Git pauses the merge and outputs a conflict warning:
   ```text
   Auto-merging config.txt
   CONFLICT (content): Merge conflict in config.txt
   Automatic merge failed; fix conflicts and then commit the result.
   ```
5. Inspect the contents of `config.txt` to see the visual conflict markers injected by Git:
   ```bash
   $ cat config.txt
   ```
   ```text
   <<<<<<< HEAD
   timeout_ms = 3000
   =======
   timeout_ms = 10000
   >>>>>>> feature-timeout
   ```
6. **Resolution Protocol (4 steps from the theoretical slides):**
   * **Steps 1 & 2:** Decide on the final value (e.g., `8000`) and replace the file contents while **removing all conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`):
     ```bash
     $ echo "timeout_ms = 8000" > config.txt
     ```
   * **Step 3:** Stage the resolved file into the *Staging Area*:
     ```bash
     $ git add config.txt
     ```
   * **Step 4:** Complete the merge commit:
     ```bash
     $ git commit -m "fix(config): resolve merge conflict setting timeout to 8000ms"
     $ git branch -d feature-timeout
     ```

-----

## Part 3: Distributed Collaboration, Workflows & GitHub Releases

In this final section (corresponding to **Part IV** of the theoretical slides), you will publish your project to GitHub, synchronize remote changes (`fetch`, `pull`, `push`), execute the proposed collaborative model (**Scaled Trunk-Based Development with Feature Branches and Pull Requests**), and publish a **GitHub Release**.

### Exercise 10: Remote Repositories (`origin`) and Synchronization (`push`, `fetch`, `pull`)

1. In your browser, go to [GitHub.com](https://github.com/) and create a **new empty repository**:
   * **Repository name:** `iei-git-project`
   * **Visibility:** Public
   * **Important:** **DO NOT** check *Add a README file*, `.gitignore`, or *license*. Click **Create repository**.
2. In your local terminal (`~/IEI/class06/my-project`), associate the remote repository under the canonical name `origin`:
   ```bash
   # Replace <USERNAME> with your GitHub username
   $ git remote add origin git@github.com:<USERNAME>/iei-git-project.git
   $ git remote -v
   ```
   *(If using HTTPS/PAT, use `https://github.com/<USERNAME>/iei-git-project.git`).*
3. **Publish your local branch (`git push`):**
   ```bash
   $ git push -u origin main
   ```
   Refresh the GitHub page in your browser and confirm that all files and commit history are now hosted in the cloud.
4. **Practical difference between `git fetch` and `git pull`:**
   * On the GitHub web interface, click `README.md`, click the pencil icon (**Edit this file**), append a line (`## Development Team`), and click **Commit changes...** directly in the browser.
   * The remote server (`origin/main`) now has a new commit that your local machine does not know about!
   * In your local terminal, run `git fetch origin` first:
     ```bash
     $ git fetch origin
     $ cat README.md
     $ git log --graph --oneline --all
     ```
     > **Verification:** As studied in the slides, `git fetch` downloaded the new commit from the server (visible as `origin/main` in `git log`), but **did not touch the files in your Working Tree**!
   * Now integrate the downloaded changes into your local `main` branch:
     ```bash
     $ git pull --rebase origin main
     $ cat README.md
     ```

### Exercise 11: Proposed Model — Trunk-Based Workflow with Feature Branches & Pull Requests

In team projects, we adopt **Scaled Trunk-Based Development**: we create *Short-Lived Feature Branches* from `main`, keep them updated via `rebase`, and integrate them through **Pull Requests (PR)** with **Peer Code Review**.

Execute the complete end-to-end sequence step by step (matching the practical workflow slide):

```bash
# 1. Ensure local 'main' is synchronized and create a short-lived feature branch
$ git switch main && git pull --rebase
$ git switch -c feat/oauth-authentication
```

2. **Develop iteratively with small, atomic commits (Conventional Commits):**
   ```bash
   $ echo "<h2>Secure OAuth2 Authentication</h2>" >> login.html
   $ git add login.html
   $ git commit -m "feat(auth): add OAuth2 authentication support"
   ```
3. **Before submitting, update `main` and linearize the feature branch (prevent conflicts):**
   ```bash
   $ git switch main && git pull --rebase
   $ git switch feat/oauth-authentication && git rebase main
   ```
4. **Push the branch to the remote repository:**
   ```bash
   $ git push -u origin feat/oauth-authentication
   ```
5. **Open the Pull Request and conduct *Code Review* on GitHub:**
   * Open your repository page on GitHub and click the green **Compare & pull request** button.
   * Confirm the merge direction: `base: main` $\leftarrow$ `compare: feat/oauth-authentication`.
   * Fill in the description explaining the feature and click **Create pull request**.
   * On the Pull Request page, click the **Files changed** tab, hover over the added line in `login.html`, click the `+` icon, and add an inline *Code Review* comment.
   * Return to the **Conversation** tab and complete the integration by clicking **Merge pull request** $\rightarrow$ **Confirm merge**.
6. **Once approved and merged on GitHub, update local `main` and delete the temporary branch:**
   ```bash
   $ git switch main && git pull --rebase
   $ git branch -d feat/oauth-authentication
   $ git log --oneline -5
   ```

### Exercise 12: Publishing Versions and GitHub Releases

To conclude the development cycle, let us tag the stable release `v1.0.0` (after merging the Pull Request) and publish an official **GitHub Release**:

1. In your terminal (on the updated `main` branch), create the lightweight tag `v1.0.0`:
   ```bash
   $ git tag v1.0.0
   ```
2. Because regular `git push` does not transfer tags to the remote server, explicitly push the tag to `origin`:
   ```bash
   $ git push origin v1.0.0
   ```
   *(Note: To push all local tags at once, you can also run `git push origin --tags`).*
3. **Create the Release on GitHub:**
   * On your repository's main page on GitHub, locate the **Releases** section (right sidebar) and click **Create a new release** (or **Draft a new release**).
   * Under **Choose a tag**, select `v1.0.0`.
   * Set **Release title** to `v1.0.0 — First Stable Release`.
   * Click **Generate release notes** (to see how GitHub automatically builds the changelog from your *Conventional Commits* and *Pull Requests*!) and click **Publish release**.

-----

## Part 4: Autonomous Consolidation Challenges

To consolidate your engineering skills, try the following independent challenges:

### Challenge A: The "Time Machine" and *Detached HEAD* State
1. View your compact history: `git log --oneline`.
2. Pick the SHA hash of your first commit (e.g., `98ca9c2`) and run:
   ```bash
   $ git checkout <FIRST_COMMIT_HASH>
   ```
3. Run `git status` and notice that Git reports you are in **Detached HEAD** mode (the `HEAD` pointer points directly to a commit rather than symbolically pointing to a branch).
4. Verify with `ls` that all files created after that commit have temporarily disappeared from the *Working Tree*.
5. Immediately return to the present safely with:
   ```bash
   $ git switch main
   ```

### Challenge B: Fast Change Lookup with `git log -S`
1. Suppose you want to find out exactly which commit introduced the string `"OAuth2"` into the project:
   ```bash
   $ git log -S "OAuth2" -p
   ```
2. Observe how the `-S` (*pickaxe*) option searches history for commits that added or removed occurrences of that string.

-----

## Summary of Essential Commands Covered

| Command | Operational Description |
| :--- | :--- |
| `git init` | Initializes a new local Git repository (`.git/`). |
| `git clone <url>` | Clones a complete remote repository to the local machine. |
| `git status` | Inspects file states across the *Working Tree* and *Staging Area*. |
| `git add <file>` | Promotes changes from the *Working Tree* to the *Staging Area*. |
| `git restore --staged <file>` | Unstages a file from the *Staging Area* without modifying the *Working Tree*. |
| `git commit -m "<msg>"` | Records the *Staging Area* contents as a new immutable snapshot. |
| `git commit --amend` | Replaces the latest local commit to fix its message or contents. |
| `git log --oneline --graph` | Displays commit history and branch topology in compact form. |
| `git tag v1.0.0` | Creates a lightweight tag pointing to the current commit (`HEAD`). |
| `git branch -a` | Lists all known local and remote-tracking branches. |
| `git switch <branch>` | Switches to an existing branch and updates the *Working Tree*. |
| `git switch -c <new-branch>` | Creates a new branch and switches to it immediately. |
| `git merge <branch>` | Integrates the specified branch into the active branch (*Fast-Forward* or *3-Way*). |
| `git rebase main` | Linearizes the current branch by reapplying its commits onto the tip of `main`. |
| `git branch -d <branch>` | Safely deletes an already-merged local branch. |
| `git remote add origin <url>` | Registers a remote repository under the default alias `origin`. |
| `git fetch origin` | Downloads remote updates without modifying the local *Working Tree*. |
| `git pull --rebase` | Synchronizes the local branch by linearizing it onto the remote tip. |
| `git push -u origin <branch>` | Publishes local branch commits to the remote repository. |
| `git push origin v1.0.0` | Explicitly publishes a version tag to the remote server. |
