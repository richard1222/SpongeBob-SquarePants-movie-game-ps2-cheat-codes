# HealthMenu static safety audit — 2026-10-22

**Scope:** GitHub `HealthMenuPatch.json`, `DEVELOPER-SPEC.json`, `test_health_menu.py` and `test_patchers.py`. This is a static review, **not** a newly executed test or a hardware verification. Existing HealthMenu and DamageMenu game images are unchanged.

## Patch windows: pass

Sorted windows (end-exclusive):

| ISO start | End | Length | Changed bytes |
|---:|---:|---:|---:|
| 878517296 | 878517360 | 64 | 0 |
| 879194816 | 879195008 | 192 | 0 |
| 879195176 | 879195240 | 64 | 16 |
| 880619504 | 880619932 | 428 | 283 |
| 880791698 | 880791803 | 105 | 27 |

All are non-overlapping and have equal-length old/new payloads. Total: **326 changed bytes**, matching the existing receipt. Two unchanged windows intentionally carry source-byte guards; zero changed bytes there is not an error. Patch code uses SHA-256 checks, source byte checks, a separate temporary output, an expected final hash and overwrite refusal.

## Button/input paths: evidence and limits

The test interpreter enumerates 6,656 combinations of visibility, row, button press, pad presence, music state and audio handles, and a 12-step interaction sequence. It checks row navigation, Select visibility, the action button, damage toggle and diagnostics flags. The backend audio/scene/position calls are *modeled*, not executed. The full hardware matrix remains necessary; in particular, test music toggle, Select hide/show and level transitions on the new HP image.

## Health and pointer guard: review finding

The `valid(p)` predicate in the test harness checks a four-byte aligned **base pointer** within `[0x100000, 0x1fff000)`. The HP getter then reads at **base + 0x460**. Its test-accepted boundary base `0x1ffeffc` produces a field read at `0x1fff35c`, outside that *base-pointer admissibility interval*. This does **not** prove an invalid dereference: the permitted base interval is a heuristic, not a verified mapped-memory boundary. It does mean the existing guard test alone does not prove that the full referenced object is resident and valid. Similar risks apply if a pointer remains aligned/in-range but refers to a freed or wrong-type object.

**Recommendation:** do not change the already working patch based only on this. On subsequent versions, verify the actual mapped memory range and object lifetime; add modeled pointer-lifetime and out-of-bounds field-read tests, and consider guarding the dereference span if justified by runtime memory mapping. Never treat the range test as proof of object validity.

## Test harness limitation

The health instruction interpreter models external routines and a sparse memory dictionary; it is not a cycle-accurate PS2 emulator. It does not independently prove behavior under every memory transition. `python -O` previously bypassed assertions; the two test entry points now explicitly refuse optimization.

## Next steps

1. Run `python tools/test_patchers.py` and the matching-ELF `tools/health-menu/test_health_menu.py` on Neptune, without `-O`.
2. Exercise new-image music pause/resume and Select hide/show on PS3, logging observed results.
3. If investigating rare freezes, trace the `0x007ABC10` root pointer and `+0x460` read across death, loading and player transitions with a debugger; don't assume alignment/range tests suffice.
4. Keep known-good DamageMenu and currently successful HealthMenu images unchanged until an actual regression is reproduced.
