# Neptune/Muse interim report — 2026-10-22

Source: user-pasted Muse report describing a Neptune-local handoff file, `SpongeBob_Movie_XboxDemo_Interim_FromMobile_2026-10-22.md` (4,890 bytes) in `Documents\\Codex\\2026-10-21\\we-x20\\outputs\\`. **This document records the reported findings, not independently verified access to that local file.**

## Reported checks

- Neptune regression tests: **14/14 fixture cases passed**, and **7/7 ISO stages reproduced byte-identical**; DamageMenu output SHA-256 begins `9df18605`, HealthMenu output SHA-256 begins `fbfa8154`. No working ISOs modified.
- PowerShell test caveat: at 80-column terminal width, the expected “existing output” test can appear to fail because error text wraps. Fix assertion strategy or normalize output; do not confuse with patcher corruption.
- Demo manifests reverified: two compilation variants differ only in `SBMovie.xbe` (SHA-1 A `2246507a…` and B `c8204630…`); demo `sb04.ini` both `3132600d…`, retail Xbox `2dbbd00c…`.
- Muse reports `Build_OXM` is a **leftover launcher directory on Xbox Exhibition Volume 1** rather than direct evidence for a release on Official Xbox Magazine. Earlier inferred OXM connection is therefore superseded pending independent disc documentation.
- Xbox Exhibition Volume 7 demo reported confirmed as Redump **9264**, but Muse reports no publicly reachable dump.
- E3-related marker `E3DemoStart` reported; context and origin should be inspected before drawing conclusions about developer functionality.
- Retail PS2 `SB04.INI` report: `G.CheatFlyToggle = 1`; empty `DebugMode =` entry in an E3-related block. **Their parser call sites and runtime semantics remain unverified**.
- No accessible `SBMovie.xbe` binaries found, so executable section and debug-code comparison remains blocked.

## Next steps

1. On Neptune, locate PS2 `SLUS_209.04` parser xrefs for `G.CheatFlyToggle`, `DebugMode` and E3-related strings. Determine whether `CheatFlyToggle` is consumed at startup only, whether it has an actual activation input, and what it changes. The owner's scope excludes Free Camera, so do not propose a camera hack on the basis of the name.
2. Inspect the actual context/section around `E3DemoStart` when data is available; distinguish scene boot control, demo script, and debug menus.
3. Preserve HealthMenu and DamageMenu ISOs. If a new safe feature is identified, make a separate candidate with recorded exact offsets and full hashes; no overwrite.
4. Improve the error-path fixture to inspect exit codes and normalized output rather than line-wrapped PowerShell text.
5. Request non-copyrighted XBE header/section metadata or lawful local binaries before attributing differences to developer code.

No game binaries are included.
