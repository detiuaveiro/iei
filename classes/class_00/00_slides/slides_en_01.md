---
title: 47138 - Introduction to Computer Engineering
subtitle: Workspace Setup
institute: Universidade de Aveiro
date: September 14, 2026
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

# Setting Up Your Digital Workspace

**Session Goal:** Ensure that everyone has a development environment ready for lab classes.

### Session Agenda:
1. **Core concepts:** Operating systems and filesystems
2. **The Linux choice:** Why standardize on a Unix/Linux-based environment?
3. **Three setup paths:**
   - Option 1: Native installation (*dual-boot*)
   - Option 2: Pre-configured Virtual Machine (VirtualBox / UTM)
   - Option 3: Windows Subsystem for Linux (WSL 2)
4. **Comparison and next steps**

# What is an Operating System (OS)?

The Operating System is the **central manager** of all computer hardware and software resources:

- **Resource management:** CPU (processing), RAM (active memory), and storage (persistent data).
- **Interface:** Provides graphical user interfaces (GUI) and command-line interfaces (CLI).

### Major Operating System families:
- **Windows:** The most common desktop OS for personal computers.
- **Linux:** An open-source, Unix-based OS family. Dominates web servers, cloud computing (AWS, GCP, Azure), supercomputers, and software development.
- **macOS:** Based on Unix (Darwin/BSD). Shares command-line architecture (POSIX) with Linux.

# Filesystems

A filesystem is the **library catalog** of your computer. It defines how the OS organizes, stores, and finds your files. 🗂️

\vspace{2em}

**Understanding the path structure is crucial for locating your files and running programs from the command line\!**

