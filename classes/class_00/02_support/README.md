# Class 0 (Setup)

## VM 

The VM to be used in the classes can be found [here](https://filesender.fccn.pt/?s=download&token=6eb748bf-0687-412f-822c-942fdb369ae8)

## Setup the VM for the students

Since I am already using Linux (Slackware64-current), I will use the qemu tool to create a small disk and then install the latest debian on it.

1. Grab the latest version of debian netinstall from [here](https://www.debian.org/).
2. Create one virtual hard disk `qemu-img create -f qcow2 vm.qcow2 20G`
