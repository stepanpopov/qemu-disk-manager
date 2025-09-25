from typing import Tuple
import uuid

from src.models import DiskInfo
from src.guest_agent import QemuGuestAgentClient
from src.utils.lsblk_output import parse_lsblk_out


class QemuMethods:
    def __init__(self, socket_path: str):
        self.qga = QemuGuestAgentClient(socket_path)

    def lsblk(self) -> list[DiskInfo]:
        _, response = self.qga.execute_command("lsblk")
        return parse_lsblk_out(response)

    def mount(self, device: str, mountpoint: str) -> str:
        command = f"mkdir -p {mountpoint}"
        st, outp = self.qga.execute_command("sh", ["-c", command])
        if st != 0:
            return outp

        command = f"mount {device} {mountpoint}"
        st, outp = self.qga.execute_command("sh", ["-c", command])
        if st != 0:
            return f"failed to mount device {device}: {outp}"

        return f"device {device} successfully mounted ({mountpoint})"

    def umount(self, device: str) -> str:
        command = f"umount {device}"
        st, out = self.qga.execute_command("sh", ["-c", command])
        if st != 0:
            return f"failed to umount device {device}: {out}"
        return f"device {device} successfully umounted"

    def mkfs_ext4(self, device: str) -> str:
        command = f"mkfs.ext4 -F {device}"
        st, outp = self.qga.execute_command("sh", ["-c", command])
        if st != 0:
            return f"failed to format: {outp}"
        return outp

    def ping(self) -> bool:
        return self.qga.guest_ping()


if __name__ == "__main__":
    try:
        qemu_methods = QemuMethods("/tmp/qga-83df907b.sock")

        print(qemu_methods.lsblk())

        print(qemu_methods.mkfs_ext4("/dev/vdb"))
        print(qemu_methods.mount("/dev/vdb", f"/mnt/{str(uuid.uuid4())}"))
        print(qemu_methods.umount("/dev/vdb"))

    except Exception as e:
        print("Error:", str(e))
