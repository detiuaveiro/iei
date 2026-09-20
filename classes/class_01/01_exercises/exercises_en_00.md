---
title: Linux Terminal
subtitle: Introdução Engenharia Informática
#author: Mário Antunes
institute: Universidade de Aveiro
date: September 21, 2026
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
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Practical Lab Guide

This lab guide is designed for a **3-hour** session and is organized into two parts:

* **Part I — Core Competencies (Exercises 1 to 8):** Essential foundation. All students should complete these exercises during the classroom lab hours.
* **Part II — Customization, Scripting & Automation (Exercises 9 to 12):** Deeper dives and challenge tasks. If not finished in class, complete them as independent study.

\vspace{1em}

> **Terminal Survival Tips:**
>
> * **Auto-completion with `<Tab>`:** Type the first few characters of a path, file, or command and press `<Tab>`. Double `<Tab>` displays all available possibilities.
> * **Command History with `↑` and `↓` arrows:** Never retype a long command because of a single typo; press the up arrow to recall and edit previous commands.
> * **Cancel with `Ctrl + C`:** If a command hangs, blocks, or loops, press `Ctrl + C` to abort and return to the prompt.

\newpage

# Part I: Core Competencies

## Exercise 1: Finding Your Way Around

This exercise reinforces fundamental navigation and inspection commands: **`pwd`**, **`ls`**, **`cd`**, and user identity info.

1. Open your terminal. Verify your initial starting directory (your home directory) by printing the current working directory:
   ```bash
   $ pwd
   ```
2. List the contents of your home directory. Then list it again in **long** listing format (`-l`) showing **all** files (`-a`), including hidden configuration files:
   ```bash
   $ ls
   $ ls -la
   ```
3. Navigate to the system log directory at `/var/log` and list its contents.
   *(Try typing `cd /var/l` and pressing `<Tab>` to auto-complete!)*
   ```bash
   $ cd /var/log
   $ ls
   ```
4. Query session identity: check your username and current system time:
   ```bash
   $ whoami
   $ date
   ```
5. Return to your home directory using the fastest shortcut:
   ```bash
   $ cd ~
   ```
   *(Note: executing `cd` with no arguments produces the exact same result).*

-----

## Exercise 2: Exploring Key System Directories

Consolidate understanding of the Linux filesystem tree by inspecting key directories.

1. Navigate to `/etc`, which stores system-wide configuration files:
   ```bash
   $ cd /etc
   ```
2. List its contents. You will see numerous config files and subdirectories:
   ```bash
   $ ls
   ```
3. Inspect the contents of `os-release` to view information about the installed Linux distribution:
   ```bash
   $ cat os-release
   ```
   *(The `cat` utility prints the full file contents. To view only the first 5 lines, try: `head -n 5 os-release`).*
4. Navigate to `/bin` (where core command binaries and utilities reside):
   ```bash
   $ cd /bin
   $ ls
   ```
   *(Check if you recognize commands you have already used, such as `ls`, `date`, or `pwd`).*
5. Return to your home directory:
   ```bash
   $ cd ~
   ```

-----

## Exercise 3: Creating & Managing Files

Create, copy, move, rename, and delete files and directories.

1. From your home directory, create a new directory named `IEI`:
   ```bash
   $ cd ~
   $ mkdir IEI
   ```
2. Change into the new directory:
   ```bash
   $ cd IEI
   ```
3. Create an empty file named `notes.txt`:
   ```bash
   $ touch notes.txt
   ```
4. Write text into the file using the redirection operator `>` and verify with `cat`:
   ```bash
   $ echo "My first line of text in the terminal." > notes.txt
   $ cat notes.txt
   ```
5. Make a copy of the file named `notes_backup.txt`:
   ```bash
   $ cp notes.txt notes_backup.txt
   $ ls -l
   ```
6. Rename the original `notes.txt` to `important_notes.txt`:
   ```bash
   $ mv notes.txt important_notes.txt
   $ ls -l
   ```
7. Remove the backup file:
   ```bash
   $ rm notes_backup.txt
   $ ls -l
   ```
   *(⚠️ Remember: the command line has no Trash bin. Files removed with `rm` cannot easily be restored).*

-----

## Exercise 4: Understanding File Permissions

Read and modify file permissions using **`chmod`**.

1. Inside your `~/IEI` folder, create a new file named `secret_data.txt`:
   ```bash
   $ touch secret_data.txt
   ```
2. Inspect the default permissions assigned to the file:
   ```bash
   $ ls -l secret_data.txt
   ```
