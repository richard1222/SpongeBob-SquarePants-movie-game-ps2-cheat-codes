SPONGEBOB MOVIE - COMBINED HEALTH MENU + REFILL TEST
USA SLUS_209.04 - v0.4 development candidate, not a published v0.4 release.

WHAT THIS COMBINES
The owner-tested four-row HealthMenu and the separately owner-tested retail
six-slot cheat refill. There is no new menu row: refill uses the original
retail cheat sequence below. The combined image has not been tested on PS3 yet.

BUILD
Input: SpongeBob-Movie-USA-HealthMenu-TEST.iso (stable v0.3 output), SHA-256
fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a
Run APPLY-HEALTH-MENU-REFILL.cmd and select that image.
It creates SpongeBob-Movie-USA-HealthMenuRefill-TEST.iso separately.
Existing outputs are rejected; about 1.25 GB free space is needed.
Source hash, original patch bytes and final output hash are checked.
No game files are included in the patcher ZIP.

OUTPUT SHA-256
8b9d5d006d6b3db0417e44736e1b4eacc68a53aa6fcdbef534157313a61e1883

CONTROLS
SELECT shows/hides the menu. UP/DOWN selects a row; X changes it.
1 Music pause/resume; 2 XYZ readout; 3 Scene/controller readout;
4 Damage 1 normal / 0 disabled, with current HP displayed.
Hiding the menu does not reset Damage. Restore Damage 1 when finished.

PS3 TEST
1. Mount the new HealthMenuRefill-TEST ISO on the same working CFW setup.
2. Enter a level. Check all four menu rows and SELECT still work.
3. Set Damage 1, take ordinary enemy damage until HP reads 1 or 2.
4. Pause with START, then hold L1+L2+R1+R2. While holding them, press:
   CIRCLE, CIRCLE, CIRCLE, CIRCLE, SQUARE, CIRCLE, SQUARE, CIRCLE.
5. Release the shoulders and resume. Check both the normal HUD and menu HP.
   The cheat grants six slots; the added refill copies the current maximum
   health into current HP. The isolated test was reported to produce six.
   If this build gives HP3 with six slots, record it: maximum sync timing
   still needs live verification. Do not treat HP3 as confirmed full success.
6. Confirm Damage 0 protects against the same ordinary hit, then restore
   Damage 1 and confirm HP falls. Reenter the cheat and check refill again.
7. Check one restart or level transition and SELECT afterward.

Report HP before/after the cheat, whether the HUD agrees, and any menu or
loading regression. Use a spare save or avoid saving: the original slot
upgrade can persist in saves. Preserve the stable HealthMenu ISO as fallback.

LOCAL CHECKS
Actual ISO menu words match the tested specification. Only the two refill
sites change from HealthMenu (22 differing bytes). 6,656 menu cases, 352 callback
comparisons (704 executions), 704 interaction cases, 41 HP readout cases,
36 pointer guards, 96 damage cases, 14 patcher fixtures and 8 message tests pass.
Synthetic runtime objects and modeled external calls do not replace a console
boot, live cheat input, save/load, renderer or transition test.

DEVELOPER REPRODUCTION (full repository checkout, Python 3.11+, no -O)
python tools/health-menu-refill/test_combined.py "path/to/retail/SLUS_209.04" --health-menu-iso "HealthMenu-TEST.iso" --combined-iso "HealthMenuRefill-TEST.iso"
python tools/test_patchers.py --patcher health-menu-refill/Apply-HealthMenuRefill.ps1 --manifest HealthMenuRefillPatch.json
python tools/test_patcher_messages.py

COMMAND LINE BUILD
powershell.exe -NoProfile -ExecutionPolicy Bypass -File Apply-HealthMenuRefill.ps1 -InputIso "HealthMenu-TEST.iso" -OutputIso "new-output.iso"

The patcher writes a unique temporary .partial file and publishes its final
name only after the expected hash passes. Handled failures remove the partial
file; a killed process or power loss may leave an incomplete .partial file.
