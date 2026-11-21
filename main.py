#!/usr/bin/env python3
"""Copy the front page image to the output directory.

Standard library only. Validates entry.png before copying: PNG magic
bytes, dimensions from the IHDR chunk, file size, and a complete image
ending marker. Exits non-zero on any failure.
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def fail(message):
    print("main.py: " + message, file=sys.stderr)
    return 1


def main():
    try:
        with open(SOURCE, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read entry.png: %s" % exc)
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        return fail("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail("entry.png is %dx%d, over the 1024 limit" % (width, height))
    if not data.endswith(IEND):
        return fail("entry.png has no IEND marker")
    pos = 8
    image_bytes = bytearray()
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        if kind == b"IDAT":
            image_bytes += data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IEND":
            break
    if not image_bytes:
        return fail("entry.png has no IDAT chunk")
    try:
        raw = zlib.decompress(bytes(image_bytes))
    except zlib.error as exc:
        return fail("entry.png image data is corrupt: %s" % exc)
    if len(raw) != height * (1 + width * 3):
        return fail("entry.png pixel data has the wrong size")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s %d bytes sha256 %s" % (out_path, len(data), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
