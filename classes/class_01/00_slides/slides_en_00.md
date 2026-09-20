---
title: 47138 - Introduction to Computer Engineering
subtitle: Linux Terminal
institute: Universidade de Aveiro
date: September 21, 2026
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
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Welcome to the Command Line\! 🐧

### More Than Just a Black Box

The **Terminal** is your direct, text-based connection to the operating system.

  * **Why use it?**
      * **Power & Speed:** Execute complex tasks instantly.
      * **Automation:** Script repetitive jobs.
      * **Efficiency:** Uses minimal system resources.
      * **Industry Standard:** Essential for developers and system administrators.

**Analogy:** A GUI is the restaurant menu: you can only pick what is already listed. The CLI is stepping into the kitchen and crafting your own custom recipe.

-----

## The Shell & Bash

The **shell** is the program that interprets your commands. The terminal is the window; the shell is the brain inside.

  * Several shells exist across Unix/Linux environments:
      * `sh` (Bourne Shell): The classic historical shell.
      * `zsh` (Z Shell): Modern default in macOS, highly customizable.
      * `fish`: Focused on out-of-the-box user-friendliness.
      * **`bash` (Bourne Again SHell):** The *de facto* standard across Linux distributions and the core focus today.

-----

## Shell Survival & Productivity ⚡

Four essential shortcuts that save time and prevent frustration:

  * **`<Tab>` Key (Auto-completion):**
      * Start typing and press `<Tab>`: auto-completes command names or paths.
      * Double `<Tab>`: lists all matching options.
  * **`↑` and `↓` Arrows (Command History):**
      * Browse and reuse previously typed commands without retyping.
      * The `history` command prints recent command entries.
  * **`Ctrl + C` (Cancel / Terminate):**
      * Instantly kills a hanging command or infinite loop.
  * **`clear` or `Ctrl + L`:**
      * Clears the terminal screen without ending the session.

-----

## Getting Help in the Terminal 💡

Never try to memorize every command and flag — learn how to look up help:

  * **`--help` Flag:**
      * Built-in concise summary of usage syntax and options.
      ```bash
      $ ls --help
      $ grep --help
      ```
  * **System Manual (`man`):**
      * Full official manual pages for commands and utilities.
      ```bash
      $ man ls
      ```
      * Use `↑` and `↓` arrows to scroll; press `/` to search text; press `q` to exit.

-----

## The Linux Filesystem (Part 1)

The filesystem is a single unified hierarchical tree rooted at **`/`**.

  * `/`: The **root directory**. Everything starts here.
  * `/home`: Personal folders for regular users (e.g., `/home/student`).
  * `/bin`: Essential user **binaries** (programs like `ls`, `cp`, `bash`).
  * `/etc`: System-wide **configuration** files.
  * `/var`: **Variable** runtime data, such as system logs (`/var/log`).
  * `/tmp`: Directory for **temporary** files (cleared on reboot).

-----

## The Linux Filesystem (Part 2)

Other key locations you will encounter regularly:

  * `/opt`: Optional third-party software installed standalone.
  * `/usr`: User utilities and secondary software (`/usr/bin`, `/usr/lib`).
  * `/usr/local`: Locally compiled/installed software by the administrator.
  * `/root`: Home directory of the **superuser** (*root*). Do not confuse with `/`!

-----

## Paths: Absolute vs. Relative 🧭

Understanding file paths is critical to moving around and running tools:

  * **Absolute Path:**
      * Always starts from the root directory `/`. Unambiguous regardless of current directory.
      ```bash
      $ cd /var/log
      $ ls /etc/os-release
      ```
  * **Relative Path:**
      * Evaluated relative to the current working directory.
      ```bash
      $ cd Documents/Work
      $ ls ./report.txt
      ```
  * **`~` Shortcut (Home):**
      * Expands to your personal home directory (e.g., `~/IEI` equals `/home/student/IEI`).

-----

## Hidden Files & Directories

Files starting with a period (`.`) are treated as hidden.

  * Commonly used to store user-level configurations and histories:
      * `~/.bashrc`: Startup script and settings for the Bash shell.
      * `~/.bash_history`: Recorded history of executed commands.
      * `~/.gitconfig`: Global configuration for Git.
      * `~/.config`: Standard folder for modern application settings.
  * Standard `ls` hides these files by default.

-----

## Basic Navigation: `pwd` and `cd`

Fundamental commands to navigate the directory tree:

  * `pwd`: **P**rint **W**orking **D**irectory. Outputs the full absolute path of your current location.
    ```bash
    $ pwd
    /home/student
    ```
  * `cd`: **C**hange **D**irectory. Changes the current working directory.
    ```bash
    $ cd /var/log          # Absolute path
    $ cd Documents         # Relative path into subdirectory
    ```

-----

