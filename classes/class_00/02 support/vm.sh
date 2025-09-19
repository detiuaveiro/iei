#!/usr/bin/env bash

qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 4 \
-m 4G \
-display gtk \
-drive file=vm.qcow2 \
-boot d
