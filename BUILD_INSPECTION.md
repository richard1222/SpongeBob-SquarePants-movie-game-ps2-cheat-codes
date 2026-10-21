# Prototype acquisition and initial inspection

October 21, 2026.

## Download verification

All three files were downloaded and SHA-1 checked against Archive.org metadata:

| File | Bytes | SHA-1 |
| --- | ---: | --- |
| English compilation prototype archive | 2182266325 | 90b5dc4f414a49fb4fb741c7f8076dcb72d5832d |
| French/Dutch Movie NR-disc archive | 1175946275 | 32e3c2a71998c375b1d0217596aa6a83a9c675e4 |
| GBA Movie beta | 6871418 | 68c7be5be01db6d428a4fe7c5b54ec58f6f793e4 |

Sources: [English compilation](https://archive.org/details/thq-2-in-1-spongebob-europe-prototype-2.7z), [NR disc](https://archive.org/details/the-sponge-bob-square-pants-movie-nr-disc.-7z), [GBA](https://archive.org/details/TheSpongeBobSquarePantsMovieGBABetaUSA).

These checks establish download integrity against those records, not independent prototype authenticity.

## GameCube contents

Both archives extracted successfully.

- English compilation slot3.gcm: Movie content, disc header GU4P78 / THQ Multipak.
- English compilation slot4.gcm: Battle for Bikini Bottom content, same compilation header.
- Localization GGVX78.iso: The SpongeBob SquarePants Movie.

Each disc image is 1459978240 bytes. The English Movie disc includes Game.dol (3952128 bytes), SB04.ini (53449 bytes), and sb04gc_nm.elf (6240736 bytes).

The ELF retains a symbol table. Its debug initialization/update/exit/timestamp functions are each only four bytes long in the symbol table; this warrants checking the actual instructions before treating debug names as functional features.

The configuration contains DebugMode, ShowMenuOnBoot, and G.Cheat entries. Their presence alone does not establish a functioning developer menu. ShowMenuOnBoot may refer to the ordinary frontend. No camera or level-selection patches were made.

## Dolphin setup and testing

A portable Dolphin 2609 Linux x86-64 AppImage from pkgforge-dev/Dolphin-emu-AppImage was downloaded and extracted. This is a third-party package, not the official Dolphin distribution. The command-line help runs with QT_QPA_PLATFORM=offscreen.

Launch attempts with the English Movie disc and extracted Game.dol using the Null graphics backend timed out without a confirmed game boot. No gameplay or menu behavior is verified.

Xvfb and supporting libraries were obtained and extracted locally. Xvfb failed to establish local display sockets in this environment, so a graphical gameplay test remains blocked.

The emulator and game images are not committed to this repository.

## Next verification

- Obtain a working graphical emulator session.
- Boot the English Movie disc (slot3.gcm), record displayed version and frontend behavior.
- Confirm the debug-function instructions and trace configuration handling.
- Keep PS2 and GameCube addresses and patch formats separate.
