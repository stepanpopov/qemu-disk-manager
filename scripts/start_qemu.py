import os
import subprocess
import shutil
from typing import List, Optional


class QEMUVirtualMachine:
    def __init__(self, image_dir: str = "./images/"):
        self.image_dir = image_dir
        self.main_image = "boot/debian-13-nocloud-amd64.qcow2"
        self.backup_image = "boot/debian-13-nocloud-amd64.qcow2.backup"
        self.memory = "2G"

        self.qga_socket = "/tmp/qga.sock"
        print(f"QEMU QGA SOCKET = {self.qga_socket}")

        self.qmp_socket = "/tmp/qmp.sock"
        self.drives = []

        self.add_drive(self.main_image, "MAIN", bootindex=0)

    def add_drive(
        self, filename: str, serial: str, bootindex: Optional[int] = None
    ) -> None:
        image_path = os.path.join(self.image_dir, filename)
        if not os.path.exists(image_path):
            print(f"Warning: Drive image {image_path} does not exist")

        drive_config = {"filename": filename, "serial": serial, "bootindex": bootindex}
        self.drives.append(drive_config)
        print(f"Added drive: {filename} with serial {serial}")

    def reset_main_image(self) -> None:
        main_image_path = os.path.join(self.image_dir, self.main_image)
        backup_image_path = os.path.join(self.image_dir, self.backup_image)

        if os.path.exists(main_image_path):
            os.remove(main_image_path)
            print(f"Removed {main_image_path}")

        if os.path.exists(backup_image_path):
            shutil.copy2(backup_image_path, main_image_path)
            print(f"Restored {main_image_path} from backup")
        else:
            print(f"Warning: Backup file {backup_image_path} not found")

    def build_qemu_command(self) -> List[str]:
        cmd = [
            "qemu-system-x86_64",
            "-m",
            self.memory,
            "-device",
            "virtio-serial",
            "-chardev",
            f"socket,path={self.qga_socket},server=on,wait=off,id=qga0",
            "-device",
            "virtserialport,chardev=qga0,name=org.qemu.guest_agent.0",
            "-qmp",
            f"unix:{self.qmp_socket},server,nowait",
        ]

        for i, drive in enumerate(self.drives):
            drive_id = f"drive{i}"

            if drive.get("use_full_path", False):
                image_path = drive["filename"]
            else:
                image_path = os.path.join(self.image_dir, drive["filename"])

            cmd.extend(
                ["-drive", f"file={image_path},format=qcow2,if=none,id={drive_id}"]
            )

            device_args = f"virtio-blk-pci,drive={drive_id},serial={drive['serial']}"
            if drive["bootindex"] is not None:
                device_args += f",bootindex={drive['bootindex']}"

            cmd.extend(["-device", device_args])

        return cmd

    def run(self, reset_image: bool = True) -> None:
        if reset_image:
            self.reset_main_image()

        qemu_cmd = self.build_qemu_command()

        print("Starting QEMU with command:")
        print(" ".join(qemu_cmd))
        print()

        try:
            subprocess.run(qemu_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"QEMU failed with error: {e}")
        except FileNotFoundError:
            print(
                "Error: qemu-system-x86_64 not found. Please ensure QEMU is installed."
            )
        except KeyboardInterrupt:
            print("\nQEMU terminated by user")


# Example usage
if __name__ == "__main__":
    vm = QEMUVirtualMachine()

    vm.add_drive("disk2.qcow2", "DISK2")
    vm.add_drive("disk3.qcow2", "DISK3")
    vm.add_drive("disk4.qcow2", "DISK4")

    vm.run()
