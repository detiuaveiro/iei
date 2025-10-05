#!/usr/bin/env bash

if [ "$1" = "arm" ]; then
echo -e "Start ARM flavor..."

qemu-system-aarch64 \
  -m 4G \
  -machine virt,gic-version=max,iommu=smmuv3 \
  -accel tcg \
  -cpu max \
  -smp 4 \
  -rtc base=utc \
  -initrd "./boot_arm/initrd-from-guest.gz" \
  -kernel "./boot_arm/vmlinuz-from-guest" \
  -drive file="./vm_arm.qcow2",id=hd,if=none,media=disk \
  -device virtio-scsi-device \
  -device scsi-hd,drive=hd \
  -device virtio-gpu-pci \
  -display sdl \
  -usb \
  -device qemu-xhci,id=xhci \
  -device usb-tablet \
  -device usb-kbd \
  
else

echo -e "Start AMD64 flavor..."
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 4 \
-m 4G \
-display sdl \
-vga virtio \
-drive file=vm.qcow2 \
-boot c

fi

echo -e "Done."
