---
title: VirtualBox VM Setup
subtitle: Introdução Engenharia Informática
#author: Mário Antunes
institute: Universidade de Aveiro
date: September 14, 2026
colorlinks: true
highlight-style: tango
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

### Part 1: Installing VirtualBox 💻

First, install VirtualBox and the essential Extension Pack, which adds better device support and performance.

#### For Windows Hosts

1.  **Download:** Go to the official [VirtualBox downloads page](https://www.virtualbox.org/wiki/Downloads).
2.  Click the link for **"Windows hosts"** to download the installer.
3.  On the same page, download the **"VirtualBox Oracle VM VirtualBox Extension Pack"**.
4.  **Install VirtualBox:** Run the `.exe` installer. Accepting the default settings is fine.
5.  **Install Extension Pack:** Once VirtualBox is installed, double-click the downloaded `.vbox-extpack` file. VirtualBox will open and ask you to confirm the installation. Click **Install**.

#### For macOS Hosts

1.  **Download:** Visit the official [VirtualBox downloads page](https://www.virtualbox.org/wiki/Downloads).
2.  Click the link for **"macOS / Intel hosts"** (if you have an Intel CPU) or **"macOS / Apple Silicon hosts"** (if you have an Apple Silicon CPU) to download the `.dmg` file.
3.  Download the **"VirtualBox Oracle VM VirtualBox Extension Pack"** from the same page.
4.  **Install VirtualBox:** Open the `.dmg` file and double-click the `VirtualBox.pkg` installer. Follow the prompts.
5.  **Approve the Kernel Extension:** During installation, macOS will block a system extension from Oracle. A popup will appear. Open **System Settings \> Privacy & Security**. Scroll down and you'll see a message that system software from "Oracle America, Inc." was blocked. Click **Allow**.
6.  **Install Extension Pack:** Double-click the downloaded `.vbox-extpack` file to have VirtualBox install it.

-----

### Part 2: Download the Linux VM Image 📀

Before you can create the virtual machine, you need to download the Linux distribution image. You can use any distro and flavour you want. We recommend Debian or Ubuntu.

1.  **Download the Image:** Click the link below to download the Linux distribution image (`.iso`) file.
      * **Link:** [Ubuntu 26.04 LTS](https://ubuntu.com/download/desktop)
2.  **Save the File:** The file is large, so the download may take some time. Save it to a location you can easily find later, like your `Downloads` or `Documents` folder.

-----

### Part 3: Creating the Linux VM

This process is the same on Windows and macOS. Follow these steps carefully to create the virtual machine "shell" and then attach the class disk file you just downloaded.

1.  **Start a New VM:**

      * Open VirtualBox and click the **"New"** button.
      * Set the options as follows:
      * **ISO Image:** Select the Linux image you just downloaded.
      * **VM Name:** `Linux IEI-TIA` (or another name you like).
      * **VM Folder:** leave it as is.
      * **OS:** `Linux`
      * **OS Distribution:** `Ubuntu` (or the distro you downloaded).
      * **OS Version:** `Ubuntu 26.04 LTS` (or the distro you downloaded). The exact version might not exist, pick a close one. Or leave the value picked by default.
      * Untick **Proceed with Unattended Installation**.
      * Click **Next**.

2.  **Allocate Memory (RAM), CPUs, Disk Size:**

      * Set the base memory size. **2048 MB (2 GB)** is a good starting point, but **4096 MB (4 GB)** or more is better if you have the resources available.
      * Set the number of CPUs. **2** is a good starting point, but **4** or more is better if you have the resources available.
      * Set the disk size (the disk space you will have in the VM). At least 25GB is recommended.
      * Click **Next** and **Finish**.

3.  **Start the VM:**

      * Select your `Linux IEI-TIA` VM and click the green **"Start"** arrow.
      * The Linux system will boot. Follow the instructions to install Linux.

-----

### Part 4: Installing Guest Additions for Better Performance 🚀

Guest Additions are drivers that improve performance, allow a resizable screen, and enable a shared clipboard.

1.  **Prepare the System:**

      * Once logged into the VM, open a terminal. First, update your package lists, then install the tools required to build the Guest Additions.
        ```bash
        $ sudo apt update
        $ sudo apt install build-essential dkms linux-headers-$(uname -r)
        ```

    The `$(uname -r)` part automatically inserts your current kernel version, ensuring you get the correct files.

2.  **Insert the Guest Additions CD:**

      * In the VirtualBox window menu for your running VM, go to **Devices \> Insert Guest Additions CD image...**.

3.  **Mount the CD and Install:**

      * In the VM's terminal, create a mount point and mount the CD drive.
        ```bash
        $ sudo mkdir -p /mnt/cdrom
        $ sudo mount /dev/cdrom /mnt/cdrom
        ```
      * Now, run the installer script from the mounted CD.
        ```bash
        $ sudo /mnt/cdrom/VBoxLinuxAdditions.run
        ```
      * After the installation finishes, reboot the VM for the changes to take effect.
        ```bash
        $ sudo reboot
        ```

    Your VM should now feel much smoother and more responsive.

-----

### Part 5: FAQ & Troubleshooting ❓

  * **"My VM is running very slow."**

      * The most common reason is that Guest Additions are not installed. Follow Part 4. You can also shut down the VM and give it more resources in **Settings \> System \> Processor** (increase to 2 CPUs).

  * **"My mouse is stuck inside the VM window\!"**

      * This is the main symptom of missing Guest Additions. The temporary fix is to press the **Host Key** to release the mouse. This key is the **Right Ctrl** key on Windows/Linux and the **Left Command (⌘)** key on macOS.

  * **"VirtualBox says VT-x is not available or I can only create 32-bit VMs." (Windows)**

      * This means hardware virtualization is disabled on your computer. You must restart your computer, enter the **BIOS/UEFI settings**, and look for an option called **"Intel Virtualization Technology (VT-x)"** or **"AMD-V"**. **Enable** it and save your settings.

  * **"A popup on my Mac says 'System Extension Blocked'."**

      * This is normal. Open **System Settings \> Privacy & Security**. Scroll down until you see a message about software from "Oracle America, Inc." and click the **Allow** button. You may need to restart the installation.

  * **"Guest Additions installation failed."**

      * This usually means the kernel headers are missing or incorrect. Carefully re-run the command from Step 1 of Part 4 to ensure the correct packages are installed:
        `$ sudo apt install build-essential dkms linux-headers-$(uname -r)`