## Navigation Shortcuts with `cd`

Handy shortcuts for rapid directory hopping:

  * **Go up one level (`..`):**
    ```bash
    $ cd ..
    ```
  * **Current directory (`.`):**
    ```bash
    $ cd .
    ```
  * **Go straight to your home directory (`~`):**
    ```bash
    $ cd ~                 # or simply: cd
    ```
  * **Going back to the previous directory (last visited):**
    ```bash
    $ cd -
    ```

-----

## Listing Directory Contents: `ls`

The `ls` command lists files and folders:

  * **Basic listing:**
    ```bash
    $ ls
    Documents  Downloads  Music  Scripts
    ```
  * **Long listing format (`-l`):** Shows permissions, owner, size, and date.
    ```bash
    $ ls -l
    -rw-r--r-- 1 student student 4096 Sep 21 09:30 doc.txt
    drwxr-xr-x 2 student student 4096 Sep 21 09:30 Scripts
    ```
  * **Show hidden files (`-a`):**
    ```bash
    $ ls -a
    .  ..  .bashrc  .profile  Documents
    ```
  * **Combine flags (`-la` or `-lah`):**
    `-h` prints file sizes in human-readable units (K, M, G).

-----

## Creating Directories: `mkdir`

Use `mkdir` (**m**a**k**e a **dir**ectory) to create folders:

  * **Create a single directory:**
    ```bash
    $ mkdir my_project
    ```
  * **Create nested directory trees (`-p` / parents):**
    Creates all required missing parent directories along the path automatically.
    ```bash
    $ mkdir -p Documents/Work/2026/Reports
    ```

-----

## Creating & Editing Files: `touch` & `nano`

  * **`touch`:** Quickly creates an empty file or updates its timestamp:
    ```bash
    $ touch notes.txt
    ```
  * **`nano`:** Simple, user-friendly terminal text editor:
    ```bash
    $ nano notes.txt
    ```
      * Type and edit text directly.
      * `Ctrl + O` and press `Enter`: Save file changes.
      * `Ctrl + X`: Exit editor (prompts to save if modifications exist).

-----

## Copying & Moving: `cp` and `mv` 📂

  * **`cp` (Copy):** Copies files or whole directories to a destination.
    ```bash
    $ cp notes.txt notes_backup.txt       # Copy file
    $ cp notes.txt ~/Documents/           # Copy into directory
    $ cp -r folder/ folder_copy/          # Copy directory recursively (-r)
    ```
  * **`mv` (Move):** Moves or renames files and directories.
    ```bash
    $ mv notes.txt important_notes.txt    # Rename file
    $ mv important_notes.txt ~/IEI/       # Move file to another directory
    ```

-----

## Deleting & Viewing: `rm` and `cat` 🗑️

  * **`rm` (Remove):** Deletes files or folders.
    ```bash
    $ rm notes_backup.txt                 # Remove file
    $ rm -r old_folder/                   # Remove directory recursively (-r)
    ```
    ⚠️ **Warning:** The command line **has no Trash/Recycle Bin**. Items deleted with `rm` are gone permanently!
  * **`cat` (Concatenate):** Prints the entire contents of a file to stdout:
    ```bash
    $ cat /etc/os-release
    ```

-----

## Viewing Large Files: `head`, `tail` and `less` 📄

For large files where `cat` floods the screen, use specialized readers:

  * **`head` and `tail`:** View the beginning or end of a file.
    ```bash
    $ head -n 5 /var/log/syslog           # First 5 lines
    $ tail -n 5 /var/log/syslog           # Last 5 lines
    ```
  * **`less` (Interactive Pager):**
    ```bash
    $ less /var/log/syslog
    ```
      * `↑` / `↓` or `Space`: Scroll text.
      * `/keyword`: Search for text.
      * `q`: Exit reader.

-----

## Output Redirection: `>` and `>>`

Redirect standard command text output directly into files:

  * **`>` Operator (Overwrite):**
    Directs output to a file, **overwriting** any previous content:
    ```bash
    $ echo "First line" > notes.txt
    $ ls -l /var/log > log_list.txt
    ```
  * **`>>` Operator (Append):**
    Appends output to the **end** of the file without erasing existing lines:
    ```bash
    $ echo "Second line" >> notes.txt
    $ echo "Run at $(date)" >> activity.log
    ```

-----

## Searching Content & Files: `grep` and `find` 🔎

  * **`grep` (Text Search):** Searches for lines matching a string or pattern.
    ```bash
    $ grep "root" /etc/passwd             # Find lines containing 'root'
    $ grep -i "confidential" report.txt   # Case-insensitive search (-i)
    $ grep -rn "TODO" ~/IEI/              # Recursive (-r) with line numbers (-n)
    ```
  * **`find` (File Search):** Searches the filesystem hierarchy for files.
    ```bash
    $ find ~/IEI -name "*.txt"            # Files matching *.txt
    $ find /var/log -type f -name "*.log" # Regular files only (-type f)
    ```

