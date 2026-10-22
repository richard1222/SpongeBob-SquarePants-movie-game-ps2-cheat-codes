# RR — Custom debug panel test, October 22, 2026

Target: USA PS2 `SLUS_209.04`, CFW PS3 testing. Goal: validate show/hide, row selection, and test-value activation before adding gameplay controls.

## Rundown

**Proven owner reports:** the controller/status overlay and custom Select toggle worked on the owner's CFW PS3. **Proven static result:** a first custom panel candidate now reuses the retained text renderer, presents one selectable test row, and passes 192 emitted-instruction cases plus a nine-step interaction sequence. The patcher produced a full ISO with changes restricted to four intended windows. **Unknown:** the panel's actual rendering and interaction on the console. No screenshot or new hardware result is claimed.

## In plain language

This turns the proven display into a small input/UI experiment. Select shows/hides the panel. Up or Down changes whether its single row is selected; a `>` marker shows selection. X switches the row's displayed OFF/ON value only while selected. The value has no gameplay effect.

The game is not paused and buttons are not consumed, so ordinary menu/game controls can also react. Begin at the title screen. This is a custom panel, not a recovered original developer menu.

## Reproducible implementation

[Windows patcher and data](../tools/debug-panel/) contain no game ISO. Run `APPLY-PANEL.cmd` and select the working `SpongeBob-Movie-USA-Select-Toggle-TEST.iso`. It validates the entire input hash and expected original bytes, creates a separate `SpongeBob-Movie-USA-Panel-TEST.iso`, and checks its output hash. Existing outputs are refused.

The 160-byte input driver fits in the former pad-formatting region at 0x004A9240. The existing renderer's textbox initialization and rendering path remain in use. Its second-controller loop is replaced with an exit so a single panel is drawn and input is processed once per handler invocation. The former controller format string holds the panel template and short marker/value strings.

State shares the existing debug word: bit 0 visible, bit 1 row selected, bit 2 test value. The update entry calls the handler even when hidden, allowing Select to reopen it. No game settings or save fields are modified.

## Evidence

| Check | Result |
| --- | --- |
| Exact emitted-instruction cases | 192 passed |
| Interaction sequence | Nine steps passed |
| Published test runner | Passed against published patch JSON |
| Actual Windows patcher | Generated full candidate ISO |
| Wrong-source guard | Rejected |
| Output overwrite guard | Rejected |
| Full-ISO comparison | 328 differing bytes, all inside four intended windows |
| Console rendering/input | Pending |

- Input SHA-256: `78b5b1530a179ad25a2e06167b24aacc369977d57fcdc9b0433d0f7b120303f7`.
- Output SHA-256: `9da1560b7ae33e50624aa0699ada215a40a984a5b12dbeb6a1395ed63709d32b`.
- ISO size: 1,249,804,288 bytes.
- Patch windows: runtime 0x00403BB0 (64 bytes), 0x004A9240 (192 bytes), 0x004A93A0 (16 bytes), 0x0062F012 (105 bytes).
- [Machine-readable verification](../tools/debug-panel/VERIFICATION.json).
- Instruction test: `python tools/debug-panel/test_panel.py`. This simulates the emitted driver and external-call arguments; it does not emulate the whole game, GPU, text renderer, or PS3.
- Patcher ZIP upload: 4,289 bytes; server size and MD5 matched the local archive. Full copyrighted images remain outside the repository.

## New research results

[Actual PS2 config inventory](PS2-CONFIG-INVENTORY.csv) covers 41 candidate keys. Twenty-five have direct references found by the bounded LUI plus ADDIU/ORI address scanner. The CSV separates stock INI values, executable literals, direct address references, and runtime status. A missing direct reference is not proof that a key is unused: dynamically constructed keys and other addressing forms are not covered. Presence and references do not establish safe runtime effects or bounds.

The downloaded continuity handoff names `SLUS_213.91`, conflicting with the inspected `SLUS_209.04` baseline. Its 0x429C30 lead was checked under both simple interpretations: runtime 0x00429C30 lies among floating-point instructions, whereas file offset 0x00429C30 maps to zero-filled bytes at runtime 0x00529BB0. Neither inspection establishes a debug-flag table. No patch uses that lead.

## Next hardware gate

1. Apply the small patcher to the working Select-toggle ISO; preserve that baseline.
2. Boot the new panel ISO at the title screen.
3. Check the heading and row, select with Up, change OFF/ON with X, deselect with Down, and confirm X then leaves the value unchanged.
4. Hide/reopen with Select and check state persistence.
5. Report visible output, normal-control conflicts, flicker/crashes, and a photo if possible.

Only after this gate should verified gameplay controls be connected to panel rows.