3. Remove all permissions for all classes using octal notation:
   ```bash
   $ chmod 000 secret_data.txt
   $ ls -l secret_data.txt
   ```
   *(In numeric mode, $r=4$, $w=2$, and $x=1$. A value of $0$ means nobody has read, write, or execute permission).*
4. Attempt to view the file with `cat`:
   ```bash
   $ cat secret_data.txt
   ```
   *(You should see an error message: **"Permission denied"**).*
5. Restore read (`r`) and write (`w`) permissions solely for yourself (user/owner):
   ```bash
   $ chmod u+rw secret_data.txt
   $ cat secret_data.txt
   ```
6. Create an empty script file `my_script.sh` and make it executable:
   ```bash
   $ touch my_script.sh
   $ chmod u+x my_script.sh
   $ ls -l my_script.sh
   ```
   *(Notice the `x` in the owner field and how the filename highlighting may change).*

-----

## Exercise 5: Finding Files & Content with `find` and `grep`

Locate files by name and search for text patterns inside files.

1. Inside `~/IEI`, create a subfolder and a file with sample text:
   ```bash
   $ mkdir -p ~/IEI/reports
   $ echo "This is a confidential report for the IEI course." > ~/IEI/reports/report-2026.txt
   ```
2. Use the `find` command to locate all `.txt` files under `~/IEI`:
   ```bash
   $ find ~/IEI -name "*.txt"
   ```
3. Use `grep` to search for the word "confidential" in the report. The `-i` flag makes the search case-insensitive:
   ```bash
   $ grep -i "confidential" ~/IEI/reports/report-2026.txt
   ```

-----

## Exercise 6: Managing Processes

Launch background processes, inspect Process IDs (PIDs), and terminate them from the terminal.

1. Start a background process that sleeps for 120 seconds. The trailing `&` places it in the background:
   ```bash
   $ sleep 120 &
   ```
   *(The shell outputs the job number, e.g. `[1]`, followed by the assigned **PID**).*
2. Confirm the process is running and query its PID using `pgrep`:
   ```bash
   $ pgrep sleep
   ```
3. Terminate the process using the `kill` command followed by the PID returned above (replace `PID` with the actual number):
   ```bash
   $ kill PID
   ```
4. Verify the process has terminated:
   ```bash
   $ pgrep sleep
   ```
   *(The command should return nothing, confirming the process has stopped).*

-----

## Exercise 7: Managing Software with APT

Install and remove system utilities using Ubuntu/Debian's official package manager.

1. Synchronize the local package index with remote repositories:
   ```bash
   $ sudo apt update
   ```
   *(Enter your password if prompted for `sudo`; note that no characters appear while typing passwords).*
2. Search for the interactive process viewer `htop`:
   ```bash
   $ apt search htop
   ```
3. Install `htop`:
   ```bash
   $ sudo apt install htop
   ```
4. Launch `htop` to observe CPU, memory, and process lists:
   ```bash
   $ htop
   ```
   *(Press `q` to quit and return to the terminal).*
5. Remove the package from the system:
   ```bash
   $ sudo apt remove htop
   ```

-----

## Exercise 8: Combining Commands with Pipes & Redirection

Explore linking program streams using the **pipe (`|`)** and appending outputs using **`>>`**.

1. `ps aux` lists all active processes. Use a pipe to pass this output to `grep` to filter for "bash":
   ```bash
   $ ps aux | grep "bash"
   ```
2. Create an activity log file `activity.log` with an initial timestamp:
   ```bash
   $ echo "$(date): Started lab work." > ~/IEI/activity.log
   ```
3. Append a second line without overwriting previous content using `>>`:
   ```bash
   $ echo "$(date): Finished Part I of the lab." >> ~/IEI/activity.log
   ```
4. Verify that the log contains both records:
   ```bash
   $ cat ~/IEI/activity.log
   ```

\newpage

# Part II: Customization, Scripting & Automation

## Exercise 9: Customizing Your Environment with `.bashrc`

Set up persistent shell aliases and shortcuts.

1. Open your `~/.bashrc` file using the `nano` editor:
   ```bash
   $ nano ~/.bashrc
   ```
2. Scroll to the end of the file and append the following alias definition:
   ```bash
   alias ll='ls -alF'
   ```
3. Save changes (`Ctrl + O`, then `Enter`) and exit the editor (`Ctrl + X`).
4. Apply the updated settings to the current terminal session:
   ```bash
   $ source ~/.bashrc
   ```
