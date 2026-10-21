# The SpongeBob SquarePants Movie — PS2 cheat and debug research

Research for the 2004 Heavy Iron Studios console game, focused on PlayStation 2. Last updated: October 21, 2026.

## Goal

Find and verify cheat codes, investigate whether a debug menu can be restored or enabled, and identify other useful development features and unused content. Research prototype, beta, review, and demo builds where evidence is available.

Free camera and level selection are outside the current requested scope. This is a separate project from Creature from the Krusty Krab.

## Current progress

| Work | Status |
| --- | --- |
| Identify the PS2 USA release | SLUS-20904; executable expected as SLUS_209.04. The user's actual disc has not been inspected. |
| Research existing controller cheats | Published PS2 button sequences located; not yet tested by this project. |
| Search prototype sources | Hidden Palace, Internet Archive metadata, auction records, and indexed forum results searched. |
| Verify an actual PS2 prototype | An August 31, 2004 test disc is documented by Heritage Auctions. No verified public dump located in this search. |
| Check Wayback Machine | Targeted ASSEMblergames CDX request returned HTTP 503. Archived forum coverage remains incomplete. |
| Obtain the working ISO | User reports the ISO is on Google Drive. Exact link/file ID is still needed; Drive discovery did not locate it. |
| Inspect executable and assets | Pending ISO access. |
| Enable and test a PS2 debug menu | Not achieved; no working PS2 debug-menu patch is claimed. |
| Release cheats or patches | No project-tested patch or release yet. |

## Prototype findings

- **PS2, August 31, 2004 test build:** [Heritage Auctions, lot 79058](https://comics.ha.com/itm/video-games/other/the-spongebob-squarepants-movie-game-wata-certified-prototype-test-build-8-31-2004-the-harvey-collection-ps2-thq-2004-usa/a/44210-79058.s). The listing identifies a genuine PS2 prototype certified by Wata with the Video Game History Foundation. Sold September 7, 2023. This documents a physical disc, not an available ISO or a confirmed debug menu.
- **GameCube, November 8, 2004:** [Hidden Palace](https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Nov_8,_2004_build)) and [Internet Archive](https://archive.org/details/the-sponge-bob-square-pants-movie-nr-disc.-7z). French/Dutch localization build; Hidden Palace reports it matches the final FAH retail release. It is not a PS2 beta.
- **GameCube, November 10, 2005 compilation prototype:** [Hidden Palace](https://hiddenpalace.org/2_Games_in_1:_The_SpongeBob_SquarePants_Movie_/_Battle_for_Bikini_Bottom_(Nov_10,_2005_prototype)) and [Archive release metadata](https://archive.org/details/thq-2-in-1-spongebob-europe-prototype-2.7z). This is the Movie/Battle for Bikini Bottom compilation, not a PS2 build. Debug-menu availability is unverified.
- **Game Boy Advance prototype:** [Hidden Palace](https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Prototype)) and [Internet Archive](https://archive.org/details/TheSpongeBobSquarePantsMovieGBABetaUSA). This is a different game implementation. GBA Beta 2 debug codes, including those on [GameHacking.org game 6058](https://gamehacking.org/game/6058), must not be presented as PS2 codes.

No verified publicly downloadable PS2 prototype was found in the searches completed so far. This does not establish that none exists. Forum and Wayback research is incomplete.

## Published PS2 controller cheats — awaiting local testing

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

1. Obtain the exact Drive link for the Movie PS2 ISO.
2. Identify the disc serial, region, executable, and hashes before proposing patches.
3. Inspect executable strings and code references for debug menus, development flags, cheat handlers, and disabled features.
4. Inspect HIP/HOP assets for unused UI and development content; compare relevant prototypes where useful.
5. Continue targeted forum and Wayback research around the August 31, 2004 disc and other documented builds.
6. Test candidate changes in PCSX2, documenting original bytes, patched bytes, addresses, game CRC, activation steps, and results.

## Research tools and references

- [IndustrialPark](https://github.com/igorseabra4/IndustrialPark): HIP/HOP editor supporting the Movie console game.
- [Console game research on The Cutting Room Floor](https://tcrf.net/The_SpongeBob_SquarePants_Movie_(GameCube,_PlayStation_2,_Xbox)).
- [PS2 USA disc reference](https://psxdatacenter.com/psx2/games2/SLUS-20904.html).

Keep platform, region, and verification status attached to each finding. Publish research, original tools, and patches here; the working ISO and private Drive link are not included.
