SELECT-TOGGLE TEST â€” SPONGEBOB MOVIE USA / CFW PS3

1. Extract this small ZIP into a folder.
2. Double-click APPLY-SELECT-TOGGLE.cmd on Windows.
3. Choose the extracted Pad-Debug-PROBE.iso that already showed the controller overlay on your PS3. Do not choose the .7z file or the original retail ISO.
4. The patcher checks the full source SHA-256, then creates SpongeBob-Movie-USA-Select-Toggle-TEST.iso next to it. The source is untouched and existing outputs are refused.
5. Transfer/mount the new ISO through your usual CFW PS2 ISO setup.
6. Tap SELECT, release it, then tap it again. Check whether the controller overlay hides and returns. Try at the title screen and in gameplay. SELECT may also activate its normal in-game function.

Report: Does the game boot? Does each SELECT tap toggle the overlay once? Any flicker, crash or repeated toggle? This candidate has not been run on hardware. The original always-on overlay is the only hardware-confirmed feature so far.

This is a CUSTOM OVERLAY TOGGLE, not the original developer menu. It is the next input-integration experiment toward an interactive debug interface.

No game data is bundled. Windows PowerShell is sufficient; no Python, admin privileges, network access, or additional installation is required. The patcher reads your selected ISO and writes a separate copy beside it. Allow about 1.25 GB free space there.

Expected output SHA-256: 78b5b1530a179ad25a2e06167b24aacc369977d57fcdc9b0433d0f7b120303f7.

Static verification: 20 exact-instruction cases passed; actual patcher generated a full ISO; full-image comparison found 49 changed bytes, all in the 64-byte debug-update window. Wrong input and output overwrite were rejected. These checks do not establish runtime integration or controller edge timing across game modes.
