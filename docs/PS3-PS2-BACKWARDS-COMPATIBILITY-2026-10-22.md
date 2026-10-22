# PS3 PS2-backwards-compatibility research — October 22, 2026

Target: The SpongeBob SquarePants Movie USA PS2, `SLUS_209.04`; owner's CECH-2001A PS3 Slim with CFW, Cobra/webMAN MOD, and owner-tested HealthMenu.

## Emulator families

- `ps2_emu.self`: CECHA/CECHB; relies on actual PS2 Emotion Engine/Graphics Synthesizer hardware.
- `ps2_gxemu.self`: CECHC/CECHE; PS2 Graphics Synthesizer hardware, emulated Emotion Engine.
- `ps2_netemu.self`: software-based PS2 Classics environment, used on models without dedicated PS2 hardware, including the owner's Slim. CFW/Cobra permits launching a PS2 ISO through this software route.

These environments are **not interchangeable proof of compatibility**. Working on the owner’s PS3 netemu does not automatically prove a patch on an original PS2, early backwards-compatible PS3 or PCSX2.

## SpongeBob-specific compatibility

PS3 Developer Wiki's PS2 Classics compatibility list records **SpongeBob SquarePants: The Movie** as Playable / PS2 Classic with an empty emulator config and warns that audio can be unsynchronized in some cutscenes. Treat this as a documented *retail-game* baseline, **not** certification of our debug-modified image.

## Files and controls

- webMAN MOD lists CFW PS2 ISO images under `/dev_hdd0/PS2ISO`; PS2 Classics `.BIN.ENC` uses a different launch/packaging path.
- Emulator-level `.ISO.CONFIG` files can sometimes address `ps2_netemu` compatibility issues. They are **not** game engine `SB04.INI` settings and do not unlock developer features by themselves.
- Do not add an emulator CONFIG to the current working HealthMenu image without identifying a real, reproducible issue. A game-specific config may alter assumptions about timing and behavior.
- To compare reports, record console model, CFW/Cobra and webMAN versions, launcher path (raw ISO versus Classics), existence/hash of a sidecar CONFIG, game serial and patched ISO SHA-256.

## Practical research implications

1. **Continue developer-feature reverse engineering in the PS2 executable and SB04.INI**; avoid treating PS3 emulator internals as game debug switches.
2. Preserve existing owner-tested HealthMenu and DamageMenu images unchanged.
3. When sound or cutscene timing differs, retest with the unmodified game under the same emulator before blaming our patch.
4. Later external testing should cover PCSX2 and actual PS2 independently; neither has been verified for the modified image.

## Sources

- PS3 Developer Wiki, PS2 Emulation: https://www.psdevwiki.com/ps3/PS2_Emulation
- PS3 Developer Wiki, PS2 Classics Emulator Compatibility List: https://www.psdevwiki.com/ps3/PS2_Classics_Emulator_Compatibility_List
- webMAN MOD Game Paths & Covers: https://github.com/aldostools/webMAN-MOD/wiki/Game-Paths-%26-Covers
- ConsoleMods, PS2 Games and Fixes: https://consolemods.org/wiki/PS3:PS2_Games,_Multiplayer,_and_Fixes
- PS2 Classics CONFIG Guide: https://ps3classics.github.io/ps2/config-guide.html

This is external documentation research plus earlier owner reports, not an inspection of the PS3 emulator binary or a new runtime test.
