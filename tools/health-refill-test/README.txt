SpongeBob Movie (PS2, SLUS_209.04) - v0.4 EXPERIMENT: health cheat also heals
============================================================================

WHAT THIS IS
------------
An experimental patch built on the v0.4 Phase 2 trace
(docs/V0.4-PHASE2-HEALTH-CHEAT-TRACE-2026-10-22.md). The retail cheat
"unlock all six health slots" (cheatList[1], callback 0x002D2620) raises the
slot maximum but never touches current HP - by design (Phase 2 verdict).
This experiment tests the integration the callback's decomp-era name
(GEC_cb_RestoreHealth) suggests: after the retail callback runs, also
restore current HP to the player's current maximum, using the exact
operation the game itself performs at 0x00331504 (HP := max HP, both 32-bit
fields of the player struct reached via the pointer at 0x007ABC10:
current HP at +0x460, max HP at +0x464).

STATUS: designed and validated on Neptune (build, byte-diff audit,
extracted-ELF disassembly round-trip, full repo regression). Owner subsequently
reported: "it worked i got 6" on 2026-10-22, established CFW PS3 setup.
This confirms basic reported success; extended coverage remains unverified.

THE PATCH (2 sites, 6 words, fully reversible)
----------------------------------------------
1. VA 0x002D26CC, inside the retail callback: a dead nop word (it sits
   after the unlockables-refresh loop, before the UI-refresh tail; at
   that point $t0/$t1 are dead and the callback restores $ra from its own
   stack frame) becomes:
       jal 0x0010F06C            (word 0x0C043C1B)
2. VA 0x0010F06C: five zero words of inter-function padding (immediately
   after a jr $ra epilogue; unreachable by fall-through; no instruction,
   branch target, pointer, or computed address anywhere in the ELF
   references them - verified by full-binary scans) become the heal leaf:
       lui  $t0, 0x7B
       lw   $t0, -0x43F0($t0)    ; $t0 = *(0x007ABC10), the player pointer
       lw   $t1, 0x464($t0)      ; $t1 = max HP
       jr   $ra
       sw   $t1, 0x460($t0)      ; (delay slot) current HP = max HP
   The leaf clobbers only $t0/$t1 and returns to the callback, whose
   UI-refresh flow and return then proceed exactly as retail.

Nothing else changes: the cheat table, the sequences, the flags, the save
format, and every other callback are byte-identical to retail. The input
must be the unmodified retail ISO (SHA-256 c0494ad7...); the patcher
verifies the input hash and both guard sites before writing, refuses to
overwrite an existing output, and verifies the output hash afterwards.

KNOWN BOUNDARIES (from the trace, stated honestly)
--------------------------------------------------
- The heal runs on the callback's refresh path; if the unlockables table
  count (*(0x00636528)) were 0 the callback skips that path and no heal
  occurs (slots still apply). The table is populated in retail, so the
  heal is expected on every successful entry.
- Like the retail code it mirrors (0x00331504 and 165 other sites), the
  leaf dereferences the player pointer without a null check. The cheat
  handler only runs while paused in a level, where the pointer is the
  active player; the retail full-heal makes the same assumption.
- Whether the player struct's max HP (+0x464) already reflects the new
  6 slots at cheat time is the main open question the hardware test
  answers: healing to the struct max is always consistent (the game's
  own clamp at 0x00322638 enforces HP <= max), but the observed refill
  amount (3 vs 6) will show whether the max syncs from the slot words
  immediately or only at spawn/level load.

OWNER HARDWARE TEST (basic success now reported; protocol retained)
--------------------------------------------------------------------------
1. Mount SpongeBob-Movie-USA-HealthRefill-TEST.iso.
2. Enter a level, take damage so HP is below max (e.g. 1 or 2 HP).
3. Pause, hold L1+L2+R1+R2, enter: Circle x4, Square, Circle, Square,
   Circle (the retail health-slots code).
4. Expected if the design is right: success jingle, confirm flow, health
   display grows to 6 slots AND current HP refills (to 6 if the struct
   max has synced, otherwise to the pre-cheat max of 3).
5. Control: on the retail ISO the same steps grow the slots but HP stays
   where it was (Phase 2 prediction).

REVERSING
---------
Delete the experimental ISO. The retail ISO is never modified (the
patcher writes a new file and hash-guards the source).

INDEPENDENT REVIEW - 2026-10-22
352 original-versus-patched callback scenarios pass (704 executions), with
saved registers, stack return, slots, bonus bytes and UI-call behavior checked.
The existing ISO hash and its extracted executable match the tested bytes.
The callback's UI tail refers to PAUSESTATE MENU OR POWERUP COUNTER at
0x61FEC4 and calls the UI function when the found counter's count EQUALS 2.
Earlier HP-confirm string and inverted-state descriptions were incorrect.
No candidate ISO bytes changed. The owner subsequently reported it worked and
produced six; broader hazard, character and transition coverage remains open.

Python 3.11+, standard library, no -O:
python test_health_refill.py "path/to/original/SLUS_209.04" --patched-iso "path/to/HealthRefill-TEST.iso"
Hash/object/UI function bodies are modeled. This does not run the game renderer
or establish live pointer safety. See docs/V0.4-HEALTH-REFILL-REVIEW-2026-10-22.md.

OWNER RESULT - 2026-10-22
Exact report after the supplied refill test: "it worked i got 6".
Keep this isolated candidate and stable v0.3 as separate baselines. A combined
HealthMenu-plus-refill build has not been tested or released.

MENU ASSET FOLLOW-UP - 2026-10-22
The actual PS2 MNUI.HIP confirms the checked object is CNTR. The conditional
event targets PU SET TEXT ALL GROUP, containing 11 members including the
health-upgrade condition. See docs/PS2-MENU-CROSS-PLATFORM-2026-10-22.md.
