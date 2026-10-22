# HealthMenu-TEST — PS3 validation worksheet

Date prepared: 2026-10-22  
Target: The SpongeBob SquarePants Movie (USA), PS2 `SLUS_209.04` on the established CFW PS3 test setup.

## What is already known

The four-row **DamageMenu-TEST** baseline was reported working by the owner. The newer **HealthMenu-TEST** candidate adds a read-only live `HP` number beside the Damage row; its emitted code and source-image windows have passed local tests, but **no successful hardware test of this new HP build is recorded yet**. Do not describe HealthMenu-TEST as hardware-verified until results below are observed.

See [the original implementation evidence](HEALTH-MENU-2026-10-22.md). Keep the working DamageMenu-TEST ISO and pristine source ISO unchanged.

## Test prerequisites

- Identify which ISO is being launched: HealthMenu-TEST versus DamageMenu-TEST. Don't infer from the filename alone if multiple copies exist.
- If checking integrity, the documented HealthMenu-TEST output SHA-256 is `fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a`; MD5 is `6e3e6c97a86d326bd5d4c0f539d56767`.
- Do not overwrite a working image; preserve ordinary save data, and avoid saving during experiments.
- Capture exact displayed HP and visible in-game health before and after each action; `HP-1` denotes an invalid/unavailable pointer, whereas `HP0` is a valid numeric zero.

## Hardware test matrix

| ID | Action | Expected observation | Result / exact values |
| --- | --- | --- | --- |
| H01 | Launch HealthMenu-TEST to stable gameplay; open custom menu | Menu appears with `Damage … HP…`, no freeze or clipped rows | PARTIAL PASS — HP display visible; no reported crash |
| H02 | Note HUD health and menu HP before taking damage | Numeric HP is plausible and stable | PENDING |
| H03 | With Damage 1, take one ordinary enemy hit | HP decreases in step with game health | PASS — owner reported HP3 → HP1 after 2 hits, 2 hamburgers lost; toggle state not independently recorded |
| H04 | Collect an ordinary health pickup | HP increases or otherwise matches observed game health behavior | PASS — owner reported recovery to 2 hamburgers and HP2; pickup type not explicitly reported |
| H05 | Switch to Damage 0; take comparable ordinary hit | Existing damage-off behavior remains and HP reflects actual value | PENDING |
| H06 | Restore Damage 1 and repeat ordinary hit | Damage behavior returns; HP changes appropriately | PENDING |
| H07 | Exercise other menu rows, music pause/resume, and Select hide/show | Prior controls keep working | PENDING |
| H08 | Pass through loading, level transition, and player-character transition if available | No crash, stale value, or bogus pointer-read display | PENDING |
| H09 | Die/restart and reopen menu | No freeze; HP reflects new player state | PENDING |
| H10 | Return to title and reload a level | Menu and HP behave correctly after reinitialization | PENDING |

For each failure, record **test ID, image identifier/hash, area and character, action sequence, expected/actual HP, whether the HUD changed, and whether the console froze**. A screenshot or short video is useful when available but not required.

## Go / no-go

**Go:** H01–H07 pass and H08–H10 show no stability or lifecycle regressions; describe exact observed coverage when updating the README.  
**No-go:** wrong/stale HP, persistent `HP-1` during stable gameplay, freeze, or a regression in existing controls. Revert testing to DamageMenu-TEST; do not alter the original ISO. Investigate pointer lifetime, formatter stack argument, or retained delay-slot behavior based on the failing case.

**Unverified until owner results arrive:** all rows above; no console outcome has been inferred from modeled MIPS tests.

## Owner console observations — October 22, 2026

On PS3, owner reported initial `HP3`, followed by `HP1` after two hits and loss of two hamburger health units. Owner subsequently reported two hamburgers and `HP2`, consistent with health recovery. These are **owner-reported hardware observations**, not an independently captured trace. Exact build hash on PS3, Damage toggle setting during hits, and transition behavior still need separate confirmation. Preserve the working DamageMenu fallback.
