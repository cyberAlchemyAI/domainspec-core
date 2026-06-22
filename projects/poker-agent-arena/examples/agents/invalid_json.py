#!/usr/bin/env python3
import sys

for line in sys.stdin:
    if not line.strip():
        continue
    print("I prefer vibes to JSON.", flush=True)
