# SpongeBob Movie: live HP display candidate

- Date: October 22, 2026.
- Target: USA PS2 SLUS_209.04 in the established CFW PS3 testing context.
- Goal: show the current health integer beside the existing Damage toggle, without modifying health.
- Success condition: the number follows ordinary damage and health pickups on the console while existing controls continue to work.

## Rundown

A separate HealthMenu-TEST ISO adds `HP` to row 4, for example `Damage 1 HP3`. The previous four controls remain. HP-1 means the player data pointer was unavailable; HP0 is a legitimate zero value. This readout does not heal or grant upgrades.

**Proven locally:** the image and emitted instructions pass the checks below. **Unknown:** the new HP display's console behavior. The owner reported the preceding DamageMenu-TEST works fine; that report does not cover this new image. Keep the damage-menu ISO as the working fallback.

## Retail evidence

The retail variable-name table at 0x005FE088 pairs the string `Player Current Health` (0x00621255) with getter 0x002DFC70. That getter loads the pointer from 0x007ABC10 and then the 32-bit member at +0x460. The existing damage-decrement branch uses the same member. Exact original getter instructions and table bytes were checked against the known retail executable hash.

The panel reads this field only after the shared alignment/range guard accepts the pointer. It uses -1 when the pointer fails the check. Range/alignment checks cannot prove every otherwise in-range pointer is a live object.

The extra integer is the ninth argument to sprintf, including destination and format. It is stored in the first outgoing stack argument slot, matching the original renderer's use of stack slots for arguments beyond its eight argument registers. Renderer initialization, register saves and epilogue remain in place.

## Verification

| Class | Result | Practical limit |
| --- | --- | --- |
| Proven | 6,656 menu instruction cases, 36 existing pointer-guard cases, 41 health-readout cases and a 12-step interaction sequence pass. | Position/scene formatter and external sound backend calls are modeled; the renderer is not executed. |
| Proven | Health cases cover zero, positive and large values, rejected pointers, accepted boundary pointers and the outgoing stack argument. | Not evidence of all runtime object lifetimes. |
| Proven | Full ISO comparison: 326 changed bytes within the same five intended patch windows; image size remains 1,249,804,288 bytes. | Console testing remains required. |
| Proven | Windows PowerShell produced the expected image, and wrong-source/existing-output checks passed. | Only the exact matching input is supported. |
| Unknown | HP follows ordinary hits/pickups and remains reliable through transitions on PS3. | No new owner report or console screenshot supplied. |

Input SHA-256: `9df1860529ac4e6e5d2bb542ba59b1c171bb1ae797a24c8aef80eb75c4a12630`.

Output SHA-256: `fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a`.

Output MD5: `6e3e6c97a86d326bd5d4c0f539d56767`.

The action block now occupies 424/428 bytes and the formatter block 60/64 bytes. Moving safe pointer loads into call delay slots and shortening equivalent address sequences made room inside the existing areas. This refactoring needs console regression testing along with the HP readout.

## Next console check

With Damage 1, take an ordinary enemy hit and collect a health pickup; compare HP with the game health display. Check the same hit at Damage 0 and then restore Damage 1. Check the existing rows, title/loading, death/restart and a character or level transition separately. Report wrong numbers, stale values, missing text or crashes. Avoid saving during the experiment.

[Tools, manifests and reproducible tests](../tools/health-menu/). No game image, full executable, SDK or hardware screenshot is bundled.
