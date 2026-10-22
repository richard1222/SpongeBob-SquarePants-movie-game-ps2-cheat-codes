![Platform](https://img.shields.io/badge/Platform-PS2-blue)
![Region](https://img.shields.io/badge/Target_Region-USA-green)
![Serial](https://img.shields.io/badge/Target_Serial-SLUS__209.04-orange)
![Stable](https://img.shields.io/badge/Stable-v0.3-blue)
![Development](https://img.shields.io/badge/Development-v0.4-orange)

# The SpongeBob SquarePants Movie (PS2) — cheats and debug research

Research for the 2004 Heavy Iron Studios console game, focused on PlayStation 2. Last updated: October 22, 2026.

---

## Table of Contents

- [Project Goal](#project-goal)
- [Current Status](#current-status)
- [Prototype Findings](#prototype-findings)
- [PS2 Button Cheats](#ps2-button-cheats)
- [Next Steps](#next-steps)
- [Progress Chart](#progress-chart)
- [Tools](#tools)
- [Third-party tools and research credits](#third-party-tools-and-research-credits)
- [Resources](#resources)
- [Project Notes](#project-notes)

---

## Project goal

Find and verify cheat codes, investigate whether a debug menu can be restored or enabled, and identify other useful development features and unused content. Research prototype, beta, review, and demo builds where evidence is available.

Free camera and level selection are outside the current requested scope. This is a separate project from Creature from the Krusty Krab.

## Current status

**Stable release:** [v0.3](https://github.com/richard1222/SpongeBob-SquarePants-movie-game-ps2-cheat-codes/releases/tag/v0.3) — owner-tested custom HealthMenu for CFW PS3 Slim `ps2_netemu`, with all seven tested cumulative patcher stages. **Active development: v0.4**, investigating the *original* Heavy Iron retail cheat system. This does **not** indicate a published v0.4 release. [v0.4 milestone and release gates](releases/v0.4/DEVELOPMENT_STATUS.md).

**v0.4 first hardware milestone — October 22, 2026:** Muse traced `zGameCheatsUpdate` at PS2 retail address `0x002D2740` and confirmed a nine-record cheat table. A separate one-data-byte `CheatSeq-TEST` ISO replaced the Patrick Caveman code with **Square ×6, Circle ×2**. On PS3 Slim, the owner reported success sound for the new sequence and no success for the replaced original sequence; Muse verified the mounted ISO's SHA-256 `f603d78aa4be977bdc06d4ab77da322547c549de764fe580501bd90a2225e4ac`. **Correct entry:** start a level, pause with START, hold all four shoulder buttons L1+L2+R1+R2, then press the Square/Circle sequence. The initial *Triangle* instructions were incorrect. This probe uses the **original retail ISO**, not a combined HealthMenu+cheat build. [PS2 instruction-level trace](docs/V0.4-PS2-CHEAT-TRACE-2026-10-22.md) · [Probe and verification](tools/cheat-seq-test/).

**v0.4 health-refill candidate — October 22, 2026:** a separate clean-retail build adds full healing to the original six-slot health cheat. Independent review passes 352 retail/patched callback comparisons (704 executions), with the built ISO hash and executable bytes verified. **Console testing remains pending.** The wrapped-PowerShell-error harness bug is fixed; eight message tests and all 14 patcher fixtures pass. [Review and corrected UI-flow details](docs/V0.4-HEALTH-REFILL-REVIEW-2026-10-22.md) · [Candidate and tests](tools/health-refill-test/). Stable v0.3 is unchanged; this is not a combined HealthMenu-plus-refill release.

**Current owner-tested candidate — October 22, 2026:** a separate **live HP display** adds the current health integer beside row 4's Damage toggle. It passed 6,656 menu instruction cases, 36 existing pointer-guard cases and 41 health-readout cases. **PS3 hardware checks now confirm** HP3→HP1 after two hits, HP2 after recovery, Damage 0 protection, restoration of damage with Damage 1, HP3 after restart and after reaching level 2, and owner-reported continued operation of the existing controls. These are owner reports, not independently captured traces; other PS2 hardware and emulators remain untested. [Console results](docs/HEALTH-MENU-CONSOLE-VALIDATION-2026-10-22.md). [HP patcher and tests](tools/health-menu/) · [Retail evidence and checks](docs/HEALTH-MENU-2026-10-22.md).

**Working baseline — October 22, 2026:** a separate **four-row damage-menu test** adds a reversible retail damage-flag control at 0x007ABB20. It passed 6,656 menu instruction cases, 36 pointer-guard cases and 96 focused retail health-decrement cases; the full ISO differs by 388 bytes within the intended windows. **Owner report: “it works fine” on the established CFW PS3 setup.** This confirms basic reported success; separate damage-off/damage-on observations and broader hazard/transition coverage were not described. [Patcher and tests](tools/damage-menu/) · [Retail evidence and test instructions](docs/DAMAGE-MENU-2026-10-22.md). The owner-tested three-row menu is preserved as the fallback.

**Previous milestone — October 22, 2026:** the owner reports that the real music pause/resume test **worked** on the CFW PS3. A new **three-row custom debug-menu ISO** now adds guarded XYZ and scene/controller diagnostics while retaining that music control and Select hide/show. It passes 4,992 instruction cases, 36 pointer-guard cases, a 12-step sequence, and a full-image comparison showing 656 changed bytes in five intended windows. **The owner subsequently reported “it worked fine” for the expanded menu on the established CFW PS3 setup.** This records basic reported success; individual feature and transition coverage were not separately described. [Tools and controls](tools/debug-menu/) · [Implementation, hashes and first-console-test receipt](docs/EXPANDED-DEBUG-MENU-2026-10-22.md). This remains a custom interface; original developer-menu restoration is unconfirmed.

| Work | Status |
| --- | --- |
| Identify the PS2 USA release | Actual USA disc inspected: SLUS_209.04; executable and source ISO hashed. |
| Research existing controller cheats | Original cheat input traced; modified Patrick Caveman sequence owner-tested successfully on PS3 in isolated v0.4 probe. |
| Search prototype sources | Hidden Palace, Internet Archive metadata, auction records, and indexed forum results searched. |
| Verify an actual PS2 prototype | An August 31, 2004 test disc is documented by Heritage Auctions. No verified public dump located in this search. |
| Check Wayback Machine | Targeted ASSEMblergames CDX request returned HTTP 503. Archived forum coverage remains incomplete. |
| Obtain the working ISO | Actual Movie USA ISO found locally and inspected on October 21, 2026. |
| Inspect executable and assets | Executable and INI inspected; retained debug-display path traced. Menu asset investigation continues. |
| Custom debug panel | Basic display, row selection, test-value changes and Select hide/show confirmed by owner report. Original developer-menu restoration remains unconfirmed. |
| Patches | Overlay, Select toggle, first custom panel and music pause/resume owner-confirmed; expanded three-row menu now reported working by the owner; extended stability remains unverified. |

## Prototype findings

- **PS2, August 31, 2004 test build:** [Heritage Auctions, lot 79058](https://comics.ha.com/itm/video-games/other/the-spongebob-squarepants-movie-game-wata-certified-prototype-test-build-8-31-2004-the-harvey-collection-ps2-thq-2004-usa/a/44210-79058.s). The listing identifies a genuine PS2 prototype certified by Wata with the Video Game History Foundation. Sold September 7, 2023. This documents a physical disc, not an available ISO or a confirmed debug menu.
- **GameCube, November 8, 2004:** [Hidden Palace](https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Nov_8,_2004_build)) and [Internet Archive](https://archive.org/details/the-sponge-bob-square-pants-movie-nr-disc.-7z). French/Dutch localization build; Hidden Palace reports it matches the final FAH retail release. It is not a PS2 beta.
- **GameCube, November 10, 2005 compilation prototype:** [Hidden Palace](https://hiddenpalace.org/2_Games_in_1:_The_SpongeBob_SquarePants_Movie_/_Battle_for_Bikini_Bottom_(Nov_10,_2005_prototype)) and [Archive release metadata](https://archive.org/details/thq-2-in-1-spongebob-europe-prototype-2.7z). This is the Movie/Battle for Bikini Bottom compilation, not a PS2 build. Debug-menu availability is unverified.
- **Game Boy Advance prototype:** [Hidden Palace](https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Prototype)) and [Internet Archive](https://archive.org/details/TheSpongeBobSquarePantsMovieGBABetaUSA). This is a different game implementation. GBA Beta 2 debug codes, including those on [GameHacking.org game 6058](https://gamehacking.org/game/6058), must not be presented as PS2 codes.

No verified publicly downloadable PS2 prototype was found in the searches completed so far. This does not establish that none exists. Forum and Wayback research is incomplete.

## PS2 button cheats

**Status: original cheat handler traced; one isolated sequence replacement owner-tested successfully on PS3 (v0.4 development).**

Source: [GameFAQs PS2 cheats](https://gamefaqs.gamespot.com/ps2/920196-the-spongebob-squarepants-movie/cheats).

Pause the game and hold **L1 + L2 + R1 + R2** while entering a sequence.

| Effect | Sequence |
| --- | --- |
| All moves | Square, Square, Circle, Square, Circle, Circle, Square, Square |
| All moves upgraded to Macho | Square, Square, Circle, Square, Circle, Circle, Square, Circle |
| Six health slots | Circle, Circle, Circle, Circle, Square, Circle, Square, Circle |
| Double Manliness | Circle, Circle, Square, Square, Circle, Square, Square, Circle |
| Caveman SpongeBob | Square, Square, Square, Square, Circle, Square, Square, Square |
| Goofy Goober Patrick | Square, Square, Square, Square, Circle, Square, Circle, Square |

These are original retail cheat sequences, not evidence of a developer debug menu. **On the isolated v0.4 CheatSeq-TEST ISO only**, Patrick Caveman's original `Square ×4, Circle, Square, Circle ×2` is replaced by `Square ×6, Circle ×2`. This does not modify the v0.3 release. Record region and observed behavior when testing.

## Next steps

**Active v0.4 milestone plan:** [View the v0.4 roadmap](docs/V0.4-ROADMAP.md). Stable v0.3 is preserved; v0.4 is not a published release. The first original-cheat probe has passed owner-reported PS3 testing, but a combined HealthMenu+cheat build remains untested.

1. Test the separate HealthMenu-TEST: compare HP against ordinary damage and pickups, then check all four controls and transitions. Preserve the owner-reported working DamageMenu-TEST and the three-row fallback.
2. Use the verified USA executable/hash baseline in [the debug-path receipt](docs/DEBUG-PATH-2026-10-21.md).
3. Inspect executable strings and code references for debug menus, development flags, cheat handlers, and disabled features.
4. Inspect HIP/HOP assets for unused UI and development content; compare relevant prototypes where useful.
5. Continue targeted forum and Wayback research around the August 31, 2004 disc and other documented builds.
6. Test candidate changes in PCSX2, documenting original bytes, patched bytes, addresses, game CRC, activation steps, and results.

---

## Progress Chart

| Task | Progress | Evidence |
| --- | --- | --- |
| Project scope | ✅ Defined | Debug menu, cheats, development features, and unused content |
| PS2 prototype identification | ✅ Documented | August 31, 2004 test disc auction record |
| Public PS2 prototype search | 🔄 In progress | No verified public dump located so far |
| Forum and Wayback research | 🔄 In progress | Archive coverage incomplete; CDX request returned HTTP 503 |
| Controller cheat verification | ✅ First isolated v0.4 probe passed | Owner reported modified Square/Circle cheat successful on PS3; not integrated into v0.3 |
| Working ISO access | ✅ Inspected | USA ISO, executable and INI verified locally |
| Executable and asset inspection | 🔄 In progress | Retained debug path traced; full menu investigation pending |
| Original developer-menu activation | ⏳ Pending | Custom panel works by owner report; original menu not recovered |
| Hardware validation | 🔄 In progress | Overlay, Select toggle, basic custom panel and music owner-confirmed; expanded menu also reported working; detailed diagnostic coverage and broader modes/stability remain unverified |

**Legend:** ✅ Documented or defined · 🔄 In progress · ⏳ Pending

## Tools

**Historical v0.2 toolset:** [release notes](releases/v0.2/RELEASE_NOTES.md) · [all seven stages and quick start](tools/README.md). The update fixes hashing compatibility and incomplete output handling, adds manifest checks and includes the new experimental HP readout. v0.1 remains available unchanged.

**Stable v0.3 baseline:** [live HP patcher](tools/health-menu/) — adds the current health number beside Damage; owner-reported console tests passed. **v0.4 research probe:** [original cheat-sequence replacement](tools/cheat-seq-test/) owner-tested separately on PS3; not yet integrated into HealthMenu.

**Owner-tested damage baseline:** [four-row damage-menu patcher](tools/damage-menu/) adds Damage 1/0 to the existing controls; the owner reports this build works fine on the established CFW PS3 setup; detailed hazard and transition coverage remains open. [Build and retail-code evidence](docs/DAMAGE-MENU-2026-10-22.md).

**Owner-tested baseline:** [expanded debug-menu patcher](tools/debug-menu/) — three selectable rows for music, guarded XYZ, and scene/controller diagnostics. Use the matching Music-TEST input. [Build and verification receipt](docs/EXPANDED-DEBUG-MENU-2026-10-22.md). The owner reports this build worked fine on the CFW PS3; extended testing remains open.

**v0.1 retains the original four-stage toolset:** [overlay](tools/overlay/), [Select toggle](tools/select-toggle/), [custom panel](tools/debug-panel/), [music pause/resume candidate](tools/music-panel/), tests and research utilities. See [release notes and verification status](releases/v0.1/RELEASE_NOTES.md). Music audio behavior is now confirmed by owner report; extended mode/transition behavior remains unverified.

- **IndustrialPark** — HIP/HOP asset inspection and editing for the Movie console game.
- **PCSX2** — planned runtime checks for candidate cheats and debug features.

The [custom panel patcher](tools/debug-panel/) is published with input/overwrite guards, a verification receipt, and an instruction-level test runner. Its basic display and interaction are now confirmed by owner report; full game-mode coverage and extended stability remain unverified.

---

## Third-party tools and research credits

This project's **seven-stage PowerShell ISO patchers, patch manifests, test harnesses and custom debug-menu changes** are project work. The external projects below are credited for their own tools, research, or documentation; they are **not claimed as our code**. Listing a project here does not imply endorsement, collaboration, or that its binaries are distributed in this release.

| External project / creators | Credit and use |
| --- | --- |
| [Industrial Park — igorseabra4 and contributors](https://github.com/igorseabra4/IndustrialPark) | Heavy Iron HIP/HOP archive viewer and editor; game asset inspection reference ([GPL-3.0 license](https://github.com/igorseabra4/IndustrialPark/blob/master/LICENSE.md)). |
| [PCSX2 — PCSX2 contributors](https://github.com/PCSX2/pcsx2) | Open-source PS2 emulator and compatibility-testing resource; separate from our patchers ([license information](https://github.com/PCSX2/pcsx2)). |
| [The SpongeBob SquarePants Movie decompilation — bfbbdecomp contributors](https://github.com/bfbbdecomp/tssm) | GameCube-oriented decompilation, symbols and engine structures used as research references; not PS2 source code or shipped binaries ([upstream license](https://github.com/bfbbdecomp/tssm/blob/main/LICENSE)). |
| [TSSM Dolphin Toolkit — ItsPepperpot](https://github.com/ItsPepperpot/TSSM-Dolphin-Toolkit) | GameCube runtime/configuration documentation and memory research; its addresses are **not** assumed valid on PS2. |
| [Dolphin Emulator — Dolphin contributors](https://dolphin-emu.org/) | GameCube/Wii emulation ecosystem referenced by the external toolkit; not included in our release. |
| [webMAN MOD — aldostools and contributors](https://github.com/aldostools/webMAN-MOD) | PS3 homebrew launcher environment relevant to the owner's PS2-ISO testing; not distributed with our patchers. |
| [XboxArchive/hashes — its maintainers and contributors](https://github.com/XboxArchive/hashes) | Xbox game/demo file-hash manifests used for cross-build research; no Xbox executables bundled. |
| [Hidden Palace](https://hiddenpalace.org/), [Internet Archive](https://archive.org/), [Redump](https://redump.org/), [The Cutting Room Floor](https://tcrf.net/) | Preservation records and historical reference material; no disc images redistributed. |

Additional upstream credit: **Heavy Iron Studios** developed the original game; **THQ** published it. SpongeBob SquarePants and related properties belong to their respective rights holders. Community research does not imply rights-holder affiliation.

**Redistribution and licenses:** Links above point to upstream projects and their own terms. Do not copy third-party code, assets, binaries, or licensed components into this repository/release without reviewing and complying with the applicable license and attribution requirements. This project's package contains original patching tools and documentation only, not the third-party tools listed here.

## Resources

- [IndustrialPark](https://github.com/igorseabra4/IndustrialPark): HIP/HOP editor supporting the Movie console game.
- [Console game research on The Cutting Room Floor](https://tcrf.net/The_SpongeBob_SquarePants_Movie_(GameCube,_PlayStation_2,_Xbox)).
- [PS2 USA disc reference](https://psxdatacenter.com/psx2/games2/SLUS-20904.html).

## Project notes

Keep platform, region, and verification status attached to each finding. Publish research, original tools, and patches here; the working ISO and private Drive link are not included.


*The SpongeBob SquarePants Movie and associated characters belong to their respective owners. This is an independent research project.*


## Debug-path milestone — October 21, 2026

**Proven:** the actual USA PS2 image has been inspected. `displayPadDebugInfo` is parsed and gates a retained handler; a local diagnostic ISO enables it with exactly **40 changed bytes**, all in one INI comment line, leaving executable code untouched. **Unknown:** visible output and complete debug-menu restoration. `ShowMenuOnBoot=1` was already stock and is not a debug unlock. The owner subsequently reported **“it worked”** on the established CFW PS3 setup. The exact visible overlay behavior remains unspecified; this is not confirmation of a complete debug menu.

[Read the full evidence, addresses, hashes, limitations, and test steps](docs/DEBUG-PATH-2026-10-21.md).


### Hardware report — October 21, 2026

The owner reports that the controller-debug probe **worked** in the CFW PS3 testing context. This records the owner's result; a screenshot or detailed description is still needed to distinguish successful boot from visible debug output. **Full developer-menu restoration remains unconfirmed.** [Hardware report and evidence](docs/DEBUG-PATH-2026-10-21.md#owner-hardware-report--october-21-2026).


### Visible overlay confirmed; interactive-toggle experiment

The owner explicitly confirms that the **controller/status overlay appeared** on the CFW PS3. The always-on display is therefore hardware-confirmed by owner report. A separate **custom Select-toggle candidate** now passes 20 instruction-level cases, full-ISO change-boundary verification, and patcher input/overwrite guards; **its console behavior is not yet tested**. Full original developer-menu restoration remains unconfirmed. [Evidence and next test](docs/DEBUG-PATH-2026-10-21.md#overlay-confirmed-select-toggle-candidate--october-21-2026).


### Select overlay toggle — hardware-confirmed by owner report

After testing the supplied toggle ISO and Select hide/show instructions, the owner reported **“it worked.”** Both the controller/status overlay and its custom Select on/off control are now confirmed by owner report on the established CFW PS3 setup. This confirms the basic reported interaction, not all game modes or extended stability. **Full original developer-menu restoration remains unconfirmed.** [Hardware test receipt](docs/DEBUG-PATH-2026-10-21.md#select-toggle-hardware-report--october-21-2026).


## Debug-All expansion and PC handoff — October 21, 2026

The existing hardware-confirmed overlay/SELECT-toggle baseline is preserved. A new [Debug-All research and PC handoff](docs/DEBUG-ALL-PC-HANDOFF-2026-10-21.md) inventories candidate config-based debug functionality and a staged verification/test plan. These additional GameCube-documented INI controls are **not yet verified on PS2**; no new runtime patch or full developer menu is claimed.
