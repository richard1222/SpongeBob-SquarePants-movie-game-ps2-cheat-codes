# SpongeBob Movie Debug Tools v0.4

v0.4 combines the four-row HealthMenu with the original six-slot health cheat's refill. The owner reports **“everything worked in order no issues”** for the combined image on the established CFW PS3 Slim CECH-2001A / ps2_netemu setup. The earlier HP3 message was starting health, not a refill failure. Exact post-cheat HP was not separately recorded. [Console receipt](../../docs/HEALTH-MENU-REFILL-CONSOLE-2026-10-22.md).

## Complete tools package

- All **eight cumulative patch stages**, from the matching retail USA SLUS_209.04 ISO through overlay, Select toggle, panel, music, diagnostics, Damage, HP display, and combined refill.
- Separate clean-retail cheat-sequence and health-refill probes; these are alternatives for research, not required steps in the cumulative chain.
- All project test scripts, manifests, archive/Xbox comparison helpers and research notes. External tools are credited and linked, not bundled.
- Windows CMD launchers and PowerShell patchers. Python 3.11+ is only required for developer tests.
- Source-commit identity, per-file SHA-256 manifest, release archive checksum and package verification receipt.

Extract the entire ZIP. If you already have the stable HealthMenu ISO, run **tools/health-menu-refill/APPLY-HEALTH-MENU-REFILL.cmd** and select that image. Starting with retail requires all eight stages in order; see [tools/README.md](../../tools/README.md) and [STAGES.json](../../tools/STAGES.json). Every stage requires the exact preceding hash and writes a separate output.

## Controls and refill

Select shows/hides the custom menu; Up/Down selects rows and X changes the selected value. Rows control music pause/resume, XYZ display, scene/controller display, and Damage 0/1 with current HP. Hiding the menu does not restore Damage: choose Damage 1 to resume normal damage.

For refill, enter a level, press START to pause, hold **L1 + L2 + R1 + R2**, and press **Circle four times, Square, Circle, Square, Circle**. Release the shoulders and resume. The original cheat grants six slots; the added action copies the player's current maximum into current HP. There is no new refill menu row. The separate Caveman input-sequence experiment is not incorporated into this cumulative build.

## Fixes and verification

- Whitespace-normalized error matching fixes false test failures when PowerShell wraps an error across lines.
- The shared fixture harness accepts a selected patcher/manifest while keeping stable defaults.
- Combined tests now write a run receipt only with explicit `--receipt`, using a new-file guard. Running them no longer overwrites the shipped owner-validation receipt.
- ISO identity: **8b9d5d006d6b3db0417e44736e1b4eacc68a53aa6fcdbef534157313a61e1883**, 1,249,804,288 bytes. The same owner-tested image is retained; no game patch bytes change for release packaging.
- Local combined checks: 6,656 menu cases; 352 retail/patched callback comparisons (704 executions); 704 menu/refill interaction cases; 41 HP readout cases; 36 pointer guards; 96 damage cases. External renderer, sound and event bodies are modeled, not a full game run.
- The final archive is tested after extraction: default and combined patcher fixtures, eight wrapped-message tests, all eight full-image stage rebuilds, combined instruction checks, source preservation, archive integrity and per-file hashes. The attached PACKAGE-VERIFICATION.json records the actual package results.

## Limits and preservation

Original PS2 hardware, PCSX2, other firmware setups and exhaustive hazards/characters/save-load coverage remain unverified. This is a custom interface; original developer-menu restoration is not established. No Free Camera or level selection is included. The original six-slot upgrade can persist in saves; use a spare save when experimenting.

Existing outputs are refused. Patchers hash the locked source, check original bytes/bounds/overlap, build a unique temporary output and verify the complete hash before publishing its filename. Handled failures remove temporary outputs; interruption or power loss may leave an incomplete .partial file. Each retained stage requires about 1.25 GB; eight outputs plus retail use about 11.25 GB decimal.

v0.3 and earlier releases remain available unchanged. No ISO, ELF, XBE, DOL, HIP/HOP game assets, credentials or SDK binaries are included in this release. [Third-party credits and upstream links](../../README.md#third-party-tools-and-research-credits) include Industrial Park/HipHopTool, bfbbdecomp/tssm, PCSX2, Dolphin, XboxDev/xemu and the other cited preservation/research projects. Heavy Iron Studios developed the original game, published by THQ; rights remain with their holders.

The package is identified by SOURCE_COMMIT.txt inside the ZIP. Publication is established by the v0.4 GitHub release page, not by this preparation document alone.
