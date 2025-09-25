import re

from typing import List
from src.models import DiskInfo


def parse_lsblk_out(disk_string: str) -> List[DiskInfo]:
    disk_info_list = []

    lines = disk_string.strip().split("\n")[1:]

    for line in lines:
        if not line.strip():
            continue

        parts = line.split()

        if len(parts) >= 6:
            name = parts[0]
            name = re.sub(r"[\u2500\u2502\u251c\u2514\-]", "", name)

            size = parts[3]

            mountpoint = " ".join(parts[6:]) if len(parts) > 6 else None

            if mountpoint == "":
                mountpoint = None

            disk_info_list.append(DiskInfo(name, mountpoint, size))

    return disk_info_list


if __name__ == "__main__":

    def print_lsblk_out_pretty(disk_string: str) -> str:
        print("=" * 50)
        disks = parse_lsblk_out(disk_string)
        for disk in disks:
            print(
                f"Name: {disk.device:8} | Size: {disk.size:6} | Mountpoint: {disk.mountpoint or 'None'}"
            )

    disk_string = """NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
    fd0       2:0    1    4K  0 disk 
    sr0      11:0    1 1024M  0 rom  
    vda     254:0    0    3G  0 disk 
    ├─vda1  254:1    0  2.9G  0 part /
    ├─vda14 254:14   0    3M  0 part 
    └─vda15 254:15   0  124M  0 part /boot/efi
    vdb     254:16   0   10G  0 disk 
    vdc     254:32   0   10G  0 disk 
    """

    print_lsblk_out_pretty(disk_string)
