import os
from fastapi.responses import HTMLResponse

from src.http_api.main_page import MainPageRenderer
from src.models import DiskInfo
from src.qemu_methods import QemuMethods
from src.utils.utils import make_dev


class Handlers:
    # TODO: return error pages.
    def __init__(self, mount_url: str, unmount_url: str, format_url: str):
        self.socket = os.getenv("QEMU_SOCKET_PATH") or "/tmp/qga.sock"
        self.qemu_methods = QemuMethods(self.socket)

        self.main_page_renderer = MainPageRenderer(
            self.socket, mount_url, unmount_url, format_url
        )

    def main_page(self) -> HTMLResponse:
        disks: list[DiskInfo] = self.qemu_methods.lsblk()
        return HTMLResponse(self.main_page_renderer.render(disks))

    def mount_disk(self, device: str) -> HTMLResponse:
        output = self.qemu_methods.mount(make_dev(device), f"/mnt/{device}")

        return HTMLResponse(self._render_disk_method_resp(output))

    def unmount_disk(self, device: str):
        output = self.qemu_methods.umount(make_dev(device))

        return HTMLResponse(self._render_disk_method_resp(output))

    def format_disk_ext4(self, device):
        output = self.qemu_methods.mkfs_ext4(make_dev(device))

        return HTMLResponse(self._render_disk_method_resp(output))

    # helpers

    def _render_disk_method_resp(self, output: str):
        html_content = f"""
        <html>
        <head>
            <style>
                .terminal {{
                    font-family: 'Courier New', monospace;
                    background: black;
                    color: #00ff00;
                    padding: 20px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            <div class="terminal">{self._render_terminal_output(output)}</div>
        </body>
        </html>
        """
        return html_content
        # return HTMLResponse(content=html_content)

    def _render_terminal_output(self, text: str):
        lines = text.split("\n")
        processed_lines = []

        for line in lines:
            result = []
            for char in line:
                if char == "\b":
                    if result:
                        result.pop()
                else:
                    result.append(char)
            processed_lines.append("".join(result))

        return "<br>".join(processed_lines)


# @app.get("/", response_class=HTMLResponse)
# def get_disks(_request: Request) -> str:
#     html_content = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Disk Management for QEMU instance</title>
#         <style>
#             table {{
#                 width: 100%;
#                 border-collapse: collapse;
#             }}
#             th, td {{
#                 border: 1px solid black;
#                 padding: 8px;
#                 text-align: left;
#             }}
#             th {{
#                 background-color: #f2f2f2;
#             }}
#             button {{
#                 margin: 0 5px;
#                 padding: 5px 10px;
#                 cursor: pointer;
#             }}
#         </style>
#     </head>
#     <body>
#         <h1>Disk Management for QEMU instance (socket = {socket})</h1>
#         <table>
#             <thead>
#                 <tr>
#                     <th>Disk Device</th>
#                     <th>Size</th>
#                     <th>Mount Point</th>
#                     <th>Actions</th>
#                 </tr>
#             </thead>
#             <tbody>
#     """

#     disks: DiskInfo = qemu_methods.lsblk()

#     # Generate rows for each disk
#     for disk in disks:
#         html_content += f"""
#         <tr>
#             <td>{disk.device}</td>
#             <td>{disk.size}</td>
#             <td>{disk.mountpoint or "Not Mounted"}</td>
#             <td>
#                 <form action="/disks/mount" method="post" style="display:inline;">
#                     <input type="hidden" name="device" value="{disk.device}">
#                     <button type="submit">Mount</button>
#                 </form>
#                 <form action="/disks/unmount" method="post" style="display:inline;">
#                     <input type="hidden" name="device" value="{disk.device}">
#                     <button type="submit">Unmount</button>
#                 </form>
#                 <form action="/disks/format" method="post" style="display:inline;">
#                     <input type="hidden" name="device" value="{disk.device}">
#                     <button type="submit">Format</button>
#                 </form>
#             </td>
#         </tr>
#         """

#     html_content += """
#             </tbody>
#         </table>
#     </body>
#     </html>
#     """
#     return html_content


# @app.post("/disks/mount")
# def mount_disk(device: str = Form(...)):
#     return resp(qemu_methods.mount(make_dev(device), f"/mnt/{str(uuid.uuid4())}"))


# @app.post("/disks/unmount")
# def unmount_disk(device: str = Form(...)):
#     return resp(qemu_methods.umount(make_dev(device)))


# @app.post("/disks/format")
# def format_disk(device: str = Form(...)):
#     return resp(qemu_methods.mkfs_ext4(make_dev(device)))
