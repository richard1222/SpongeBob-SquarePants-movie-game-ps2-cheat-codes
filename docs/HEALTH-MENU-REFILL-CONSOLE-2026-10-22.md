# Combined HealthMenu + refill: owner PS3 validation

- Audience: owner and contributors.
- Date: October 22, 2026.
- Scope: the supplied HealthMenuRefill-TEST protocol on the established CFW PS3 Slim CECH-2001A / ps2_netemu setup.
- Success condition: complete the ordered menu, damage/refill and basic restart/transition checks without a reported problem.

## Rundown

**Proven as an owner report:** “everything worked in order no issues.” This records a successful owner test of the combined candidate after the supplied instructions. The combined image can now proceed to v0.4 release preparation; it is not yet a published v0.4 release.

The earlier message “it says HP3” described current starting health. The owner explicitly clarified “no i'm just letting you know my hp right now.” It is **not a reported refill failure**. After instructions to take damage to HP1/HP2, enter the original paused shoulder-button cheat, and report the result, the owner supplied the success report above.

## Current state

| Class | Claim | Evidence and limit |
| --- | --- | --- |
| Proven | Owner reports completing the ordered checks without issues. | Exact report in this chat: “everything worked in order no issues.” No independent console capture. |
| Inference | Combined menu controls and refill were compatible during the supplied test. | Overall owner report follows the combined protocol; individual numeric HP/HUD values were not separately supplied. |
| Unknown | Exact post-cheat HP value and internal maximum synchronization timing. | Do not convert the overall success report into a separately measured HP6 result. |
| Unknown | Extended character, hazard, save/load and prolonged transition coverage. | An ordered basic test is not an exhaustive compatibility test. |

## Artifact and prior local evidence

- Supplied ISO: `SpongeBob-Movie-USA-HealthMenuRefill-TEST.iso`.
- Supplied ISO SHA-256: `8b9d5d006d6b3db0417e44736e1b4eacc68a53aa6fcdbef534157313a61e1883`.
- Build/tools commit: [7b7375d](https://github.com/richard1222/SpongeBob-SquarePants-movie-game-ps2-cheat-codes/commit/7b7375db0a71d6c30dfde9519206fa1f38831103).
- [Combined build and protocol](HEALTH-MENU-REFILL-2026-10-22.md), [machine-readable receipt](../tools/health-menu-refill/VERIFICATION.json).
- Previous local checks remain unchanged: 6,656 menu cases, 352 callback comparisons (704 executions), 704 menu/refill interaction cases, 41 HP readout cases, 36 pointer guards, 96 damage cases, 14 patcher fixtures and eight message tests.
- No console-copy hash was independently rechecked with this report. No new screenshot or runtime memory trace was supplied. No game bytes or release assets changed.

## Next step

Prepare and verify the complete tools-only v0.4 package and release notes, preserving stable v0.3 and the separate working images. The combined owner console milestone is now recorded; a GitHub v0.4 release still requires packaging and publication.
