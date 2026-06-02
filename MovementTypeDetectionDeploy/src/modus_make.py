"""
Helpers to run ModusToolbox make (clean, build, program),
ModusToolbox Programmer, and standalone OpenOCD hex flashing from Python.

Uses Cygwin.bat so PATH/CYSDK are set; runs make via bash -c to avoid
"cannot set terminal process group" / "no job control" messages.
"""

import platform
import subprocess
import sys
import tempfile
from pathlib import Path


def _win_to_cygwin(p: Path) -> str:
    """Convert Windows path to Cygwin path for bash."""
    s = str(p.resolve()).replace("\\", "/")
    if len(s) >= 2 and s[1] == ":":
        return "/cygdrive/" + s[0].lower() + s[2:]
    return s


def run_make(
    target: str,
    modus_shell_path: Path,
    mtb_project_path: Path,
    target_args: str = "",
) -> int:
    """
    Run one make target (e.g. 'clean', 'build', 'program') in the ModusToolbox environment.

    Args:
        target: Make target name (clean, build, program).
        modus_shell_path: Path to Cygwin.bat or modus-shell executable.
        mtb_project_path: ModusToolbox project root (where the Makefile is).
        target_args: Optional extra args (e.g. 'TARGET=BOARD').

    Returns:
        Process return code (0 on success).
    """
    p = Path(modus_shell_path)
    if not p.exists():
        print("Set MODUS_SHELL_PATH to your ModusToolbox Cygwin.bat (e.g. ...\\modus-shell\\Cygwin.bat).")
        return 1
    cygwin_path = _win_to_cygwin(Path(mtb_project_path))
    make_cmd = f'cd "{cygwin_path}" && make {target} {target_args}'.strip()
    # Batch sets PATH/CYSDK then starts bash. Pipe one line: bash -c '...' so the inner bash
    # runs non-interactively (no "cannot set terminal process group" / "no job control").
    if p.suffix.lower() == ".bat":
        piped = ("bash -c " + repr(make_cmd) + "\nexit\n").encode("utf-8")
        proc = subprocess.Popen(
            ["cmd", "/c", str(p)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(mtb_project_path),
        )
        out, err = proc.communicate(input=piped, timeout=600)
    else:
        proc = subprocess.Popen(
            [str(p), "-c", make_cmd],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(mtb_project_path),
        )
        out, err = proc.communicate(timeout=600)
    for line in (out or b"").decode("utf-8", errors="replace").splitlines():
        print(line)
    for line in (err or b"").decode("utf-8", errors="replace").splitlines():
        print(line, file=sys.stderr)
    if proc.returncode != 0:
        print(f"make {target} exited with code {proc.returncode}")
    return proc.returncode


def open_programmer(hex_path: Path) -> None:
    """
    Open ModusToolbox™ Programmer with the given .hex file.
    The user can then connect to the board and flash from the GUI.

    Auto-detects the mtb-programmer executable from:
    - C:\\Infineon\\Tools\\ModusToolboxProgtools-*  (Windows)
    - ~/ModusToolbox/tools_*/mtb-programmer         (cross-platform)
    """
    hex_path = Path(hex_path).resolve()
    if not hex_path.is_file():
        print(f"Hex file not found: {hex_path}")
        return

    exe_name = "mtb-programmer.exe" if platform.system() == "Windows" else "mtb-programmer"
    candidates: list[Path] = []

    if platform.system() == "Windows":
        infineon_tools = Path("C:/Infineon/Tools")
        if infineon_tools.is_dir():
            candidates.extend(
                sorted(infineon_tools.glob(f"ModusToolboxProgtools-*/mtb-programmer/{exe_name}"), reverse=True)
            )

    mtb_base = Path.home() / "ModusToolbox"
    if mtb_base.is_dir():
        candidates.extend(
            sorted(mtb_base.glob(f"tools_*/mtb-programmer/{exe_name}"), reverse=True)
        )

    programmer = next((p for p in candidates if p.is_file()), None)
    if programmer is None:
        print(
            "ModusToolbox™ Programmer not found.\n"
            "Install ModusToolbox™ Programming Tools (see README — Requirements and Tools)."
        )
        return

    subprocess.Popen([str(programmer)])
    print(f"Opened ModusToolbox™ Programmer")
    print(f"  Programmer: {programmer}")
    print(f"\nHex file to program:\n  {hex_path}")


def _find_openocd() -> tuple[Path, Path] | None:
    """
    Locate the OpenOCD executable and scripts directory.
    Searches ModusToolbox Programming Tools (C:\\Infineon\\Tools) and
    ModusToolbox tools_* directories (~/ModusToolbox).
    Returns (openocd_exe, scripts_dir) or None.
    """
    candidates: list[Path] = []

    if platform.system() == "Windows":
        infineon_tools = Path("C:/Infineon/Tools")
        if infineon_tools.is_dir():
            candidates.extend(sorted(infineon_tools.glob("ModusToolboxProgtools-*/openocd"), reverse=True))

    mtb_base = Path.home() / "ModusToolbox"
    if mtb_base.is_dir():
        candidates.extend(sorted(mtb_base.glob("tools_*/openocd"), reverse=True))

    exe_name = "openocd.exe" if platform.system() == "Windows" else "openocd"
    for ocd_dir in candidates:
        exe = ocd_dir / "bin" / exe_name
        scripts = ocd_dir / "scripts"
        if exe.is_file() and scripts.is_dir():
            return exe, scripts
    return None


def _find_qspi_config(mtb_project_path: Path | None) -> Path | None:
    """
    Locate the qspi_config.cfg needed by OpenOCD to define SMIF flash banks.

    The combined hex for PSOC Edge contains data in external QSPI/SMIF flash
    (CM33 code at 0x60xxxxxx, CM55 at 0x70xxxxxx).  Without this config,
    OpenOCD only knows about the internal RRAM and silently skips those regions.

    Search order:
      1. <mtb_project_path>/bsps/**/qspi_config.cfg  (BSP-generated)
      2. Create a default config for KIT_PSE84_AI in a temp directory
    """
    if mtb_project_path is not None:
        mtb_project_path = Path(mtb_project_path)
        matches = list(mtb_project_path.glob("bsps/**/qspi_config.cfg"))
        if matches:
            return matches[0]

    # Default SMIF bank layout for KIT_PSE84_AI (matches QSPI Configurator output)
    tmp_dir = Path(tempfile.gettempdir()) / "_openocd_qspi"
    tmp_dir.mkdir(exist_ok=True)
    cfg = tmp_dir / "qspi_config.cfg"
    cfg.write_text(
        "set SMIF_BANKS {\n"
        "  1 {addr 0x60000000 size 0x4000000 psize 0x100 esize 0x40000}\n"
        "}\n",
        encoding="utf-8",
    )
    return cfg


def flash_hex(
    hex_path: Path,
    mtb_project_path: Path | None = None,
    target_cfg: str = "target/infineon/pse84xgxs2.cfg",
    interface_cfg: str = "interface/kitprog3.cfg",
) -> int:
    """
    Flash a .hex file onto the board using OpenOCD (from ModusToolbox Programming Tools).

    KIT_PSE84_AI uses the PSE84xGxS2 device variant, so the default target
    config is pse84xgxs2.cfg.  ENABLE_ACQUIRE is set to allow test mode
    acquisition required for programming PSOC Edge devices.

    The combined hex contains data for both internal RRAM and external SMIF
    flash.  A qspi_config.cfg is required so OpenOCD defines the SMIF flash
    banks; without it, regions at 0x60xxxxxx / 0x70xxxxxx are silently skipped.

    NOTE: The 'verify' step is intentionally omitted because OpenOCD reports
    a spurious checksum mismatch on PSOC Edge even when programming succeeds.
    OpenOCD may report success while the firmware does not run — if the board
    does not respond after flashing, use Option A (make program) or Option B
    (ModusToolbox Programmer) instead.

    Args:
        hex_path: Path to the .hex file to flash.
        mtb_project_path: Optional path to the MTB project (used to locate
            qspi_config.cfg in the BSP).  If None, a default config for
            KIT_PSE84_AI is generated automatically.
        target_cfg: OpenOCD target config (default: PSE84xGxS2 for KIT_PSE84_AI).
        interface_cfg: OpenOCD interface config (default: KitProg3).

    Returns:
        Process return code (0 on success).
    """
    hex_path = Path(hex_path).resolve()
    if not hex_path.is_file():
        print(f"Hex file not found: {hex_path}")
        return 1

    result = _find_openocd()
    if result is None:
        print(
            "OpenOCD not found. Install ModusToolbox™ Programming Tools\n"
            "(see README — Requirements and Tools)."
        )
        return 1

    openocd_exe, scripts_dir = result
    hex_str = str(hex_path).replace("\\", "/")

    # Locate qspi_config.cfg so OpenOCD can define external SMIF flash banks
    qspi_cfg = _find_qspi_config(mtb_project_path)
    qspi_search_dir = str(qspi_cfg.parent) if qspi_cfg else None

    cmd = [
        str(openocd_exe),
        "-s", str(scripts_dir),
    ]
    if qspi_search_dir:
        cmd += ["-s", qspi_search_dir]
    cmd += [
        "-f", interface_cfg,
        "-c", "set ENABLE_ACQUIRE 1",
        "-f", target_cfg,
        "-c", f"init; reset init; program {hex_str}; reset; shutdown",
    ]

    print(f"Flashing {hex_path.name} via OpenOCD...")
    print(f"  OpenOCD:     {openocd_exe}")
    print(f"  Target:      {target_cfg}")
    if qspi_cfg:
        print(f"  QSPI config: {qspi_cfg}")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate(timeout=120)
    out_text = (out or b"").decode("utf-8", errors="replace")
    err_text = (err or b"").decode("utf-8", errors="replace")
    for line in out_text.splitlines():
        print(line)
    for line in err_text.splitlines():
        print(line, file=sys.stderr)

    combined = out_text + err_text
    if "unable to find a matching CMSIS-DAP device" in combined:
        print(
            "\n--- Troubleshooting ---\n"
            "OpenOCD cannot find the KitProg3 debug probe (CMSIS-DAP).\n"
            "Possible causes:\n"
            "  1. The board is not connected — plug it in via the KitProg3 USB-C port\n"
            "  2. Another tool is using the debug interface — close ModusToolbox\n"
            "     Programmer, VS Code debugger, or any other OpenOCD instance\n"
            "  3. KitProg3 is in Bulk mode — press the Mode button on the board\n"
            "     to switch to CMSIS-DAP mode (LED pattern changes)\n"
            "  4. Try Option A (make program) or Option B (ModusToolbox Programmer)\n"
        )
    elif "no flash bank found for address" in combined:
        print(
            "\n--- Troubleshooting ---\n"
            "OpenOCD could not find flash banks for some hex regions.\n"
            "The QSPI/SMIF config may be missing or incorrect.\n"
            "  - If you have the MTB project, pass mtb_project_path to flash_hex()\n"
            "  - Try Option A (make program) or Option B (ModusToolbox Programmer)\n"
        )
    elif proc.returncode == 0:
        print("Flash completed successfully.")
    else:
        print(f"OpenOCD exited with code {proc.returncode}")
    return proc.returncode
