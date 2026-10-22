SPONGEBOB MOVIE - v0.4 CHEAT SEQUENCE PROBE (RESEARCH TEST, NOT A RELEASE)

Input: retail Nickelodeon SpongeBob SquarePants - The Movie (USA).iso (SLUS_209.04).
Run APPLY-CHEATSEQ.cmd. Full source hash and patch bytes are checked.
It creates SpongeBob-Movie-USA-CheatSeq-TEST.iso separately. Existing output
is rejected. About 1.25 GB free space is required. No game files are bundled.

WHAT IT CHANGES (one 32-bit word; one byte differs in the ISO):
Cheat table record 9 of 9 (cheatList at ELF 0x005FBCB0, record at 0x005FBD30),
key-sequence word 13 of 16 at ELF VA 0x005FBB60:
Circle (0x00020000) -> Triangle (0x00080000).
That cheat's 8-press entry sequence changes from
  Triangle Triangle Triangle Triangle Circle Triangle Circle Circle
to
  Triangle Triangle Triangle Triangle Triangle Triangle Circle Circle
No code bytes change. No other record changes. The traced retail handler is
zGameCheatsUpdate at 0x002D2740; see docs/V0.4-PS2-CHEAT-TRACE-2026-10-22.md.

WHY THIS CANNOT ALTER A SAVE:
The affected cheat flag bit is 0x10000000. The retail save routine
(zGameExtras_Save at 0x002D2AB0) writes only flags & 0xFFFF, so this bit is
never persisted. The patch is data-only and fully reversible: delete the test
ISO and use the retail ISO. Nothing else is modified.

OWNER TEST (in the game's cheat-entry screen):
1. Enter the OLD sequence above. Expect NO success jingle: that code no
   longer exists (after the entry window expires, the failure jingle plays
   if presses were registered).
2. Enter the NEW sequence. Expect the CHEAT_SUCCESS jingle and the toggle
   effect of that record (an Extras/costume flag) to flip.
3. The other eight cheat codes and normal play must be unchanged.
Report exactly which jingles/effects occur for each sequence. Avoid saving
during this experiment, to keep the test clean.

HARDWARE-UNVERIFIED. Research build 2026-10-22; not part of v0.3.
