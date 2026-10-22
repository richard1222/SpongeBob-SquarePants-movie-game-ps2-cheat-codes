# SpongeBob Movie: four-row damage-menu candidate

- Date: 2026-10-22
- Audience: owner and PS2 patch contributors.
- Target: USA retail SLUS_209.04, established CFW PS3 test setup.
- Success condition: build a separate, guarded ISO whose new row reversibly changes the retail damage flag, then verify ordinary damage stops and returns on the console.

## Rundown

A new custom menu candidate adds row 4, `Damage 1` / `Damage 0`, to the owner-tested three-row menu. Select shows/hides, Up/Down wraps through four rows, and X changes the selected row. The previous music, XYZ and scene/controller rows remain.

**Proven locally:** instruction simulation, source/output hash checks and a complete ISO comparison passed. **Unknown:** the candidate's behavior on the console. No new owner test or console screenshot has been received. This is a custom menu, not recovery of the original developer interface.

## Retail discovery

The disc INI contains `G.TakeDamage = 1`, but the retail executable does not contain that parser-key string. Related keys are stored with a lowercase `g`. Finding an INI line alone would not prove it controls retail behavior.

The actual retail initialization writes the 32-bit value `1` to **0x007ABB20** at **0x0046BA98**. The adjacent `g.DamageTimeHit` parse result is stored at 0x007ABB24. Their adjacency agrees with the [decompilation's zGlobalSettings layout](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/src/SB/Game/zGlobals.h). That layout is supporting evidence, not the source of the retail address.

At **0x0032B778**, the retail code loads the flag; the branch at 0x0032B77C enters a health-decrement block when it is nonzero. The block subtracts at **0x0032BAE8** and stores at **0x0032BAEC**. With zero, execution bypasses that subtraction. Additional direct reads were observed at 0x0024759C, 0x00373E44, 0x003742C0, 0x00374818 and 0x00374CAC. Their complete gameplay effects were not established.

## What the toggle does

On a new X press with row 4 selected and the menu visible, it reads the flag and writes 1 if zero, otherwise 0. It displays the actual current value as an integer. It does not force the value every frame, and hiding the menu does not restore it. Set Damage to 1 before hiding when finished.

The menu retains its existing input path; normal gameplay button actions can still happen. Reloads or initialization can reset the flag. Protection from pits, scripted death or every possible hazard is unverified.

## Evidence

| Class | Result | Limit |
| --- | --- | --- |
| Proven | 6,656 emitted-instruction cases; 36 pointer-guard cases; 12 interaction steps passed. | Models position/scene formatter calls and sound backend; does not execute the renderer. |
| Proven | 96 focused cases execute actual retail instructions around one health-decrement branch. Zero skips its health write; nonzero allows subtraction. | Does not simulate all callers, damage routes or death logic. |
| Proven | Explicit checks cover 0/1 toggling, noncanonical incoming values, hidden-menu isolation and other-row isolation. | Simulation, not a hardware result. |
| Proven | Windows PowerShell created the image; wrong source and existing output were rejected. | Only the named source image is supported. |
| Proven | Full comparison found **388 changed bytes**, all within the five existing patch windows; output remains **1,249,804,288 bytes**. | Does not establish runtime stability. |
| Unknown | Ordinary enemy damage stops and resumes on the owner's console. | Requires the test below. |

Input SHA-256: `53f66e48d05bf22c5e3ac351f220526a912f067e65d08a430f76657a47e9b8f8`.

Output SHA-256: `9df1860529ac4e6e5d2bb542ba59b1c171bb1ae797a24c8aef80eb75c4a12630`.

Output MD5: `5bb8149862a63187f93eecf1f2ebf5d0`.

The action block uses 428 of its 428 audited bytes. Other capacities remain unchanged. The tests exercise emitted instructions, including a useful LUI in the new dispatch branch's delay slot. Existing renderer initialization and epilogue remain outside the changed regions.

## Next console test

1. Boot the separate DamageMenu-TEST ISO and check all four rows and Select hide/show.
2. At Damage 1, find a repeatable ordinary enemy hit that removes health.
3. Select row 4 and press X once. Confirm it reads 0; repeat the same hit.
4. Press X again. Confirm it reads 1; repeat the hit and check damage returns.
5. Report text changes, damage prevention and restoration separately. Check restart and level transitions separately. Avoid saving during this experiment.

The [patcher and reproducible tests](../tools/damage-menu/) contain original tools and patch metadata, with no game image, full executable or SDK binaries. The owner-tested three-row ISO is retained as the fallback.

