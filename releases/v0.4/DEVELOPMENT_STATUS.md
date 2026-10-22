# v0.4 development status — October 22, 2026

**Development milestone only — NOT a published v0.4 GitHub release.**

- **Stable published release:** [v0.3](https://github.com/richard1222/SpongeBob-SquarePants-movie-game-ps2-cheat-codes/releases/tag/v0.3), seven cumulative patcher stages and owner-tested HealthMenu on CFW PS3 Slim.
- **New v0.4 evidence:** Original PS2 cheat handler and nine cheat records statically traced; isolated one-byte key-sequence modification passed owner PS3 testing (Square ×6, Circle ×2, paused, four shoulder buttons held). SHA-256 `f603d78aa4be977bdc06d4ab77da322547c549de764fe580501bd90a2225e4ac`. Probe is built on clean retail ISO, **not** the stable HealthMenu ISO.
- **Current task:** decide on one original callback to exercise and design safe isolated verification, then investigate integration into cumulative HealthMenu without rewriting the stable releases.
- **Unfinished:** integration, regression suite for combined variant, console validation of combined variant, tool-only ZIP, SHA-256, notes, and verified GitHub release.

[See the milestone-by-milestone v0.4 roadmap](../../docs/V0.4-ROADMAP.md). [PS2 retail cheat trace](../../docs/V0.4-PS2-CHEAT-TRACE-2026-10-22.md). [Experiment](../../tools/cheat-seq-test/).

Restrictions: no Free Camera/level selection; no ISOs/game binaries in repository; preserve all existing originals and v0.3.
