#!/usr/bin/env bash

# Set variables
DISK="alpine_disk.qcow"
DISK_SIZE="10G"
IMAGE_URL="https://dl-cdn.alpinelinux.org/alpine/v3.22/releases/x86_64/alpine-standard-3.22.1-x86_64.iso"
INTERFACE=$(sudo /sbin/ip route get 8.8.8.8 | awk '{print $5}')
NETWORK="nat"
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
# Setup                                                    #
############################################################
Setup()
{
    echo -e "Create a qemu disk as storage for FreeDos"
    qemu-img create -f qcow2 $DISK $DISK_SIZE > /dev/null 2>&1

    if [ ! -f alpine.iso ]; then
        echo -e "Download Alpine Standard Image..."
        curl -L $IMAGE_URL --output alpine.iso --progress-bar
    fi

    echo -e "Start VM for linux setup"
    qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
    -k pt-pt -rtc base=localtime -display gtk -hda $DISK -cdrom alpine.iso \
    -net nic -net user,hostfwd=tcp::5555-:22 -boot d

    #rm -rf alpine.iso
}

############################################################
# NAT                                                      #
############################################################

VM_NAT()
{
    echo -e "Start Alpine (NAT)"
    sudo qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
    -k pt-pt -rtc base=localtime -display gtk -hda $DISK \
    -net nic -net user,hostfwd=tcp::5555-:22 \
    -net user,hostfwd=tcp::8888-:80
}

############################################################
# BRIDGE                                                   #
############################################################

VM_BRIDGE()
{
    echo -e "Setup Bridge Interface"
    sudo /sbin/ip link add virtbr0 type bridge
    sudo /sbin/ip link set dev $INTERFACE master virtbr0
    sudo /sbin/ip addr flush dev $INTERFACE
    sudo /sbin/dhclient virtbr0
    sudo /sbin/ip link set dev $INTERFACE up
    sudo /sbin/ip link set dev virtbr0 up

    echo -e "Start Alpine (BRIDGE)"
    sudo qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
    -k pt-pt -rtc base=localtime -display gtk -hda $DISK \
    -netdev bridge,id=net0,br=virtbr0 -device virtio-net-pci,netdev=net0

    echo -e "Clean Bridge Interface"
    sudo /sbin/ip link set virtbr0 down
    sudo /sbin/ip link del virtbr0
    sudo /sbin/dhclient $INTERFACE
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
while getopts ":d:s:n:rh" option; do
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
        n) # define network
            NETWORK="${OPTARG}"
            ;;
        r) # restart: deletes the disk and start the setup again
            RESTART=true
            ;;
        \?) # Invalid option
            echo -e "Invalid option: -${OPTARG}."
            exit;;
   esac
done

if [ $RESTART = true ]; then
    echo -e "Restart, by deleting $DISK"
    rm -rf $DISK
fi

if [ ! -f $DISK ]; then
    echo -e "Alpine disk not found, initiate setup..."
    Setup
fi

case $NETWORK in

  nat)
    VM_NAT
    ;;

  bridge)
    VM_BRIDGE
    ;;
esac

echo -e "Done..."