#!/usr/bin/env python3
"""Ship the finished 20 November 2026 news image (v2) to the output folder.

The picture is rendered in advance by draw.py and stored here as
entry.png. When make.fun runs this file, all it does is put an exact
copy at $MAKEFUN_OUTPUT_DIR/entry.png (falling back to /output when
that variable is unset). Pure standard library, no network, no
third-party packages.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def output_path():
    """Where the image goes, honouring MAKEFUN_OUTPUT_DIR."""
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def main():
    source = HERE / "entry.png"
    if not source.is_file():
        raise SystemExit("entry.png is missing next to main.py")
    target = output_path()
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("copied entry.png has the wrong size")
    print(f"entry.png ({target.stat().st_size} bytes) copied to {target}")


if __name__ == "__main__":
    main()
