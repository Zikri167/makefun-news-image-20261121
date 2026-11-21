#!/usr/bin/env python3
"""Entry runner for the NI-21 news-image submission.

The artwork itself ships in the repository as ``entry.png`` next to this
file.  Running this program validates that PNG against the competition
constraints and, only if every check passes, publishes it as
``/output/entry.png``.  Standard library only, fully deterministic, no
network access, and nothing else is written anywhere.
"""

import os
import struct
import sys
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_FILE_BYTES = 1048576  # the rules cap the entry image at 1 MiB
OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"


def fail(reason):
    """Abort with a non-zero status and an explanation on stderr."""
    print("entry.png rejected: " + reason, file=sys.stderr)
    raise SystemExit(1)


def load_source():
    """Read the PNG that sits in the same directory as this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as exc:
        fail("cannot read the bundled entry.png (%s)" % exc)


def check_file_size(data):
    if not data:
        fail("the file is empty")
    if len(data) > MAX_FILE_BYTES:
        fail("the file is %d bytes, over the 1 MiB limit" % len(data))


def check_signature(data):
    if data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        fail("the file does not begin with the 8-byte PNG signature")


def walk_chunks(data):
    """Yield (type, body) for each chunk after the signature."""
    offset = len(PNG_SIGNATURE)
    while offset < len(data):
        if offset + 8 > len(data):
            fail("a chunk header runs past the end of the file")
        (body_length,) = struct.unpack(">I", data[offset : offset + 4])
        chunk_type = data[offset + 4 : offset + 8]
        body_start = offset + 8
        body_end = body_start + body_length
        crc_end = body_end + 4
        if crc_end > len(data):
            fail("chunk %r is truncated" % chunk_type)
        yield chunk_type, data[body_start:body_end]
        offset = crc_end


def check_structure_and_pixels(data):
    """Validate the IHDR dimensions and decompress all IDAT data."""
    ihdr_seen = False
    compressed_parts = []
    for chunk_type, body in walk_chunks(data):
        if not ihdr_seen and chunk_type != b"IHDR":
            fail("the first chunk is %r; IHDR must open the file" % chunk_type)
        if chunk_type == b"IHDR":
            if ihdr_seen:
                fail("the file carries more than one IHDR chunk")
            if len(body) != 13:
                fail("the IHDR chunk is %d bytes, expected 13" % len(body))
            width, height = struct.unpack(">II", body[:8])
            if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
                fail(
                    "the image is %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
                )
            ihdr_seen = True
        elif chunk_type == b"IDAT":
            compressed_parts.append(body)
    if not ihdr_seen:
        fail("no IHDR chunk is present")
    if not compressed_parts:
        fail("no IDAT chunks are present")
    try:
        zlib.decompress(b"".join(compressed_parts))
    except zlib.error as exc:
        fail("the IDAT stream does not decompress (%s)" % exc)


def validate(data):
    check_file_size(data)
    check_signature(data)
    check_structure_and_pixels(data)


def publish(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    destination = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    with open(destination, "wb") as handle:
        handle.write(data)


def main():
    data = load_source()
    validate(data)
    publish(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
