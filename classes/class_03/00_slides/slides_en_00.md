---
title: 47138 - Introduction to Computer Engineering
subtitle: "Virtualization: Architecture, Hypervisors & Systems Virtualization"
institute: Universidade de Aveiro
date: October 12, 2026
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

This session covers architectural foundations and practical mechanisms of systems virtualization:

  * **Virtualization Fundamentals & Hypervisors:** Hardware abstraction, CPU privilege rings, Type-1 vs. Type-2 hypervisors.
  * **Emulation vs. Virtualization:** Software translation principles, relative performance, and engineering use cases.
  * **I/O, Storage & Virtual Networks:** VirtIO framework, virtual disk formats (QCOW2, VDI), and network topologies (NAT, Bridge, Host-Only).
  * **Practical Virtualization Tools:** Oracle VirtualBox, QEMU/KVM via CLI, Proxmox VE, and comparative matrix.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part I: Fundamentals \& Hypervisors}}
\end{center}

-----

## Virtualization: Definition

**Virtualization** abstracts physical hardware to instantiate multiple isolated virtual environments (*VMs*) on a single physical computer:

  * **Host:** Physical hardware platform (CPU, memory, storage, network interfaces).
  * **Hypervisor (VMM):** Software layer managing hardware, isolating instances, and scheduling physical resources.
  * **Virtual Machine (VM):** Isolated abstraction boundary exposing virtual hardware (vCPU, vRAM, vDisk, vNIC).
  * **Guest:** Operating system and applications executing within a VM.

\vspace{0.2em}

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.50\textheight,keepaspectratio]{virtual_vs_traditional_architecture.png}
\end{center}

-----

## The Virtualization Challenge: Privilege Rings

Modern processor architectures enforce hardware privilege levels (rings) to isolate application code from kernel execution:

  * **Ring 3 (User Space):** Applications execute non-privileged instructions. Privileged operations require invoking system calls (`syscall`) to the kernel.
  * **Ring 0 (Kernel Space / Supervisor Mode):** The operating system kernel executes privileged instructions (e.g., direct MMU control, interrupt handling, I/O ports).

  **How can multiple Guest OSs execute privileged instructions and manage hardware safely?**

  * The answer lies in the hypervisor as mediator and arbiter. Hypervisors intercept sensitive instructions and mediate hardware access, delegating direct execution to physical hardware whenever possible.

-----

## Hypervisor Types: Type-1 and Type-2

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.75\textheight,keepaspectratio]{hypervisor_types.png}
\end{center}

-----

## Type-1 Hypervisors (Bare-Metal)

**Type-1 Hypervisors** execute directly on physical hardware without an intermediary general-purpose operating system:

  * **Execution Layer:** Operates directly at the hardware privilege layer. The hypervisor acts as the primary kernel and resource arbiter.
  * **Architecture:** Device drivers and management domains run within a minimal hypervisor microkernel or a dedicated management partition (e.g., Xen Dom0, Linux KVM).
  * **Key Characteristics:**
      * Negligible abstraction overhead and sub-millisecond hypervisor latency.
      * High I/O throughput and maximum hardware resource utilization efficiency.
      * Independent of desktop operating system lifecycle or failures.
  * **Production Examples:** VMware ESXi, Proxmox VE / KVM, Microsoft Hyper-V, Xen.

-----

## Type-2 Hypervisors (Hosted)

**Type-2 Hypervisors** execute as standard user-space processes on top of an existing host operating system:

  * **Execution Layer:** Relies on the host operating system kernel for physical resource scheduling, memory management, and device drivers.
  * **Architecture:** Uses kernel-mode drivers to access hardware virtualization extensions, routing I/O requests through host OS subsystems.
  * **Key Characteristics:**
      * Double scheduling overhead: guest kernel schedules virtual processes, and host OS schedules hypervisor processes.
      * Straightforward installation and usage on workstations and personal laptops.
      * Convenient desktop integration between host and guest (shared clipboard, dynamic window resizing, shared folders).
  * **Production Examples:** Oracle VirtualBox, VMware Workstation, Parallels Desktop.

-----

## Hypervisor Comparison: Type-1 vs. Type-2

