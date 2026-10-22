# PS2 menu inspection using GameCube and Xbox references

- Audience: owner and contributors to the SpongeBob Movie PS2 debug-menu project.
- Date: October 22, 2026.
- Scope: GameCube engine structures, Xbox debugging documents, and the actual USA PS2 executable/menu archive.
- Success condition: turn cross-platform references into a reproducible finding in PS2 game data before using them in a patch.

## Rundown

**Proven:** the PS2 health cheat checks a named counter and, conditionally, sends event `0x3C` through a named-event wrapper to `PU SET TEXT ALL GROUP`. The actual menu archive contains that group, with 11 members including a health-upgrade condition. This materially improves the previous generic description of a “UI refresh.”

**Inference:** the counter's runtime halfword at `+0x14` is its count, and event `0x3C` is Evaluate. GameCube headers describe exactly those meanings; PS2 archive types and executable behavior support the mapping. This is a static semantic match, not a captured runtime trace.

The useful next step is to preserve this retail refresh behavior when combining the owner-tested refill with HealthMenu. This research changes no ISO or release assets. The Xbox documents provide a future tracing method; actual Xbox executable comparison remains open.

## What the actual PS2 game contains

The read-only inspector walks bounded archive chunks, validates every asset header's payload range, rejects duplicate IDs, and checks selected asset payload IDs and sizes. It found **1,156 asset headers** in `MNUI.HIP`.

| Class | Finding | Evidence |
| --- | --- | --- |
| Proven | Counter ID `0xC052244B`, type `CNTR`, initial count 1, no outgoing links. | Header file offset `0xDF1E`; 12-byte payload at `0x462E50`. Base type 22, flags `0x001D`. |
| Proven | The counter's archive display name is truncated to `PAUSESTATE MENU OR POWERUP COUN`. | Archive debug-name field. The full executable string `PAUSESTATE MENU OR POWERUP COUNTER` hashes to the same ID using multiplier 131. |
| Proven | Target group ID `0x5BCC2912`, `PU SET TEXT ALL GROUP`, type `GRUP`. | Header offset `0x78E8`; 56-byte payload at `0x462E10`, 11 members, delegation 0 (all items per Industrial Park), no outgoing links. |
| Proven | One group member is ID `0xC83DA473`, `PU_UGRADE_COND HP LV 0`, type `COND`. | Member ID resolves to an asset header in the same archive. |
| Proven | Other members are the BA, BB, BF, CW, HS, KS, SB, SW and TH level-0 upgrade conditions, plus `PU EVAL ALL HASH COND`. | All 11 member IDs resolve in the same archive; the receipt lists each. |
| Inference | The group is used to reevaluate power-up display conditions after the health-slot cheat. | Group/member names, group contents, the callback's conditional event call and the GameCube event enum agree. Handler bodies and final rendering were not executed here. |

The archive inspection establishes the menu's structure; it does not establish that a hidden developer menu exists. No new visual gameplay or emulator observation was made in this research pass. The owner's earlier report, “it worked i got 6,” remains the hardware evidence for the separate HealthRefill-TEST.

## PS2 executable trace

Input: retail `SLUS_209.04`, SHA-256 `2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956`. Addresses below are PS2 virtual addresses; file offsets use bias `0xFFF80` for these sites.

1. `0x002D26D0–0x002D26E0`: the health callback hashes the full counter name at `0x0061FEC4` through `0x0044DEA0`, then looks up its object through `0x002EED90`.
2. `0x002D26F0–0x002D26FC`: if found, it reads a signed halfword at object `+0x14` and checks **equality with 2**. The GameCube `_xCounter` layout names this field `count`; its separate byte `state` is at `+0x16`. Previous notes saying “state at +0x14” were imprecise.
3. `0x002D270C`: loads the event-target string pointer from `GP-0x76C4`. With GP `0x0063DBF0`, the word at `0x0063652C` points to `0x0061F5A7`: `PU SET TEXT ALL GROUP`.
4. `0x002D2710`, delay slot `0x002D2714`: calls `0x003EB940` with event `0x3C`.
5. Wrapper `0x003EB940` hashes its string target, looks it up, and calls `0x003EB670` only if found. This matches the named `zEntEvent(char*, U32)` overload described by the GameCube header. Exact retail symbol names remain inferred.

Important distinction: the checked counter and the event's destination group are **different objects**. The callback does not send Evaluate to the counter itself. The previous instruction-level refill test modeled these external calls; these findings improve their interpretation without changing the patch or its tested control flow.

## Cross-platform sources and limits

- [GameCube xCounter.h](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/src/SB/Core/x/xCounter.h): runtime count/state layout. [xBase.h](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/src/SB/Core/x/xBase.h) supplies the 32-bit base structure. These are references; PS2 evidence is checked separately.
- [GameCube xEvent.h](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/src/SB/Core/x/xEvent.h): counting the sequential enum from zero gives `eEventEvaluate = 60 = 0x3C`; the header also declares named-event overloads. An enum name alone does not prove every event remains implemented on PS2.
- [HipHopTool Section_AHDR](https://github.com/igorseabra4/HipHopTool/blob/47bf644b14dcbc6a805218b578120f6f24b990e8/HipHopFile/Sections/Section_AHDR.cs): big-endian header metadata and absolute payload offsets.
- [Industrial Park AssetCNTR](https://github.com/igorseabra4/IndustrialPark/blob/593134993788e772aae5d321203ef3a9ff758a68/IndustrialPark/Assets/ObjectAssets/AssetCNTR.cs) and [AssetGRUP](https://github.com/igorseabra4/IndustrialPark/blob/593134993788e772aae5d321203ef3a9ff758a68/IndustrialPark/Assets/ObjectAssets/AssetGRUP.cs): signed 16-bit counter payload count and group member/delegation layout. Our PS2 payloads are little-endian despite big-endian archive metadata.
- [xemu guest debugging](https://xemu.app/docs/dev/debug/guest/): `-s` enables guest GDB on localhost port 1234; `-S` starts paused. This could trace a legitimately available Xbox build. No Xbox game was launched here.
- [Caustik's XBE format](https://www.caustik.com/cxbx/download/xbe.htm): useful for eventual executable section/header comparisons. The displayed table duplicates a section-header offset, so a real parser and bounds checks are needed before relying on numerical fields. No Xbox XBE is available in the inspected project files.
- [nxdk](https://github.com/XboxDev/nxdk): an SDK for building Xbox software; building new debug-enabled software does not restore removed retail game code.

## Reproduce and input identity

Use Python 3, standard library only:

```text
python tools/inspect_menu_counter.py "path/to/PS2/MNUI.HIP"
```

Archive size: **4,837,376 bytes**. SHA-256: `119771102d55561f4cc9357093f2ea22b0bc02e0eb8e836f15085470eb6784dc`.

The companion `PS2-MENU-COUNTER-2026-10-22.json` contains metadata only. The tool reads one supplied archive, prints JSON and never writes back to it. It is a targeted PS2 inspector, not a universal HIP converter or cross-platform runtime mapper. No original assets, executable bytes or disc image are included.

## Next step / unknowns

Preserve the retail count check and group event in a separately validated HealthMenu-plus-refill candidate. Its release still requires integration checks and its own console test. Stable v0.3 and the isolated owner-tested refill remain separate baselines.

Unknown: live changes to this counter throughout all pause states, exact conditional/event-handler behavior, original developer-menu survival, and Xbox/GameCube binary differences. No cross-platform code addresses have been copied into the PS2 patch.
