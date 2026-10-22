# Xbox and GameCube documentation: cross-platform PS2 research opportunities (2026-10-22)

This is research for PS2 `SLUS_209.04`, NOT proof that missing game code or assets have been recovered. Stable v0.3 and separate v0.4 test ISOs remain untouched.

## GameCube: high-confidence source of names and behavior

- [bfbbdecomp/tssm](https://github.com/bfbbdecomp/tssm) is a work-in-progress **GameCube GGVE78** reconstruction. Use `zGameExtras`, `xDebug`, `xPad`, scene/task management and cheat callbacks as behavioral and structure references.
- [bfbbdecomp/bfbb](https://github.com/bfbbdecomp/bfbb) reconstructs the older Heavy Iron engine. Useful for naming shared classes and comparing debug/tweak design, but do not presume Movie implementation matches it.
- **Cross-map by behavior and references**: callback effects, state serialization, input mask, text/hash cross-references, struct layouts, and named HIP/HOP objects. Do NOT copy GameCube PowerPC code or addresses into PS2 MIPS.

## Xbox: strong build-comparison and live-debug possibility

- Original Xbox XBE is an x86 executable format carrying code/data sections, executable title metadata and library/XDK version stamps. See [XBE parser explanation](https://github.com/sp00nznet/xboxrecomp/blob/main/docs/pipeline/01-xbe-parsing.md) and [XBE format documentation](https://xbdev.net/fileformats/xbe/NonOfficialXBEFileFormat.pdf).
- [xemu guest debugging](https://xemu.app/docs/dev/debug/guest/) documents enabling GDB on localhost port 1234 with `-s` (and `-S` to start paused) and debugging guest code. This only becomes useful once a legitimately obtained playable Xbox game/demo image and reliable XBE hashes are available.
- Our prior XboxArchive manifest work has two differing `SBMovie.xbe` SHA-1 values but **no actual verified executable bytes yet**; differing hashes do not prove debug code, cut assets, or earlier gameplay.
- Compare each real XBE's headers, section sizes, import tables, executable strings, cheat callbacks, INI keys and instruction differences only after authenticating build identity. Avoid attributing differences exclusively to game logic if headers may differ.

## Asset comparison across three platforms

[Industrial Park](https://github.com/igorseabra4/IndustrialPark) supports The SpongeBob SquarePants Movie HIP/HOP on GameCube, Xbox and PS2. This is the highest-leverage tool for determining whether missing PS2 objects survive in an alternative platform build. Prefer cross-platform **normalized manifests** containing level identifier, archive relative path, asset type, name/ID, byte size, hash, and metadata. Do not assume identical RenderWare binary encoding, platform textures, endianness, compression or pointer layout.

Candidate priority:
1. **GG01**: inspect complete file lists of authenticated alternative-platform/demo builds for `GG01.HIP`, `GG01.HOP`, `GG01_US.HIP` or regional equivalents. Retail PS2 has no GG01 assets per Muse's recent analysis.
2. **Cheat/extras**: cross-reference known retail `SB04.INI` seven Extras against each platform's INI values and HIP/HOP assets. A name by itself is NOT a restored executable feature.
3. **Menu cheat assets**: compare CHEAT_SUCCESS / CHEAT_FAILED / CHEAT_STEP sounds and UI paths across game builds, tracing actual code where available.
4. **Debug structures**: GameCube named `xDebugAddTweak` and `xDebugModeAdd` references can guide PS2 call-graph comparisons, but retail PS2 stubs imply features may have been stripped.

## Practical work packet for Muse/PC counterpart

A. From already-owned GameCube/Xbox disc backups, build **file hash and named asset inventories** only; do not publish game assets.
B. Match `zGameExtras` callbacks by side effect across platforms and against PS2 retail's now-confirmed nine-cheat table; distinguish retail-complete functions from genuine cut content.
C. If two Xbox demo `SBMovie.xbe` binaries become locally available, compare XBE certificates/library revisions, sections, entrypoint, code and string diffs. Explicitly distinguish build metadata from game-code evidence.
D. If alternative-platform GG01 assets are discovered, record provenance and verify what they contain before proposing a conversion workflow. Console-specific assets and scripts may require adaptation; do not claim drop-in portability.
E. Save findings as evidence-rich GitHub notes with input hashes, per-asset comparisons and confidence levels. No copyright-protected ISOs, XBEs, DOLs or HIP/HOP game assets in the repo.

**Current verdict:** GameCube decomp + cross-platform Industrial Park manifests are actionable immediately with existing lawful inputs; Xbox executable binary-diff depends on obtaining actual verified bytes. No new beta or recovered GG01 asset was located in this documentation pass.
