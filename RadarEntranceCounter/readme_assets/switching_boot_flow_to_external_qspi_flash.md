# Switching the Boot Flow to External QSPI Flash

The PSoC™ 6 AI Evaluation Kit (CY8CKIT-062S2-AI) primarily boots from internal flash (default, up to 2 MB capacity) for most applications, including the Entrance Counter demo. However, it supports booting from external Quad Serial Peripheral Interface (QSPI) flash (512 Mb S25FL512S) for larger firmware sizes via execute-in-place (XIP) mode.

This code example uses internal flash booting by default, as do most other examples like the [Hello world](https://github.com/Infineon/mtb-example-psoc6-hello-world). Switching to external QSPI is for apps exceeding internal flash limits (e.g., complex ML models). For details, see the "QSPI XIP" section in the [AN228571 – Getting started with PSoC™ 6 MCU on ModusToolbox™ software](https://www.infineon.com/AN228571) (v08_00 or later).

## Standard Deployment: Flashing .hex to Internal Flash
For the Entrance Counter application:
1. Compile the project in ModusToolbox™ to generate `Entrance_counter.hex`.
2. Connect the kit via USB Type-C (J2 port).
3. Use **ModusToolbox™ Programmer**:
   - Launch Programmer > Select Device (auto-detects CY8C62x6).
   - Load .hex file
   - Click **Program**—the app boots automatically post-flash.
4. Monitor outputs via UART (virtual COM port, 115200 baud) using a terminal like Tera Term.

This method is recommended for quick deployment; no boot flow changes needed.

## Boot from External QSPI Flash (Advanced)
If your firmware exceeds internal flash:
- **Prerequisite**: Install ModusToolbox™ software (v3.6 or later) and ensure the Board Support Package (BSP) for CY8CKIT-062S2-AI is the latest version (check via Library Manager). Refer to the [mtb-example-psoc6-qspi-xip GitHub repository](https://github.com/Infineon/mtb-example-psoc6-qspi-xip) for setup.
- Configure QSPI XIP:
  1. Open QSPI Configurator in ModusToolbox™ (under Tools).
  2. Enable XIP mode, set clock (up to 133 MHz), and map external flash addresses.
  3. Update `Makefile` (add `CY_BOOT_USE_EXTERNAL_FLASH=1`) and linker script (e.g., `cy8c62x6_cm4_dual.ld` for external sections).
- Build and flash the updated .hex via Programmer (selects external flash automatically in XIP mode).

For full QSPI details, see the "QSPI Configurator" section in [AN228571](https://www.infineon.com/AN228571) and the [mtb-example-psoc6-qspi-xip README](https://github.com/Infineon/mtb-example-psoc6-qspi-xip).

> **Note:** To revert to internal flash (e.g., for other examples like [Hello world](https://github.com/Infineon/mtb-example-psoc6-hello-world)), disable XIP in the Makefile (`CY_BOOT_USE_EXTERNAL_FLASH=0`) and rebuild/flash. Always verify flash integrity post-programming. For Entrance Counter, internal flash suffices (~200-500 KB typical).
