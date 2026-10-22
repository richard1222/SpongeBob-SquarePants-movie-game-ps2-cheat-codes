# RR — Movie PS2 debug-path investigation

Date: 2026-10-21. Target: USA `SLUS_209.04`. Goal: identify retained debug-menu functionality and test a minimal diagnostic before changing control flow.

## Owner hardware report — October 21, 2026

**Proven report:** after receiving the controller-debug probe and PS3 testing instructions, the owner reported **“it worked”** and requested that this result be recorded on GitHub. This is an owner-reported successful probe test in the established CFW PS3 context (CECH-2001A), not an independently observed runtime result.

**Unknown:** the owner has not yet specified whether “worked” means successful boot alone or a visible controller/status overlay. No screenshot/video, displayed text, exact runtime behavior, save/load result, or stability duration has been supplied. A complete debug menu remains unconfirmed. The next step is to capture the visible result and identify which retained debug feature is active.

The original static-analysis and pre-test record below is retained as history; references to pending testing describe that earlier stage.

## Rundown

**Proven:** the actual Movie USA PS2 ISO has now been inspected. Its INI parser reads `displayPadDebugInfo`, and a surviving code path tests that variable before calling a substantial handler. A separate diagnostic ISO enables that setting without changing the executable. **Inference:** this is a useful way to test the retained controller-debug display. **Unknown:** the handler's visible behavior and whether a usable developer menu can be restored. No working menu is claimed.

## Current state

| Class | Finding | Evidence |
| --- | --- | --- |
| Proven | Actual executable is SLUS_209.04. | ISO directory listing and SYSTEM.CNF |
| Proven | ShowMenuOnBoot is already 1 in the original INI. | Original SB04.INI |
| Proven | displayPadDebugInfo is read as an integer, default 0. | Call at 0x46C03C; store at 0x46C048 |
| Proven | Runtime state lives at 0x006378F8. | GP 0x0063DBF0 and displacement -0x62F8 |
| Proven | Function 0x00403BB0 reads that state and calls 0x004A9160 when nonzero. | Load 0x00403BB8; conditional branch 0x00403BBC; call 0x00403BCC |
| Proven | Several nearby routines are return-only stubs. | 0x00403B70, 0x00403B80, 0x00403B90, 0x00403BA0, 0x00403BF0 |
| Inference | Debug functionality was partially stripped; the remaining display may provide a runtime probe. | Stub pattern plus retained branch and upstream debug reference |
| Unknown | Complete menu implementation, activation controls, and visible probe result. | Runtime test pending |

## How it works

The diagnostic replaces one existing comment line with `displayPadDebugInfo=1`, padding the replacement to keep the INI exactly the same length. This sends the retained debug-update path through its existing conditional call. No executable instructions, camera settings, or level selection are modified.

The upstream decompilation's DWARF reference helps identify likely function roles, but addresses are not universally identical to this retail binary. Direct examination of this executable is authoritative. In particular, upstream xDebug addresses must not be patched blindly.

## Evidence and conditions

- Source ISO: 1,249,804,288 bytes; SHA-256 `c0494ad78fab34dc19fb52b831facb1b27500e66bf0a57a77e627e7b805096f0`.
- Executable: 5,467,144 bytes; SHA-256 `2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956`.
- ELF entry: 0x00100008. Loaded file-to-address bias: 0x000FFF80.
- SB04.INI: byte offset 875,300,864; length 53,452 bytes.
- Local diagnostic ISO SHA-256: `eecc8a3fddec908daf626762c39dbed697b32746604b9bafd3f29ee82b3fa6c9`.
- Full-image comparison: exactly 40 changed bytes, offsets 875,300,906–875,300,948 inclusive with gaps, all inside the replaced INI comment.
- The original archive, base ISO, executable and INI length are unchanged.
- Capstone's generic MIPS64 decoder was used for supported instructions. R5900-specific instructions are not assumed to match its unrelated MIPS extension decoding.
- No emulator or console runtime test and no console screenshot were produced.

## Negative results and open questions

