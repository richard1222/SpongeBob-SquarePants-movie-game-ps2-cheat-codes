# Debug-All research and PC handoff — 2026-10-21

## Scope and status

Target: **The SpongeBob SquarePants Movie (2004), USA PS2, SLUS_209.04**. This is not Creature from the Krusty Krab. Owner wants a broad debug interface, beyond the already-working pad overlay. Preserve the working PS3 build.

**Hardware reported working:** controller/status overlay and custom SELECT hide/show toggle on owner's CFW PS3. Evidence and SHA-256 are in [DEBUG-PATH-2026-10-21.md](DEBUG-PATH-2026-10-21.md). This does **not** prove an original retail developer menu exists or has been restored.

**No new ISO, PS2 binary patch, or runtime test was made in this handoff.** The connected GitHub repository is the handoff location; a separate PC chat/session can read it, but it is not automatically running or receiving a direct message.

## New research lead: documented SB04.INI tuning surface

The community [TSSM Dolphin Toolkit](https://github.com/ItsPepperpot/TSSM-Dolphin-Toolkit) catalogs game-config keys on GameCube, which may indicate corresponding functionality on PS2. **Treat every key below as unverified for PS2 until located in the actual PS2 executable / INI and tested.** Do not copy GameCube runtime addresses to PS2.

| Category | Candidate INI keys from GameCube toolkit | What to inspect |
| --- | --- | --- |
| Abilities | `G.KarateSpin`, `G.Bash`, `G.MachoBowl`, `G.WaveGuitar`, `G.BellyBump`, `G.Cartwheel`, `G.BellyFlop`, `G.Throw` | Parser references, upgrade states 0/1/2; gameplay effects |
| Health | `G.HealthSB`, `G.HealthPat` | Bounds, UI cap, save interactions |
| Gameplay | `G.Gravity`, `G.TakeDamage`, `G.DamageTimeHit` | Whether parser accepts safe toggles, level reset needed |
| Presentation | `NoMusic`, `NoCutscenes`, `NoPadCheck`, `AsyncLoadingScreen` | Debug/troubleshooting value; check defaults |
| Speed | `SB.JumpGravity` | Controlled physics experiment without modifying working baseline |
| Startup | `BOOT` | DO NOT change until valid HIP area names/loader behavior confirmed; arbitrary values can crash |
| Existing proven PS2 path | `displayPadDebugInfo` | Already traced in retail ELF and confirmed visually by owner report |

Toolkit also documents `G.AttractModeDuringGameplay`, `G.ShinyValuePurple`, `G.ShinyValueBlue`, `G.ShinyValueGreen`, `G.ShinyValueYellow`, `G.ShinyValueRed`, and `Upgrade1`–`Upgrade14`. These are *candidate configuration controls*, not proof of a hidden UI.

## Implementation approach

1. **Lock verified baseline.** Record source USA ISO hash `c0494ad78fab34dc19fb52b831facb1b27500e66bf0a57a77e627e7b805096f0`; successful SELECT-toggle candidate hash `78b5b1530a179ad25a2e06167b24aacc369977d57fcdc9b0433d0f7b120303f7`. Create new outputs, never overwrite either baseline.
2. **Inventory configuration.** Extract `SB04.INI` from owner's disc and make a table of exact key names, values, placement, and byte lengths. Run strings/xrefs on USA `SLUS_209.04` for every candidate key. Separate `present in stock INI`, `ELF parser xref proven`, and `GameCube-only hypothesis`.
3. **Build one safe experiment at a time.** Prefer same-length INI edits when possible, no executable changes; verify changed-byte offsets remain entirely inside intended INI span, and hashes change as expected. Make separate candidate outputs, retain manifest and rollback.
4. **Define 'Debug-All' as a CUSTOM menu if original UI is absent.** Reuse verified input structure and surviving display routine. First prototype a simple on/off or mode-cycling overlay. Add options only after safe memory address, parser, and game-mode update frequency are proved. Do not mislabel this as a recovered original developer menu.
5. **Resolve SELECT conflicts.** Current toggle reads pressed mask from controller at `0x007AB520 + 0x30`, tests bit `0x2`, toggles flag `0x006378F8`, and calls display handler `0x004A9160` via patched function at `0x00403BB0`. Investigate press-edge handling/debounce and input conflicts before adding more shortcuts.
6. **Test matrix.** Title screen, normal gameplay, sliding, driving, pauses, death/respawn, level transition, save/load, and repeated rapid SELECT presses. Log result, build SHA, observed visual change and crashes.
7. **Menu archaeology.** Check surviving stubs `0x00403B70/80/90/A0/F0` and xrefs; inventory `MN*` HIP/HOP at asset level (not just ASCII), and investigate hashed names/code-built menus. Do not assume stripped functions can be recovered from GameCube addresses.

## Evidence handling

- PS2 confirmed: owner-reported SELECT toggle and display, retail ELF/INI analysis as recorded in existing debug-path receipt.
- GameCube documented: INI key catalog in third-party toolkit. Portability to this PS2 build **unverified**.
- Upstream [bfbbdecomp/tssm](https://github.com/bfbbdecomp/tssm) is a **GameCube** decompilation, not directly buildable PS2 source; use structures and symbols as leads only.
- No newly generated menu, cheat code, PS2 ISO, or patch has yet passed hardware testing.

## Handoff to PC counterpart

Open this document and the existing debug-path receipt in this GitHub repository. Continue with owner's locally available extracted ISO, ELF, and patcher; these are not accessible through this mobile chat's container. Produce a **small verified patcher**, diff receipt, and candidate ISO *on PC* only after confirming local source hashes; never commit proprietary ISOs, ELF files, or assets. Report each step to GitHub with verified/unverified status.

## Research sources

- [Project debug-path hardware receipt](DEBUG-PATH-2026-10-21.md)
- [GameCube community memory/config toolkit](https://github.com/ItsPepperpot/TSSM-Dolphin-Toolkit)
- [GameCube work-in-progress TSSM decomp](https://github.com/bfbbdecomp/tssm)
