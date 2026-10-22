# Expanded custom debug menu — 2026-10-22

- Audience: owner and PS2 patch contributors.
- Target: USA retail SLUS_209.04, tested through PS2 emulation on the owner's CFW PS3.
- Success condition: build a reproducible three-row menu candidate, verify its instruction behavior and full-image change boundaries, then test the new rows on the console.

## Rundown

A new custom debug-menu ISO is built. It retains the music pause/resume behavior the owner just confirmed, adds selectable XYZ and scene/controller diagnostic rows, and keeps Select hide/show. The new menu is a hardware-test candidate, not a recovered original developer menu.

The new readouts are OFF at boot. Enabling them checks pointers before calling the game's own text formatters. Invalid pointers show N/A. The owner now needs to check the expanded layout and diagnostic rows at title, in gameplay, and through transitions.

## Current truth

| Class | Claim | Evidence |
| --- | --- | --- |
| Proven | Owner reported the Music-TEST ISO worked after the pause/resume and sound-effect test instructions. | Owner message “it worked”, October 22, 2026. This is an owner report, not a captured console trace or extended stability test. |
| Proven | Expanded-menu instructions passed 4,992 combinations, 36 pointer-guard cases and a 12-step sequence. | [Test runner](../tools/debug-menu/test_debug_menu.py), [developer spec](../tools/debug-menu/DEVELOPER-SPEC.json), [receipt](../tools/debug-menu/VERIFICATION.json). External position/scene formatters and sound backend are modeled. Actual retail music pause/resume instructions are included. |
| Proven | Windows patcher generated the full image and rejected a wrong input and existing output. | Output SHA-256 below; the final patcher was run again in an isolated local check and produced the same hash. |
| Proven | 656 changed bytes are confined to five intended windows. | Full source/output comparison and exact patch-byte checks; receipt records windows. |
| Inference | The added diagnostics should stay usable when player/scene objects are absent. | Null/range/alignment checks and simulated invalid-pointer cases. Runtime object lifetime is not established by static guards alone. |
| Unknown | Expanded layout, transitions and diagnostic rows work reliably on the PS3. | First hardware test pending. No new console screenshot is available. |

## Controls and expected behavior

The title shows the selected row as 1/3, 2/3 or 3/3. Up/Down wraps between rows. X changes the selected row. Select hides or shows the menu.

1. **Music:** X pauses/resumes music; PLAYING/PAUSED follows the engine flag.
2. **XYZ:** X enables/disables the live integer position string. OFF is disabled; N/A means an unavailable or rejected pointer.
3. **Scene:** X enables/disables scene ID and controller diagnostics. The pad line shows held/newly pressed engine button bits as hexadecimal values.

Normal button actions still reach gameplay. The menu does not consume controls or pause gameplay. These diagnostic rows do not alter player positions, scene state, progression, unlocks or saved settings.

## Implementation and evidence

The menu retains the retail controller-overlay rendering prologue, renderer and epilogue. The entry at 0x00403BB0 tails into it. The new dispatcher occupies the old pad formatter at 0x004A9240. Additional logic reuses the old pad-state/type label table at 0x00604F70; direct address-construction scans found its old formatter references. The ELF's file-backed PT_LOAD marks the region readable, writable and executable. The format continuation at 0x004A93A8 is entered only by the custom logic; the draw-return path at 0x004A93A0 continues to exit.

The guard allows four-byte-aligned pointers in 0x00100000..0x01FFEFFF. Excluding the final RAM page leaves room for the +0x80C member access. XYZ follows the retail globals/player/transform chain before calling 0x002E0690. Scene validates the scene pointer and nonzero scene ID before calling 0x002E0720. These checks do not prove that an in-range pointer remains a live object.

The original 0x460-byte rendering frame is retained. Temporary readout strings and saved pointers are used only before the retail renderer initializes that frame area. The final menu uses five formatting arguments in the existing register convention, with no extra variadic stack slots. Output remains inside the original text buffer.

- Input: owner-tested Music-TEST.iso, 1,249,804,288 bytes.
- Input SHA-256: `973e1ed3098acef2d211c2fbbc877bff4bec17687ff00627949a631665ea9b13`.
- Output: SpongeBob-Movie-USA-DebugMenu-TEST.iso, 1,249,804,288 bytes.
- Output SHA-256: `53f66e48d05bf22c5e3ac351f220526a912f067e65d08a430f76657a47e9b8f8`.
- Output MD5: `8ad2dfeb97c11b8251778dcbf35a36d6`.

The patcher uses .NET hashing directly so it does not depend on Get-FileHash availability in the PowerShell environment. This was checked after a child-shell verification run exposed the missing cmdlet.

## First console test

Boot, check the three-row layout and row wrapping, then verify the retained music control. Enable both diagnostic rows at title and in gameplay. Move to check XYZ, change levels to check scene ID, and check hide/show, death/restart and returning to title. Report crashes, flicker, missing text, stale values or unexpected audio changes.

The original Music-TEST image remains a known baseline by owner report. The prior v0.1 release is unchanged. New tools and receipts are in [tools/debug-menu](../tools/debug-menu/). No game image, executable, external SDK binaries or account data are committed.