## Filesystem - Windows (NTFS)

  - Uses independent **drive letters** (`C:`, `D:`).
  - Path separator: **backslash (`\`)**
    — E.g.: `C:\Users\Name\document.txt`.
  - File names are **case-insensitive**: `file.txt` and `File.txt` refer to the same file.

## Filesystem - Linux (ext4, Btrfs, etc.)

  - **Single, unified tree hierarchy** rooted at `/` (no drive letters).
  - Everything, including hardware devices, is treated as a file.
  - Path separator: **forward slash (`/`)**
    — E.g.: `/home/name/document.txt`.
  - File names are **case-sensitive**: `file.txt` $\neq$ `File.txt`.

# Why a Standardized Environment? (The Linux Choice)

In this course, we standardize work on a **Linux-based** command-line environment because:

- **Industry Standard:** It is the backbone of the Web, cloud computing (AWS, GCP, Azure), and scientific computing.
- **Unrivaled Tooling:** Powerful ecosystem of terminal utilities, scripting (Bash), programming, and automation.
- **Transparency and Control:** Allows deep understanding of what processes, networks, and the operating system are actually doing without hidden layers.

# Three Paths to the Linux Environment 🗺️

1. **Native Linux Installation (Dual-Boot or Dedicated)** 🐧
   - Linux is installed directly on the computer hardware.
   - *Best for:* Maximum performance and full immersion in the Linux ecosystem.

2. **Virtual Machine (Pre-configured VM)** 🖥️
   - A complete Linux computer runs inside a window on your host OS.
   - *Best for:* Safety, isolation, and simple restoration.

3. **Windows Subsystem for Linux (WSL 2)** 🪟+🐧
   - Direct integration of a native Linux kernel inside Windows.
   - *Best for:* Windows users who want a fast, integrated Linux terminal.

# Option 1: Native Linux Installation 🐧

Installing a Linux distribution directly on the hardware (alongside Windows in *dual-boot* or on a dedicated drive).

- **Pros:**
  - **✅ Maximum performance:** Direct access to CPU, GPU, and memory with zero virtualization overhead.
  - **✅ Total immersion:** Excellent for learning and adapting to the Linux environment.
- **Cons:**
  - **❌ Complex setup:** Requires disk partitioning and BIOS/UEFI configuration (risk of data loss).
  - **❌ Hardware compatibility:** Some hardware may not be fully supported or may require extra setup.

**Target audience:** Adventurous or experienced students, or those with a secondary computer available for testing.

# Option 1: Precautions and Installation Steps

### Essential precautions before starting:
- **Backup:** Back up all your important personal files.
- **BitLocker (Windows 11):** Save your 48-digit recovery key beforehand (available in your Microsoft account).

### Recommended steps:
1. **Distribution:** We recommend **Ubuntu 26.04 LTS** (stable, long-term support).
2. **Bootable USB drive:** Create one using tools like [Rufus](https://rufus.ie/) or [BalenaEtcher](https://www.balena.io/etcher/).
3. **Boot:** Restart, enter the boot menu (F12 / F2 / Del), and follow the installer instructions.

# Option 2: Virtual Machine (VM) 🖥️

A hypervisor (such as VirtualBox) emulates a complete computer in software, running a ready-made Linux image.

- **Pros:**
  - **✅ Complete safety (*sandbox*):** Any issue remains confined to the VM, without endangering the host OS.
  - **✅ Instant recovery:** Supports snapshots (restore points).
- **Cons:**
  - **❌ Resource consumption:** Requires a machine with 8 GB+ RAM and multi-core CPU, as it runs two operating systems at once.
  - **❌ Graphics performance:** Less visual fluidity compared to a native install.

**Target audience:** Default recommended option for most students due to the balance of safety and simplicity.

# Option 2: Installation and Recommendations

### Setup steps:
1. **Install VirtualBox:** Download the latest version of [VirtualBox](https://www.virtualbox.org/) and its Extension Pack.
2. **Download Linux Image:** Download a Linux .iso image, e.g., [Ubuntu 26.04 LTS](https://ubuntu.com/download/desktop).
3. **Create new VM:** In VirtualBox, select `Machine > New` and follow the prompts.
4. **Start:** Once created, select the VM and click **Start**.

**⚠️ Note for Mac users (Apple Silicon - M1/M2/M3/M4):** On Apple Silicon Macs, using **UTM** (with an Ubuntu ARM64 image) or native Unix tools via **Homebrew** is recommended.

# Option 3: Windows Subsystem for Linux (WSL 2) 🪟+🐧

WSL allows you to run a genuine Linux kernel and environment directly inside Windows, without the overhead of a full VM. It provides powerful integration between both systems.

# Option 3: Windows Subsystem for Linux (WSL 2) 🪟+🐧

### Notable features:
- **Networking:** WSL automatically shares the network connection of your Windows host.
- **Filesystem Integration:** Your Windows drives (like `C:`) are automatically mounted inside Linux at `/mnt/`. For instance, your folder `C:\Users\YourName` is accessible at `/mnt/c/Users/YourName`.

**⚠️ Important:** For best performance, always keep your project files inside the Linux filesystem (`/home/yourname/`), rather than on mounted Windows drives (`/mnt/c/`).

# Option 3: Windows Subsystem for Linux (WSL 2) 🪟+🐧

- **Pros:**
  - **✅ Excellent Performance:** Near-native speed for compilation and terminal tools.
  - **✅ Great integration:** Easily invoke Linux tools from Windows and vice-versa. For example, use VS Code on Windows to edit files directly inside WSL.
- **Cons:**
  - **❌ CLI-focused:** Primarily designed for command line (graphical applications require WSLg).
  - **❌ Potential Complexity:** Advanced networking or hardware access may be more complex than in a VM or native install.

**Target audience:** Windows users who want a fast, integrated command-line environment.

# Option 3: WSL 2 Installation

1. **Enable WSL:** Open **PowerShell** or **Windows Terminal** as **Administrator**.
2. **Run installation command:**
   ```powershell
   wsl --install
   ```
   *This enables required Windows features, downloads the latest Linux kernel, and installs Ubuntu by default.*
3. **Restart:** Reboot your computer when prompted.
4. **Set credentials:** In the launched Ubuntu terminal window, set your username and password (*remember this password!*).
5. **Access Linux terminal:** You can launch your Linux terminal from the Start Menu (search for "Ubuntu").

# Comparative Summary of Options

The ideal choice depends on your operating system, computer capabilities, and personal experience:

| Feature | Native Install | Virtual Machine (VM) | WSL 2 (Windows) |
| :--- | :---: | :---: | :---: |
| **Performance** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Isolation & Safety** | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Ease of Setup** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Host OS Integration** | N/A | ⭐ | ⭐⭐⭐ |
| **Recommended for** | Enthusiasts / Experienced | **Everyone (Safe default)** | Windows Users |

*macOS users: Can work directly in the native Unix terminal (with Homebrew) or use a VM via UTM.*

# Next Steps

1. **Choose and set up** one of the three options (Native, VM, or WSL 2) on your laptop.
2. **Test the Linux terminal:** Open the command line and verify that you have a working shell (`bash`).
3. **Confirm basic tools:** Verify that commands such as `whoami`, `uname -a`, and `pwd` respond properly.

### Questions or roadblocks?
- Seek guidance from professors during office hours and lab classes.
- Do not hesitate to ask classmates and teaching assistants.

**Having your workspace ready is the first major step toward success in this course. Happy coding! 🎉**
