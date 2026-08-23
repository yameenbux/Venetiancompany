#!/usr/bin/env python3
"""CLI entry point: python generate.py "<brief>"

Streams a self-contained pitch page out of Claude using the house aesthetics prompt,
saves it to html_outputs/, and opens it if a browser is available.
"""

import sys

from helpers import generate_html_with_claude
from prompts import SYSTEM_PROMPT


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        print("\nExample:")
        print(
            '  python generate.py "A single-page site for The Venetian Company. '
            'Hero, what we do, selected work, contact."'
        )
        return 1

    brief = " ".join(sys.argv[1:])
    generate_html_with_claude(SYSTEM_PROMPT, brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
