#!/usr/bin/env python3
"""Read-only comparison of two locally held Xbox Movie INIs or executables.

Never bundles game files and never modifies its inputs.
"""
import argparse
import difflib
import hashlib
from pathlib import Path
import struct


def hashes(path):
    h1 = hashlib.sha1()
    h256 = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            h1.update(block)
            h256.update(block)
    return h1.hexdigest(), h256.hexdigest()


def read_xbe_header(path):
    with path.open("rb") as stream:
        data = stream.read(0x200)
    if len(data) < 0x12C or data[:4] != b"XBEH":
        raise ValueError(f"{path}: not an Xbox XBE header")
    u32 = lambda off: struct.unpack_from("<I", data, off)[0]
    return {
        "base_address": f"0x{u32(0x104):08X}",
        "image_size": u32(0x10C),
        "header_timestamp_raw": u32(0x114),
        "certificate_virtual_address": f"0x{u32(0x118):08X}",
        "section_count": u32(0x11C),
        "section_table_virtual_address": f"0x{u32(0x120):08X}",
        "entry_point_encoded": f"0x{u32(0x128):08X}",
    }


def compare_ini(a, b):
    left = a.read_bytes().decode("utf-8-sig", errors="replace").splitlines()
    right = b.read_bytes().decode("utf-8-sig", errors="replace").splitlines()
    print("\nINI line differences (local only; do not publish copyrighted original files):")
    changes = list(difflib.unified_diff(left, right, fromfile=a.name, tofile=b.name, lineterm=""))
    for line in changes[:250]:
        print(line)
    if len(changes) > 250:
        print(f"... {len(changes) - 250} additional diff lines omitted")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("first", type=Path)
    p.add_argument("second", type=Path)
    p.add_argument("--type", choices=("ini", "xbe"), required=True)
    a = p.parse_args()
    for path in (a.first, a.second):
        if not path.is_file():
            p.error(f"Missing file: {path}")
        h1, h256 = hashes(path)
        print(f"{path.name}: bytes={path.stat().st_size} SHA1={h1} SHA256={h256}")
    if a.type == "ini":
        compare_ini(a.first, a.second)
    else:
        x, y = read_xbe_header(a.first), read_xbe_header(a.second)
        print("\nXBE header fields (certificate contents and code sections not compared):")
        for key in x:
            print(f"{key}: {x[key]}  /  {y[key]}")


if __name__ == "__main__":
    main()
