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

    def __init__(self, inFile, outFile):

        print("LEGO Racers - Mass Value Editor\n")
        self.axis = "y"
        self.changeValue = 20
        self.inFile = os.path.abspath(inFile)
        self.outFile = os.path.abspath(outFile)
        self.__fileContent = self._readFile()
        self.__prefixRegex = re.compile(r"(float|byte)")
        self.__commentRegex = re.compile(r"//.*")
        self.__positions = {
            "x": 1,
            "y": 2,
            "z": 3,
            "tu": 2,
            "tv": 4,
            "r": 5,
            "g": 6,
            "b": 7,
            "a": 8
        }

    def _readFile(self):

        with open(self.inFile, "rt") as f:
            lines = f.readlines()
        return lines

    def writeFile(self):

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

    def _joinLine(self,  parts, pos):

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

        def _doMaths(value, i):
            # Perform the math(s) operation
            # Addition
            if self.changeValue >= 0:
                value += self.changeValue

            # Subtraction
            else:
                value -= self.changeValue
            return value

        # Scan just the first 10 lines
        for i in range(1, 10):
            parts = self._splitLine(self.__fileContent[i])

            # Make sure we are on the correct line before math(s)
            if i == self.__positions[self.axis]:
                parts[1] = _doMaths(parts[1], i)

            # Merge the parts back together
            self._joinLine(parts, i)

        # Now do the rest of the lines using the same process
        for i in range(11, len(self.__fileContent), 9):
            parts = self._splitLine(self.__fileContent[i])
            parts[1] = _doMaths(parts[1], i)
            self._joinLine(parts, i)

    def _commandLine(self):
        """Command-line arguments parser."""
        pass


if __name__ == "__main__":
    inFile = "Testing/original.txt"
    outFile = "Testing/updated.txt"
    editor = LRMVE(inFile, outFile)
    editor.changeValues()
    editor.writeFile()
