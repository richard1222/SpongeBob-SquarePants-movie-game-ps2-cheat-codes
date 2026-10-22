# v0.3 release candidate — readiness checklist (October 22, 2026)

**Status: PREPARATION ONLY. Not tagged, published or packaged as v0.3.**

## Proposed scope

Promote the already implemented **HealthMenu** feature from the experimental v0.2 add-on to the documented stable **owner-verified PS3/ps2_netemu baseline**, retaining all seven reproducible patch stages. This is a release hardening/documentation milestone, not a claim that the original developer menu was recovered.

## Evidence supporting release

- Owner-reported CFW PS3 test: `HP3` -> `HP1` after two enemy hits, recovery to `HP2`, Damage 0 prevents ordinary hit damage, Damage 1 restores damage, successful death/restart and level 1-to-2 transition, Select hide/show and overall existing controls.
- Muse reported regression pass on Neptune: 14/14 fixtures, all 7 stage outputs reproduce byte-identically. Known error-text wrapping false negative is a test-output formatting issue that should be documented or fixed.
- HealthMenu ISO expected SHA-256: `fbfa8154a436e7c1cb1a06b54b85296524ab151d1098bcf631b0b8e3ec9e629a`.
- Prior DamageMenu ISO SHA-256: `9df1860529ac4e6e5d2bb542ba59b1c171bb1ae797a24c8aef80eb75c4a12630`.

## Ship gate

- [ ] Refresh `releases/v0.2/RELEASE_NOTES.md`? **No:** leave historical v0.2 text intact, explicitly supersede it via v0.3 notes.
- [ ] Update `tools/README.md`, main README and validation status: remove outdated statements that HP hardware testing is pending, while preserving recorded gaps.
- [ ] Confirm tagged release archive has intended original tools/manifests/notes, *not* ISOs, ELF, XBEs, copyrighted game assets or credentials.
- [ ] Run regression tests against actual v0.3 packaged toolset on Neptune; record output and SHA-256 of distributable ZIP.
- [ ] Complete release notes with console coverage, install stage order, correct source hash requirements and the distinction between original PS2/PCSX2 (untested) and PS3 `ps2_netemu` (owner-tested).
- [ ] Publish tag and GitHub release, attach verified ZIP. GitHub release/tag creation is not yet available through the current connected action set; use a desktop GitHub workflow or a connector that exposes release publishing.

## Explicitly out of scope

- `G.CheatFlyToggle`, `DebugMode`, `E3DemoStart`: leads requiring executable parser/runtime tracing; no unverified new feature is shipped.
- No Free Camera or level selection.
- No claim of compatibility on original PS2, PCSX2, or every PS3 emulator family.
- Keep the original USA ISO, proven HealthMenu ISO and DamageMenu fallback unmodified.
