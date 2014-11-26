#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""GDBump - Mass value editor for when manually editing .GDB files.

Created 2014 Triangle717
<http://Triangle717.WordPress.com/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""

import os
import re
import sys

import constants as const

__all__ = ("GDBump", "commandLine", "main")


class GDBump(object):

    """Main GDBump class."""

    def __init__(self, axis, changeValue, inFile, outFile, test=False):
        """Initialize public and private properties.

        Exposes six public properties and two public methods:
        * axis: The user's desired axis to edit, converted to lowercase.
        * changeValue: The value the user wishes to increase/decrease by
            or replace with.
        * inFile: The user's input file containing the values to edit.
        * outFile: The user's desired destination file.
        * timesChanges: An integer stating the number of edits performed.
        * linesChanged: An array containing the changed lines.
        * processFile(): Manages and performs the actual editing.
        * writeFile(): Saves the changed .GDB code to file.

        @param {String|Number} axis
        @param {String|Number} changeValue
        @param {String} inFile
        @param {String} outFile
        @param {Boolean} [test=False] Overwrite certain actions.
            For unit testing only!
        """
        self.__doReplace = False
        self.axis = axis.lower()
        self.changeValue = self._replaceMode(changeValue)
        self.inFile = os.path.abspath(inFile)
        self.outFile = os.path.abspath(outFile)
        self.timesChanged = 0
        self.linesChanged = []
        self.__test = test
        self.__indentSize = "\t"
        self.__fileContent = self._readFile()
        self.__prefixRegex = re.compile(r"(float|byte)")
        self.__commentRegex = re.compile(r"//.*")
        self.__positions = {"x": 1,
                            "y": 2,
                            "z": 3,
                            "tu": 4,
                            "tv": 5,
                            "r": 6,
                            "g": 7,
                            "b": 8,
                            "a": 9
                            }

        # Confirm the desired axis is valid
        try:
            self.__positions[self.axis]
        # That is not a valid axis
        except KeyError:
            self._displayError('The axis chosen ("{0}") is not a valid axis!'
                               .format(self.axis), True)

    def _displayError(self, msg, shutdown=False):
        """Report any errors.

        @param {String} msg The error message to display.
        @param {Boolean} [shutdown=False] Flag to close GDBump upon error.
            For unit testing only!
        @return {Boolean} Always returns False.
        """
        print("\nError!\n{0}".format(msg))

        # Short-circuit parameter if we are runnning unit tests
        if self.__test:
            shutdown = False

        if not shutdown:
            return False
        else:
            raise SystemExit(1)

    def _convertToNumber(self, value):
        """Determine if a number is an integer or float.

        @param {String|Number} value The string to be converted to a number.
        @return {Number} An integer or float.
        """
        # It is already a number
        if type(value) in (int, float):
            return value

        # Convert it to the proper type
        if value.find(".") > -1:
            value = float(value)
        else:
            value = int(value)
        return value

    def _replaceMode(self, value):
        """Enable replace mode.

        @param {String|Number} value The change value being used.
        @return {Number} Numeric version of the change value.
        """
        if type(value) == str:
            # Remove the replace operator and enable replace mode
            if value.startswith("~"):
                value = value.lstrip("~")
                self.__doReplace = True
        return self._convertToNumber(value)

    def _readFile(self):
        """Read the source file.

        @return {Array} Array contaning contents of source file.
        """
        if not os.path.exists(self.inFile):
            self._displayError("{0} does not exist!".format(self.inFile), True)

        with open(self.inFile, "rt") as f:
            lines = f.readlines()
        return lines

    def writeFile(self):
        """Write the destination file.

        @return {Boolean} Always returns True.
        """
        with open(self.outFile, "wt") as f:
            f.write("".join(self.__fileContent))
        return True

    def _splitLine(self, line):
        """Split a line into seperate parts suitable for editing.

        @param {String} line The line to be split.
        @return {Array|Boolean} Three index list containing
            the line's text, value, and comment (if any).
            False if the line could not be split.
        """
        # Confirm the line starts correctly
        match = self.__prefixRegex.search(line)
        if match:
            # Get the indentation, line text, and current value
            self.__indentSize = line[:line.find("(")]
            text = "({0})".format(match.group(0))
            value = line.strip().replace(text, "")
            comment = None

            # Strip comments as needed
            commentMatch = self.__commentRegex.search(value)
            if commentMatch:
                comment = commentMatch.group(0)
                value = value.replace(comment, "")

            # Make it a number for math(s) operations
            value = self._convertToNumber(value)
            return [text, value, comment]
        return False

    def _joinLine(self, parts, pos):
        """Join the split parts of a line back together.

        @param {Array} parts The line sections to be merged.
        @param {Integer} pos The line number to update with the changed value.
        @return {String} Returns the joined line.
        """
        # Join the parts
        newLine = "{0}{1}".format(parts[0], parts[1])

        # Restore the comment if needed
        if parts[2] is not None:
            newLine = "{0}    {1}".format(newLine, parts[2])

        # Restore the indentation and trailing new line
        newLine = "{0}{1}\n".format(self.__indentSize, newLine)

        # Update the file contents with the new line
        self.__fileContent[pos] = newLine
        return newLine

    def _changeValue(self, text, value, structPos):
            """Perform the math(s) operation.

            Any value requirements for the .GDB format will also be perfomed,
            including forcing byte values to be integers
            and clamping RGBa values into valid ranges.
            This may produce unexpected results for you,
            but this is expected behavior for the game.

            @param {String} text The format structure the value belonds to.
            @param {Number} value The value to be changed or replaced.
            @param {Number} structPos The type of value to be edited.
            @return {Number} The revised value.
            """
            # The replace operator was used
            if self.__doReplace:
                newValue = self.changeValue
            else:
                # Python is cool by subtracting values with the plus sign
                # if the second addend is a negative number. :D
                newValue = value + self.changeValue

            # Byte values must be integers regardless
            if text == "(byte)":
                newValue = int(newValue)

            # Clamp RGBa values between 0-255 inclusive
            if (structPos >= 6 and structPos <= 9):
                if newValue > 255:
                    newValue = 255
                elif newValue < 0:
                    newValue = 0
            return newValue

    def _areasToEdit(self):
        """Determine the boundaries of the editing area.

        @return {Array.<Number>} A two index array containing
            the start and end points of the editing area, respectively.
        """
        boundaries = []
        keywords = ("k_2A", "k_2D")

        for keyword in keywords:
            for i in range(0, len(self.__fileContent)):
                if keyword in self.__fileContent[i]:
                    if keyword == keywords[0]:
                        # Mark the position of the offset + magic number 2
                        # so we start editing on the proper line
                        boundaries.append(i + 2)

                    # We have completed or exceeded the area we can edit
                    elif keyword == keywords[1]:
                        boundaries.append(i - 1)
                    break
        return boundaries

    def processFile(self):
        """Manage and perform the actual editing.

        @return {Boolean} Always returns True.
        """
        # Skip the lines we cannot edit,
        # and make sure we edit the correct lines
        startLine, endLine = self._areasToEdit()
        structPos = self.__positions[self.axis]

        for i in range(startLine + structPos, endLine, 9):
            parts = self._splitLine(self.__fileContent[i])
            # Make sure we have lines to edit
            if parts:
                # Do math(s), merge the parts back together
                parts[1] = self._changeValue(parts[0], parts[1], structPos)
                newLine = self._joinLine(parts, i)
                self.timesChanged += 1
                self.linesChanged.append(newLine)
        return True