-----

## The Power of the Pipe `|`

The **Pipe (`|`)** embodies Unix philosophy: *connect one command's output to the next command's input*.

$$\text{Command A} \xrightarrow{\quad\text{output}\quad} \mathbf{\huge\mid} \xrightarrow{\quad\text{input}\quad} \text{Command B}$$

  * **Example 1: Filter directory listing:**
    ```bash
    $ ls /var/log | grep ".log"
    ```
  * **Example 2: Search running processes:**
    ```bash
    $ ps aux | grep "bash"
    ```
  * **Example 3: Count output lines:**
    ```bash
    $ ls -l /etc | wc -l
    ```

-----

## Users: Standard vs. Superuser

Linux enforces multi-user privileges and isolation:

  * **Standard User** (e.g., `student` or your personal username):
      * Daily account restricted to the user's home directory.
  * **Superuser (`root`):**
      * Full administrative authority over hardware, processes, and files.
  * **`sudo` (SuperUser DO):**
      * Temporarily executes administrative commands with root privileges:
      ```bash
      $ sudo apt update
      ```

-----

## Understanding File Permissions 🔐

The `ls -l` command displays permissions across 10 characters (e.g., `-rwxr-xr--`):

  * **1st character:** Type (`-` regular file, `d` directory, `l` symlink).
  * **Next 9 characters:** 3 permission triplets:
    * **Owner (*User* - u)**: `rwx`
    * **Group (*Group* - g)**: `r-x`
    * **Others (*Others* - o)**: `r--`
  * **Meaning:**
    * `r` (*read*): Read file contents or list directory contents.
    * `w` (*write*): Modify/delete file or add/remove directory entries.
    * `x` (*execute*): Run file as a program or navigate into directory (`cd`).

-----

## Managing Permissions with `chmod`

Use `chmod` (**ch**ange **mod**e) to adjust access permissions:

  * **Method 1: Symbolic Mode (`u`, `g`, `o`, `a` with `+` and `-`):**
    ```bash
    $ chmod u+x script.sh          # Grant execute to owner
    $ chmod go-w secret.txt        # Revoke write from group and others
    $ chmod a+r document.txt       # Grant read to everyone (all)
    ```
  * **Method 2: Octal / Numeric Mode ($r=4, w=2, x=1$):**
    * Add values per class: $4 (\text{read}) + 2 (\text{write}) + 1 (\text{exec}) = 7$.
    ```bash
    $ chmod 755 script.sh          # u=rwx (7), g=rx (5), o=rx (5)
    $ chmod 644 text.txt           # u=rw (6), g=r (4), o=r (4)
    $ chmod 000 secret.txt         # No permissions for anyone (0, 0, 0)
    ```

-----

## System Information & Processes ⚙️

Commands to quickly inspect system and process status:

  * `whoami`: Current logged-in username.
  * `date`: Current system date and time.
  * `uname -a`: Kernel details and processor architecture.
  * **What is a Process?**
      * A running program instance. Each process is assigned a unique **PID** (*Process ID*).
  * `ps aux`: Complete snapshot of active system processes.

-----

## Controlling Processes: Background & `kill`

  * **Background Processes:**
      * Adding `&` to the end of a command frees up the prompt immediately:
      ```bash
      $ sleep 120 &
      [1] 4521                       # [Job number] and assigned PID
      ```
  * **Locate a Process PID:**
      * Use `pgrep`:
      ```bash
      $ pgrep sleep
      4521
      ```
  * **Terminating Processes (`kill`):**
      * Sends a signal to stop the specified process PID:
      ```bash
      $ kill 4521                    # Clean termination (SIGTERM)
      $ kill -9 4521                 # Forced immediate termination (SIGKILL)
      ```

-----

## Package Management with APT 📦

**APT** (*Advanced Package Tool*) manages software installation and updates on Debian/Ubuntu systems:

  1. **Update package repositories list (`update`):**
     ```bash
     $ sudo apt update
     ```
  2. **Search for available packages (`search`):**
     ```bash
     $ apt search htop
     ```
  3. **Install a package (`install`):**
     ```bash
     $ sudo apt install htop
     ```
  4. **Remove a package (`remove` / `purge`):**
     ```bash
     $ sudo apt remove htop         # Removes package files
     $ sudo apt purge htop          # Removes package and config files
     ```

-----

## Essential Session Variables: `$USER`, `$HOME`, and `$PATH`

