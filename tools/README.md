# SpongeBob Movie Debug Tools — v0.3

Extract the complete release ZIP before running a CMD launcher. Each stage is self-contained in its folder. Windows PowerShell is sufficient for patching; Python is only needed for developer tests. Use the exact matching USA SLUS_209.04 image for the selected stage.

| Folder | Input ISO | Output stage |
| --- | --- | --- |
| overlay | Original matching USA ISO | Controller/status overlay probe |
| select-toggle | Pad-Debug-PROBE | Select-Toggle-TEST |
| debug-panel | Select-Toggle-TEST | Panel-TEST |
| music-panel | Panel-TEST | Music-TEST |
| debug-menu | Music-TEST | DebugMenu-TEST: three rows |
| damage-menu | DebugMenu-TEST | DamageMenu-TEST: four rows |
| health-menu | DamageMenu-TEST | HealthMenu-TEST: live HP beside Damage |

All seven stage images have been reproduced byte-identically in Muse's Neptune regression run (14/14 fixtures, 7/7 full-image stages). The owner also reports the HealthMenu stage working on a CFW PS3's PS2 software emulator: HP display followed hits, recovery, restart and the first level transition; Damage 0/1 and Select still worked. These are owner reports, not independent console traces. Original PS2 hardware and PCSX2 remain untested. This is a custom debug interface, not a recovered original developer menu.

Each patcher checks complete source and output SHA-256 values, original bytes, patch bounds and non-overlap. It keeps the input open against modification while hashing/copying. It writes a unique `.partial` file and moves it to the final filename only after verification, refusing overwrites. Handled failures clean up their temporary file. Force-killing PowerShell or losing power can leave a `.partial` file; it is not a completed ISO.

Allow roughly 1.25 GB of free space for each new stage output you retain. Starting from an existing DamageMenu-TEST only requires the health-menu stage. Building and retaining the entire chain uses about 8.75 GB for seven outputs, plus the original image.

Optional command-line use, shown for the HP stage:

```powershell
powershell.exe -NoProfile -File tools/health-menu/Apply-HealthMenu.ps1 -InputIso "DamageMenu-TEST.iso" -OutputIso "HealthMenu-TEST.iso"
```

Default output names use the complete `SpongeBob-Movie-USA-...` names recorded in [STAGES.json](STAGES.json). They do not depend on your input filename: the source hash determines compatibility.

Run the game-free patcher regression fixtures with Python 3.11 or newer and Windows PowerShell:

```text
python tools/test_patchers.py
```

Full private-ISO checks are optional:

```text
python tools/test_patchers.py --iso-dir "folder with stage inputs" --original-iso "original USA.iso"
```

Individual menu tests accept a privately extracted, matching original SLUS_209.04 executable. The debug-panel test needs no game files. `dolphin_container_smoke.py` is a retained GameCube container helper; it is not PS2 runtime validation.

No ISO, full executable, game asset, credentials or third-party SDK binaries are included.