def commandLine():
    """Command-line arguments parser.

    @return {Tuple|Boolean} A four index tuple containing the parameters given,
        False if all arguments were not passed or the help was invoked.
    """
    def cmdHelp():
        """Print command-line arguments help text."""
        print("""Command-line Usage Help:

{0} [Axis] [Change value] [Input file] [Output file]

Axis: The axis you want to edit.
    Values are x, y, z, tu, tv, r, g, b, and a.
Change value: The positive or negative value of your desired change.
    Prefixing the value with a tilde (~) will replace all values
    on the chosen axis with the value instead of editing them.
    RGBa values will be clamped to valid ranges per format specifications.
Input file: Text file containing decoded .GDB format structure,
    as decompiled using the LR1 Binary Editor.
Output file: Destination text file for changed values.
""".format(const.exeName))
        return False

    # No arguments or the help parameter was given
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        cmdHelp()
        return False

    try:
        axis = sys.argv[1]
        changeValue = sys.argv[2]
        inFile = sys.argv[3]
        outFile = sys.argv[4]
        return (axis, changeValue, inFile, outFile)

        # All the arguments required were not given
    except IndexError:
        cmdHelp()
        return False


def main():
    """Entry point for primary usage."""
    print("\n{0} v{1}".format(const.appName, const.version))
    arguments = commandLine()
    if arguments:
        gdbump = GDBump(arguments[0], arguments[1],
                        arguments[2], arguments[3], False)
        gdbump.processFile()
        gdbump.writeFile()
        print('\n{0} updated "{1}" values saved to {2}'.format(
              gdbump.timesChanged, arguments[0], arguments[3]))
        raise SystemExit(0)


if __name__ == "__main__":
    main()
