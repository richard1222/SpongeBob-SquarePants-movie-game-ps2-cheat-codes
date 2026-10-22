# Multi-console prototype and archive hunt — 2026-10-22

Scope: The SpongeBob SquarePants Movie (2004), **not** another SpongeBob game. Sources searched: Internet Archive, Hidden Palace, TCRF, Heavy Iron Modding, search-indexed forum references, Reddit and Wayback Machine CDX. Focus on developer-feature research; do not equate a marketing, press, localization, or retail disc with an early debug build.

## Verified preservation records

| Platform | Build | Status | Developer-feature relevance |
| --- | --- | --- | --- |
| PS2 | August 31, 2004 test disc documented by Heritage Auctions lot 79058 | Physical prototype documented; public dump not verified | **Highest-priority lead**, predates retail; contents and developer-menu status unknown |
| GameCube | Nov 8, 2004 NR localization disc (French/Dutch) | Archive.org item `the-sponge-bob-square-pants-movie-nr-disc.-7z`; Hidden Palace says same as final FAH retail | Good for regional cross-platform comparisons; **not evidence of an early debug build** |
| GameCube | Nov 10, 2005 NPDP 2-in-1 Movie / Battle for Bikini Bottom compilation | Hidden Palace released preservation record; both games described as final builds | Lower priority for removed gameplay or early developer controls |
| GBA | iNDEPENDENT scene prototype, release record Aug 1, 2004, `ind-sbma.zip` | Hidden Palace and TCRF record; Hidden Palace internal download reports missing file | Different implementation; historical interest, do not copy codes/offsets to PS2 |
| Xbox | Original Xbox Movie game | No verified public pre-release dump found in searches recorded in this pass | Search further using Xbox review/debug-disc terminology |

## Direct sources

- PS2 prototype auction: https://comics.ha.com/itm/video-games/other/the-spongebob-squarepants-movie-game-wata-certified-prototype-test-build-8-31-2004-the-harvey-collection-ps2-thq-2004-usa/a/44210-79058.s
- GC Nov 8 preservation: https://archive.org/details/the-sponge-bob-square-pants-movie-nr-disc.-7z
- Hidden Palace GC Nov 8: https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Nov_8,_2004_build)
- Hidden Palace 2005 2-in-1: https://hiddenpalace.org/2_Games_in_1:_The_SpongeBob_SquarePants_Movie_/_Battle_for_Bikini_Bottom_(Nov_10,_2005_prototype)
- Hidden Palace GBA: https://hiddenpalace.org/The_SpongeBob_SquarePants_Movie_(Prototype)
- TCRF GBA: https://tcrf.net/Proto:The_SpongeBob_SquarePants_Movie_(Game_Boy_Advance)
- Heavy Iron Modding index: https://heavyironmodding.org/wiki/Category:The_SpongeBob_SquarePants_Movie

## Wayback and forum limitations

A targeted Wayback CDX query for archived ASSEMblergames SpongeBob discussions could not be accessed in this search environment. Searches of indexed old forums did not establish a verifiable PS2 or original Xbox dump. This is incomplete coverage, **not proof one does not exist**.

## Next research strategy

1. Locate contemporary mentions, photographs, labels, serials, and build timestamps for the August 31 PS2 test disc, and contact preservers through official public channels if appropriate.
2. Search old forums and archived pages for `SpongeBob Movie`, `THQ`, `Heavy Iron`, `SLUS 20904`, `debug`, `review disc`, `NPDP`, and `Xbox XDK`.
3. Inventory GameCube regional build files and metadata against original PS2 files *without* claiming retail localization equals beta content.
4. If a new candidate appears, verify system, executable ID, date and SHA-256; isolate from existing HealthMenu project images.
5. Avoid distributing proprietary game images in GitHub; publish only descriptive research, safe diffs, manifests, and original tools.
