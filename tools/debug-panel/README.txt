CUSTOM DEBUG PANEL — FIRST HARDWARE TEST

Use the working Select-toggle ISO as the source.

1. Extract this ZIP into a folder on Windows.
2. Double-click APPLY-PANEL.cmd.
3. Choose SpongeBob-Movie-USA-Select-Toggle-TEST.iso (the one whose Select toggle worked).
4. The patcher creates SpongeBob-Movie-USA-Panel-TEST.iso beside it. Keep the working source unchanged.
5. Transfer and launch the NEW ISO through your usual CFW PS3 PS2 ISO setup.

Expected screen: SB MOVIE DEBUG, one Test row showing OFF/ON, and control instructions.

SELECT: show/hide the panel.
UP or DOWN: select/deselect the single row. A > marker means selected.
X: switch the displayed test value OFF/ON while the row is selected.
The test value has no gameplay effect. The panel does not pause the game or consume buttons, so normal menu/game controls may also react. Test at the title screen first.

Test sequence:
- Check whether the panel appears.
- Press Up: does > appear beside Test row?
- Press X: does OFF become ON?
- Press X again: does ON become OFF?
- Press Down: does > disappear? X should then leave the value unchanged.
- Hide with Select, then reopen. Does the selection/value persist?
- After the title test, briefly check gameplay and report any flicker/crash.

Please send a photo of the panel and tell us which steps worked.

This is a custom panel candidate, not a restored original developer menu. No new console test is claimed. Static checks: 192 emitted-instruction cases, 9-step state sequence, actual patcher execution, source/overwrite guards, and full-image comparison showing 328 changed bytes confined to four patch windows.

No ISO is bundled. Windows PowerShell is sufficient; no Python, administrator rights, or network access is needed by the patcher. It validates the source hash and original bytes, writes a separate copy, and checks its final hash. Allow about 1.25 GB free beside the source.

Expected input SHA-256: 78b5b1530a179ad25a2e06167b24aacc369977d57fcdc9b0433d0f7b120303f7
Expected output SHA-256: 9da1560b7ae33e50624aa0699ada215a40a984a5b12dbeb6a1395ed63709d32b

