from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

from src.http_api.handlers import Handlers

app = FastAPI()


class URLS:
    MOUNT_URL = "/disks/mount"
    UMOUNT_URL = "/disks/unmount"
    FORMAT_URL = "/disks/format"


handlers = Handlers(
    mount_url=URLS.MOUNT_URL, unmount_url=URLS.UMOUNT_URL, format_url=URLS.FORMAT_URL
)


@app.get("/", response_class=HTMLResponse)
def get_disks(_request: Request) -> str:
    return handlers.main_page()


@app.post(URLS.MOUNT_URL, response_class=HTMLResponse)
def mount_disk(device: str = Form(...)):
    return handlers.mount_disk(device)


@app.post(URLS.UMOUNT_URL, response_class=HTMLResponse)
def unmount_disk(device: str = Form(...)):
    return handlers.unmount_disk(device)


@app.post("/disks/format", response_class=HTMLResponse)
def format_disk(device: str = Form(...)):
    return handlers.format_disk_ext4(device)
