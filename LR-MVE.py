#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""LR-MVE - WIP thingy for JimbobJeffers.

Created 2014 Triangle717
<http://Triangle717.WordPress.com/>

LR-MVE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LR-MVE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LR-MVE. If not, see <http://www.gnu.org/licenses/>.

"""

import os
import re
import sys


class LRMVE(object):

    def __init__(self, axis, changeValue, inFile, outFile):

        self.axis = axis
        self.inFile = os.path.abspath(inFile)
        self.outFile = os.path.abspath(outFile)
        self.timesChanged = 0
        self.__fileContent = self._readFile()
        self.__prefixRegex = re.compile(r"(float|byte)")
        self.__commentRegex = re.compile(r"//.*")

        # Determine if the multipler is an integer or float
        if changeValue.find(".") > -1:
            self.changeValue = float(changeValue)
        else:
            self.changeValue = int(changeValue)

    def _readFile(self):
        """Write the source file.

        @return {array} Array contaning contents of source file.
        """
        with open(self.inFile, "rt") as f:
            lines = f.readlines()
        return lines

    def writeFile(self):
        """Write the destination file.

        @return {boolean} Always returns True.
        """
        with open(self.outFile, "wt") as f:
            f.write("".join(self.__fileContent))
        return True

    def _splitLine(self, line):

        # Confirm the line starts correctly
        match = self.__prefixRegex.search(line)
        if match:
            # Get the text and the current value
            text = "({0})".format(match.group(0))
            value = line.strip().replace(text, "")
            comment = None

            # Strip comments as needed
            commentMatch = self.__commentRegex.search(value)
            if commentMatch:
                comment = commentMatch.group(0)
                value = value.replace(comment, "")

            # Make it an integer for math(s) operations
            value = int(value)
            return [text, value, comment]
        return False

    def _joinLine(self,  parts, pos):
        """TODO.

        @param {array} parts TODO.
        @param {integer} pos The line number to update with the changed value.
        @return {boolean} Always returns True.
        """
        # Join the parts
        newLine = "{0}{1}".format(parts[0], parts[1])

        # Restore the comment if needed
        if parts[2] is not None:
            newLine = "{0} {1}".format(newLine, parts[2])

        # Restore the indentation and trailing new line
        newLine = "\t{0}\n".format(newLine)

        # Update the file contents with the new line
        self.__fileContent[pos] = newLine
        return True

    def changeValues(self):
        """TODO.

        @return {boolean} Always returns True.
        """
        def _doMaths(value, i):
            """Perform the math(s) operation."""
            return value + self.changeValue

        positions = {"x": 1,
                     "y": 2,
                     "z": 3,
                     "tu": 4,
                     "tv": 5,
                     "r": 6,
                     "g": 7,
                     "b": 8,
                     "a": 9
                     }

        # Scan just the first 10 lines
        for i in range(1, 10):
            parts = self._splitLine(self.__fileContent[i])

            # Make sure we are on the correct line before math(s)
            if i == positions[self.axis]:
                parts[1] = _doMaths(parts[1], i)

            # Merge the parts back together
            self._joinLine(parts, i)
            self.timesChanged += 1

        # Now do the rest of the lines using the same process
        for i in range(9 + positions[self.axis], len(self.__fileContent), 9):
            parts = self._splitLine(self.__fileContent[i])
            if parts:
                parts[1] = _doMaths(parts[1], i)
                self._joinLine(parts, i)
                self.timesChanged += 1
        return True


def commandLine():
    """Command-line arguments parser.

    @return {tuple|Boolean} A four index tuple containing the parameters given,
        False if all arguments were not passed or the help was invoked.
    """
    def cmdHelp():
        """Print command-line arguments help text."""
        print("""LR-MVE Command-line Usage

{0} [Axis] [Change value] [Input file] [Output file]


Axis: The axis you want to edit.
    Values are x, y, z, tu, tv, r, g, b, and a.
Change value: The positive or negative value of your desired change.
Input file: Text file containing decoded GDB format structure,
    as decompiled using the LR Binary File Viewer.
Output file: Destination text file for changed values.
""".format(os.path.basename(__file__)))
        return False

    # No arguments were given
    try:
        sys.argv[1]
    except IndexError:
        cmdHelp()
        return False

    # The help parameter was given
    if sys.argv[1] in ("-h", "--help"):
        cmdHelp()
        return False

    # All the arguments required were not given
    try:
        axis = sys.argv[1]
        changeValue = sys.argv[2]
        inFile = sys.argv[3]
        outFile = sys.argv[4]
        return (axis, changeValue, inFile, outFile)
    except IndexError:
        cmdHelp()
        return False


def main():
    """Entry point for entire program."""
    print("\nLEGO Racers - Mass Value Editor\n")
    arguments = commandLine()
    if arguments:
        lrmve = LRMVE(arguments[0], arguments[1], arguments[2], arguments[3])
        lrmve.changeValues()
        lrmve.writeFile()
        print("{0} updated values saved to {1}".format(
              lrmve.timesChanged, arguments[3]))


if __name__ == "__main__":
    main()
