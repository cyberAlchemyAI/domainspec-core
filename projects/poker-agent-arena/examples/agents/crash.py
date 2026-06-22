#!/usr/bin/env python3
import sys

for line in sys.stdin:
    if line.strip():
        raise SystemExit(7)
