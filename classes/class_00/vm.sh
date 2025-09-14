#!/usr/bin/env bash

qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 4 \
-m 4G \
-display gtk \
-drive file=vm.qcow2 \
-cdrom debian-13.1.0-amd64-netinst.iso \
-boot d