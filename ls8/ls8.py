#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) < 2:
    print("Usage: ls8.py examples/file_name")
    sys.exit(1)

cpu = CPU()

program_file = sys.argv[1]
cpu.load(program_file)
cpu.run()
