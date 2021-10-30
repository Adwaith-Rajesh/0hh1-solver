from __future__ import annotations

import argparse
from typing import Sequence

from .web import run as web_runner


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("type", type=str, help="web or android")
    parser.add_argument("shape", type=int, help="the shape of the puzzle (4, 6, 8, 10, 12)")

    args = parser.parse_args(argv)
    print(args)

    if args.type == "web":
        web_runner(args.shape)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
