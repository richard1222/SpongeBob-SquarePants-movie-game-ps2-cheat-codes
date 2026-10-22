Stage 1: run APPLY-OVERLAY.cmd and select the original USA Movie PS2 ISO. It creates the owner-tested controller debug overlay probe as a separate ISO. Full input/output hashes and original-byte guards are enforced. No game image is included. Use only the exact SLUS_209.04 baseline.

V0.2 PATCHER UPDATE
This script uses .NET hashing and validates the manifest before copying.
It builds a uniquely named .partial file beside the requested output and
publishes the final filename only after the expected SHA-256 passes. Handled
failures remove the temporary file; force-killing PowerShell or loss of power
may leave a .partial file. It is not a completed ISO. Existing outputs are kept.
Optional command line: powershell.exe -NoProfile -File Apply-Overlay.ps1 -InputIso "input.iso" -OutputIso "new-output.iso"