| Architectural Dimension | Type-1 (Bare-Metal) | Type-2 (Hosted) |
| :--- | :--- | :--- |
| **Execution Layer** | Directly on physical hardware | On top of Host OS |
| **Host OS Requirement** | None (hypervisor is the kernel) | Standard desktop/server OS mandatory |
| **Performance Overhead** | Minimal (< 2% CPU overhead) | Moderate (dual scheduler and I/O stack latency) |
| **I/O Latency** | Direct / Near-native | Mediated by host OS drivers |
| **Fault Isolation** | High (independent VMs) | Bound to host OS stability |
| **Primary Use Cases** | Data Centers, Cloud (AWS, GCP) | Software Development, Testing, Education |
| **Representative Tools**| Proxmox VE, VMware ESXi, KVM | Oracle VirtualBox, VMware Workstation |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part II: Emulation vs. Virtualization}}
\end{center}

-----

## Emulation: Definition and Use Cases

**Emulation** reconstructs hardware behavior and instruction set architecture (ISA) entirely through software:

  * **Mechanism:** Software interpreter or Dynamic Binary Translator (JIT). The emulator translates each guest instruction into native host CPU instructions in real time.
  * **Architectural Independence:** Guest ISA can differ completely from host ISA (e.g., executing ARM64, PowerPC, or legacy x86-16 code on an x86-64 host).
  * **Performance Overhead:** Very high computational penalty (typically 5x to 20x slower than native execution).
  * **Engineering Use Cases:**
      * Legacy operating systems and software (e.g., FreeDOS with SoundBlaster emulation in Lab Part 2).
      * Cross-platform embedded development (e.g., QEMU for ARM or RISC-V).
      * Mobile ecosystem simulation (e.g., Android Virtual Device / AVD).

-----

## Emulation vs. Virtualization

| Dimension | Software Emulation | Hardware-Assisted Virtualization |
| :--- | :--- | :--- |
| **Instruction Set (ISA)** | Can differ (e.g., ARM on x86) | Must match (e.g., x86 on x86) |
| **Instruction Execution** | Translated instruction by instruction in software | Executed directly on CPU silicon |
| **CPU Performance** | Very slow (5x to 20x penalty) | Near-native (< 3% overhead) |
| **I/O Performance** | Very slow (circuits simulated in code) | Accelerated by paravirtualized drivers (VirtIO) |
| **Flexibility** | Maximum (any hardware can be simulated) | Constrained to host physical CPU architecture |
| **Practical Example** | FreeDOS / DOOM (Lab Part 2) | Alpine Linux / VirtualBox (Lab Part 3) |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part III: I/O, Storage \& Virtual Networks}}
\end{center}

-----

## I/O Virtualization: Emulated Hardware vs. VirtIO Framework

Input/output (I/O) devices (disk and network) represent the primary performance bottleneck in virtualization:

  * **Emulated Hardware (Compatible, but Slow):**
      * The hypervisor simulates legacy hardware circuits in software (e.g., Intel E1000 NIC, IDE disk controller).
      * Allows any guest OS to run without extra drivers, but every I/O read/write must be intercepted and simulated by the hypervisor.
      * Leads to high latency and CPU overhead under intensive network traffic or disk transfers.
  * **Paravirtualized I/O with VirtIO (Cooperative and Efficient):**
      * The guest OS uses specialized (**VirtIO**) drivers that are aware they run inside a virtual machine.
      * Eliminates hardware simulation: guest and hypervisor exchange data directly through shared memory queues.
      * Batches requests with minimal overhead, achieving near-native throughput (the industry standard in cloud instances and in QEMU via `-device virtio-net-pci`).

-----

## Direct Hardware Access: Passthrough & IOMMU

**Passthrough** grants a virtual machine exclusive and direct control over a physical host peripheral (PCIe or USB):

  * **Native Performance:** Guest OS drivers interact directly with physical device circuits, bypassing hypervisor translation and overhead.
  * **The Role of the IOMMU (Hardware Security Isolation):**
      * Hardware component in CPU and motherboard chipset (Intel **VT-d**, AMD **AMD-Vi**).
      * **Memory Isolation:** Restricts physical device memory accesses strictly to the RAM assigned to that target VM, preventing devices from touching host or peer VM memory.
  * **Engineering Use Cases:**
      * **Dedicated GPU:** Graphics acceleration and AI / Machine Learning model training inside a VM.
      * **USB Peripherals:** Direct connection of microcontrollers and dev boards (Arduino, ESP32) to virtual machines.

-----

## Virtual Storage: Virtual Disk Architectures

