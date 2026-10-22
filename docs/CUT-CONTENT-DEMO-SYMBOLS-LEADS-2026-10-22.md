# Online cut-content and beta-build follow-up — October 22, 2026

## New high-value verification lead: OPM demo debug symbols

The PS2 index at https://www.debugging.games/PlayStation%202 lists:

`[PS2] Nickelodeon SpongeBob SquarePants - The Movie (USA) (Official U.S. PlayStation Magazine Demo Disc 90, [SCUS-97442]) (DWARF).7z` (~3 MB), indexed upload January 4, 2026.

**Interpretation:** This is an indexed debugger-symbol/executable research archive associated with Official U.S. PlayStation Magazine Demo Disc 90. It is NOT evidence that a full retail-replacement beta game ISO is available; the file's archive contents and identity relative to the already examined symbol-bearing build were **not yet compared**. The developer-symbol lead is especially useful for identifying unused functionality. Compare SHA-256, ELF headers, DWARF source paths and function names before calling it a distinct build. Prior Muse findings show symbol-build and PS2 retail addresses differ, so DO NOT transplant offsets.

## Cut-content lead: Goofy Goober Dream Platforming

The console-game development article https://spongebob.fandom.com/wiki/The_SpongeBob_SquarePants_Movie_(video_game)/development records a planned **Goofy Goober Dream Platforming** level before Sundae Driving, unused related costume/enemy concept art, and **five unused objective strings** reported in game code. Secondary community evidence; not yet independently located inside the owner's PS2 `SLUS_209.04` executable.

Task for Muse: inspect retail PS2 binary and extracted menu/string files for those exact unused tasks and associated string IDs/xrefs, then inventory potential scene/HIP/HOP material. Missing level assets must not be reconstructed or claimed recoverable without evidence.

## Earlier console-game visuals and costumes

https://spongebob.fandom.com/wiki/List_of_early_versions_of_video_games describes unused costume concepts (SpongeBob including DoodleBob and Viking; Patrick including Barnacle Boy) and changes in prototype footage. These are **art/pre-release visual reports**, not proof that corresponding playable assets survive in the shipping disc.

August 25 2004 GameSpot hands-on https://www.gamespot.com/articles/the-spongebob-squarepants-movie-updated-hands-on/1100-6105652/ independently confirms an in-progress PS2 build was demonstrated, but not a released beta ISO.

## Physical / preserved build status

August 31 2004 PS2 prototype remains a documented physical disc without a verified public game image: https://comics.ha.com/itm/video-games/other/the-spongebob-squarepants-movie-game-wata-certified-prototype-test-build-8-31-2004-the-harvey-collection-ps2-thq-2004-usa/a/44210-79058.s

Hidden Palace category https://hiddenpalace.org/Category:The_SpongeBob_SquarePants_Movie_prototypes currently exposes two named entries: Nov 8 2004 GameCube localization build and GBA prototype. GBA implementation and debug codes are not transferable to PS2. Exhibition Xbox demos are recorded separately in this repository, but no byte-level downloadable XBE was found in the earlier Muse search.

## Prioritized action

1. Compare the debugging.games DWARF demo listing/metadata to the already-inspected Neptune symbol build; avoid duplicate research.
2. Hunt for and extract the five Dream Platforming objective strings from the exact retail PS2 game files, recording actual byte offsets and calling functions.
3. Match unused costume/concept-art claims to real PS2 asset identifiers and files, not just pictures.
4. Keep stable v0.3 unchanged. Conduct experiments in a separate v0.4 test image only after concrete static evidence.

No new prototype executable, ISO or cut-level asset was downloaded or tested in this research pass.
