# Xbox demo executable comparison and OXM identity audit — 2026-10-22

## Method

Compared file-level SHA-1 records from two independently catalogued compilation-disc manifests in `XboxArchive/hashes`. Stripped only the `Build_OXM/` and `SpongeBob/` prefixes and compared matching relative paths (case-insensitive). These are published file hash records, not downloaded executables.

Manifest A: https://github.com/XboxArchive/hashes/blob/cb1925f10b80a8bbe1eef7dc1ecd2d916d454773/redump/ffcbc07887fa554b1715c61fe6aadbdb5fbf1dc7

Manifest B: https://github.com/XboxArchive/hashes/blob/cb1925f10b80a8bbe1eef7dc1ecd2d916d454773/redump/d2d6d97d26b65e208d1f6bb603eee00aa927ebb1

## Result

Both directories contain exactly **63 identifiable relative paths**, all present in both. **62 files have identical SHA-1**. Exactly one differs:

| File | Manifest A | Manifest B |
|---|---|---|
| `SBMovie.xbe` | `2246507aab79757ee051b12588d7d80a2c27e53a` | `c82046303363e6be20971b0febe58c7f133d49d2` |

The entries for `sb04.ini`, the menu HIP/HOP files and all other 61 data files match. **This is a highly focused executable-difference lead**, not proof of a debug compiler or an early game beta. Differences could involve packaging, executable certificates, demo-mode limits, localization, build date, or executable code.

## Separate retail Xbox manifest

Comparison to a separately indexed retail/region Xbox disc manifest
https://github.com/XboxArchive/hashes/blob/cb1925f10b80a8bbe1eef7dc1ecd2d916d454773/redump/3d19126c60909d9a13f07200a368deac520f34c0

- 40 overlapping named paths with demo A, **13 same hashes and 27 different**.
- The demo's `sb04.ini` and retail `sb04.ini` differ by SHA-1. This means a **configuration difference exists**, but its keys/values are not visible in a hash manifest.
- Key HIP/HOP assets also differ; could reflect demo trimming and region-specific packaging, not necessarily removed content.
- The retail manifest uses `DEFAULT.XBE` rather than `SBMovie.xbe`, so **do not make a direct filename-matched executable comparison** from these manifests.

## OXM issue identity investigation

- A forum statement from January 10, 2005 suggests a SpongeBob Movie demo on the following OXM disc; its identification remains unverified.
- **OXM disc 41** (February 2005) cataloged playable contents do not include SpongeBob Movie: https://www.pricecharting.com/game/xbox/official-xbox-magazine-demo-disc-41
- **OXM disc 42** (March 2005) cataloged playable contents also do not include SpongeBob Movie: https://www.pricecharting.com/game/xbox/official-xbox-magazine-demo-disc-42
- VGHF holds preserved scans of issues 41 and 42: https://library.gamehistory.org/repositories/2/resources/80

Thus the contemporary forum claim cannot presently be reconciled with these two issue listings. `Build_OXM` is a **directory name**, not adequate independent proof of a particular OXM issue or disc. The related Xbox compilation may be a publisher preview, magazine-master preparation, or compilation repack; do not assign source without disc metadata.

## Console/XBE investigation steps

1. Obtain lawful access to the two demo XBEs or their file headers through a preservation record, then extract certificate title ID, entry point, timestamp/header flags, executable section hashes, and readable strings **without** uploading game executables publicly.
2. Distinguish altered certificate/header/demo expiry from changed `.text` or `.rdata` sections. If code differs, align functions by signatures; search for debug/init flag handling and developer interfaces.
3. Obtain lawful access to demo and retail `sb04.ini`; run a key/value diff and separately list removed or changed entries, especially retained debug options.
4. Compare menu asset inventories by name/asset IDs, not just SHA-1 difference, to identify actual unused menu content.
5. Compare discoveries conceptually to retail PS2 `SLUS_209.04`, not by transplanting Xbox binary offsets. No Free Camera or level-select feature is requested.

## Important boundaries

These are **manifest-level findings only**, not a disassembly or execution of the Xbox binaries. The successful PS3 HealthMenu ISO is unchanged.
