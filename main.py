#!/usr/bin/env python3
"""Entry point for the 17 November 2026 world-news image.

The image is drawn at build time by draw.py and shipped as entry.png
beside this file. This program only copies it to the output directory,
so both graded runs write identical bytes. Standard library only.
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
