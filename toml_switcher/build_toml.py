# SPDX-FileCopyrightText: 2022 Alec Delaney, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
``build_toml.py``
=================

Functionality for building the ``pyproject.toml`` files for the bundle libraries

* Author(s): Alec Delaney

"""

import os
import typer
from setup_py_parser import parse_setup_py
from iterate_libraries import iter_local_bundle_with_func, LocalLibFunc_IterResult

app = typer.Typer()

REPLACE_MAP = {
    "name": "{{PIP_NAME}}",
    "description": "{{DESCRIPTION}}",
    "url": "{{URL}}",
    "keywords": "{{KEYWORDS}}"
}

def create_toml(lib_path: str, output_dir: str = "tomls", template_filepath: str = "pyproject.toml.template") -> None:
    """Take the template file and create individual ``pyproject.toml``
    files for each library
    
    :param str lib_path: The path to the library
    :param str output_dir: The output directory for files
    :param str template_filepath: The filepath for the template
        ``pyproject.toml`` file
    """

    libname = os.path.basename(lib_path)

    try:
        setup_filepath = os.path.join(lib_path, "setup.py")
        with open(setup_filepath, mode="r", encoding="utf-8") as setupfile:
            setup_contents = setupfile.read()
    except FileNotFoundError:
        with open("pyproject.toml.disabled.template", mode="r", encoding="utf-8") as distemp:
            disable_contents = distemp.read()
        disfile_path = os.path.join(output_dir, libname + "_pyproject.toml.disabled")
        with open(disfile_path, mode="w", encoding="utf-8") as disfile:
            disfile.write(disable_contents)
        return

    with open(template_filepath, mode="r", encoding="utf-8") as tempfile:
        template_contents = tempfile.read()

    setup_dict = parse_setup_py(setup_contents, [*REPLACE_MAP.keys(), "py_modules", "packages"])

    library_type = "py-modules" if setup_dict["py_modules"] else "packages"

    template_contents.replace("{{LIBRARY_TYPE}}", library_type)

    for setup_arg, template_text in REPLACE_MAP.items():
        template_contents.replace(template_text, setup_dict[setup_arg])

    tomlpath = os.path.join(output_dir, libname + "_pyproject.toml")
    with open(tomlpath, mode="w", encoding="utf-8") as tomlfile:
        tomlfile.write(template_contents)


@app.command()
def build_tomls(output_dir: str = "tomls", bundle_path: str = "submodules/bundle") -> LocalLibFunc_IterResult[None]:
    """Build the ``pyproject.toml`` files
    
    :param str output_dir: The filepath of the output directory
    :param str bundle_path: The path to the cloned Adafruit Bundle
    """

    return iter_local_bundle_with_func(bundle_path, [(create_toml, (output_dir,), {})])


if __name__ == "__main__":
    app()