5. Test the shortcut:
   ```bash
   $ ll
   ```

-----

## Exercise 10: Understanding the `$PATH` Variable

Discover how the shell resolves executable commands.

1. Inspect your current `$PATH` environment variable:
   ```bash
   $ echo $PATH
   ```
   *(Notice it is a colon-separated list of directories).*
2. Create an executable script named `hello` (without file extension) inside `~/IEI`:
   ```bash
   $ echo '#!/bin/bash' > ~/IEI/hello
   $ echo 'echo "Hello from my custom script command!"' >> ~/IEI/hello
   $ chmod +x ~/IEI/hello
   ```
   *(In Linux, file extensions like `.sh` are optional; execution relies on the shebang `#!/bin/bash` and `+x` permissions).*
3. Try executing it directly by name:
   ```bash
   $ hello
   ```
   *(This fails with "command not found" because `~/IEI` is not in `$PATH`).*
4. Run the script using its relative path:
   ```bash
   $ cd ~/IEI
   $ ./hello
   ```
5. Temporarily append `~/IEI` to `$PATH` and run it by name from any folder:
   ```bash
   $ export PATH="$HOME/IEI:$PATH"
   $ cd ~
   $ hello
   ```
   *(This change to `$PATH` remains active only for the current terminal session. An in-depth study of environment variables, exporting, and persistence will be covered in the next class).*

-----

## Exercise 11: Bash Scripting Challenge

Automate standard project scaffolding with checks in a shell script.

1. Open a new script file in `nano`:
   ```bash
   $ nano ~/IEI/setup_project.sh
   ```
2. Enter the following script code:
   ```bash
   #!/bin/bash
   PROJECT_DIR="$HOME/IEI/my_project"

   # Validation: exit if project directory already exists
   if [ -d "$PROJECT_DIR" ]; then
     echo "Error: Directory '$PROJECT_DIR' already exists."
     exit 1
   fi

   mkdir -p "$PROJECT_DIR"
   echo "Created base directory: $PROJECT_DIR"

   # Create subfolders using a for loop
   for folder in assets source docs tests
   do
     mkdir "$PROJECT_DIR/$folder"
     echo "-> Created subfolder: $folder"
   done

   echo "Project layout initialized successfully!"
   ```
3. Save (`Ctrl + O`, then `Enter`) and exit (`Ctrl + X`).
4. Make the script executable and run it:
   ```bash
   $ chmod +x ~/IEI/setup_project.sh
   $ ~/IEI/setup_project.sh
   ```
5. Inspect the generated directory hierarchy:
   ```bash
   $ ls -R ~/IEI/my_project
   ```
6. Run the script again to confirm the `if [ -d ]` check catches existing folders:
   ```bash
   $ ~/IEI/setup_project.sh
   ```

-----

## Exercise 12: Scheduling Tasks with `cron`

Schedule an automated recurring task executed every minute.

1. **Create the Logger Script:** In `~/IEI`, create `log_time.sh`:
   ```bash
   $ echo '#!/bin/bash' > ~/IEI/log_time.sh
   $ echo 'date >> $HOME/IEI/cron_log.txt' >> ~/IEI/log_time.sh
   $ chmod +x ~/IEI/log_time.sh
   ```
2. **Find Your Absolute Path:**
   Cron tasks run in non-interactive environments and require absolute paths. Query the full path:
   ```bash
   $ echo "$HOME/IEI/log_time.sh"
   ```
   *(Example output: `/home/student/IEI/log_time.sh` or `/home/john/IEI/log_time.sh`).*
3. **Open Crontab:**
   Launch the user schedule editor:
   ```bash
   $ crontab -e
   ```
   *(If prompted to choose an editor, select `nano` — usually option 1).*
4. **Add the Job:**
   Scroll to the end and paste the schedule line (replace `/full/absolute/path` with the path printed in step 2):
   ```cron
   * * * * * /full/absolute/path/IEI/log_time.sh
   ```
   Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).
5. **Verify Job Execution:**
   > **Note for WSL (Windows Subsystem for Linux) Users:** In WSL, background daemons may not start automatically. Run: `sudo service cron start`.

   Wait approximately 2 minutes while cron runs. Then verify the log output:
   ```bash
   $ cat ~/IEI/cron_log.txt
   ```
6. **Clean Up:**
   To prevent the job from writing to disk indefinitely, remove the cron schedule:
   ```bash
   $ crontab -r
   ```
   *(⚠️ Warning: `crontab -r` deletes the user's entire crontab table without confirmation).*
