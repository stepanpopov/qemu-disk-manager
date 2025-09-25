rm ./images/boot/debian-13-nocloud-amd64.qcow2
cp ./images/boot/debian-13-nocloud-amd64.qcow2.backup ./images/boot/debian-13-nocloud-amd64.qcow2

qemu-system-x86_64 \
  -drive file=./images/boot/debian-13-nocloud-amd64.qcow2,format=qcow2,if=none,id=main \
  -device virtio-blk-pci,drive=main,bootindex=0,serial=MAIN \
  -m 2G \
  -device virtio-serial \
  -chardev socket,path=/tmp/qga.sock,server=on,wait=off,id=qga0 \
  -device virtserialport,chardev=qga0,name=org.qemu.guest_agent.0 \
  -qmp unix:/tmp/qmp-sock,server,nowait \
  -drive file=./images/disk2.qcow2,format=qcow2,if=none,id=disk2 \
  -device virtio-blk-pci,drive=disk2,serial=DISK2
