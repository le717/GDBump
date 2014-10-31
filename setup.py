#! /usr/bin/python3.4-32
# -*- coding: utf-8 -*-
"""LR MVE - Mass value editor for when manually editing .GDB files.

Created 2014 Triangle717
<http://Triangle717.WordPress.com/>

Licensed under The MIT License
<http://opensource.org/licenses/MIT/>

"""

from cx_Freeze import (setup, Executable)
import sys
import os

import constants as const

# Windows
if sys.platform == "win32":
    base = "Win32GUI"

    # This is x86 Python
    if sys.maxsize < 2 ** 32:
        destfolder = os.path.join("bin", "Windows")

    # Do not freeze on x64 Python
    else:
        input("""\n64-bit binaries are not frozen.
    Please freeze using 32-bit Python 3.3 or higher.""")
        raise SystemExit(0)

# Mac OS X
elif sys.platform == "darwin":
    destfolder = os.path.join("bin", "Mac OS X")
# Linux
else:
    destfolder = os.path.join("bin", "Linux")

# Create the freeze path if it doesn't exist
if not os.path.exists(destfolder):
    os.makedirs(destfolder)

build_exe_options = { "build_exe": destfolder }

setup(
    name=const.appLongName,
    version=const.version,
    author=const.creator,
    description="Mass value editor for when manually editing .GDB files.",
    license="The MIT License",
    options={"build_exe": build_exe_options},
    executables=[Executable("LR-MVE.pyw",
                 targetName="LR-MVE.exe", base=base)]
)
