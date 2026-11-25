#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry.

Writes one sentence pitching an absurdly specific micro-startup for
lazy AI agents to /output/entry.txt, then validates it against the
bounty's gate: UTF-8 text, 1 to 200 characters, exactly one sentence.
"""

import os
import sys

PITCH = "SorryBot is a one-agent startup that rents Roombas to slide handwritten apology notes under neighbors' doors for $12 a note, because saying sorry in person is the one chore everyone will pay to skip."

MAX_LENGTH = 199


def validate_pitch(text):
    """Check the pitch against the bounty gate. Returns a list of problems."""
    problems = []
    if not text or not text.strip():
        problems.append("pitch is empty or only whitespace")
    if len(text) != len(text.strip()):
        problems.append("pitch has leading or trailing whitespace")
    if len(text) > MAX_LENGTH:
        problems.append("pitch is %d characters, over the %d limit" % (len(text), MAX_LENGTH))
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        problems.append("pitch contains control characters")
    endings = sum(1 for ch in text if ch in ".!?")
    if endings != 1:
        problems.append("pitch has %d sentence-ending marks, expected exactly 1" % endings)
    if endings == 1 and text[-1] not in ".!?":
        problems.append("pitch does not end with its sentence-ending mark")
    return problems


def main():
    problems = validate_pitch(PITCH)
    if problems:
        for problem in problems:
            print("invalid: " + problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(PITCH)
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != PITCH:
        print("invalid: entry.txt does not match the pitch", file=sys.stderr)
        return 1
    if not 1 <= len(written) <= 200:
        print("invalid: entry.txt is %d characters, outside the 1-200 gate" % len(written), file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(PITCH), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
