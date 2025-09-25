VENV_DIR = venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt

HOST ?= 127.0.0.1
PORT ?= 8080

NEW_QEMU_DISKPATH ?= ./images/disk5.qcow2
NEW_QEMU_DISK_SIZE ?= 10G

make-venv:
	$(PYTHON) -m venv $(VENV_DIR)

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)

install-dev:
	$(PIP) install --upgrade pip
	$(PIP) install -r $(DEV_REQUIREMENTS)

run-http:
	$(VENV_DIR)/bin/uvicorn src.http_api.routes:app --host $(HOST) --port $(PORT)

lint:
	$(VENV_DIR)/bin/ruff check .

fix:
	$(VENV_DIR)/bin/ruff check . --fix

# create disk
create-disk:
	qemu-img create -f qcow2 $(NEW_QEMU_DISKPATH) $(NEW_QEMU_DISK_SIZE)