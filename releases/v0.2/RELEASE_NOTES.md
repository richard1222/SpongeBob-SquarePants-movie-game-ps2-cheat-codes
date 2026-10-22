# SpongeBob Movie Debug Tools v0.2

v0.2 packages all seven patch stages for USA PS2 SLUS_209.04, including the owner-reported working four-row damage menu and a new experimental live HP display. It fixes patcher failure handling and removes older patchers' dependence on Get-FileHash.

## Included

- Controller/status overlay probe, Select toggle and first interactive panel.
- Music pause/resume, three-row diagnostics and four-row Damage 1/0 menu.
- New HealthMenu-TEST patcher: live HP beside the Damage row, with pointer guards and HP-1 when unavailable.
- Stage manifests, expected hashes, original-byte guards, developer instruction tests, patcher regression fixtures and research notes.

## Patcher fixes

All seven PowerShell patchers now use .NET stream hashing and require both source and output hashes. They validate patch encodings, equal lengths, integer offsets, bounds and non-overlap. The source remains open against writes through checking/copying.

Outputs are built as unique temporary files. The final filename appears only after the expected hash passes, and handled failures remove the partial output. Existing files are never replaced. An optional -OutputIso selects a separate output location. Force-killing PowerShell or power loss may leave a .partial file; it is not a completed ISO.

The Select toggle now has the same external manifest format as other stages. Stale status wording was corrected; original reports and limitations remain in the research history.

## Verification and limits

**Proven locally:** 14 patcher regression cases passed, including wrong input, malformed/overlapping/out-of-range patches, same input/output, preserved existing output, failed-output-hash cleanup and an unavailable Get-FileHash command. All seven updated patchers produced the expected 1,249,804,288-byte full ISO outputs, with unchanged source hashes.

The new HP build additionally passed 6,656 menu instruction cases, 36 existing pointer-guard cases, 41 health-readout cases and a 12-step interaction sequence. Its full-image comparison found 326 changed bytes inside the existing intended windows.

**Owner-reported working:** the first six stage images, through DamageMenu-TEST, on the established CFW PS3 setup. Detailed per-hazard, character, mode and transition coverage remains incomplete.

**Hardware-unverified:** the new HP display and its refactored hook. No new console result or screenshot is claimed. These are custom interfaces, not recovery of an original developer menu.

## Start here

Download and extract SpongeBob-Movie-Debug-Tools-v0.2.zip. Open tools/README.md and run the CMD launcher for the stage matching the ISO you already have. If you have the working DamageMenu-TEST, use tools/health-menu/APPLY-HEALTH-MENU.cmd to create the new HP candidate separately.

No ISO, full executable, game assets, credentials or SDK binaries are included. Keep the owner-tested damage-menu ISO as the fallback. v0.1 remains available unchanged.

Next: test whether HP follows ordinary damage and pickups on the console, then check the four controls and transitions. See docs/HEALTH-MENU-2026-10-22.md.
