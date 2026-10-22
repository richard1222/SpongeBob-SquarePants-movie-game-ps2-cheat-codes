# v0.4 release: publication receipt

- Audience: owner and contributors; October 22, 2026.
- Scope: complete project tools release and public download verification.
- Success condition: publish all project tools, pass checks on the exact extracted archive, and verify the downloaded release assets.

## Rundown

**Proven:** [v0.4 is published](https://github.com/richard1222/SpongeBob-SquarePants-movie-game-ps2-cheat-codes/releases/tag/v0.4) with the complete tools ZIP, checksum and package receipt. All three public downloads match the local files and GitHub SHA-256 digests. All eight patch stages rebuilt from the extracted archive with expected output hashes; original stage inputs stayed unchanged. The existing owner-tested game patch bytes and earlier releases are preserved.

In plain language, someone can download the complete toolset and build the same combined menu/refill image that the owner tested. Developer test reruns preserve the included owner-validation record.

## Evidence

| Class | Finding | Evidence |
| --- | --- | --- |
| Proven | Complete tools package: 120 entries, eight cumulative stages and two independent probes. | ZIP size 235,414 bytes; source commit 8201ee937d99f85dc101696f79a3ae9a3afaab46. |
| Proven | Archive content and downloaded bytes match. | ZIP SHA-256 2f0eb5ebd90e11adb0dda19276afc856ad7250f83f478fd6bd85095f20848cb2; all three attachment download checks passed. |
| Proven | Exact extracted tools pass release checks. | Eight full-image stages; default 14 fixtures; combined 14 fixtures; eight message tests; 6,656 menu cases; 352 callback comparisons; 704 interactions; 41 HP cases; 36 guards; 96 damage cases. |
| Recorded owner report | Combined PS3 test completed without issues. | “everything worked in order no issues.” No new console test was performed during release packaging. |
| Unknown | Broad compatibility and exact final HP. | No separately supplied numeric final HP, independent console trace, original PS2/PCSX2 or exhaustive save/character/hazard testing. |

[Package verification](PACKAGE-VERIFICATION.json) and [publication verification](PUBLISHED-RELEASE.json) contain the artifact identities and download results. No game assets or external tool/SDK binaries are included.

## Next

The requested release is complete. Future game work can use this owner-tested baseline; wider runtime coverage and original developer-feature research remain open.
