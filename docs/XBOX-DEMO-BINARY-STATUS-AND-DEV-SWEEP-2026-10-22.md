# Xbox demo binary status, regression re-run, and developer-function sweep — 2026-10-22

Follow-up to XBOX-DEMO-MANIFEST-DIFF-2026-10-22.md and
XBOX-DEMO-OXM-AND-ARCHIVE-DEEP-DIVE-2026-10-22.md. Scope exclusions stand:
no Free Camera, no level selection. No game binaries are published here;
hashes and offsets only. The working DamageMenu and HealthMenu ISOs were
not modified by any step below.

## 1. Regression tests re-run (Neptune, fresh clone of this repo)

tools/test_patchers.py, run on Windows against the outputs folder as
--iso-dir and the retail USA ISO as --original-iso:

- Fixture suite: 14/14 cases pass (success, wrong source, old bytes,
  offset bounds, negative offset, fractional offset, overlap, bad hex,
  odd hex, length mismatch, output mismatch cleanup, existing output,
  same input output, hash cmdlet unavailable).
- Full ISO stages: 7/7 regenerate byte-identical outputs (SHA-256):
  overlay eecc8a3fddec908daf626762c39dbed697b32746604b9bafd3f29ee82b3fa6c9,
  select-toggle 78b5b1530a179ad25a2e06167b24aacc369977d57fcdc9b0433d0f7b120303f7,
  debug-panel 9da1560b7ae33e50624aa0699ada215a40a984a5b12dbeb6a1395ed63709d32b,
  music-panel 973e1ed3098acef2d211c2fbbc877bff4bec17687ff00627949a631665ea9b13,
  debug-menu 53f66e48d05bf22c5e3ac351f220526a912f067e65d08a430f76657a47e9b8f8,
  damage-menu 9df1860529ac4e6e5d2bb542ba59b1c171bb1ae797a24c8aef80eb75c4a12630,
  health-menu fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a.
  The harness asserts every source ISO is unchanged afterwards.

Harness fragility found: on an 80-column console the "existing output"
fixture case false-fails, because PowerShell wraps the patcher's error
text mid-phrase ("already" / "exists" split across lines) and the
substring assertion misses. Re-running with a 500-column console buffer
passes. This is a test-environment issue, not a patcher regression.

## 2. Local file search (Neptune) — negative

Searched the full user profile (depth 5) and all filesystem drives
(depth 4; only C: exists) for *.xbe, Exhibition, Build_OXM, sb04.ini and
SBMovie names. No demo or Build_OXM files are on the PC. The only .xbe
present is an unrelated softmod payload (Downloads\xbox og). No GameCube
disc images from BUILD_INSPECTION.md were found on the PC either.

## 3. Manifest verification (independent re-check)

Re-fetched XboxArchive/hashes at commit cb1925f1 and re-compared:

- Compilation A (Build_OXM/ prefix) vs compilation B (SpongeBob/
  prefix): identical 63 relative paths, 62 identical SHA-1, exactly one
  difference — SBMovie.xbe:
  A 2246507aab79757ee051b12588d7d80a2c27e53a
  B c82046303363e6be20971b0febe58c7f133d49d2
- sb04.ini is identical in both compilations:
  3132600d36cf64ebfb4c755fa51a22e356b23a87
- Demo vs retail disc manifest (basename match, 40 overlapping paths):
  13 identical, 27 differ. Retail sb04.ini SHA-1
  2dbbd00ca09ea8353ae669844d2414197b4b8cc1 (differs from the demo ini).
  Retail executable is listed as DEFAULT.XBE,
  26aa1fa19b16b6eefc2bd0cff98258505008cd67. The retail manifest contains
  no SBMovie.xbe and no E3DemoStart entry.

## 4. Preservation status of the demo discs

- Xbox Exhibition Volume 7 is redump disc 9264, "Exhibition: Volume 7
  (Demo Disc)", serial X10-20974, barcode 805529993365, catalogued as an
  XDK/Exhibition sample; content listings confirm the SpongeBob Movie
  demo. No public dump was located (archive.org and Hidden Palace
  checked 2026-10-22).
- Build_OXM is a folder inside the Exhibition Volume 1 disc structure
  (redump 64277): a leftover multi-title launcher bundle, also seen in
  Volume 2 — not evidence of an Official Xbox Magazine build. Redump's
  file records for that disc list the SpongeBob demo in the sibling
  Spongebob/ folder with SBMovie.xbe, four sb04*.bik movies,
  config_*.hip files and an E3DemoStart level file (E3-demo lineage).
- The archive.org item for that disc was downloaded and checked at file
  level on 2026-10-22: its ISO is only 14,319,616 bytes (SHA-1
  e27f0c94aef79ced704d122d5062574a2376c636), a small ISO9660 image whose
  contents contain no game files at all (filename scan negative for
  SBMovie, sb04 and any .xbe). It is not the game-bearing disc image. A
  "Volume 2 HDD-ready" archive.org item cited in some listings could
  not be located on 2026-10-22.
- Which XBE variant (A or B above) belongs to which physical disc is not
  established by the manifests. Unknown.

## 5. SBMovie.xbe code-vs-header comparison — BLOCKED

No SBMovie.xbe bytes are available locally or from any public
preservation record found (section 4 documents the archive.org items
checked and excluded), so the section-level comparison (certificate /
header fields versus .text/.rdata differences) cannot be performed yet.
tools/compare_xbox_movie_builds.py currently reads header fields only;
a section-hash diff is the next tool step once a dump is lawfully
available. Blocked on: a dump of Exhibition Volume 7 (redump 9264) or of
either compilation disc behind the manifests in section 3.