Virtual machines store persistent data in virtual disk image files that encapsulate guest filesystem blocks:

  * **RAW Format:**
      * Linear sector-by-sector copy of a physical disk.
      * Maximum sequential read and write performance.
      * Does not natively support internal snapshots, sparse expansion, or compression.
  * **QCOW2 Format (QEMU Copy-On-Write 2):**
      * Advanced format supporting dynamic allocation, compression (zstd/zlib), and multi-level snapshots.
      * Implements backing files: a base golden image can be shared across multiple VMs via differential write layers.
  * **VDI (VirtualBox) & VMDK (VMware) Formats:**
      * Workstation-oriented disk containers supporting dynamic expansion and point-in-time snapshots.

-----

## Storage Provisioning: Fixed vs. Dynamic Allocation

Virtual disk images support two primary storage allocation strategies:

  * **Preallocated Allocation (Fixed / Preallocated):**
      * The hypervisor immediately reserves the total specified capacity on host storage at creation time (e.g., creates a 20 GB file immediately).
      * Advantages: Eliminates host filesystem fragmentation and guarantees predictable write latency under heavy loads.
      * Disadvantage: Consumes uncommitted host storage while the guest filesystem remains sparsely filled.
  * **Dynamic Allocation (Sparse / Thin Provisioned):**
      * The virtual disk file starts small with metadata and grows on-demand as new blocks are written by the guest OS.
      * Advantages: Maximizes storage density and enables storage overcommitment.
      * Disadvantage: Slight write penalty upon allocating new blocks and risk of host disk exhaustion if overcommitted.

-----

## Virtual Networking: NAT Mode & Port Forwarding

The hypervisor manages network connectivity between virtual machines and external networks:

  * **NAT Mode (Default):**
      * The virtual machine shares the host computer's network connection.
      * **Internet Access:** Guest reaches the internet seamlessly without additional network configuration (e.g., package downloads, web browsing).
      * **Inbound Isolation:** External local network devices cannot initiate connections directly to the VM.
  * **Port Forwarding:**
      * Creates an explicit conduit from a specific host port to a service port inside the VM.
      * **Practical Example:** Mapping host `localhost:8006` $\to$ VM port `8006` enables accessing the Proxmox web portal in the host browser without exposing the VM to the external LAN.

-----

## Virtual Networking: Bridged Mode & Host-Only Mode

Alternative topologies for server deployments and isolated laboratory testbeds:

  * **Bridged Mode:**
      * The virtual machine behaves as an independent physical device attached directly to the local router.
      * Obtains its own IP address from the physical LAN DHCP server (e.g., `192.168.1.x`), just like a separate physical computer.
      * **Ideal for Servers:** Any device on the local network can access services hosted in the VM (as demonstrated with the Alpine web server exercise).
  * **Host-Only Mode:**
      * Creates a strictly isolated private network accessible exclusively between host and guest VMs.
      * No route to external internet or physical LAN; ideal for secure testbeds and controlled development.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Part IV: Practical Virtualization Tools}}
\end{center}

-----

## Oracle VirtualBox: Desktop Architecture & Workflow

Oracle VirtualBox provides a production-grade Type-2 virtualization platform tailored for desktop workstations:

  * **Core Components:**
      * **VirtualBox Graphical Manager:** Intuitive desktop GUI for VM creation, snapshot management, and media configuration.
      * **VBoxManage CLI:** Scriptable command-line interface providing complete programmatic control of all hypervisor capabilities.
      * **VirtualBox Guest Additions:** Kernel modules installed inside the guest for graphical acceleration, seamless mouse integration, dynamic display resizing, and bidirectional clipboard sharing.
  * **Extension Pack:** Additional package supporting USB 2.0/3.0 controllers, webcam passthrough, and RDP encryption.

-----

## QEMU + KVM: Architecture & Kernel Integration

The combination of QEMU + KVM forms the backbone of modern Linux server virtualization and cloud infrastructure:

  * **KVM (Kernel-based Virtual Machine):**
      * Linux kernel module (`kvm.ko`, `kvm-intel.ko` / `kvm-amd.ko`) exposing the `/dev/kvm` character device.
      * Turns the Linux kernel into a Type-1 hypervisor, handling CPU scheduling, memory virtualization (EPT/NPT), and hardware execution.
  * **QEMU (Quick EMUlator):**
      * User-space process managing device emulation, buses, storage backends, and graphical display pipelines.
      * When executed with `-enable-kvm`, guest CPU instructions execute directly on physical CPU cores via KVM, achieving near-native performance.

-----

