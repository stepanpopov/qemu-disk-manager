from src.models import DiskInfo


class MainPageRenderer:
    HEAD = """
    <head>
        <title>Disk Management for QEMU instance</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            button {
                margin: 0 5px;
                padding: 5px 10px;
                cursor: pointer;
            }
        </style>
    </head>
    """

    def __init__(self, socket: str, mount_url: str, unmount_url: str, format_url: str):
        self.socket = socket
        self.mount_url = mount_url
        self.unmount_url = unmount_url
        self.format_url = format_url

    def render(self, disks: list[DiskInfo]) -> str:
        disks_html_table = ""
        for disk in disks:
            disks_html_table += self._html_disk_row(
                disk,
            )

        return f"""
        <!DOCTYPE html>
        <html>
            {MainPageRenderer.HEAD}
            <body>
                <h1>Disk Management for QEMU instance (socket = {self.socket})</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Disk Device</th>
                            <th>Size</th>
                            <th>Mount Point</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    {disks_html_table}
                    </tbody>
                </table>
            </body>
        </html>
        """

    def _html_disk_row(self, disk: DiskInfo) -> str:
        return f"""
        <tr>
            <td>{disk.device}</td>
            <td>{disk.size}</td>
            <td>{disk.mountpoint or "Not Mounted"}</td>
            <td>
                <form action="{self.mount_url}" method="post" style="display:inline;">
                    <input type="hidden" name="device" value="{disk.device}">
                    <button type="submit">Mount</button>
                </form>
                <form action="{self.unmount_url}" method="post" style="display:inline;">
                    <input type="hidden" name="device" value="{disk.device}">
                    <button type="submit">Unmount</button>
                </form>
                <form action="{self.format_url}" method="post" style="display:inline;">
                    <input type="hidden" name="device" value="{disk.device}">
                    <button type="submit">Format</button>
                </form>
            </td>
        </tr>
        """
