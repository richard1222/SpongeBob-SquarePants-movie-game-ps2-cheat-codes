# v0.4 development status — October 22, 2026

**Development milestone only — NOT a published v0.4 GitHub release.**

- **Stable published release:** [v0.3](https://github.com/richard1222/SpongeBob-SquarePants-movie-game-ps2-cheat-codes/releases/tag/v0.3), seven cumulative patcher stages and owner-tested HealthMenu on CFW PS3 Slim.
- **New v0.4 evidence:** Original PS2 cheat handler and nine cheat records statically traced; isolated one-byte key-sequence modification passed owner PS3 testing (Square ×6, Circle ×2, paused, four shoulder buttons held). SHA-256 `f603d78aa4be977bdc06d4ab77da322547c549de764fe580501bd90a2225e4ac`. Probe is built on clean retail ISO, **not** the stable HealthMenu ISO.
- **Current candidate:** the original health-slot callback now has a separate health-refill experiment, built and locally validated. Independent review adds 352 retail/patched comparisons (704 executions), verifies the actual ISO/executable bytes, and corrects the UI-flow address/state descriptions. The owner subsequently reported **“it worked i got 6”** for the isolated refill candidate on the established CFW PS3 setup. Basic reported success is recorded; broader coverage remains open. [Review](../../docs/V0.4-HEALTH-REFILL-REVIEW-2026-10-22.md).
- **Current task:** combined HealthMenu-plus-refill candidate built and uploaded. Owner PS3 console test is next. [Combined evidence, download and test](../../docs/HEALTH-MENU-REFILL-2026-10-22.md). Stable v0.3 and the isolated owner-tested refill are preserved.
- **Combined local checks:** 6,656 menu cases, 352 callback comparisons (704 executions), 704 interaction cases, 41 HP readout cases, 36 pointer guards, 96 damage cases, 14 combined-patcher fixtures and eight message tests pass. Only 22 bytes differ from HealthMenu, at the existing refill sites. Incremental tools-only ZIP is built; combined ISO SHA-256 is `8b9d5d006d6b3db0417e44736e1b4eacc68a53aa6fcdbef534157313a61e1883`.
- **Unfinished:** combined console validation, broader live behavior/save/transition coverage, full v0.4 release packaging and verified GitHub release. The combined candidate is not yet a stable release.

[See the milestone-by-milestone v0.4 roadmap](../../docs/V0.4-ROADMAP.md). [PS2 retail cheat trace](../../docs/V0.4-PS2-CHEAT-TRACE-2026-10-22.md). [Experiment](../../tools/cheat-seq-test/).

Restrictions: no Free Camera/level selection; no ISOs/game binaries in repository; preserve all existing originals and v0.3.