## QEMU/KVM Configuration and Permissions

Setting up the KVM virtualization environment on Debian/Ubuntu-based distributions:

  * **1. Hypervisor Package Installation:**
    ```bash
    $ sudo apt update
    $ sudo apt install qemu-system-x86 kvm bridge-utils
    ```
  * **2. Execution Permissions:** Add the user to the `kvm` group to enable direct access to `/dev/kvm` without `root` privileges:
    ```bash
    $ sudo usermod -aG kvm $USER
    ```

-----

## Disk Management with `qemu-img`

Command-line virtual disk creation and inspection:

  * **Create Thin-Provisioned QCOW2 Image:**
    ```bash
    $ qemu-img create -f qcow2 disco_alpine.qcow2 8G
    ```
  * **Inspect Disk Format and Allocated Footprint:**
    ```bash
    $ qemu-img info disco_alpine.qcow2
    ```

-----

## Launching a Virtual Machine in QEMU

Complete command to instantiate a VM integrating KVM acceleration, VirtIO storage, and network:

```bash
$ qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -smp 4 \
    -cpu host \
    -drive file=disco_alpine.qcow2,if=virtio,format=qcow2 \
    -netdev user,id=net0,hostfwd=tcp::8080-:80 \
    -device virtio-net-pci,netdev=net0 \
    -display gtk
```

  * `-enable-kvm` & `-cpu host`: Enables native hardware acceleration via the KVM kernel module.
  * `-m 4096` & `-smp 4`: Allocates 4 GB of RAM and 4 virtual CPU cores.
  * `-drive if=virtio`: High-performance virtual disk utilizing VirtIO drivers.
  * `-netdev ... -device virtio-net-pci`: VirtIO network adapter in NAT mode with port forwarding (`8080` host $\to$ `80` VM).
  * `-display gtk`: Launches a graphical window for guest console interaction.

-----

## Proxmox Virtual Environment (VE)

**Proxmox VE** is an open-source enterprise virtualization platform for server infrastructure management:

  * **Underlying Architecture:** Built on Debian Linux, integrating KVM for hardware-assisted virtualization and LXC for system containers.
  * **Management Interface:** Centralized web portal accessible by default on port `8006` (`https://<server-ip>:8006`) with complete REST API support.
  * **Storage and Networking:** Out-of-the-box support for enterprise storage (ZFS, Ceph, LVM-thin, NFS) and Linux network bridges (`vmbr0`).
  * **Laboratory Testbeds (Nested Virtualization):** On personal workstations, it can run inside another hypervisor (VirtualBox or QEMU) via **nested virtualization**.

-----

## Hypervisor Ecosystem: Comparative Matrix

| Evaluation Dimension | Oracle VirtualBox | QEMU + KVM | Proxmox VE |
| :--- | :--- | :--- | :--- |
| **Hypervisor Type** | Type-2 (Hosted) | Type-1 / Hybrid | Type-1 (Bare-Metal) |
| **Host Operating System** | Windows, macOS, Linux | Linux | Dedicated Debian Base |
| **Primary Interface** | Desktop GUI | Command-Line Interface (CLI) | Centralized Web Portal |
| **Performance Overhead**| Moderate | Minimal (Near-native) | Minimal (Production grade) |
| **Automation Capabilities**| VBoxManage (Good) | CLI Flags / Libvirt (Broad) | REST API / CLI / GUI (Total)|
| **Storage Formats** | VDI, VMDK | RAW, QCOW2 | ZFS, Ceph, QCOW2, LVM |
| **Target Audience** | Desktop users, students | Kernel developers, sysadmins | Data centers, server clusters |

-----

## Authorized Technical References

Official documentation and architectural specifications for systems engineering study:

  * **Kernel-based Virtual Machine (KVM):**
      * [Linux Kernel Virtualization Documentation](https://docs.kernel.org/virt/kvm/)
  * **QEMU System Emulation:**
      * [QEMU System Emulation User Guide](https://www.qemu.org/docs/master/system/index.html)
  * **Oracle VirtualBox:**
      * [Oracle VirtualBox User Manual](https://www.virtualbox.org/manual/)
  * **Proxmox Virtual Environment:**
      * [Proxmox VE Administration Guide](https://pve.proxmox.com/pve-docs/)
  * **VirtIO Specification:**
      * [OASIS VirtIO Standard Specification](https://docs.oasis-open.org/virtio/virtio/v1.2/virtio-v1.2.html)
