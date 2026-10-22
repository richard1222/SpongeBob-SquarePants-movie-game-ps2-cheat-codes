# PS3 Slim / Sony PS2 software-emulation documentation — 2026-10-22

Target hardware: owner PS3 Slim **CECH-2001A**, CFW/Cobra, webMAN MOD, PS2 Movie `SLUS_209.04` inside **ps2_netemu**. Scope: v0.4 research and correct testing method; not a patch to v0.3.

## Confirmed emulator architecture

[PS3 Developer Wiki — PS2 Emulation](https://www.psdevwiki.com/ps3/PS2_Emulation) distinguishes:
- `ps2_emu.self` on early CECH-A/B with PS2 EE/GS chips;
- `ps2_gxemu.self` on some CECH-C/E models with hardware GS;
- `ps2_netemu.self` on subsequent models (including our Slim), using full software emulation and designed for digital PS2 Classics.

The emulator operates at the hypervisor/guest-OS level rather than as an ordinary PS3 application. This makes generic LV2/PS3 process patches or PS3 cheat-engine assumptions unsafe for the PS2 game. The existing ISO patcher's static MIPS/PS2 game-file changes remain the direct supported approach.

## Binary per-game CONFIG files

[PS3 Developer Wiki — PS2 Config Commands](https://www.psdevwiki.com/ps3/PS2_Emulation/PS2_Config_Commands), [official config catalog](https://www.psdevwiki.com/ps3/PS2_Classics_Configuration_Files_%28Official%29) and [PS2 Classics CONFIG Guide](https://ps3classics.github.io/ps2/config-guide.html): ps2_netemu supports optional external binary configs for emulator-environment changes, performance and some game fixes; documentation gives max **16384 bytes** for external config. A commonly used version header starts `3D 00 00 00`, and command `0x3D` stores config revision. CONFIG support depends on installed emulator/firmware revision. A config does not conjure up cut content, original dev menu, or missing GG01.

**Action:** inventory existing game-specific configs before generating anything. If owner-tested HealthMenu functions correctly, do not add a speculative CONFIG and conflate it with gameplay patch testing.

## Cobra/webMAN MOD loading

[webMAN MOD Game Paths & Covers](https://github.com/aldostools/webMAN-MOD/wiki/Game-Paths-%26-Covers): PS2 `.ISO` plus optional `.CONFIG` on **CFW** uses `/dev_hdd0/PS2ISO`; ISOs discovered on external storage get copied to the internal PS3 drive when mounted. PS2 Classics `.BIN.ENC` is a different format, usable with launcher on HEN or CFW. [ConsoleMods PS2 games guide](https://consolemods.org/wiki/PS3:PS2_Games,_Multiplayer,_and_Fixes) likewise distinguishes CFW decrypted ISO workflow from HEN encrypted Classics workflow.

For this project we should focus on the existing proven **CFW decrypted ISO + Cobra/webMAN** route. Don't treat HEN packaging details as evidence of Slim CFW behavior.

## Hardware-specific validation controls

- Owner-validated PS3 Slim/ps2_netemu stable baseline: HealthMenu ISO SHA-256 `fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a`; original retail ISO SHA-256 `c0494ad78fab34dc19fb52b831facb1b27500e66bf0a57a77e627e7b805096f0`.
- For new v0.4 feature isolate **one gameplay patch change at a time** and record CFW/firmware version, webMAN/Cobra version, PS2 emulator route, mounted ISO SHA-256, optional CONFIG presence/hash, game save used, observed screen result and reproducibility.
- Test clean copied save or new game; back up primary saves first. Some shipped INI TaskStatus overrides mention non-existent objectives showing in menus on new-game save creation; do not modify live save when examining GG01 residue.
- Failure triage: same ISO different emulator/config versus different ISO same emulator/config; PS2 level script behavior vs netemu timing/compatibility vs file-patch artifact.
- Do not modify emulator SELF/PS3 firmware as part of this work. Do not infer original PS2 or PCSX2 compatibility from the owner test.

## Further reference

- [PS2 Classics compatibility database](https://ps3classics.github.io/ps2/) for community-reported compatibility, not proof that our patched variant works.
- [ConsoleMods PS3 FAQ](https://consolemods.org/wiki/PS3:FAQ) documents emulator variants.
- [PS3 Developer Wiki PS2 Emulation](https://www.psdevwiki.com/ps3/PS2_Emulation) has firmware-specific emulator memory layout and BIOS/IOP details for advanced research.

## Next deliverable for Muse

Inventory (do not change) the current PS3 console's CFW/Cobra and ps2_netemu revision if readily inspectable, the installed webMAN MOD version and whether a per-game CONFIG is used for `SLUS_209.04`. Validate one small original cheat-handler experiment separately from emulator CONFIG experiments. Do not use Free Camera or level selection. Keep v0.3 unmodified.

No Sony proprietary BIOS, SELF binaries or ISOs committed.
