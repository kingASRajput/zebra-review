#!/usr/bin/env python3
"""Run Zebra without installing: `python3 zebra.py scan .`"""
import sys
from zebra.cli import main

if __name__ == "__main__":
    sys.exit(main())
