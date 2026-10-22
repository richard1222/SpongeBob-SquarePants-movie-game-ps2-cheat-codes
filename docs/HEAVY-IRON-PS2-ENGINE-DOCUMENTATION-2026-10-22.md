# Heavy Iron Studios PS2 engine documentation research — 2026-10-22

## Findings and attribution

No verified **officially published Heavy Iron Studios PS2 internal developer manual** emerged from this targeted search. The strongest available documentation is community-produced reconstruction and tooling. The Movie's target in this project is **USA PS2 SLUS_209.04**; cross-platform source references are guides, not binary-accurate PS2 addresses.

### Technical source catalog

1. **The SpongeBob SquarePants Movie decompilation (bfbbdecomp/tssm):** https://github.com/bfbbdecomp/tssm — work-in-progress reconstruction with `src/`, `include/`, `dwarf/SB04_Multi_Sku/Engine/`, `docs/`. Project focuses on GameCube GGVE78, not a fully rebuilt PS2 retail executable. Especially useful for naming xDebug, xPad, xIni, menu and extras functions. Address layout differs from retail PS2, as already reported in the Neptune sweep.
2. **Battle for Bikini Bottom decompilation (bfbbdecomp/bfbb):** https://github.com/bfbbdecomp/bfbb — prior Heavy Iron game with shared engine structures and code patterns; not a drop-in source tree for the Movie. Community's earlier [BFBB decomp guide](https://github.com/bfbbdecomp/bfbb-decomp-guide) is an additional methodology reference.
3. **Industrial Park (igorseabra4 and contributors):** https://github.com/igorseabra4/IndustrialPark — cross-platform HIP/HOP asset viewer/editor with PS2 support, including asset inspection and modification. [Heavy Iron Modding Wiki editor documentation](https://heavyironmodding.org/wiki/Industrial_Park_(level_editor)).
4. **Industrial Park Hans:** https://github.com/igorseabra4/IndustrialParkHans — save-file editor supporting PS2 raw save formats; README notes that editing save files may require bypassing checksum checks. Treat it as a structure reference, not a safe path to modify live user saves.
5. **HIP/HOP file formats:** https://wiki.serp.co/file-types/hip/ — third-party description associates the Evil Engine with HIP asset archives and HOP level archives, alongside RenderWare. Verify implementation using Industrial Park's actual parser rather than rely on a generic file-extension site.
6. **PS2-specific crash diagnostics:** https://gamefaqs.gamespot.com/ps2/920196-the-spongebob-squarepants-movie/data — contributor trivia claims the PS2 build can present an `IOP CRASH DETECTED` screen with recently accessed files. This is **an unverified community report**, not proof that a callable debug menu exists. Avoid intentionally crashing the working v0.3 ISO.

### Historical development context

- THQ's 2004 annual report confirms Heavy Iron was developing The SpongeBob SquarePants Movie following Battle for Bikini Bottom: https://media.corporate-ir.net/media_files/irol/96/96376/THQ_AR.pdf
- GameSpot August 25, 2004 documented an in-progress PS2 showing: https://www.gamespot.com/articles/the-spongebob-squarepants-movie-updated-hands-on/1100-6105652/

## What Muse should actually do on Neptune

1. Match PS2 retail ELF call patterns around known `displayPadDebugInfo`, `xPad`, menu CHEAT_SUCCESS/CHEAT_FAILED and `G.Cheat*` key handling against GameCube reference functions by behavior or signatures, **not addresses**.
2. Identify error/IOP crash handler strings and call sites in the retail ELF. Classify as reachable via normal error paths, dormant, or absent. Do not trigger a crash on the owner's PS3.
3. Inventory HIP/HOP assets for unused Function/Cheat extras and Dream Platforming mission strings. Correlate archive asset IDs and executable references; asset existence is not runtime proof.
4. Record exact PS2 ELF/ISO SHA-256, function locations, original bytes and confidence levels. All experiments must branch from v0.3 into separate versioned files.
5. Avoid Free Camera and level selection, and never claim original developer-menu restoration without runtime evidence.

## Boundaries

External tools, wiki pages, and decompilation authors retain their own attribution and licenses; none are presented as original project code. No copyrighted ISO, ELF, third-party SDK, or proprietary assets are committed in this research file.
