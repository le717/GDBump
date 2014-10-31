# GDBump [![Build Status](https://travis-ci.org/le717/GDBump.svg)](https://travis-ci.org/le717/GDBump) #

**GDBump** is a LEGO&reg; Racers modding tool designed to speed up the process of modifying GDB files. It enables users to increase or decrease a specific value of all vertex entries in a file - for example, the Y axis - through a simple interface, instead of having to spend a lengthy amount of time doing it manually. This is useful for moving about objects in the game, particularly those made by the developers that can be difficult to edit otherwise. GDBump is best used in combination with the [LR1 Binary Editor](http://www.rockraidersunited.com/topic/4367-binary-file-editor/).

## Usage ##
```
GDBump.exe [Axis] [Change value] [Input file] [Output file]

Axis: The axis you want to edit.
Possible values are `x`, `y`, `z`, `tu`, `tv`, `r`, `g`, `b`, and `a`.
Change value: The positive or negative value of your desired change.
Input file: Text file containing decoded GDB format structure,
as decompiled using the LR1 Binary Editor.
Output file: Destination text file for changed values.
```

# Downloads ##
All downloads are on the [Releases](https://github.com/le717/GDBump/releases) page.

## License ##
[The MIT License](LICENSE)

Created 2014 [Triangle717](http://le717.github.io)
