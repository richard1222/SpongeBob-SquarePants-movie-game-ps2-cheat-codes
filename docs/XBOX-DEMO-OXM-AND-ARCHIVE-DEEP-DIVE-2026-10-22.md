# Deep research: 2004 Movie prototype, Xbox demo distributions and preservation indexes
Date: 2026-10-22

## Major new verified lead — original Xbox playable demos

**Xbox Exhibition Demo Disc Volume 7** contains a playable *The SpongeBob SquarePants Movie* demo. Its catalog record identifies item P60-00007, barcode 805529993365. Redump catalogs the disc as **XK-045**. This is a definite alternate playable distribution, not automatically a prototype and not necessarily earlier code than retail.

- Disc catalog: https://vgcollect.com/item/29550
- Redump catalog: https://redump.info/discs?dumper=h0lylag
- Xbox Exhibition volume list: https://gamicus.fandom.com/wiki/Xbox_Exhibition_disks

**Official Xbox Magazine (OXM)**: a contemporary January 10, 2005 forum post previewed a *SpongeBob Movie* playable demo on the following month's OXM disc. This supplies an independently contemporary lead for another publication/disc release. Disc number and binary identity are **not established**; avoid assuming it is a unique compiled build.

- Contemporary forum source: https://chat.freeola.com/thread/1112300000/latest-oxm-disc-review-type-thng.html

**XboxArchive/hashes** contains independently catalogued file manifests from compilation media with `Build_OXM/sb04.ini`, `Build_OXM/MN/*HIP`, and `SpongeBob/sb04.ini`, plus separate retail-region file hash manifests. This is a source for exact **hash-based build comparison**, but the path alone does not prove the executable is a debug build. Compare these manifests to the individual demo content and retail Xbox images before claiming differences.

- https://github.com/XboxArchive/hashes/blob/cb1925f10b80a8bbe1eef7dc1ecd2d916d454773/redump/ffcbc07887fa554b1715c61fe6aadbdb5fbf1dc7
- https://github.com/XboxArchive/hashes/blob/cb1925f10b80a8bbe1eef7dc1ecd2d916d454773/redump/d2d6d97d26b65e208d1f6bb603eee00aa927ebb1

## Early press build evidence

- GameSpot described a preliminary playable version on July 26, 2004, and an updated **work-in-progress PS2** version shown at THQ's press event in coverage published August 25, 2004. These reports are direct contemporaneous evidence early playable code existed in circulation among press and publisher, not proof that a public disc image survives.
- https://www.gamespot.com/articles/the-spongebob-squarepants-movie-first-look/1100-6103444/
- https://www.gamespot.com/articles/the-spongebob-squarepants-movie-updated-hands-on/1100-6105652/
- Heritage Auctions separately documented the dated **August 31, 2004 PS2 Test Build** (lot 79058); a dump has not been verified: https://comics.ha.com/itm/video-games/other/the-spongebob-squarepants-movie-game-wata-certified-prototype-test-build-8-31-2004-the-harvey-collection-ps2-thq-2004-usa/a/44210-79058.s

## GitHub and tooling

- `XboxArchive/hashes`: Xbox demo/retail file-level SHA-1 manifests, useful to identify a different game file set without sharing images.
- `igorseabra4/IndustrialPark`: parses/edits the game's HIP/HOP assets across PS2, GC, Xbox: https://github.com/igorseabra4/IndustrialPark
- `bfbbdecomp/tssm`: GameCube decompilation reference, **not** an original leaked PS2 source tree: https://github.com/bfbbdecomp/tssm
- `ItsPepperpot/TSSM-Dolphin-Toolkit`: GameCube configuration reference; PS2 portability is unverified: https://github.com/ItsPepperpot/TSSM-Dolphin-Toolkit

## Reddit and public torrent/private-tracker references

Public Reddit searches uncovered contemporary hobbyist disc collections (for example an OXM collector with 60 discs) but **no verifiable dumped pre-release Movie PS2 or original Xbox XDK image** from the posts inspected. Some purported SpongeBob demo references actually concern *Battle for Bikini Bottom*, unrelated later games, or the separately developed PC Movie game. Do not conflate them.

- OXM collector discussion: https://www.reddit.com/r/originalxbox/comments/1rdx311/i_have_almost_every_official_xbox_magazine_demo/
- Generic original Xbox demo memory: https://www.reddit.com/r/tipofmyjoystick/comments/ko4yqm

Public search-engine coverage of torrent catalogues and references to invite-only trackers has not yielded a **verifiable release name plus image hash** for an early Movie PS2 or Xbox XDK dump. Access to authenticated private indexes was unavailable; this is **not** an exhaustive private-tracker search. No torrent payloads were fetched, no credentials used, and no content authenticity inferred from filenames.

## Prioritized next verification

1. Verify Exhibition Vol. 7 original Xbox demo's executable build timestamp, title ID, executable hash and file inventory against retail; don't mix up the disc launcher Title ID (e.g. 584B002D) and the Movie demo's own title ID.
2. Identify the actual OXM issue/disc from the January 2005 preview and reconcile it with the `Build_OXM` hashes. If matched, compare `sb04.ini` and HIP/HOP SHA-1 with retail.
3. If executable or content differences are found, search for retained debug strings and configure **comparison notes only**. Avoid treating a demo's time/level limits as developer features.
4. Continue investigating the August 2004 PS2 test-build provenance through official public records and request preservation metadata, not private bidder details.
5. Record platform, dates, redump IDs, executable hashes, and whether evidence is physical, index-only or byte-verified. Do not post proprietary ISOs or XBE executables.

## Caveats

No Xbox demo image was downloaded or inspected byte-for-byte in this session, and no actual private-tracker login occurred. The working PS3 HealthMenu and DamageMenu ISOs remain untouched.
