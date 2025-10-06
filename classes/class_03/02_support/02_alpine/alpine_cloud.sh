#!/usr/bin/env bash

# Set variables
IMAGE_URL="https://dl-cdn.alpinelinux.org/alpine/v3.22/releases/cloud/generic_alpine-3.22.1-x86_64-bios-cloudinit-r0.qcow2"
RESTART=false

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Helper script to emulate freedos using qemu"
   echo
   echo "Syntax: freedos [-h]"
   echo "options:"
   echo "h     Print this Help."
   echo
}

############################################################
# Help                                                     #
############################################################
Setup()
{
    echo -e "Download Alpine Cloud..."
    curl -L $IMAGE_URL --output alpine_cloud.qcow2 --progress-bar
}


############################################################
############################################################
# Main program                                             #
############################################################
############################################################
############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts "rh" option; do
   case $option in
        h) # display Help
            Help
            exit;;
        r) # restart: deletes the disk and start the setup again
            RESTART=true
            ;;
        \?) # Invalid option
            echo -e "Invalid option: -${OPTARG}."
            exit;;
   esac
done

if [ $RESTART = true ]; then
    echo -e "Restart, by deleting alpine_cloud.qcow2"
    rm -rf alpine_cloud.qcow2
    rm -rf config.img
fi

if [ ! -f alpine_cloud.qcow2 ]; then
    echo -e "Alpine Cloud disk not found, initiate setup..."
    Setup
fi

if [ ! -f config.img ]; then
    echo -e "Setup Cloud-init"
    # Create empty virtual hard drive file
    dd if=/dev/zero of=config.img bs=1 count=0 seek=2M > /dev/null 2>&1
    # put correct filesystem and disk label on
    /sbin/mkfs.vfat -n cidata config.img > /dev/null 2>&1
    # mount it somewhere so you can put the config data on
    mkdir -p mnt/cloud-init/
    sudo mount config.img mnt/cloud-init/
    sudo cp -vf user-data mnt/cloud-init/user-data
    sudo cp -vf meta-data mnt/cloud-init/meta-data
    sudo umount mnt/cloud-init/
    rm -rf mnt/cloud-init/
fi

#echo -e "Start Alpine"
qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
    -k pt-pt -rtc base=localtime -display gtk -hda alpine_cloud.qcow2 \
    -net user,hostfwd=tcp::5555-:22 -net nic \
    -drive file=config.img,format=raw 

echo -e "Done..."