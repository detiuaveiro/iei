---
title: Virtualization
subtitle: Introduction to Computer Engineering
institute: Universidade de Aveiro
date: October 12, 2026
colorlinks: true
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

# Practical Laboratory Guide

This guide is designed for a **3-hour** laboratory session structured across five progressive parts exploring systems virtualization:

* **Part 1 — Virtualization Environment Setup:** Preparation of reference virtualization platforms through two distinct paradigms: graphical interface (Oracle VirtualBox) and command-line interface (QEMU on Linux and macOS).
* **Part 2 — Legacy Platform Emulation (FreeDOS):** Software emulation of x86-16 CPU instructions, classic audio peripherals (SoundBlaster 16), and secondary storage injection.
* **Part 3 — Systems Virtualization with Alpine Linux:** Deployment of a minimal Linux distribution, evaluation of virtual network topologies (NAT vs. Bridged), and HTTP network service hosting.
* **Part 4 — Nested Virtualization with Proxmox VE:** Deployment of a Type-1 bare-metal hypervisor inside a virtual machine (*nested virtualization*) and web console administration.
* **Part 5 — Autonomous Extension: Mobile Architecture Emulation (Android):** Mobile platform simulation and virtual peripheral management via the Android Virtual Device (AVD).

\vspace{0.5em}

### Workspace Directory Setup

Before starting the exercises, create and enter a dedicated workspace directory for today's session:

```bash
$ mkdir -p ~/IEI/class03
$ cd ~/IEI/class03
```

All files generated throughout the laboratory session (virtual disk images `*.qcow2`, downloaded ISO files, and shared folders) should be kept within this directory.

