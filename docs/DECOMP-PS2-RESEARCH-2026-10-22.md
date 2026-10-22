# SpongeBob Movie — decomp and PS2 research, 2026-10-22

- Audience: owner and future PS2 patch contributors.
- Scope: sources for expanding the custom debug panel in USA retail SLUS_209.04.
- Success condition: identify concrete, attributable leads and validate candidates against the retail executable before changing a game image.

## Rundown

The research provides a path to more diagnostic rows and better references for the original tweak system. It does not recover an original Movie developer menu. No new ISO patch was made during this research.

The most immediately actionable result is a retail text-variable table linking PlayerPosition, CurrentScene, and CurrentLevel to formatter functions. A position display should be investigated before invasive camera or progression controls.

## Current state

| Class | Finding | Evidence and limit |
| --- | --- | --- |
| Proven | Movie's public header defines typed tweak values, callbacks, and xDebugModeAdd. | [Movie xDebug.h](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/src/SB/Core/x/xDebug.h). Declarations are not a menu implementation. |
| Proven | Related BFBB xDebugModeAdd returns -1; the checked duplotron branch also has empty debug entry points. | [BFBB branch source](https://github.com/joeyballentine/bfbb/blob/duplotron/src/SB/Core/x/xDebug.cpp), checked 2026-10-22. This is not proof of Movie retail behavior. |
| Proven | The Jan 18, 2006 Ratatouille prototype project documents DEBUG, RELEASE, MASTERDEBUG and MASTER variants, plus richer tweak declarations. | [README](https://github.com/seilc/rat/blob/3ebb77239aa38294f841c7d23dff41fea6aadfa8/README.md), [xDebugTweak.h](https://github.com/seilc/rat/blob/3ebb77239aa38294f841c7d23dff41fea6aadfa8/src/rt/Engine/Core/x/xDebugTweak.h). xDebug and xDebugTweak remain NonMatching in configure.py; checked .cpp paths were absent. |
| Proven | PS2SDK raw button constants and Movie engine button constants differ. | Raw Select 0x1 / Cross 0x4000; engine Select 0x2 / X 0x10000. See sources below. |
| Inference | Prototype tweak definitions can guide our custom panel's row and callback design. | Similar named structures; different title, build, CPU and layouts prevent a direct binary transplant. |
| Unknown | A complete original developer menu survives and can be enabled in this retail build. | No enabling switch or complete implementation established. |
| Unknown | New text formatters are safe throughout title, loading, gameplay and transitions. | Static references and code inspected; no new runtime test. |

## Retail evidence

Input executable: 5,467,144 bytes.
SHA-256: `2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956`.

An aligned direct-pointer scan of the exact NUL-terminated names found the following candidate table entries. The table stores a name pointer, a length, and then a function pointer.

| Name | Name-pointer slot | Candidate formatter |
| --- | --- | --- |
| PlayerPosition | 0x005FDEA4 | 0x002E0690 |
| CurrentScene | 0x005FDDB4 | 0x002E0720 |
| CurrentLevel | 0x005FDDA8 | 0x002E0770 |
| SoundMusicVolume | 0x005FDED4 | 0x002E0470 |
| SoundFXVolume | 0x005FDEC8 | 0x002E0510 |

PlayerPosition code dereferences a GP-relative root, then offsets 0x80C and 0x48, reads three floats at 0x30/0x34/0x38, converts them to integers, calls the existing formatter, and returns a static buffer at 0x0067FF70. There are no null checks on that pointer chain in the inspected function. Do not call it unconditionally from a panel visible at boot.

CurrentScene also dereferences a scene pointer. CurrentLevel performs a scene lookup and returns text. Runtime lifetimes and correct game-state guards must be established before adding these to the panel.

The public DWARF listing labels PlayerPosition at 0x002E0800, while the retail name table points at 0x002E0690. This concrete discrepancy shows why importing addresses without validation is unsafe. [DWARF listing](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/dwarf/SB04_Multi_Sku/Engine/Game/zVar.cpp).

## PS2 documentation and practical implications

- [PS2SDK libpad](https://github.com/ps2dev/ps2sdk/blob/329e2bb43287e16af16c4dde1c614e2662c24468/ee/rpc/pad/include/libpad.h) documents raw button bits, state and buffers. [Movie xPad.h](https://github.com/bfbbdecomp/tssm/blob/50ea01767e4c894f09db8ff2f4e52136a6e89ca4/src/SB/Core/x/xPad.h) describes the engine's processed on/pressed/released fields. Use engine pressed events for one toggle per press and preserve the existing input path.
- [PS2SDK register compatibility header](https://github.com/ps2dev/ps2sdk/blob/329e2bb43287e16af16c4dde1c614e2662c24468/common/include/as_reg_compat.h) explicitly distinguishes register aliases across ABIs. Record physical register numbers when checking instructions. Do not assume a disassembler's t0/a4 naming convention establishes the retail compiler ABI.
- [PS2SDK kernel header](https://github.com/ps2dev/ps2sdk/blob/329e2bb43287e16af16c4dde1c614e2662c24468/ee/kernel/include/kernel.h) defines separate data writeback and instruction-cache invalidation operations. A future runtime code patch needs cache handling; this does not establish a defect in the current pre-boot ISO patch method.
- [Sony/SCEE PS2 Programming Optimisations, George Bain, AGDC 2002](https://lukasz.dk/files/PS2Optimisations.pdf) covers EE caches, DMA alignment and graphics-path synchronization. Practical inference: continue using the game's working text rendering path rather than adding an independent GS/DMA overlay without synchronization work.

## Other useful public research

[ItsPepperpot's TSSM Dolphin Toolkit](https://github.com/ItsPepperpot/TSSM-Dolphin-Toolkit/blob/b5539106dbdebc17843d05f397e0a6508da28366/README.md) documents health, upgrades, camera settings and built-in text variables. Its GameCube addresses are references to behavior, not PS2 patch addresses. It also distinguishes static position copies from the live player position; writing a display copy is not teleportation.

## Next step and limits

1. Establish a retail game-state/player/scene guard for a read-only position and scene display.
2. Preserve register/stack behavior and prove that invalid or absent pointers bypass the formatter.
3. Test boot, title, loading, gameplay, death, character changes and level transitions before calling the display hardware-tested.
4. Keep the existing music candidate separate until the owner verifies real audio pause/resume.

The music test remains hardware-unverified. Decompilation progress percentages and debug symbols do not establish that the game's original debug menu exists.


## RenderWare documentation follow-up

The Discord resources channel links a RenderWare 3.5 API Reference for PS2 archive. The linked CDN page returned “This content is no longer available” on 2026-10-22; its contents were not inspected.

Useful available replacements:

- [EA's RenderWare3Docs](https://github.com/electronicarts/RenderWare3Docs) contains publisher-released user guides and white papers. Its README specifies the PC release; treat common API explanations as references, not exact PS2 binary layouts.
- [PS2/Sky2 rwplcore.h](https://github.com/sigmaco/rwsdk-v3.5-ps2/blob/82a98fe97a6346388e27e0c73068fc326109de68/rwsdk/include/sky2/rwplcore.h) in a preserved 3.5 reference mirror declares the platform's 2D immediate-mode rendering API.
- [Criterion's metrics overlay sample](https://github.com/sigmaco/rwsdk-v3.5-ps2/blob/82a98fe97a6346388e27e0c73068fc326109de68/shared/skel/metrics.c) draws an alpha-blended box and text, changes depth/texture/alpha states, and saves/restores the source/destination blend functions.

Practical inference: if our panel later gains a shaded background, inspect Movie's corresponding render-state wrappers and restore every state our hook changes. The sample's assumed exit defaults are not automatically valid for an arbitrary mid-frame retail hook. No RenderWare SDK binaries were installed, executed, or added to the tools release.
