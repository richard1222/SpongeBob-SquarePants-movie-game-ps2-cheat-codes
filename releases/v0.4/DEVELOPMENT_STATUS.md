# v0.4 release preparation status — October 22, 2026

**Prepared for packaging; publication is not yet confirmed.** This file is updated after the release asset is verified.

- **Game milestone:** owner reports “everything worked in order no issues” for combined HealthMenuRefill-TEST on the established CFW PS3 CECH-2001A setup. [Console receipt](../../docs/HEALTH-MENU-REFILL-CONSOLE-2026-10-22.md). HP3 was starting health, not a failed refill. Exact final HP is not separately recorded.
- **Tools:** all eight cumulative stages plus the two independent retail probes, helper scripts, tests, source identity, quick start and research notes. [Notes](RELEASE_NOTES.md).
- **Fixes:** wrapped-message checks, selectable patcher fixtures, and combined tests preserving the shipped owner receipt unless a new run path is explicitly supplied.
- **Game bytes:** unchanged owner-tested ISO SHA-256 `8b9d5d006d6b3db0417e44736e1b4eacc68a53aa6fcdbef534157313a61e1883`.
- **Next gate:** check the exact extracted package, rebuild all eight stages, verify source preservation and archive checksums, upload and publish the release, then verify its assets.
- **Unmeasured:** original PS2/PCSX2 and broad hazard, character, save/load and prolonged transition coverage.
- **Preserved:** existing v0.3 and prior releases, original retail and separate owner-tested images. No game files or SDK binaries in the tools package.

[v0.4 roadmap](../../docs/V0.4-ROADMAP.md) · [Release notes](RELEASE_NOTES.md).
