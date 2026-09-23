#!/usr/bin/env python3
"""Add the pre-v1 Android boot image DT section used by Exynos 8895."""

import hashlib
import struct
import sys
from pathlib import Path


def aligned(value: int, page_size: int) -> int:
    return (value + page_size - 1) & -page_size


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(f"usage: {sys.argv[0]} INPUT DTB OUTPUT")

    image = bytearray(Path(sys.argv[1]).read_bytes())
    dtb = Path(sys.argv[2]).read_bytes()
    if image[:8] != b"ANDROID!":
        raise SystemExit("input is not an Android boot image")

    kernel_size, ramdisk_size, second_size = struct.unpack_from("<IxxxxIxxxxI", image, 8)
    page_size, header_version = struct.unpack_from("<II", image, 36)
    if page_size < 2048 or page_size & (page_size - 1):
        raise SystemExit(f"invalid page size: {page_size}")
    if header_version != 0:
        raise SystemExit(f"legacy DT requires header version 0, got {header_version}")

    offset = page_size
    sections = []
    for size in (kernel_size, ramdisk_size, second_size):
        sections.append(bytes(image[offset : offset + size]))
        offset += aligned(size, page_size)
    if offset != len(image):
        raise SystemExit(f"unexpected trailing data: {len(image) - offset} bytes")

    digest = hashlib.sha1()
    for section in (*sections, dtb):
        digest.update(section)
        digest.update(struct.pack("<I", len(section)))

    struct.pack_into("<I", image, 28, 0x10F00000)
    struct.pack_into("<I", image, 40, len(dtb))
    image[576:608] = digest.digest().ljust(32, b"\0")
    image.extend(dtb)
    image.extend(b"\0" * (-len(dtb) % page_size))
    Path(sys.argv[3]).write_bytes(image)


if __name__ == "__main__":
    main()
