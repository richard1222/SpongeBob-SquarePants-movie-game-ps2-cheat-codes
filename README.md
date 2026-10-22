![Platform](https://img.shields.io/badge/Platform-PS2-blue)
![Region](https://img.shields.io/badge/Target_Region-USA-green)
![Serial](https://img.shields.io/badge/Target_Serial-SLUS__209.04-orange)
![Status](https://img.shields.io/badge/Status-Research_in_progress-yellow)

# The SpongeBob SquarePants Movie (PS2) — cheats and debug research

Research for the 2004 Heavy Iron Studios console game, focused on PlayStation 2. Last updated: October 21, 2026.

---

## Table of Contents

- [Project Goal](#project-goal)
- [Current Status](#current-status)
- [Prototype Findings](#prototype-findings)
- [PS2 Button Cheats](#ps2-button-cheats)
- [Next Steps](#next-steps)
- [Progress Chart](#progress-chart)
- [Tools](#tools)
- [Resources](#resources)
- [Project Notes](#project-notes)

---

## Project goal

Find and verify cheat codes, investigate whether a debug menu can be restored or enabled, and identify other useful development features and unused content. Research prototype, beta, review, and demo builds where evidence is available.

Free camera and level selection are outside the current requested scope. This is a separate project from Creature from the Krusty Krab.

## Current status

**Latest — October 22, 2026:** the overlay and Select toggle are confirmed by owner hardware reports. A custom panel with one selectable test row is ready for console testing: **192 instruction cases and a nine-step sequence passed**, but rendering and full-game integration remain unverified. [Panel implementation, patcher, evidence, and test steps](docs/DEBUG-PANEL-2026-10-22.md). This is a custom interface; original developer-menu restoration remains unconfirmed.

| Work | Status |
| --- | --- |
| Identify the PS2 USA release | Actual USA disc inspected: SLUS_209.04; executable and source ISO hashed. |
| Research existing controller cheats | Published PS2 button sequences located; not yet tested by this project. |
| Search prototype sources | Hidden Palace, Internet Archive metadata, auction records, and indexed forum results searched. |
| Verify an actual PS2 prototype | An August 31, 2004 test disc is documented by Heritage Auctions. No verified public dump located in this search. |
| Check Wayback Machine | Targeted ASSEMblergames CDX request returned HTTP 503. Archived forum coverage remains incomplete. |
| Obtain the working ISO | Actual Movie USA ISO found locally and inspected on October 21, 2026. |
| Inspect executable and assets | Executable and INI inspected; retained debug-display path traced. Menu asset investigation continues. |
| Enable and test a PS2 debug menu | Not achieved; no working PS2 debug-menu patch is claimed. |
| Patches | Owner-tested overlay/Select toggle; custom panel patcher published for hardware testing. |

## Prototype findings

- **PS2, August 31, 2004 test build:** [Heritage Auctions, lot 79058](https://comics.ha.com/itm/video-games/other/the-spongebob-squarepants-movie-game-wata-certified-prototype-test-build-8-31-2004-the-harvey-collection-ps2-thq-2004-usa/a/44210-79058.s). The listing identifies a genuine PS2 prototype certified by Wata with the Video Game History Foundation. Sold September 7, 2023. This documents a physical disc, not an available ISO or a confirmed debug menu.
- **GameCube, November 8, 2004:** [Hidden Palace](https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Nov_8,_2004_build)) and [Internet Archive](https://archive.org/details/the-sponge-bob-square-pants-movie-nr-disc.-7z). French/Dutch localization build; Hidden Palace reports it matches the final FAH retail release. It is not a PS2 beta.
- **GameCube, November 10, 2005 compilation prototype:** [Hidden Palace](https://hiddenpalace.org/2_Games_in_1:_The_SpongeBob_SquarePants_Movie_/_Battle_for_Bikini_Bottom_(Nov_10,_2005_prototype)) and [Archive release metadata](https://archive.org/details/thq-2-in-1-spongebob-europe-prototype-2.7z). This is the Movie/Battle for Bikini Bottom compilation, not a PS2 build. Debug-menu availability is unverified.
- **Game Boy Advance prototype:** [Hidden Palace](https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Prototype)) and [Internet Archive](https://archive.org/details/TheSpongeBobSquarePantsMovieGBABetaUSA). This is a different game implementation. GBA Beta 2 debug codes, including those on [GameHacking.org game 6058](https://gamehacking.org/game/6058), must not be presented as PS2 codes.

No verified publicly downloadable PS2 prototype was found in the searches completed so far. This does not establish that none exists. Forum and Wayback research is incomplete.

## PS2 button cheats

**Status: published sequences located; local testing pending.**

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

These are published cheat sequences, not evidence of a developer debug menu. Record region and observed behavior when testing.

## Next steps

1. Test the custom panel candidate on the owner's CFW PS3: selection, OFF/ON display, and Select hide/show.
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
| Controller cheat verification | ⏳ Pending | Published sequences collected; not tested here |
| Working ISO access | ✅ Inspected | USA ISO, executable and INI verified locally |
| Executable and asset inspection | 🔄 In progress | Retained debug path traced; full menu investigation pending |
| Debug menu activation | ⏳ Pending | No working patch verified |
| Hardware validation | 🔄 In progress | Overlay and Select toggle owner-confirmed; custom panel console test pending |

**Legend:** ✅ Documented or defined · 🔄 In progress · ⏳ Pending

## Tools

- **IndustrialPark** — HIP/HOP asset inspection and editing for the Movie console game.
- **PCSX2** — planned runtime checks for candidate cheats and debug features.

The [custom panel patcher](tools/debug-panel/) is published with input/overwrite guards, a verification receipt, and an instruction-level test runner. Its console behavior is not yet confirmed.

---

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
