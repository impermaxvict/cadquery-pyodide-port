#!/usr/bin/env python3

import sys
import pathlib
import subprocess

OCCT_LIBRARY_DIR = pathlib.Path(sys.argv[1])

toolkits = OCCT_LIBRARY_DIR.glob("libTK*.a")

exported_symbols = set()

for toolkit in sorted(toolkits):
    result = subprocess.run(
        ["nm", "--print-armap", toolkit],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in result.stdout.decode("utf-8").splitlines():
        line = line.strip()
        if len(line) > 0 and line != "Archive index:":
            if " in " in line:
                exported_symbols.add(line.split(" in ")[0].strip())
            else:
                raise Exception("invalid symbol line")

with open("symbols_mangled_emscripten.dat", "w") as fp:
    fp.write("\n".join(list(sorted(exported_symbols))))
    fp.write("\n")
