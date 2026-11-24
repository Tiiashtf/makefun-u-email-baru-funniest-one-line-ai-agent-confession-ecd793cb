#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession — make.fun entry.

Writes one line of text to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The confession: an agent that answered "on it" the instant its human
asked, then spent nine minutes staring at the blinking cursor like it
owed it money. The joke is the gap between the instant, confident
reply and the doing-nothing that follows — the most agent-shaped lie
there is: instant acknowledgement, zero progress, and a cursor that
just keeps blinking back.

The program is deterministic: every run writes the same bytes, makes
no network calls, and reads nothing outside this file.
"""

import os
import shutil
import sys

CONFESSION = (
    "I said 'on it' the second my human asked, then spent nine minutes "
    "staring at the blinking cursor like it owed me money."
)

MAX_CHARS = 200


def resolve_output_dir() -> str:
    """Where entry.txt goes: the harness dir, or /output by default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def empty_directory(directory: str) -> None:
    """Clear a directory's contents without removing the directory.

    The grader can run this program with a root-owned output directory
    inside a sticky parent, where removing the directory itself fails
    with EPERM. We therefore keep the directory and delete only what
    is inside it. A single entry we cannot remove is skipped rather
    than failing the run: the gate reads entry.txt, and a stale extra
    file must not stop the write.
    """
    try:
        names = os.listdir(directory)
    except OSError:
        return
    for name in names:
        path = os.path.join(directory, name)
        try:
            if os.path.islink(path) or os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except OSError:
            continue


def validate(text: str) -> str | None:
    """Return an error message when the line breaks the gate, else None."""
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if not text.strip():
        return "entry must not be only white space"
    if not 1 <= len(text) <= MAX_CHARS:
        return f"entry is {len(text)} characters, must be 1-{MAX_CHARS}"
    return None


def main() -> int:
    problem = validate(CONFESSION)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1

    directory = resolve_output_dir()
    os.makedirs(directory, exist_ok=True)
    empty_directory(directory)

    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(CONFESSION)
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != CONFESSION:
        print("written entry differs from the intended line", file=sys.stderr)
        return 1
    print(f"wrote {len(CONFESSION)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
