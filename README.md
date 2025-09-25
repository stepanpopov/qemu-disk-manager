# qemu-disk-manager

## download qemu boot image and mv it to ./images/boot
https://cloud.mail.ru/public/HR4N/RA6rs2Ume

## create venv
make make-venv

## activate venv
. venv/bin/activate

## install deps
make install

## install qemu (ubuntu)
sudo apt install qemu-system-x86

## start qemu:
sudo python3 ./scripts/start_qemu.py

## wait for boot and enter creds
enter creds (user = root, password = none)

## grant permissions to qga socket 
sudo chmod 777 /tmp/qga.sock

## start http server
PORT=8888 QEMU_SOCKET_PATH=/tmp/qga.sock make run-http

## open in browser
localhost:8888
