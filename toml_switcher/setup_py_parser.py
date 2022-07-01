# SPDX-FileCopyrightText: 2022 Alec Delaney, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=unused-variable,unused-argument,global-statement,invalid-name

"""
``setup_py_parser.py``
======================

Functionality for getting information from ``setup.py``

* Author(s): Alec Delaney

Thanks to the Dependabot Core team, for the inspiration/idea on how to
parse the ``setup.py`` file.
"""

import io
import re
from typing import Any
import setuptools

value_dict = {}


def parse_setup_py(file_contents: str, keys: list[str]) -> dict[str, Any]:
    """Parses ``setup.py`` for the requested information

    :param str file_contents: The file contents of ``setup.py``
    :param keys: A list of arguments of ``setup()`` to grab values from
    :type keys: [str, ...]
    """

    global value_dict
    value_dict = {}

    def setup(*args, **kwargs):
        """Fake ``setup()`` method"""
        for key in keys:
            value_dict[key] = kwargs.get(key)

    setuptools.setup = setup

    def noop(*args, **kwargs):
        pass

    def fake_parse(*args, **kwargs):
        return []

    global fake_open  # pylint: disable=global-variable-undefined

    def fake_open(*args, **kwargs):
        content = (
            "VERSION = ('0', '0', '1+dependabot')\n"
            "__version__ = '0.0.1+dependabot'\n"
            "__author__ = 'someone'\n"
            "__title__ = 'something'\n"
            "__description__ = 'something'\n"
            "__author_email__ = 'something'\n"
            "__license__ = 'something'\n"
            "__url__ = 'something'\n"
        )
        return io.StringIO(content)

    # Remove `print`, `open`, `log` and import statements
    file_contents = re.sub(r"print\s*\(", "noop(", file_contents)
    file_contents = re.sub(r"log\s*(\.\w+)*\(", "noop(", file_contents)
    file_contents = re.sub(r"\b(\w+\.)*(open|file)\s*\(", "fake_open(", file_contents)
    file_contents = file_contents.replace("parse_requirements(", "fake_parse(")
    version_re = re.compile(r"^.*import.*__version__.*$", re.MULTILINE)
    file_contents = re.sub(version_re, "", file_contents)

    # Set variables likely to be imported
    __version__ = "0.0.1+dependabot"
    __author__ = "someone"
    __title__ = "something"
    __description__ = "something"
    __author_email__ = "something"
    __license__ = "something"
    __url__ = "something"

    exec(file_contents)  # pylint: disable=exec-used

    return value_dict
