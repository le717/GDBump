#! /usr/bin/python3.4-32
# -*- coding: utf-8 -*-
"""GDBump - Mass value editor for when manually editing .GDB files.

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

build_exe_options = {
    "build_exe": destfolder,
    "optimize": 2,
    "include_files": [
        "README.md",
        "LICENSE"
    ]
}

setup(
    name=const.appName,
    version=const.version,
    author=const.creator,
    description=const.appName,
    license="The MIT License",
    options={"build_exe": build_exe_options},
    executables=[Executable("GDBump.py",
                 targetName="GDBump.exe")]
)
