#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDBump - Mass value editor for when manually editing .GDB files.

Created 2014 Triangle717
<http://Triangle717.WordPress.com/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import GDBump

def validateLines(shouldBe):
    """Confirm the values were correctly changed."""
    print()
    for i in range(0, len(gdbump.linesChanged)):
        line = gdbump._splitLine(gdbump.linesChanged[i])[1]
        value = shouldBe[i]

        print("{0} should be {1}".format(line, value))
        assert line == value, False
    print("\nAll values were correctly changed.")


axis = "y"
changeValue = "20"
testDir = os.path.join(os.getcwd(), "files")
inFile = os.path.join(testDir,  "y-axis.txt")
outFile = os.path.join(testDir,  "y-axis-changed.txt")

# Create an instance of GDBump
gdbump = GDBump.GDBump(axis, changeValue, inFile, outFile)
gdbump.changeValues()

# Value addition
validateLines((0, -30, 0, -40))

# Write the file and confirm it's length
gdbump.writeFile()
if os.path.isfile(outFile):
    with open(outFile, "rt") as f:
        numOfLines = f.readlines()[:]

    print("\nThere are {0} lines".format(len(numOfLines) + 1))
    assert len(numOfLines) == 38, False
    print("File is the correct length.\n")

print("*" * 7, "All tests passed.", "*" * 7)
