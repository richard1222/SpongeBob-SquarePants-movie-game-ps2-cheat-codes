SPONGEBOB MOVIE � EXPANDED DEBUG MENU TEST

Run APPLY-DEBUG-MENU.cmd on Windows and choose the owner-tested
SpongeBob-Movie-USA-Music-TEST.iso (USA SLUS_209.04).
The patcher checks the complete source hash and patch bytes and creates
SpongeBob-Movie-USA-DebugMenu-TEST.iso separately. Existing output is rejected.

The title shows the selected row as 1/3, 2/3, or 3/3:
SELECT: hide/show. UP/DOWN: move between the three rows, wrapping at the ends.
X on row 1: pause/resume real music, as in the owner-tested Music-TEST build.
X on row 2: enable/disable a live integer XYZ position readout.
X on row 3: enable/disable scene ID and held/newly-pressed controller bits.
OFF means the readout is disabled. N/A means the relevant object is unavailable.
The pad line shows held bits followed by newly pressed bits in hexadecimal.
The XYZ and scene readouts start OFF. The music row reports the actual engine flag.

This is a CUSTOM MENU, not recovery of the game's original developer menu.
This build does not provide invincibility, free camera, teleportation, unlocks,
or progression edits. Its new diagnostic rows do not write to player/scene data.
Normal gameplay button actions still occur; the menu does not consume inputs.

FIRST HARDWARE TEST
1. Boot and check that the three-row menu appears without a crash.
2. Check row navigation, music pause/resume, and SELECT hide/show.
3. At the title screen, enable rows 2 and 3; unavailable data should show N/A.
4. Start ordinary gameplay. Check that XYZ changes when moving and scene changes
   across levels. Toggle the readouts OFF and ON again.
5. Check loading, death/restart, character switches and returning to the title.
6. Report freezes, crashes, flicker, missing text, wrong coordinates or stale data.

New rows are hardware-UNVERIFIED. Pointer range/alignment/null guards and exact
instruction simulations passed; position/scene calls and audio backend were
modeled. Actual retail music pause/resume instructions were executed in the
simulation. Runtime object lifetimes and renderer behavior require console tests.

Source Music-TEST owner report: "it worked", 2026-10-22, CFW PS3.
No game image, game executable, external SDK binaries or credentials are bundled.
The patcher needs PowerShell, about 1.25 GB free space, and the matching input ISO.

DEVELOPER TESTS
Python 3, standard library only:
  python test_debug_menu.py "path/to/your/original/SLUS_209.04"
DEVELOPER-SPEC.json contains the exact emitted instructions and patch guards.
These tests model the position/scene formatter and audio backend calls; they do
not execute the game renderer or establish console compatibility.
