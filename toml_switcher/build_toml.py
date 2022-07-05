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
from library_functions import in_lib_path

app = typer.Typer()

REPLACE_MAP = {
    "name": "{{PIP_NAME}}",
    "description": "{{DESCRIPTION}}",
    "url": "{{URL}}",
}


# pylint: disable=unused-argument
@in_lib_path
def create_toml(
    lib_path: str, template_contents: str, disabled_content: str
) -> tuple[bool, str]:
    """Take the template file and create individual ``pyproject.toml``
    files for each library

    :param str lib_path: The path to the library
    :param str template_contents: The contents of the template
        ``pyproject.toml`` file
    :param str disabled_content: The contents of the disabled content file
    """

    try:
        with open("setup.py", mode="r", encoding="utf-8") as setupfile:
            setup_contents = setupfile.read()
    except FileNotFoundError:
        return False, disabled_content

    setup_contents = setup_contents.replace("open_codec(", "open(")

    setup_dict = parse_setup_py(
        setup_contents, [*REPLACE_MAP.keys(), "keywords", "py_modules", "packages"]
    )

    library_type = "py-modules" if setup_dict["py_modules"] else "packages"
    library_name = (
        setup_dict["py_modules"][0]
        if setup_dict["py_modules"]
        else setup_dict["packages"][0]
    )
    lib_keywords = [
        '    "' + keyword + '",\n' for keyword in setup_dict["keywords"].split(" ")
    ]
    lib_keywords = "".join(lib_keywords)

    template_contents = template_contents.replace("{{LIBRARY_TYPE}}", library_type)
    template_contents = template_contents.replace("{{LIBRARY_NAME}}", library_name)
    template_contents = template_contents.replace("{{KEYWORDS}}", lib_keywords)

    for setup_arg, template_text in REPLACE_MAP.items():
        template_contents = template_contents.replace(
            template_text, setup_dict[setup_arg]
        )

    return True, template_contents


def create_tomls(
    bundle_path: str = "submodules/bundle",
) -> list[LocalLibFunc_IterResult[tuple[bool, str]]]:
    """Wrapper fuction to create the TOML files

    :param str bundle_path: The path to the cloned Adafruit bundle
    """

    with open(
        "pyproject.toml.disabled.template", mode="r", encoding="utf-8"
    ) as distemp:
        disable_contents = distemp.read()

    with open("pyproject.toml.template", mode="r", encoding="utf-8") as tempfile:
        template_contents = tempfile.read()

    return iter_local_bundle_with_func(
        bundle_path, [(create_toml, (template_contents, disable_contents), {})]
    )


@app.command()
def generate_toml_files(
    output_dir: str = "tomls", bundle_path: str = "submodules/bundle"
) -> None:
    """Save the toml files to the output directory

    :param str output_dir: The output directory for files
    :param str bundle_path: The path to the cloned Adafruit Bundle
    """

    results = create_tomls(bundle_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for result in results:
        lib_path, lib_results = result
        for_pypi, file_contents = lib_results[0]
        libname = os.path.basename(lib_path)
        suffix = "_pyproject.toml" if for_pypi else "_pyproject.toml.disabled"
        filepath = os.path.join(output_dir, libname + suffix)
        with open(filepath, mode="w", encoding="utf-8") as fileobj:
            fileobj.write(file_contents)


if __name__ == "__main__":
    app()
