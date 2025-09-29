---
title: VirtualBox VM Setup
subtitle: Introdução Engenharia Informática
author: Mário Antunes
institute: Universidade de Aveiro
date: September 15, 2025
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
---

### Part 1: Installing VirtualBox 💻

First, install VirtualBox and the essential Extension Pack, which adds better device support and performance.

#### For Windows Hosts

1.  **Download:** Go to the official [VirtualBox downloads page](https://www.virtualbox.org/wiki/Downloads).
2.  Click the link for **"Windows hosts"** to download the installer.
3.  On the same page, download the **"VirtualBox Oracle VM VirtualBox Extension Pack"**.
4.  **Install VirtualBox:** Run the `.exe` installer. Accepting the default settings is fine.
5.  **Install Extension Pack:** Once VirtualBox is installed, double-click the downloaded `.vbox-extpack` file. VirtualBox will open and ask you to confirm the installation. Click **Install**.

#### For macOS Hosts (Intel CPU)

1.  **Download:** Visit the official [VirtualBox downloads page](https://www.virtualbox.org/wiki/Downloads).
2.  Click the link for **"macOS / Intel hosts"** to download the `.dmg` file.
3.  Download the **"VirtualBox Oracle VM VirtualBox Extension Pack"** from the same page.
4.  **Install VirtualBox:** Open the `.dmg` file and double-click the `VirtualBox.pkg` installer. Follow the prompts.
5.  **Approve the Kernel Extension:** During installation, macOS will block a system extension from Oracle. A popup will appear. Open **System Settings \> Privacy & Security**. Scroll down and you'll see a message that system software from "Oracle America, Inc." was blocked. Click **Allow**.
6.  **Install Extension Pack:** Double-click the downloaded `.vbox-extpack` file to have VirtualBox install it.

#### For macOS Hosts (Apple Silicon CPU - M1/M2/M3)

**Important:** The standard version of VirtualBox does **not** run on Apple Silicon Macs. You must use a special "Developer Preview" which may be unstable.

1.  **Download:** Go to the official [VirtualBox downloads page](https://www.virtualbox.org/wiki/Downloads).
2.  Find and click the link for **"macOS / Arm64 hosts"**. This will download the special preview version.
3.  Download the **"VirtualBox Oracle VM VirtualBox Extension Pack"**.
4.  **Install VirtualBox:** Open the `.dmg` and run the installer. The process is the same as for Intel Macs, including the need to **approve the kernel extension** in **System Settings \> Privacy & Security**.

-----

### Part 2: Download the Class VM Disk 📀

Before you can create the virtual machine, you need to download the pre-configured Debian virtual disk file.

1.  **Download the Disk:** Click the link below to download the virtual disk (`.vdi`) file.
      * **Link:** [Download Debian VM Disk from FCCN FileSender](https://filesender.fccn.pt/?s=download&token=6eb748bf-0687-412f-822c-942fdb369ae8)
2.  **Save the File:** The file is large, so the download may take some time. Save it to a location you can easily find later, like your `Downloads` or `Documents` folder.

-----

### Part 3: Creating the Debian VM

This process is the same on Windows and macOS. Follow these steps carefully to create the virtual machine "shell" and then attach the class disk file you just downloaded.

1.  **Start a New VM:**

      * Open VirtualBox and click the **"New"** button.
      * **Name:** `Debian IEI-TIA`
      * **Type:** `Linux`
      * **Version:** `Debian (64-bit)`
      * Click **Next**.

2.  **Allocate Memory (RAM):**

      * Set the memory size. **2048 MB (2 GB)** is a good starting point.
      * Click **Next**.

3.  **Configure the Hard Disk (CRITICAL STEP):**

      * You'll be asked to add a virtual hard disk. Since you're using a file provided by the class, select the option:
        **"Do not add a virtual hard disk"**

      * Click **Create**. A warning will appear; click **Continue**.

4.  **Attach the Provided Disk:**

      * Your new VM will appear in the list on the left with a warning icon.

      * Select the VM and click the **"Settings"** button.

      * Go to the **"Storage"** section.

      * In the "Storage Devices" panel, select the **"SATA Controller"** and click the small **"Add Hard Disk"** icon next to it.

      * In the new window, click the **"Add"** button.

      * Navigate to and select the Debian disk file you downloaded in Part 2.

      * Click **"Choose"** to attach it to the VM.

      * Click **"OK"** to save the settings. The warning icon should disappear.

5.  **Start the VM:**

      * Select your `Debian IEI-TIA` VM and click the green **"Start"** arrow.
      * The Debian system will boot. At the login prompt, use the credentials:
          * **User:** `student`
          * **Password:** `password`

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
