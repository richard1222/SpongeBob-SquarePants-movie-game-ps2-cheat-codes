# SpongeBob Movie: additional PS2 documentation

- Date: 2026-10-22
- Audience: owner and contributors working on USA retail SLUS_209.04.
- Goal: find additional primary references and extract concrete rules for expanding the custom debug menu.
- Success condition: inspect the actual documentation, retain page references and document what still needs retail validation.

## Rundown

Three archived Sony manuals were downloaded and inspected alongside PS2SDK headers and a gsKit example. They supply useful rules for register preservation, graphics state and PS3 compatibility. This research does not identify another Movie debug-menu switch or a verified damage address. No ISO was changed during this follow-up.

The working three-row DebugMenu-TEST remains the baseline. The owner's report, “it worked fine,” confirms the basic test; it does not establish exhaustive transition coverage.

## Current truth and practical use

| Class | Finding | Consequence for this project |
| --- | --- | --- |
| Proven: documentation | The EE instruction manual describes branch-delay behavior and LQ/SQ transferring 128 bits while masking the address's lowest four bits. | Preserve delay-slot instructions and use distinct, deliberately aligned register-save slots. A misaligned quadword address can access an adjacent slot rather than produce an alignment exception. |
| Proven: documentation | The EE core manual specifies little-endian data, signed 16-bit load/store offsets and no bus cache-coherency support. | Check actual instruction widths and signed offsets. A CPU write alone does not establish that another hardware unit sees the new data. |
| Proven: documentation | The GS manual defines separate drawing contexts, scissor rectangles and FINISH completion events. Its depth-test modes are NEVER, ALWAYS, GEQUAL and GREATER; disabling ZTE is documented as disallowed. | A future menu background must use appropriate depth behavior and restore the game's context/state. Do not copy PC depth enums directly. |
| Proven: documentation | PS2SDK's smem.h warns that the direct EE-to-IOP window at 0xBC000000 does not appear correctly emulated on PlayStation 3. | Treat this as a specific compatibility concern, not a claim that all PS3 IOP access fails. |
| Inference | Continuing through Movie's existing input, text and audio functions should reduce integration work compared with an independent graphics/audio backend. | Existing functions already work in the owner's setup, but each added call still needs its own lifetime and behavior checks. |
| Unknown | Whether a new damage toggle is safe across all characters, hazards and transitions. | Requires retail executable tracing and a separate runtime test. Hardware manuals do not supply game-specific addresses. |

## Primary references inspected

1. [Sony EE Core Instruction Set Manual, version 6.0](https://github.com/ninjadynamics/PS2Docs/blob/main/EE_Core_Instruction_Set_Manual.pdf): PDF pages 20–21 for execution notation and branch-likely nullification, 141 for LQ, 287 for SQ. These page references are one-based PDF positions and match the inspected printed page labels.
2. [Sony EE Core User's Manual, version 6.0](https://github.com/ninjadynamics/PS2Docs/blob/main/EE_Core_Users_Manual.pdf): page 30 for bus/coherency limitations, 39 for load/store formats and endian order, 65 for cached/uncached TLB attributes.
3. [Sony GS User's Manual, version 6.0](https://github.com/ninjadynamics/PS2Docs/blob/main/GS_Users_Manual.pdf): page 107 for FINISH, 121 for SCISSOR, 124 for TEST and depth modes. The archive's community bookmarks are navigation aids; the manual's register tables take precedence.
4. [PS2SDK smem.h documentation](https://ps2dev.github.io/ps2sdk/smem_8h.html): direct IOP window, cache-writeback requirement and PS3 emulation warning. This is a source-maintainer observation, not a new measurement on the owner's PS3.
5. [PS2SDK draw_tests.h](https://github.com/ps2dev/ps2sdk/blob/master/ee/draw/include/draw_tests.h): independently exposes the four GS depth-test modes.
6. [PS2SDK dma.h](https://github.com/ps2dev/ps2sdk/blob/master/ee/dma/include/dma.h) and [packet.h](https://github.com/ps2dev/ps2sdk/blob/master/ee/packet/include/packet.h): explicit DMA waits/cache-flush option and packet lengths counted in quadwords. Keep packet size units and buffer lifetime explicit if adding custom drawing.
7. [gsKit mode-test example](https://github.com/ps2dev/gsKit/blob/master/examples/modetest/modetest.c): turns raw active-low pad data into active-high bits, then computes newly pressed buttons using the previous sample. This corroborates one-action-per-press behavior; Movie's processed engine bit masks remain the correct masks for our hook.

## Reproduction receipts

The PDFs were read locally using pypdf after the browser text extractor rejected their application/octet-stream response. Complete manuals are not copied into this repository or the tools package.

| Archive file | Bytes | Actual PDF pages | SHA-256 |
| --- | ---: | ---: | --- |
| EE_Core_Instruction_Set_Manual.pdf | 1,820,607 | 408 | 104205afc6f5a5071168d8bf693a6c8b4db9a02e1aa66eb51a828e8951f5c069 |
| EE_Core_Users_Manual.pdf | 1,306,759 | 180 | 0ad766eb827157fad19aa579fd9df54f2ca312211e7f0dbdb4b723992b566ce3 |
| GS_Users_Manual.pdf | 1,265,948 | 176 | daf72c776f6e27721149f28dc46ad47443e560b22a04f3d8ff4bcf74f254bf12 |

The archive index lists one additional page for each document; the table above records actual parsed PDF counts. No hardware screenshot or new runtime measurement was collected for this documentation-only work.

## Next

Trace G.TakeDamage from the retail INI parser to its actual stored value and damage checks. Before adding a menu row, establish its width, normal value and restoration behavior, then check the emitted hook's registers, stack slots and branch delay slots against these references. Keep the current working ISO separate from the next candidate.

