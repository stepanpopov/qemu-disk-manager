import json
import socket
import struct
import time
import base64
from typing import Dict, Any, Tuple, Optional

_RECV_SOCKET_BYTES = 1024


class QemuGuestAgentClient:
    def __init__(self, socket_path: str, timeout: int = 30):
        self.socket_path = socket_path
        self.timeout = timeout
        self.socket = None

    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect(self.socket_path)
            return True
        except (socket.error, FileNotFoundError) as e:
            print(f"Failed to connect to QGA socket: {e}")
            return False

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def _send_command(
        self, command: str, arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.socket:
            if not self.connect():
                return {"error": "Failed to connect to QGA socket"}

        try:
            message = {"execute": command}
            if arguments:
                message["arguments"] = arguments

            json_data = json.dumps(message)

            self.socket.sendall(json_data.encode())

            response_data = self._recv_until_new_line()

            return json.loads(response_data)

        except (socket.timeout, socket.error, json.JSONDecodeError, struct.error) as e:
            return {"error": f"Communication error: {e}"}

    def _recv_until_new_line(self):
        data = b""
        delimiter = b"\n"
        while True:
            chunk = self.socket.recv(_RECV_SOCKET_BYTES)
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk
            if delimiter in data:
                break

        return data

    def execute_command(
        self,
        command: str,
        args: Optional[list] = None,
        input_data: Optional[str] = None,
        capture_output: bool = True,
    ) -> Tuple[int, str]:
        arguments = {"path": command, "capture-output": capture_output}

        if args:
            arguments["arg"] = args

        if input_data:
            arguments["input-data"] = base64.b64encode(
                input_data.encode("utf-8")
            ).decode("utf-8")

        response = self._send_command("guest-exec", arguments)

        if "error" in response:
            return -1, f"QGA error: {response['error']}"

        if "return" not in response:
            return -1, "Invalid response format from QGA"

        pid = response["return"].get("pid")
        if pid is None:
            return -1, "No PID returned from guest-exec"

        return self._wait_for_completion(pid)

    def _wait_for_completion(
        self, pid: int, check_interval: float = 0.5
    ) -> Tuple[int, str]:
        max_wait_time = 300
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            response = self._send_command("guest-exec-status", {"pid": pid})

            if "error" in response:
                return -1, f"Error checking status: {response['error']}"

            if "return" not in response:
                return -1, "Invalid status response format"

            status = response["return"]

            if status.get("exited", False):
                exit_code = status.get("exitcode", -1)

                output_data = ""
                if "out-data" in status:
                    output_data = status["out-data"]
                elif "err-data" in status:
                    output_data = status["err-data"]

                if output_data:
                    try:
                        output_data = base64.b64decode(output_data).decode(
                            "utf-8", errors="ignore"
                        )
                    except Exception as e:
                        output_data = f"Error decoding output: {e}"

                return exit_code, output_data

            elif "error" in status:
                error_desc = status.get("error-desc", "Unknown error")
                return -1, f"Command failed to start: {error_desc}"

            time.sleep(check_interval)

        return -1, "Command execution timeout"

    def guest_ping(self) -> bool:
        response = self._send_command("guest-ping")
        return "error" not in response and "return" in response

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


if __name__ == "__main__":
    try:
        with QemuGuestAgentClient("/tmp/qga-83df907b.sock") as qga:
            assert qga.guest_ping()

            success, info = qga.guest_info()
            assert success
            print("Guest info:", info)

            exit_code, output = qga.execute_command("echo", ["hello world"])
            assert exit_code == 0
            print(f"Output: {output}")

            exit_code, output = qga.execute_command("ls", ["-la", "/tmp"])
            assert exit_code == 0
            print(f"Output: {output}")

    except Exception as e:
        print(f"Unexpected error: {e}")
