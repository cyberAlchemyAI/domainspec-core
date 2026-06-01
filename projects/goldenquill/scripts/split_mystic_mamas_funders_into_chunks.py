#!/usr/bin/env python3
"""Split the Mystic Mamas master funder sheet into manageable chunks.

Input:
    orgs/mystic_mamas/mystic_mamas_funders_master.csv

Output:
    orgs/mystic_mamas/chunks/mystic_mamas_funders_chunk_01.csv
    orgs/mystic_mamas/chunks/mystic_mamas_funders_chunk_02.csv
    ...

Each chunk has the same header as the master and at most CHUNK_SIZE data rows.
Adjust CHUNK_SIZE below as needed.
"""

import csv
import math
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = BASE_DIR / "orgs" / "mystic_mamas" / "mystic_mamas_funders_master.csv"
OUT_DIR = BASE_DIR / "orgs" / "mystic_mamas" / "chunks"
CHUNK_SIZE = 25  # tweak if you want bigger/smaller slices


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with SOURCE_PATH.open(newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print("Source sheet is empty; nothing to split.")
            return

        rows = list(reader)

    total = len(rows)
    if total == 0:
        print("No data rows found in source sheet.")
        return

    num_chunks = math.ceil(total / CHUNK_SIZE)

    for i in range(num_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk_rows = rows[start:end]

        chunk_idx = i + 1
        out_path = OUT_DIR / f"mystic_mamas_funders_chunk_{chunk_idx:02d}.csv"

        with out_path.open("w", newline="") as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header)
            writer.writerows(chunk_rows)

        print(f"Wrote {len(chunk_rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