## 6. sb04.ini comparison status

| Copy | Status |
| --- | --- |
| Xbox demo ini (both compilations) | SHA-1 3132600d36cf64ebfb4c755fa51a22e356b23a87 known; content not public — key-level diff blocked |
| Xbox retail ini | SHA-1 2dbbd00ca09ea8353ae669844d2414197b4b8cc1 known; the previously cited public mirror (bfbbdecomp/configs) could not be re-fetched on 2026-10-22 (repository not found via the GitHub API — possibly renamed) |
| PS2 retail ini (inspected copy) | 53,452 bytes; SHA-1 ff030c8e0afd1e47d80c42a0e051420dc1241ef4; SHA-256 4d92750bd8eb1a4653a67661ed5a2b9fab985112ee03bdf6cfa2f26878ac8303 |
| GameCube compilation ini | 53,449 bytes per BUILD_INSPECTION.md; disc image not located on the PC on 2026-10-22 |

PS2 retail ini structure: flat KEY = value lines with # comments (no
sections), 1,481 lines. Developer-relevant entries verified in the file:

- ShowMenuOnBoot = 1
- G.TakeDamage = 1 (the runtime flag the DamageMenu build controls)
- G.CheatSpongeball = 0, G.CheatPlayerSwitch = 0, G.CheatAlwaysPortal = 0
- G.CheatFlyToggle = 1 — a cheat toggle shipped ENABLED in retail PS2
- G.InitialShinyCount / G.InitialSpatulaCount, commented as useful for
  debugging
- "DebugMode = " with an empty value (line ~1325), inside a commented
  developer block about demo recording; a nearby comment (line ~1334)
  reads "this is the release build... restore after E3" — E3-era
  leftovers in the shipping configuration
- Comment at line ~96: a debug controller's Start resets profile
  tracking
- The Unlockables block documents seven Function/Cheat extras (type 5):
  Alt Target Hand, Alternate OOB Hand, Alt Car Horn, Long Antenna,
  Antenna Fountain, Tiny Foggers, Magnetic Pickup

A key-level demo-vs-retail ini diff remains blocked on the demo ini
content (section 5's dump requirement covers it).

## 7. Developer-function and menu-asset sweep (PS2 restoration leads)

Symbol-bearing build (DWARF-recovered source, reference/xDebug.cpp):
the debug subsystem is stubbed down in the symbol build —

| Function (symbol build address) | Size | Body |
| --- | ---: | --- |
| xDrawTextRender 0x404040 | 0x8 | empty |
| xDrawTextInit 0x404050 | 0x8 | empty |
| xDebugTimestampScreen 0x404060 | 0x8 | empty |
| xDebugUpdate 0x404070 | 0x34 | minimal shell |
| xDebugInit 0x4040b0 | 0x8 | empty |
| xprintf 0x4040c0 | 0x28 | small |

This matches BUILD_INSPECTION.md's GameCube ELF observation (four-byte
debug functions). Caution: those addresses are the symbol build's
layout — spot-checking the same addresses in retail SLUS_209.04 shows
live code, so the two builds' layouts differ and the stub table must
not be transplanted to PS2 addresses.

Retail PS2 executable facts (SLUS_209.04, SHA-256
2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956):
single flat "main" segment (load 0x100000, size 0x536A00), no symbol
table and no DWARF sections in the retail disc ELF — function names
cannot be read from it directly. Direct PS2-side evidence instead:

- A cluster of stub slots at 0x403B70-0x403BAC (16-byte slots containing
  only jr $ra + nops) immediately before live handler code at 0x403BB0
  (prior disassembly, work file debug-handler.txt) — stubbed-out
  functions exist in the retail PS2 build in the cheat-handler area the
  menu builds already work around.
- Leftover developer strings in the retail ELF include
  "Demo running in debugger -- overriding bogus params!" and
  "No HIS debugging", plus a displayPadDebugInfo identifier.
- Retail menu archives (MN) still carry the cheat-code ENTRY interface
  assets (menu-string-scan.json): MNUC.HIP menu_cheat_startcheat.WAV
  (0x358E); MNUI.HIP menu_cheat_correctbutton.WAV (0x5E8A),
  CHEAT_SUCCESS (0x66D6), CHEAT_STEP_GRP (0x9C5E),
  menu_cheat_enterfailure.WAV (0xD234),
  menu_cheat_entersuccess_used.WAV (0xD6A4), CHEAT_FAILED_GRP (0xE448).

Interpretation for the PS2 restoration: the cheat-entry UI assets and
the Extras Function/Cheat unlockables shipped in retail; the debug
subsystem behind xDebug was stubbed before release. Realistic
restoration targets remain the existing menu/variable-table route (as
in the Damage/Health menus), not reviving xDebug.

## 8. Open unknowns

1. SBMovie.xbe bytes for either variant (blocks section 5 and the
   key-level ini diff).
2. Which physical disc carries XBE variant A vs B.
3. Current home of the bfbbdecomp retail-Xbox config mirror.
4. Location of the GameCube compilation disc images used for
   BUILD_INSPECTION.md (not on the PC as of 2026-10-22).
5. Whether the PS2 retail cheat handler behind the stub cluster at
   0x403B70 is reachable from the shipped cheat-entry assets — untested.
