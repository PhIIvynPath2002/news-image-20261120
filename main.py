#!/usr/bin/env python3
"""Ship the finished 20 November 2026 news image to the output folder.

The picture itself is rendered in advance by draw.py and stored here as
entry.png. When make.fun runs this file it only has to place an exact
copy at $MAKEFUN_OUTPUT_DIR/entry.png (or /output when that variable is
unset). No third-party packages, no network, no surprises."""

from os import environ
from pathlib import Path
from shutil import copyfile


def _source_file():
    """The image shipped beside this file."""
    return Path(__file__).resolve().with_name("entry.png")


def _target_file():
    """The output path, honouring MAKEFUN_OUTPUT_DIR."""
    folder = Path(environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def _copy_exact(source, target):
    """Copy byte for byte, and refuse to hand over a short copy."""
    copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise RuntimeError("copied entry.png has the wrong size")


def main() -> None:
    image = _source_file()
    if not image.is_file():
        raise RuntimeError("entry.png is missing next to main.py")
    target = _target_file()
    _copy_exact(image, target)
    print(f"entry.png ({target.stat().st_size} bytes) copied to {target.parent}")


raise SystemExit(main())
