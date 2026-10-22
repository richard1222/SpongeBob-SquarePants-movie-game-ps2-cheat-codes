SPONGEBOB MOVIE - FOUR-ROW DAMAGE MENU TEST

Input: owner-tested SpongeBob-Movie-USA-DebugMenu-TEST.iso, USA SLUS_209.04.
Run APPLY-DAMAGE-MENU.cmd. Source hash and original patch bytes are checked.
A separate SpongeBob-Movie-USA-DamageMenu-TEST.iso is created. Existing output
is rejected. About 1.25 GB free space is required. No game files are bundled.

SELECT: show/hide. UP/DOWN: choose rows 1-4, wrapping at each end.
X: change the selected row.
1 Music: pause/resume. 2 XYZ: readout. 3 Scene: scene/controller readout.
4 Damage: 1 is normal damage; 0 disables the candidate damage flag.
The game initializes the flag to 1. The menu only changes it on X at row 4.
Hiding the menu does not restore damage. Set Damage back to 1 before hiding.
The menu does not consume buttons: normal gameplay actions can also occur.

HARDWARE TEST PENDING. This is a custom menu, not an original developer menu.
The flag is statically traced to retail reads and an initialization write.
This is not a promise of protection against every death, pit or scripted event.

Test in ordinary gameplay, without saving during this experiment:
1. Check the original three rows and navigation still work.
2. At Damage 1, find a repeatable ordinary enemy hit that removes health.
3. Select row 4 and press X once. Damage must read 0. Repeat the same hit.
4. Press X again. Damage must read 1 and the same hit should hurt again.
5. Report separately: text changed, damage stopped, damage returned, crashes.
6. Check death/restart and a level transition separately; do not assume the flag
   persists across reloads. It is not forced every frame.

Instruction simulation checks navigation, flag writes, 0/1 restoration,
noncanonical incoming values, hidden-menu isolation, music and pointer guards.
The simulator models external scene/position formatters and the sound backend.
No runtime protection claim has been verified on the console yet.

Developer instruction test (Python 3, standard library):
python test_damage_menu.py "path/to/original/SLUS_209.04"

Additional retail branch test:
python test_retail_damage.py "path/to/original/SLUS_209.04"
96 cases verify one actual retail health-subtraction branch.