`DebugMode` remains in the INI, but its literal key was not found in the executable ASCII string scan. This does not rule out indirect handling. `ShowMenuOnBoot=1` is stock and cannot be presented as a discovered debug-menu unlock. `Debug%02d` has animation-style registration code and does not by itself establish a menu.

A normal pip install stalled and was stopped; the official Capstone 5.0.6 Windows wheel was fetched from PyPI and extracted locally instead. No installed system package was changed.

## Next hardware gate

Boot the local controller-debug probe using the owner's normal CFW PS3 PS2 ISO route, without additional cheats. Inspect title/menu and gameplay for controller/status output; record boot result, visible text, and a photo/video if output appears. The probe is not a restored menu. Its result will determine whether to investigate the retained handler or prioritize a different UI path.

No copyrighted ISO or extracted game assets are committed to this repository. This page publishes documentation and hashes.

## Reference

[Movie game decompilation — xDebug DWARF reference](https://github.com/bfbbdecomp/tssm/blob/main/dwarf/SB04_Multi_Sku/Engine/Core/x/xDebug.cpp).


## Overlay confirmed; Select-toggle candidate — October 21, 2026

### RR — Really Readable rundown

**Proven owner report:** the owner explicitly clarified **“Controller/status overlay appeared.”** This resolves the earlier ambiguity around “it worked”: the always-on controller-debug display is reported visible on the CFW PS3, not merely a successful boot. No screenshot/video has been supplied.

**Proven static result:** a custom Select-to-toggle candidate replaces only the 64-byte update function at 0x00403BB0. Twenty exact-instruction simulation cases passed. The Windows patcher ran against the known probe ISO, and full-image comparison found **49 differing bytes**, all inside that function window. Wrong-input and existing-output cases were rejected. **Unknown:** runtime behavior of this new toggle, including edge timing across game modes. Full original-menu restoration remains unconfirmed.

### What the patch does

It reads the controller pointer at 0x007AB520, safely returns if null, reads pressed buttons at controller +0x30, and uses Select mask 0x2 to toggle the existing display flag at 0x006378F8. It conditionally tail-calls the original display handler at 0x004A9160. The replacement remains within the original function footprint and does not overwrite the adjacent return-only initializer. Select input is not consumed; its normal game action can still occur.

The stock binary has four direct calls to this update routine (0x002C4DF0, 0x002D39E0, 0x002D4F2C, 0x00300BB4). Their mode-dependent runtime scheduling is not independently verified. The next test must check whether each tap toggles once, including title/menu and gameplay. Static simulation does not prove whole-game scheduling.

### Evidence

- Patcher input: previously tested pad-debug probe, SHA-256 `eecc8a3fddec908daf626762c39dbed697b32746604b9bafd3f29ee82b3fa6c9`.
- Output candidate: SHA-256 `78b5b1530a179ad25a2e06167b24aacc369977d57fcdc9b0433d0f7b120303f7`.
- Patch window: ISO byte offset 878,517,296; 64 bytes.
- Input file and existing outputs are protected; Windows PowerShell creates a separate ISO.
- 20 cases: null/present pointer, enabled/disabled flag, Select/no Select/other buttons. All passed the emitted-instruction branch-delay simulation.
- Direct operator invocation generated the candidate successfully; wrong source hash and overwrite attempts failed as expected.
- Small patcher ZIP: 3,303 bytes; server size and MD5 matched the local upload. No game ISO or assets are bundled.
- No new hardware run or screenshot is claimed.

The readable ASCII string scan across all seven extracted MN menu HIP/HOP files found cheat sound/group names, but no debug/tweak/developer-menu names. This is not a complete asset-level absence proof: hashed names or code-built UI remain possible.

### Next test

Run the small patcher against the already-downloaded pad-debug probe ISO. Boot the separate output on CFW and tap/release Select twice: check whether the overlay hides and returns, and note normal Select behavior, flicker, or crashes. This is a **custom overlay toggle**, an input-integration experiment toward an interactive interface; it is not the original developer menu.

[Upstream input structure and Select mask](https://github.com/bfbbdecomp/tssm/blob/main/src/SB/Core/x/xPad.h). Actual pointer/load instructions were checked in the retail executable rather than transferring upstream addresses blindly.
