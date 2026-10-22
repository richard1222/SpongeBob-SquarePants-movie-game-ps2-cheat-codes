SPONGEBOB MOVIE - LIVE HP MENU TEST

Input: owner-tested SpongeBob-Movie-USA-DamageMenu-TEST.iso (USA SLUS_209.04).
Run APPLY-HEALTH-MENU.cmd. Full source hash and patch bytes are checked.
It creates SpongeBob-Movie-USA-HealthMenu-TEST.iso separately. Existing output
is rejected. About 1.25 GB free space is required. No game files are bundled.

NEW: row 4 now reads Damage 1 HP3 (example). HP is the current retail health
integer. HP-1 means the data pointer is unavailable. HP0 can mean zero health.
This display only reads health. It does not heal, grant upgrades or save changes.

SELECT show/hide; UP/DOWN choose rows 1-4; X changes the selected row.
1 Music pause/resume; 2 XYZ readout; 3 Scene/controller readout;
4 Damage 1 normal / 0 disabled, plus the new live HP readout.
Damage is not forced every frame. Hiding does not restore it: choose Damage 1
when finished. Normal gameplay button actions can also occur.

TEST - NEW BUILD HARDWARE-UNVERIFIED
1. Check the four controls still work and the HP number is visible.
2. During ordinary gameplay with Damage 1, take an enemy hit. Check HP falls
   along with the game's health display; collect a health pickup and check it rises.
3. Change Damage to 0, repeat the same hit, and check whether HP stays unchanged.
4. Restore Damage 1 and check that ordinary damage works again.
5. Check title, loading, death/restart and a character or level transition for
   stale values or crashes. Avoid saving during this experiment.
Report a wrong number, missing HP text, crashes, or any control regression.

This is a custom menu. Protection against every hazard or scripted death is
unverified. The previous four-row build was owner-reported working on CFW PS3;
that report does not establish this new HP display's behavior.
Pointer range/alignment guards reduce invalid accesses; they do not prove an
otherwise in-range object remains valid through all game states.

Developer tests (Python 3, standard library; supply your original matching ELF):
python test_health_menu.py "path/to/original/SLUS_209.04"
python test_retail_damage.py "path/to/original/SLUS_209.04"
Position/scene formatter calls, the renderer and the external sound backend are
not executed by the menu simulation. Retail music instructions are executed.

V0.2 PATCHER UPDATE
This script uses .NET hashing and validates the manifest before copying.
It builds a uniquely named .partial file beside the requested output and
publishes the final filename only after the expected SHA-256 passes. Handled
failures remove the temporary file; force-killing PowerShell or loss of power
may leave a .partial file. It is not a completed ISO. Existing outputs are kept.
Optional command line: powershell.exe -NoProfile -File Apply-HealthMenu.ps1 -InputIso "input.iso" -OutputIso "new-output.iso"
