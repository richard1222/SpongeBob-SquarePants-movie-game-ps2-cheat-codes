# Muse GG01 retail investigation handoff — 2026-10-22

Source: [Muse report on Google Drive](https://drive.google.com/file/d/10Z5BlOKjR4Ib6vg803I9q70CETtcbfcg/view), uploaded 2026-10-22 18:05 UTC. Observations below are **Muse-reported retail ISO analysis**, not independently rerun on this device.

## Confirmed by Muse on USA PS2 SLUS_209.04

- INI contains `TaskStatus = GG01 0 0 0 0 0 0 # World 13 (Disabled, to be removed)`, plus commented-out `PointerPlayerMapping = GG01 PLS6`.
- No `GG01` archives remain; only `GG02.HIP`, `GG02.HOP`, `GG02_US.HIP` under the GG folder.
- No `GG01` string appears in retail executable.
- Five proposed Goofy Goober Dream Platforming objectives are absent from retail executable and all inspected localized text archives.
- GG02 contains complete challenge entities: `TASKBOX`, `COUNTER`, `TOKEN`, `TALKBOX`; and `RING_001`, `LAPCOUNTER_TRIG_01–06`, `CONETOWER_MECH_01A–08A`, `RAMP_SFX_TRIG_01–06`.
- INI includes warning that TaskStatus overrides can cause non-existent tasks to surface when starting a new game. Avoid trying it on the owner's main save.

## Consequences

GG01 is **not a simple enable-code restoration**. No original retail level geometry, scripts or mission text found. An earlier preserved build with GG01 would be required to restore the authentic level. A new recreation based on GG02 machinery would be a distinct fan reconstruction, not recovery of deleted assets.

## Demo-disc uncertainty

The Drive handoff separately discusses **Asian PlayStation 2 Demo Disc issue 90** (Go! Sudoku). This should NOT be conflated with **Official U.S. PlayStation Magazine Demo Disc 90** associated with the DWARF index from prior research. The same issue number describes different disc series. Muse reports SpongeBob appears in Asian series issues 87/88 but did not establish issue 90 contents. Independently confirm the U.S. OPM SCUS-97442 listing against existing symbols before drawing conclusions.

## Next work

1. Compare actual U.S. OPM Demo Disc 90 (SCUS-97442) source/archive metadata to our existing DWARF project; determine whether it is unique.
2. Search verified earlier development builds for `GG01.HIP` / `GG01.HOP` / `GG01_US.HIP`.
3. Inspect GG02 as a **reference** without modifying v0.3 or retail originals.
4. Focus near-term v0.4 experiments on retained original cheat system, since GG01 itself is absent.

No proprietary game files committed.
