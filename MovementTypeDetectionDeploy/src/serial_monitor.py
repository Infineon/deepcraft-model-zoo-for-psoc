"""
Serial monitor helpers for the PSOC Edge AI Kit (KitProg3 USB-UART bridge).

Provides:
- detect_serial_port(): auto-detect KitProg3 COM/tty port
- open_tera_term():     launch Tera Term (Windows)
- open_putty():         launch PuTTY (Windows)
- print_screen_cmd():   print the screen command (Linux/macOS)
- open_serial_terminal(): open a Python serial reader in a new terminal window
"""

import platform
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import serial.tools.list_ports

DEFAULT_BAUD_RATE = 115200


def check_board_connection() -> bool:
    """
    Check whether a KitProg3 USB-serial port is visible on this PC.
    Returns True if at least one KitProg3 port is found, False otherwise.
    """
    kitprog_ports = [
        p for p in serial.tools.list_ports.comports()
        if "KitProg3" in (p.description or "") or "KitProg3" in (p.manufacturer or "")
    ]
    if kitprog_ports:
        for p in kitprog_ports:
            print(f"Board connected: {p.device} — {p.description}")
        return True

    print("No KitProg3 port detected. Make sure the board is plugged in via the KitProg3 USB-C port.")
    print("\nAvailable ports:")
    all_ports = serial.tools.list_ports.comports()
    if all_ports:
        for p in all_ports:
            print(f"  {p.device}: {p.description}")
    else:
        print("  (none)")
    return False


def detect_serial_port(baud_rate: int = DEFAULT_BAUD_RATE) -> tuple[str, int]:
    """
    Auto-detect the KitProg3 serial port.
    Returns (port, baud_rate) and prints what was found.
    """
    kitprog_ports = [
        p for p in serial.tools.list_ports.comports()
        if "KitProg3" in (p.description or "") or "KitProg3" in (p.manufacturer or "")
    ]

    if kitprog_ports:
        port = kitprog_ports[0].device
        print(f"KitProg3 detected on {port} ({kitprog_ports[0].description})")
        if len(kitprog_ports) > 1:
            print(f"  Multiple KitProg3 ports found: {[p.device for p in kitprog_ports]}")
            print(f"  Using the first one. Override the returned port if needed.")
    else:
        port = "COM3" if platform.system() == "Windows" else "/dev/ttyACM0"
        print(f"KitProg3 not detected. Using fallback: {port}")
        print("Available ports:")
        for p in serial.tools.list_ports.comports():
            print(f"  {p.device}: {p.description}")

    return port, baud_rate


def open_tera_term(
    port: str,
    baud_rate: int = DEFAULT_BAUD_RATE,
    exe: str = r"C:\Program Files (x86)\teraterm\ttermpro.exe",
) -> None:
    """Launch Tera Term on the given serial port (Windows)."""
    if not Path(exe).is_file():
        print(f"Tera Term not found at {exe}. Update the exe path or use another option.")
        return
    # /C= expects just the port number (e.g. /C=3 for COM3)
    port_num = port.replace("COM", "")
    subprocess.Popen([exe, f"/C={port_num}", f"/BAUD={baud_rate}"])
    print(f"Opened Tera Term on {port} (port {port_num}) @ {baud_rate}")


def open_putty(
    port: str,
    baud_rate: int = DEFAULT_BAUD_RATE,
    exe: str = r"C:\Program Files\PuTTY\putty.exe",
) -> None:
    """Launch PuTTY on the given serial port (Windows)."""
    if not Path(exe).is_file():
        print(f"PuTTY not found at {exe}. Update the exe path or use another option.")
        return
    subprocess.Popen([exe, "-serial", port, "-sercfg", f"{baud_rate},8,n,1,N"])
    print(f"Opened PuTTY on {port} @ {baud_rate}")


def print_screen_cmd(port: str, baud_rate: int = DEFAULT_BAUD_RATE) -> None:
    """Print the screen command for Linux/macOS."""
    if platform.system() == "Windows":
        print("screen is a Linux/macOS tool. On Windows, use Tera Term or PuTTY.")
        return
    print(f"Run this command in a terminal:\n")
    print(f"  screen {port} {baud_rate}\n")
    print("To exit screen: press Ctrl-A, then K, then confirm with y")


def open_serial_terminal(port: str, baud_rate: int = DEFAULT_BAUD_RATE) -> None:
    """
    Open a Python serial reader in a new terminal window.
    Works on Windows (cmd), macOS (Terminal.app), and Linux (gnome-terminal, etc.).
    """
    script = textwrap.dedent(f"""\
        import serial
        print("Serial Monitor — press Ctrl-C to stop\\n")
        try:
            with serial.Serial("{port}", {baud_rate}, timeout=1) as ser:
                print(f"Listening on {port} @ {baud_rate}\\n")
                while True:
                    line = ser.readline().decode("utf-8", errors="replace").strip()
                    if line:
                        print(line)
        except KeyboardInterrupt:
            print("\\nStopped by user.")
        except serial.SerialException as e:
            print(f"Serial error: {{e}}")
        input("\\nPress Enter to close this window...")
    """)

    tmp = Path(tempfile.gettempdir()) / "_serial_reader.py"
    tmp.write_text(script, encoding="utf-8")
    py = sys.executable

    os_name = platform.system()
    if os_name == "Windows":
        subprocess.Popen(["cmd", "/c", "start", "Serial Monitor", py, str(tmp)])
    elif os_name == "Darwin":
        subprocess.Popen([
            "osascript", "-e",
            f'tell application "Terminal" to do script "{py} {tmp}"',
        ])
    else:
        for term_cmd in [
            ["gnome-terminal", "--", py, str(tmp)],
            ["konsole", "-e", py, str(tmp)],
            ["xfce4-terminal", "-e", f"{py} {tmp}"],
            ["xterm", "-e", py, str(tmp)],
        ]:
            if shutil.which(term_cmd[0]):
                subprocess.Popen(term_cmd)
                break
        else:
            print(f"No GUI terminal found. Run manually in a shell:\n  {py} {tmp}")
            return

    print(f"Launched serial reader in a new terminal window ({port} @ {baud_rate})")
