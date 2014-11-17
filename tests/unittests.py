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

    def __init__(self, inFile, outFile, axis="", changeValue="", msg=""):
        self.axis = axis
        self.changeValue = changeValue
        self.inFile = inFile
        self.outFile = outFile
        self.msg = msg
        self.testsPassed = 0
        self.gdbump = None

        # Run only GDBump if we have all the required data
        if self.axis != "" and self.changeValue != "":
            self.changeTest(self.changeValue, self.msg)

    def changeTest(self, changeValue, msg, axis=None, inFile=None):
        self.msg = msg
        self.changeValue = changeValue

        # Update the axis only when needed
        if axis is not None or (type(axis) == str and axis != self.axis):
            self.axis = axis

        # Update the input file only when needed
        if inFile is not None and (inFile != self.inFile):
            self.inFile = inFile

        # Create an instance of GDBump
        self.gdbump = GDBump.GDBump(self.axis, self.changeValue,
                                    self.inFile, self.outFile, test=True)
        self.gdbump.processFile()

    def processLines(self, shouldEqual):
        """Confirm the values were correctly changed."""
        if self.gdbump is not None:
            print("\nit {0}.".format(self.msg))
            for i in range(0, len(self.gdbump.linesChanged)):
                line = self.gdbump._splitLine(self.gdbump.linesChanged[i])[1]
                value = shouldEqual[i]

                print('"{0}" should equal  "{1}"'.format(line, value))
                assert line == value, False
                self.testsPassed += 1
        return True


def main():

    testDir = os.path.join(os.getcwd(), "files")
    inFile = os.path.join(testDir, "y-axis.txt")
    outFile = os.path.join(testDir, "y-axis-changed.txt")
    testRunner = TestRunner(inFile, outFile, "y")

    try:
        # Make sure input file exists
        testRunner.changeTest(20, "should error from non-existant file",
                              inFile=os.path.join(testDir, "y-axis-not.txt"))
        testRunner.processLines((0, 0, 0, 0))
    except FileNotFoundError:
        testRunner.testsPassed += 1

    testRunner.changeTest(20, "should increase the values by 20",
                          inFile=inFile)
    testRunner.processLines((0, -30, 0, -40))

    testRunner.changeTest(-20, "should decrease the values by 20")
    testRunner.processLines((-40, -70, -40, -80))

    testRunner.changeTest("~20", "should replace all values with 20")
    testRunner.processLines((20, 20, 20, 20))

    # Write the output file and confirm it's length
    testRunner.gdbump.writeFile()
    if os.path.isfile(outFile):
        with open(outFile, "rt") as f:
            numOfLines = f.readlines()

        print("\nThere should {0} lines in the output file.".format(
              len(numOfLines) + 1))
        assert len(numOfLines) == 38, False
        testRunner.testsPassed += 1

    print()
    print("*" * 7, "{0} tests passed.".format(testRunner.testsPassed), "*" * 7)

main()
