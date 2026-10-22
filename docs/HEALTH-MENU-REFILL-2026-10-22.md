# Combined HealthMenu and refill candidate

- Audience: owner and contributors; October 22, 2026.
- Scope: combine the existing HealthMenu with the isolated six-slot health-cheat refill.
- Success condition: retain both tested implementations byte for byte, verify the actual built ISO and their modeled interactions, then obtain a separate PS3 hardware result.

## Rundown

**Proven locally:** the combined candidate is built and passes the instruction and patcher checks below. **Owner-reported PS3 result:** “everything worked in order no issues.” The supplied ordered test is reported successful; exact post-cheat HP and extended coverage were not separately recorded. Stable v0.3 and both separate test images are preserved. This is a v0.4 development candidate, not a published v0.4 release.

The four existing menu rows remain available. Refill uses the original paused shoulder-button cheat; it is not a new row. The build adds the same two-site refill patch to the stable HealthMenu image. No other ISO bytes change. The callback retains the original pause-counter check and power-up group refresh identified in the [menu research](PS2-MENU-CROSS-PLATFORM-2026-10-22.md).

[Download the combined test ISO on GoFile](https://gofile.io/d/dsyTRJS1). Upload size and MD5 match the local artifact; the public page was inspected and shows the expected filename and 1.2 GB listing.

The separate tools-only incremental ZIP is 6,631 bytes, SHA-256 `f5b9e7fcf00ba359e1184527978679ebf432fcd87d773a1477acd92aae35e717`. It builds from the stable HealthMenu image. Full v0.4 release packaging remains pending.

## Evidence

| Class | Check | Result |
| --- | --- | --- |
| Proven | Source tool files matched repository blob hashes at `1090ef2a851b30fbb409ffe2f7622cb27d11e21a`. | Baseline manifests, instruction specs, patchers and tests authenticated before integration. |
| Proven | A separately constructed reference and the hardened PowerShell patcher produce the same full-image hash. | Output SHA-256 below. |
| Proven | Complete ISO comparison against HealthMenu. | Exactly 22 differing bytes within the two refill sites; all other bytes equal. |
| Proven | Combined executable's menu instructions checked against the tested specification. | All menu blocks and retail music instructions match; combined ELF equals the HealthMenu ELF plus the two intended refill changes. |
| Proven | Existing menu checks rerun. | 6,656 input/menu cases, 41 HP readout cases, 36 pointer guards and a 12-step sequence pass. |
| Proven | Retail-versus-combined callback comparisons. | 352 cases, 704 executions; slots, bonus bytes, event calls, saved registers, stack and memory outside current HP preserved. |
| Proven | Menu/refill interaction checks. | 704 cases across all 32 menu states, HP values through maximum 3/6, damage enabled/disabled; display follows modeled refilled HP, row-4 toggle works and repeat refill is idempotent. |
| Proven | Damage-decrement checks. | 96 cases; tested retail instruction windows are unchanged in the combined executable. |
| Proven | New combined patcher fixture checks. | 14 cases pass, including wrong source, overlap, bounds, original-byte guard, final-hash failure cleanup, existing-output preservation and missing Get-FileHash. Eight wrapped-message tests pass. |
| Inference | These checks support compatibility of the unchanged patches. | External rendering, sound, hash lookup, scene lookup and event handlers are modeled rather than running the complete game. |
| Recorded owner report | Combined test completed in order without issues. | Exact report: “everything worked in order no issues.” No independent console capture; exact final HP and extended coverage not separately recorded. |

This is byte/instruction verification; no new gameplay screenshot or emulator boot was produced.

## Artifact identity

- Input: `SpongeBob-Movie-USA-HealthMenu-TEST.iso`, SHA-256 `fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a`.
- Output: `SpongeBob-Movie-USA-HealthMenuRefill-TEST.iso`, **1,249,804,288 bytes**.
- Output SHA-256: `8b9d5d006d6b3db0417e44736e1b4eacc68a53aa6fcdbef534157313a61e1883`.
- Output MD5 for upload comparison: `36edd125f763fbcfab3d2bcc01fe2d6b`.
- Combined ELF SHA-256: `96b03ca18a8b2db1a033a291e2970d0b515f7f400737a2057c114ef6861f7eeb`.
- Added detour: PS2 VA `0x002D26CC`, ISO offset `877266764`, 4-byte span.
- Added leaf: PS2 VA `0x0010F06C`, ISO offset `875417836`, 20-byte span (18 bytes differ from zero).

No game data belongs in the tools repository or patcher ZIP. The incremental patcher expects the stable HealthMenu output, so the seven stable stages do not need changing. `tools/test_patchers.py` now accepts a patcher path and manifest filename so the same fixture suite can check the new stage; its default remains the stable HealthMenu patcher.

## PS3 test and next step

1. Mount **HealthMenuRefill-TEST**, enter a level and check the four menu rows and Select.
2. Set **Damage 1**; take ordinary damage until the menu shows HP1 or HP2.
3. Press **START** to pause. Hold **L1 + L2 + R1 + R2**, then press **Circle four times, Square, Circle, Square, Circle**.
4. Release the shoulders and resume. Record the menu HP and normal health HUD. The added action refills to the current struct maximum; the original cheat grants six slots. The isolated candidate was reported to produce six. If this combined build shows HP3 with six slots, record the discrepancy rather than declaring complete success.
5. Check Damage 0 protection, restore Damage 1, take a hit and reenter the cheat. Check one restart/level transition and menu hide/show.

Use a spare save or avoid saving during this test because the original slot upgrade can persist. Preserve the stable image. Unknowns include live maximum synchronization, other hazards/characters, save/load and prolonged transitions. The owner has now reported the combined test successful. A v0.4 release still requires separate release packaging/verification.

Reproduction commands and detailed controls are in [the incremental patcher README](../tools/health-menu-refill/README.txt); the machine-readable test receipt is [VERIFICATION.json](../tools/health-menu-refill/VERIFICATION.json).

## Owner console result received after the build

The owner reports **“everything worked in order no issues”** after the supplied sequence. The earlier HP3 message was explicitly clarified as starting health, not a failed refill result. [Full owner-result receipt and limits](HEALTH-MENU-REFILL-CONSOLE-2026-10-22.md). No patch bytes changed; this remains a v0.4 development candidate until release publication.
