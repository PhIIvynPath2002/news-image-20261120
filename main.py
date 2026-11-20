#!/usr/bin/env python3
"""Entry program for the news-image-20261120 bounty.

The summary image (entry.png) is drawn ahead of time by draw.py and
shipped beside this file. This program only copies it to the output
directory, so it needs nothing but the standard library, needs no
network, and writes byte-for-byte the same file on every run.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Fail loudly instead of handing the grader a truncated copy.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("entry.png was not copied completely")
    return 0


if __name__ == "__main__":
    sys.exit(main())
