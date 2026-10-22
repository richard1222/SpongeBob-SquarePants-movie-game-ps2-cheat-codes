# SpongeBob Movie Debug Tools v0.1

Complete tool bundle for the USA PS2 Movie build, `SLUS_209.04`, tested by the owner through PS2 emulation on a CFW PS3.

## Included

- **Overlay tool:** original matching ISO → controller/status debug overlay.
- **Select-toggle tool:** overlay probe → Select hide/show control.
- **Custom panel tool:** Select-toggle ISO → selectable test row with X activation.
- **Music panel tool:** working panel ISO → music PLAYING/PAUSED row using the game's existing pause/resume functions.
- Instruction-level panel/music test runners, verification receipts, Dolphin container smoke utility, configuration inventory, and project research documents.

Run each stage's `APPLY-*.cmd` on Windows and choose the exact input ISO described in that folder. Each stage creates a separate output; originals are preserved. Input hashes/byte guards prevent use with another edition. No Python or administrator rights are needed for the Windows patchers.

## Verification status

**Owner hardware-confirmed:** overlay, Select toggle, and the basic custom panel interaction.

**Music control is experimental:** 768 instruction-level cases and an eight-step sequence passed, including retail pause/resume instructions with zero/one/two active music tracks. The external sound backend was modeled, not executed; a console audio result is still pending. Music uses the engine's pause state and can be affected by ordinary game pause/unpause and transitions. It does not change saved volume or the INI NoMusic flag.

Panel tests: 192 instruction-level cases and a nine-step sequence passed. Full-image comparisons verified bounded edits; the music candidate differs from the working panel by 170 bytes within three intended windows.

## Limits

This is a **custom debug interface**, not a recovered original developer menu. Basic owner reports do not establish extended stability or all game modes. Normal controls can still react while the panel is visible.

No ISOs, extracted executables, game assets, account data, credentials, or third-party converter binaries are bundled. Users supply their own exact matching game image. Developer tests require Python; the music test additionally requires the user's privately extracted matching executable.

The ZIP includes a SHA-256 manifest. The separate SHA256SUMS file identifies the release archive.
