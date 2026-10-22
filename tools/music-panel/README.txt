MUSIC CONTROL — OWNER-CONFIRMED BASELINE

1. Extract this ZIP on Windows and run APPLY-MUSIC.cmd.
2. Choose the working SpongeBob-Movie-USA-Panel-TEST.iso, whose test row worked.
3. The patcher creates SpongeBob-Movie-USA-Music-TEST.iso beside it. The source is untouched.
4. Transfer/mount the NEW ISO on the same CFW PS3.

The row now says Music: PLAYING or PAUSED, using the engine's actual music-paused flag. SELECT hides/shows the panel. UP/DOWN selects/deselects the row. X pauses/resumes music only when selected.

Test with audible background music:
- At the title screen, select Music and press X. Does music stop and PAUSED appear?
- Press X again. Does music resume and PLAYING appear?
- Confirm sound effects remain audible. No sound-effect, dialogue-volume, master-volume, save, or progression fields are changed by this patch.
- Hide the panel and check the current state, then reopen it.
- After the title test, repeat in ordinary gameplay. Note normal X/Select actions still occur; the panel does not consume controls or freeze the game.
- Report any crash, flicker, no-audio response, or label mismatch. A short video would be useful.

This is an engine music PAUSE/RESUME control, not a persistent saved mute preference. Normal game pause/unpause, transitions or new tracks may change music state; the label follows the real engine pause flag, not a separate UI-only switch. Broad mode/transition behavior is not yet established. Do not test during saving; use your original working panel if this candidate misbehaves.

Static verification: 768 exact-instruction cases include the new driver/helper and real retail music pause/resume instructions, with absent/present controller and zero/one/two active tracks. The external sound backend was modeled, not executed. Eight interaction steps passed. The actual patcher produced a full ISO; wrong input and overwrite were rejected; comparison found 170 differing bytes confined to three intended patch windows.

No game image is included. PowerShell is sufficient; no admin privileges, Python, or network access are needed by the patcher. Allow about 1.25 GB free beside the input.

Input SHA-256: 9da1560b7ae33e50624aa0699ada215a40a984a5b12dbeb6a1395ed63709d32b
Output SHA-256: 973e1ed3098acef2d211c2fbbc877bff4bec17687ff00627949a631665ea9b13

Owner hardware report, 2026-10-22: "it worked", after pause/resume and sound-effect instructions on the established CFW PS3. This is reported basic success, not proof of extended mode/transition stability. This is a custom panel, not restoration of an original developer menu.

