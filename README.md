# qemu-disk-manager

## Quick start

### download qemu boot image and mv it to ./images/boot
https://cloud.mail.ru/public/HR4N/RA6rs2Ume
### create venv
make make-venv
### activate venv
. venv/bin/activate
### install deps
make install
### install qemu (ubuntu)
sudo apt install qemu-system-x86
### start qemu:
sudo python3 ./scripts/start_qemu.py
### wait for boot and enter creds
enter creds (user = root, password = none)
### grant permissions to qga socket 
sudo chmod 777 /tmp/qga.sock
### start http server
PORT=8080 QEMU_SOCKET_PATH=/tmp/qga.sock make run-http
### open in browser
localhost:8080

## Screenshots
main page
<img width="3840" height="1172" alt="image" src="https://github.com/user-attachments/assets/b58472e0-b898-473d-820e-763943f8a04b" />
format vdb
<img width="3838" height="620" alt="image" src="https://github.com/user-attachments/assets/0ea77461-63b6-4e41-83c8-4d597654c081" />
mount vdb
<img width="3840" height="254" alt="image" src="https://github.com/user-attachments/assets/480b5306-297d-4b8c-ae9d-176fe97c3b19" />
check mountpoint inside vm
<img width="2070" height="276" alt="image" src="https://github.com/user-attachments/assets/be97d009-6a7e-47b2-a23b-4dc9a647463e" />
try to format vdb again
<img width="3840" height="296" alt="image" src="https://github.com/user-attachments/assets/35b7111d-9f48-434d-bfed-0440abc83b80" />
reload main page
<img width="3834" height="1188" alt="image" src="https://github.com/user-attachments/assets/3ba07d23-5151-43ea-bf2c-431c5bb781fa" />
umount vdb
<img width="3836" height="242" alt="image" src="https://github.com/user-attachments/assets/403fc41b-def8-476c-880e-84c7e13e3449" />
umount vdb again 
<img width="3836" height="242" alt="image" src="https://github.com/user-attachments/assets/81365371-18bf-444d-b993-85ee1be8d082" />








