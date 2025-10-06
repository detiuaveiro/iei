#!/usr/bin/env bash

# Set variables
DISK="freedos_disk.qcow"
DISK_SIZE="128M"
IMAGE_URL="https://www.ibiblio.org/pub/micro/pc-stuff/freedos/files/distributions/1.4/FD14-LiveCD.zip"
DOOM_URL="https://github.com/detiuaveiro/iei/blob/master/classes/class_03/02_support/01_freedos/games/doom19s.zip?raw=true"
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
    echo -e "Create a qemu disk as storage for FreeDos"
    qemu-img create -f qcow2 $DISK $DISK_SIZE > /dev/null 2>&1

    if [ ! -f FreeDos.zip ]; then
        echo -e "Download FreeDos..."
        curl -L $IMAGE_URL --output FreeDos.zip --progress-bar
    fi
    mkdir -p /tmp/freedos/
    unzip -o FreeDos.zip -d /tmp/freedos/
    
    qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
    -k pt-pt -rtc base=localtime -device adlib -device sb16 \
    -device cirrus-vga -display gtk -hda $DISK \
    -cdrom /tmp/freedos/FD14LIVE.iso -boot d

    rm -rf /tmp/freedos/
    #rm -rf FreeDos.zip
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
while getopts ":d:s:rh" option; do
   case $option in
        h) # display Help
            Help
            exit;;
        d) # define disk name
            echo -e "d) ${OPTARG}"
            DISK="${OPTARG}"
            ;;
        s) # define disk size
            DISK_SIZE="${OPTARG}"
            ;;
        r) # restart: deletes the disk and start the setup again
            RESTART=true
            ;;
        \?) # Invalid option
            echo -e "Invalid option: -${OPTARG}."
            exit;;
   esac
done

echo -e "Using disk $DISK with size $DISK_SIZE..."

if [ $RESTART = true ]; then
    echo -e "Restart, by deleting $DISK"
    rm -Rf $DISK
fi

if [ ! -f $DISK ]; then
    echo -e "FreeDos disk not found, initiate setup..."
    Setup
fi

if [ ! -f games/doom19s.zip ]; then
    mkdir -p games
    curl -L $DOOM_URL --output games/doom19s.zip --progress-bar
fi

echo -e "Setup D: to hold doom instalation files"
mkdir -p /tmp/games/doom
unzip -o games/doom19s.zip -d /tmp/games/doom/

echo -e "Start FreeDos"
qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
    -k pt-pt -rtc base=localtime -device adlib -device sb16 \
    -device cirrus-vga -display gtk -hda $DISK -boot c \
    -drive file=fat:rw:/tmp/games/doom,format=raw 

rm -rf /tmp/games/doom

echo -e "Done..."