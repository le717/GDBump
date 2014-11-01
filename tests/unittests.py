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


class TestRunner(object):

    def __init__(self, axis, changeValue, inFile, outFile):
        self.axis = axis
        self.changeValue = changeValue
        self.inFile = inFile
        self.outFile = outFile

        # Create an instance of GDBump
        self.gdbump = GDBump.GDBump(axis, changeValue, inFile, outFile)
        self.gdbump.changeValues()

    def validateLines(self, shouldEqual):
        """Confirm the values were correctly changed."""
        print()
        for i in range(0, len(self.gdbump.linesChanged)):
            line = self.gdbump._splitLine(self.gdbump.linesChanged[i])[1]
            value = shouldEqual[i]

            print("{0} should be {1}".format(line, value))
            assert line == value, False
        print("\nAll values were correctly changed.")


testDir = os.path.join(os.getcwd(), "files")
inFile = os.path.join(testDir,  "y-axis.txt")
outFile = os.path.join(testDir,  "y-axis-changed.txt")

# Create a test runner instance
yAxisTest = TestRunner("y", 20, inFile, outFile)

# Value addition
yAxisTest.validateLines((0, -30, 0, -40))

# Write the file and confirm it's length
yAxisTest.gdbump.writeFile()
if os.path.isfile(outFile):
    with open(outFile, "rt") as f:
        numOfLines = f.readlines()[:]

    print("\nThere are {0} lines".format(len(numOfLines) + 1))
    assert len(numOfLines) == 38, False
    print("File is the correct length.\n")

print("*" * 7, "All tests passed.", "*" * 7)