The shell provides variables containing session context (in UPPERCASE):

  * **`$USER`:** Current logged-in user name (`echo $USER`).
  * **`$HOME`:** Full path to your personal home directory (essential in *scripts* and *cron*):
    ```bash
    $ echo $HOME
    /home/student
    ```
  * **`$PATH`:** Colon-separated list of directories searched for executable programs:
    ```bash
    $ echo $PATH
    /usr/local/bin:/usr/bin:/bin
    ```
  * **Why do we need `./` to run our scripts?**
    * The current directory (`.`) is **not** in `$PATH` for security reasons. We explicitly specify the relative path: `./my_script.sh`.

-----

## Customizing the Shell: `.bashrc` & Aliases

The `~/.bashrc` script executes automatically when launching interactive Bash sessions.

  * **Creating Aliases:**
    Open `~/.bashrc` with `nano` and append at the end:
    ```bash
    alias ll='ls -al'
    alias c='clear'
    ```
  * **Reloading configuration:**
    Apply changes without opening a new terminal window:
    ```bash
    $ source ~/.bashrc
    ```
  * Test your new shortcut: `ll`.

-----

## Introduction to Bash Scripting

A Bash script is an executable text file containing command sequences:

  1. **Shebang (1st line mandatory):** Defines interpreter path:
     ```bash
     #!/bin/bash
     ```
  2. **Comments:** Lines starting with `#` annotate code.
  3. **Execution Permissions:** Must grant execution rights:
     ```bash
     $ chmod +x my_script.sh
     ```
  4. **Run Script:**
     ```bash
     $ ./my_script.sh
     ```
     *(The `./` explicitly points to the current directory executable).*

-----

## Script Example 1: Hello World

Using variables and the `echo` command:

**File: `hello.sh`**
```bash
#!/bin/bash
# Simple welcome script

NAME="Student"
echo "Hello, $NAME!"
echo "Your home directory is: $HOME"
```

**Run it:**
```bash
$ chmod +x hello.sh
$ ./hello.sh
```

-----

## Script Example 2: Conditions with `if`

Verify if a folder or file exists before taking action:

**File: `check_dir.sh`**
```bash
#!/bin/bash
TARGET_DIR="$HOME/IEI"

# -d checks if directory exists (-f checks regular file)
if [ -d "$TARGET_DIR" ]; then
  echo "Directory $TARGET_DIR already exists."
else
  echo "Directory missing. Creating it now..."
  mkdir -p "$TARGET_DIR"
fi
```

-----

## Script Example 3: Loops with `for`

Automate tasks across lists or folder collections:

**File: `create_folders.sh`**
```bash
#!/bin/bash
# Builds modular project directory layout

PROJECT="$HOME/IEI/project"

for folder in data code reports docs
do
  mkdir -p "$PROJECT/$folder"
  echo "-> Subdirectory created: $folder"
done

echo "Project scaffold ready at $PROJECT!"
```

-----

## Task Scheduling with `cron` 🕒

The ***cron*** daemon executes scheduled background tasks (*cron jobs*):

  * **Primary `crontab` commands:**
      * `crontab -e`: **Edit** user's cron schedule in editor.
      * `crontab -l`: **List** current scheduled jobs.
      * `crontab -r`: **Remove** user's entire cron file (*use with care!*).

### 5 Time Field Syntax:
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6, Sunday = 0)
│ │ │ │ │
* * * * * /absolute/path/to/command
```

-----

## `crontab` Examples

Key best practices for cron jobs:

  * Always specify **absolute paths** for commands and scripts.
  * An asterisk `*` denotes "every" interval unit.

**Example 1: Run backup daily at 3:30 AM:**
```cron
30 3 * * * /home/student/scripts/backup.sh
```

**Example 2: Run every minute and append log outputs:**
```cron
* * * * * /home/student/IEI/log_time.sh >> /home/student/IEI/cron_log.txt 2>&1
```

*(The `2>&1` redirects error messages to the same output log).*

-----

## Theory to Practice

Key concepts mastered for today's lab session:

  * **Navigation & Files:** `pwd`, `cd`, `ls`, `mkdir`, `touch`, `cp`, `mv`, `rm`, `cat`.
  * **Search & Data Flow:** `grep`, `find`, redirections (`>`, `>>`), and pipes (`|`).
  * **Permissions & Processes:** `chmod` (symbolic/octal), `sudo`, `ps`, `kill`.
  * **Environment & Automation:** `$PATH`, `.bashrc`, Bash scripts, and `cron`.

**Hands on terminal:** Time to tackle the lab exercises! 🚀

-----

## Support & Further Resources 📚

Bookmark these references for study and future lab exercises:

  * **Linux Command Line Cheat Sheet:**
      * [https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/](https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/)
  * **Visual Cron Expression Generator:**
      * [https://crontab.guru/](https://crontab.guru/)
  * **Bash Scripting Cheat Sheet:**
      * [https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet](https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet)
