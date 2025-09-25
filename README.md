# qemu-disk-manager

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

## wait for boot and enter creds (user = root, password = none)

## grant permissions to qga socket 
sudo chmod 777 /tmp/qga.sock

## start http server
PORT=8888 QEMU_SOCKET_PATH=/tmp/qga.sock make run-http

## open localhost:8888
