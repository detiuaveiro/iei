#!/usr/bin/env bash

if [ "$1" = "arm" ]; then
echo -e "Start ARM flavor..."

qemu-system-aarch64 \
-m 4G \
-machine type=virt \
-cpu max \
-smp 4 \
-initrd "./initrd.gz" \
-kernel "./vmlinuz" \
-append "console=ttyAMA0" \
-drive file=./debian-13.1.0-arm64-netinst.iso,id=cdrom,if=none,media=cdrom \
  -device virtio-scsi-device \
  -device scsi-cd,drive=cdrom \
-drive file="./vm_arm.qcow2",id=hd,if=none,media=disk \
  -device virtio-scsi-device \
  -device scsi-hd,drive=hd \
-netdev user,id=net0,hostfwd=tcp::5555-:22 \
  -device virtio-net-device,netdev=net0 \
-nographic

else

echo -e "Start AMD64 flavor..."
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 4 \
-m 4G \
-display gtk \
-vga virtio \
-drive file=vm.qcow2 \
-boot c

fi

echo -e "Done."