> **Note on File Paths:**
> All terminal commands in this guide assume that your working directory is `~/IEI/class03`. If you download ISO images into a different folder (such as your browser's default Downloads folder), either move them into `~/IEI/class03` or update the command arguments with the full path (e.g., `"$HOME/Downloads/FD14LIVE.iso"`).

-----

## Part 1: Virtualization Environment Setup

This guide provides two fundamental approaches to conduct the laboratory experiments: a **graphical approach** based on Oracle VirtualBox and a **command-line approach (CLI)** based on QEMU. You may choose one or explore both concurrently.

### Approach A: Graphical Interface (Desktop) — Oracle VirtualBox
*(Available for Windows, macOS, and Linux)*

1. **Download and Installation:**
   * Navigate to the [official VirtualBox download page](https://www.virtualbox.org/wiki/Downloads) and download the binary installer for your host operating system.
   * Download the **VirtualBox Extension Pack** available on the same page.
   * Run the installer following the default options. On macOS, you must grant permission for the Oracle system extension under `System Settings > Privacy & Security`.
   * Open the downloaded Extension Pack file to install enhanced device controllers (USB 2.0/3.0 support and RDP acceleration).

2. **VirtualBox Operational Workflow:**
   * Manage virtual machines using the graphical administration interface.
   * The **"New"** button launches a guided wizard to configure a new VM (defining system name, OS type, RAM allocation, and virtual storage).
   * Hardware attributes and virtual peripherals can be adjusted by selecting any VM and accessing **"Settings"**.

### Approach B: Command-Line Interface (CLI) — QEMU
*(Available natively on Linux, in WSL2 on Windows, natively on macOS via Homebrew, or inside the Ubuntu VM created in Class 00 via VirtualBox)*

1. **QEMU Installation:**
   * **On Linux / WSL2 (or inside the Class 00 Ubuntu VM):**
     Execute in the terminal:
     ```bash
     $ sudo apt update
     $ sudo apt install qemu-system-x86 qemu-system-i386 bridge-utils
     ```
     Add your user account to the `kvm` group to enable direct access to `/dev/kvm` without requiring `sudo` privileges (log out and back in to activate):
     ```bash
     $ sudo usermod -a -G kvm $USER
     ```
   * **On macOS:**
     Using the Homebrew package manager, execute in the terminal:
     ```bash
     $ brew install qemu
     ```

2. **General Syntax and Command Anatomy:**
   QEMU operates through explicit command-line flags, which will be utilized in the subsequent exercises:
   * **Disk Provisioning (`qemu-img`):** Uses the syntax `qemu-img create -f <format> <file> <size>` (for instance, creating dynamically expanding images in `qcow2` format).
   * **Virtual Machine Instantiation (`qemu-system-*`):** Invokes the binary corresponding to the target architecture (`qemu-system-i386` for 16/32-bit or `qemu-system-x86_64` for 64-bit), specifying the allocated resources:
     * `-m <RAM>`: Memory allocation (e.g., `128` or `1G`);
     * `-cpu <model>` or `-accel <type>`: Processor type and hardware acceleration (e.g., `tcg`, `kvm`, or `hvf`);
     * `-hda <disk>` / `-drive ...`: Primary hard drive or supplementary drives;
     * `-cdrom <iso>` and `-boot <order>`: Installation media and boot sequence (e.g., `-boot d` to boot from CD).

-----

## Part 2: Legacy Platform Emulation with FreeDOS

FreeDOS is an open-source, MS-DOS-compatible 16-bit single-tasking operating system. This experiment analyzes software-based emulation of legacy hardware circuitry (Cirrus Logic VGA display controllers, SoundBlaster 16 audio hardware, and real-time clock RTC).

1. **Resource Acquisition:**
   * Download the **FreeDOS 1.4 Live CD** image from the [official repository](https://www.freedos.org/download/), utilizing the compressed archive `FD14-LiveCD.zip` [available here](https://www.ibiblio.org/pub/micro/pc-stuff/freedos/files/distributions/1.4/FD14-LiveCD.zip). Extract the archive and place `FD14LIVE.iso` directly into your working directory `~/IEI/class03/`.
   * Obtain the compressed archive of shareware **DOOM** (`doom19s.zip`), available on the course's **eLearning** portal. Save it in `~/IEI/class03/` and extract it into the `./doom` subfolder:
     ```bash
     $ cd ~/IEI/class03
     $ mkdir -p doom
     $ unzip -o doom19s.zip -d doom/
     ```

2. **FreeDOS Virtual Machine Provisioning and Installation:**

   #### Option 1: Oracle VirtualBox (GUI)
   1. Click **"New"**. Set Name to `FreeDOS`, Type to `Other`, and Version to `DOS`.
   2. Memory: assign `64 MB`.
   3. Virtual Disk: create a fixed-size VDI image with `128 MB`.
   4. Navigate to **Settings > Storage**, select the empty IDE optical drive, and attach `FD14LIVE.iso` from your working directory.
   5. Launch the VM and follow the FreeDOS wizard. In the initial phase, the disk is partitioned via FDISK and requests a reboot; upon restarting, confirm formatting drive `C:` and proceed with package installation.
   6. Once installation completes, shut down the VM and unmount the ISO from the virtual optical drive.

   #### Option 2: QEMU (CLI)
   1. Ensure you are in the directory `~/IEI/class03` and create the 128 MB virtual disk image:
      ```bash
      $ cd ~/IEI/class03
      $ qemu-img create -f qcow2 freedos.qcow2 128M
      ```
   2. Launch the virtual machine using the installation Live CD:
      * **On Linux / WSL2 (with KVM/TCG acceleration and GTK display):**
        ```bash
        $ qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
            -k pt-pt -rtc base=localtime -device adlib -device sb16 \
            -device cirrus-vga -display gtk -hda freedos.qcow2 \
            -cdrom FD14LIVE.iso -boot d
        ```
      * **On macOS (with TCG emulation and native Cocoa display):**
        ```bash
        $ qemu-system-i386 -accel tcg -m 128 -cpu pentium \
            -rtc base=localtime -device adlib -device sb16 \
            -device cirrus-vga -display cocoa -hda freedos.qcow2 \
            -cdrom FD14LIVE.iso -boot d
        ```
   3. **FreeDOS Operating System Installation:**
      * Select "Install to harddisk".
      * The installer operates in two steps: it creates the MBR partition using FDISK and requests a restart. On subsequent boot, confirm formatting drive `C:` and allow file copying to complete.
      * When the final installation confirmation appears, close the QEMU window.

3. **Game Injection (DOOM) and Launch:**
   To inject the application binaries into the virtual machine:

   #### In VirtualBox:
   * Create an ISO image containing the `./doom` folder (or use system utilities).
   * Under **Settings > Storage**, attach an optical drive with that ISO image.
   * Boot FreeDOS. The secondary storage volume will appear as drive `D:`.

   #### In QEMU (Linux and macOS):
   * Boot FreeDOS from the hard disk (`-boot c`), mapping the local `./doom` folder directly as a virtual secondary FAT drive:
     * **On Linux / WSL2:**
       ```bash
       $ qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
           -k pt-pt -rtc base=localtime -device adlib -device sb16 \
           -device cirrus-vga -display gtk -hda freedos.qcow2 -boot c \
           -drive file=fat:rw:./doom,format=raw
       ```
     * **On macOS:**
       ```bash
       $ qemu-system-i386 -accel tcg -m 128 -cpu pentium \
           -rtc base=localtime -device adlib -device sb16 \
           -device cirrus-vga -display cocoa -hda freedos.qcow2 -boot c \
           -drive file=fat:rw:./doom,format=raw
       ```

4. **Game Setup and Execution in FreeDOS:**
   * At the FreeDOS command prompt (`C:\>`), switch to the secondary drive:
     ```bat
     D:
     dir
     ```
   * Run the installer:
     ```bat
     INSTALL.BAT
     ```
   * Follow the default installation steps (install to `C:\DOOM`). In audio configuration, choose **Sound Blaster** (Port 220, IRQ 5 or 7, DMA 1).
   * Launch the game:
     ```bat
     C:
     cd DOOM
     DOOM.EXE
     ```
   * Observe hardware emulation behavior: VGA display mode (320x200), RTC timer responsiveness, and audio synthesis through the emulated SoundBlaster 16 peripheral.

-----

## Part 3: Systems Virtualization with Alpine Linux

Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and BusyBox. It is widely utilized across the software industry as a base container image and for resource-efficient virtualized environments.

1. **Alpine Linux Image Acquisition:**
   * Visit the [official Alpine Linux downloads page](https://alpinelinux.org/downloads/) and download the **STANDARD** image, placing it in `~/IEI/class03/` named as `alpine.iso`:
     * On systems with x86-64 processors (Intel/AMD): download the **x86_64** ISO.
     * On macOS with Apple Silicon processors (M1/M2/M3/M4): download the **aarch64** ISO to leverage native hardware acceleration via Hypervisor.framework (`-accel hvf`).

2. **Virtual Machine Creation and Installation:**

   #### Option 1: Oracle VirtualBox (GUI)
   1. Create a new VM: Name `Alpine`, Type `Linux`, Version `Linux 2.6 / 3.x / 4.x (64-bit)`.
   2. RAM: `1 GB`. Virtual Disk: `8 GB`.
   3. Attach `alpine.iso` under **Settings > Storage**.
   4. Boot the VM and log in as `root` (no password). Run `setup-alpine`, choosing a `"sys"` disk installation onto `sda`. Upon completion, shut down the VM and detach the ISO image.

   #### Option 2: QEMU (CLI)
   1. Ensure you are in `~/IEI/class03` and create the virtual disk image:
      ```bash
      $ cd ~/IEI/class03
      $ qemu-img create -f qcow2 alpine.qcow2 8G
      ```
   2. Initiate installation from the ISO image:
      * **On Linux / WSL2 (with KVM and x86_64 ISO):**
        ```bash
        $ qemu-system-x86_64 -enable-kvm -m 1G -smp 2 -cpu host \
            -display gtk -hda alpine.qcow2 -cdrom alpine.iso -boot d
        ```
      * **On macOS Apple Silicon (with native HVF and aarch64 ISO):**
        ```bash
        $ qemu-system-aarch64 -accel hvf -M virt -cpu host -m 1G -smp 2 \
            -display cocoa -hda alpine.qcow2 -cdrom alpine.iso -boot d
        ```
        *(Note: if using the x86_64 image on macOS Apple Silicon, use `qemu-system-x86_64` with `-accel tcg`).*
   3. In the VM console, log in as `root` and run `setup-alpine`. Select a `"sys"` install on `sda`. When complete, shut down the VM and launch on subsequent boots without the `-cdrom` parameter.

3. **Virtual Network Topology Analysis:**
   * **NAT Mode (Default):**
     Boot the virtual machine in NAT mode and inspect its IP address:
     ```bash
     # Inside Alpine VM
     $ ip addr show
     ```
     Verify that the assigned address resides within a private internal subnet (e.g., `10.0.2.15`). Verify outbound connectivity with `ping google.com`. Observe that the VM reaches external networks, but host LAN devices cannot initiate inbound connections directly.
   * **Bridged Mode:**
     Shut down the virtual machine to reconfigure the network topology:
     * **In VirtualBox:** Under **Settings > Network**, switch **Attached to:** from `NAT` to `Bridged Adapter`.
     * **In QEMU (Linux):** Configure a network bridge interface on the host linked to the physical adapter:
       ```bash
       echo -e "Setup Bridge Interface"
       sudo /sbin/ip link add virtbr0 type bridge
       sudo /sbin/ip link set dev $INTERFACE master virtbr0
       sudo /sbin/ip addr flush dev $INTERFACE
       sudo /sbin/dhclient virtbr0
       sudo /sbin/ip link set dev $INTERFACE up
       sudo /sbin/ip link set dev virtbr0 up

       echo -e "Start Alpine (BRIDGE)"
       sudo qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
           -k pt-pt -rtc base=localtime -display gtk -hda alpine.qcow2 \
           -netdev bridge,id=net0,br=virtbr0 -device virtio-net-pci,netdev=net0

       echo -e "Clean Bridge Interface"
       sudo /sbin/ip link set virtbr0 down
       sudo /sbin/ip link del virtbr0
       sudo /sbin/dhclient $INTERFACE
       ```
     * Boot the VM again and execute `ip addr show`. Verify that the assigned IP address is now located on the same physical local area network as your host computer (e.g., `192.168.1.x`).

4. **Web Service Deployment (HTTP):**
   * BusyBox provides an embedded HTTP daemon (`httpd`). Install the extended utilities package:
     ```bash
     # Inside Alpine VM
     $ apk add busybox-extras
     ```
   * Create a directory to serve static web content:
     ```bash
     $ mkdir -p /var/www/localhost/htdocs
     ```
   * Create a simple HTML document:
     ```bash
     $ echo '<h1>Virtualization Lab - Alpine Linux</h1>' > /var/www/localhost/htdocs/index.html
     ```
   * Launch the web server listening on port 80:
     ```bash
     $ httpd -f -p 80 -h /var/www/localhost/htdocs
     ```
   * Open a web browser on the host machine and navigate to the Alpine VM's IP address. Confirm receipt of the HTTP response.

-----

## Part 4: Nested Virtualization with Proxmox VE

Proxmox Virtual Environment (VE) is an enterprise-grade open-source server virtualization platform based on Debian, integrating KVM for full hardware virtualization and LXC for operating-system containers.

> **TECHNICAL NOTE: Nested Virtualization**
> Running a hypervisor within another hypervisor requires hardware virtualization instructions from the physical CPU (Intel VT-x or AMD-V) to be propagated directly into the virtual CPU (vCPU). This nested execution imposes measurable computational overhead and is intended strictly for lab evaluation.

1. **Proxmox VE Acquisition:**
   * Navigate to the [official Proxmox VE download page](https://www.proxmox.com/en/downloads) and download the latest installer ISO image, placing it in `~/IEI/class03/` named `proxmox.iso`.

2. **Proxmox Virtual Machine Provisioning:**
   This virtual machine requires higher physical resource allocation:

   #### Option 1: Oracle VirtualBox (GUI)
   1. Create a VM: Name `Proxmox`, Type `Linux`, Version `Debian (64-bit)`.
   2. Memory: minimum of `4096 MB`. Processors: minimum of `2` vCPUs.
   3. Virtual Disk: `32 GB` or greater.
   4. Under **Settings > System > Processor**, enable **Enable Nested VT-x/AMD-V**.
   5. Under **Settings > Network**, retain `NAT`.
   6. Configure a **Port Forwarding** rule mapping host port `8006` to guest port `8006`.
   7. Attach `proxmox.iso` under storage.

   #### Option 2: QEMU (CLI)
   1. Ensure you are in `~/IEI/class03` and create the 32 GB virtual disk image:
      ```bash
      $ cd ~/IEI/class03
      $ qemu-img create -f qcow2 proxmox.qcow2 32G
      ```
   2. Launch the virtual machine with nested virtualization support and port forwarding for web port `8006`:
      * **On Linux / WSL2 (with KVM acceleration):**
        ```bash
        $ qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -cpu host \
            -hda proxmox.qcow2 -cdrom proxmox.iso -boot d \
            -netdev user,id=net0,hostfwd=tcp::8006-:8006 \
            -device virtio-net-pci,netdev=net0 -display gtk
        ```
      * **On macOS:**
        *(Note: Proxmox VE requires x86-64 architecture. On Intel macOS systems, it can run with `-accel hvf`. On Apple Silicon ARM64 Macs, running an x86 hypervisor requires full software emulation via TCG; running this exercise on native Linux or VirtualBox x86 is recommended).*

3. **Installation and Initial Configuration:**
   * Boot the virtual machine and proceed through the graphical Proxmox installer.
   * In static network configuration, assign an appropriate local management IP address (e.g., `192.168.1.200/24`).
   * Once installation finishes, restart the guest system and detach the ISO image.

4. **Accessing the Web Administration Console:**
   * On the Proxmox text console, inspect the displayed HTTPS management URL. Open your host machine's browser and navigate to `https://localhost:8006`.
   * Acknowledge the security warning regarding the self-signed TLS certificate.
   * Authenticate using the `root` username and the administrative password configured during installation.

5. **Deploying a Guest Instance in Proxmox:**
   * Explore virtual resource management within the Proxmox web portal.
   * Practical Challenge: Upload the Alpine Linux ISO image to Proxmox local storage and instantiate a nested virtual machine through the web GUI.

-----

## Part 5: Autonomous Extension — Mobile Architecture Emulation (Android)

Android platform emulation allows developers to simulate mobile processor architectures and hardware peripheral subsystems. Under the Android Studio GUI, the official emulator is powered by a specialized build of the QEMU engine.

1. **Android Studio Acquisition and Installation:**
   * Navigate to the [official Android Studio portal](https://developer.android.com/studio) and download the installer package for your operating system.
   * Complete the standard setup wizard, allowing the installer to download necessary Android SDK tools and components.

2. **Virtual Device Management (AVD Manager):**
   * Launch Android Studio (no development project is required).
   * From the welcome screen or the **Tools** menu, select **Virtual Device Manager** (AVD).

3. **Virtual Device Provisioning:**
   * Select **"Create Virtual Device..."**.
   * Choose a reference phone hardware profile (e.g., Google Pixel 7).
   * Select and download a recommended Android system image.
   * Confirm memory allocation parameters and name the AVD profile.

4. **Execution and Inspection of the Emulated System:**
   * In the AVD Manager, click the launch ("Play") action on the newly created device.
   * The emulation engine boots a complete Android operating system in an independent graphical window. Inspect boot latency, graphical acceleration responsiveness, and peripheral abstraction mechanisms.
