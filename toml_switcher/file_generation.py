# SPDX-FileCopyrightText: 2022 Alec Delaney, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
``overwrite_workflows.py``
==========================

Functionality for overwriting the GitHub Actions workflows

* Author(s): Alec Delaney

"""

import os
import shutil
import typer
from library_functions import StrPath
from iterate_libraries import iter_local_bundle_with_func, LocalLibFunc_IterResult

app = typer.Typer()


def overwrite_workflow(
    lib_path: StrPath, template_filepath: StrPath, copy_local_filepath: StrPath
) -> None:
    """Library function for copying files to repositories

    :param StrPath lib_path: The repository path
    :param StrPath template_filepath: The filepath of the template to copy
    :param StrPath copy_local_filepath: The local, relative path of the file in the repository
    """

    copy_filepath = os.path.join(lib_path, copy_local_filepath)
    if not os.path.exists(copy_filepath):
        return
    shutil.copyfile(template_filepath, copy_filepath)


def overwrite_reqs(lib_path: StrPath, copy_folder: StrPath, copy_suffix: StrPath, paste_filename: StrPath) -> None:
    """Library function to force copy/paste a requirements file
    
    :param StrPath lib_path: The repository path
    :param StrPath copy_folder: The folder containing the requirements files
    :param StrPath copy_suffix: The suffix of the copy file
    :param StrPath paste_filename: The filename of the paste requirements file
    """

    libname = os.path.basename(lib_path)
    copy_filepath = os.path.join(copy_folder, libname + copy_suffix)
    paste_filepath = os.path.join(lib_path, paste_filename)
    shutil.copyfile(copy_filepath, paste_filepath)


@app.command()
def overwrite_workflows(bundle_path: str) -> list[LocalLibFunc_IterResult[None]]:
    """Bundle function for copying template files to the bundle repositories

    :param str bundle_path: The filepath to the bundle
    """

    return iter_local_bundle_with_func(
        bundle_path,
        [
            (
                overwrite_workflow,
                ("./build.yml.template", ".github/workflows/build.yml"),
                {},
            ),
            (
                overwrite_workflow,
                ("./release.yml.template", ".github/workflows/release.yml"),
                {},
            ),
        ],
    )


def copypaste_toml(
    lib_path: StrPath, tomls_folder: StrPath, *, toml_suffix: str = "_pyproject.toml"
) -> bool:
    """Library function for copy/pasting the generated `pyproject.toml` file

    :param StrPath lib_path: The repository path
    :param StrPath tomls_folder: The folder path where the generate `pyproject.toml`
        files are located
    :param str toml_suffix: The common suffix of the `pyproject.toml` files
    """

    libname = os.path.basename(lib_path)
    toml_filepath = os.path.join(tomls_folder, libname + toml_suffix)
    dest_filepath = os.path.join(lib_path, "pyproject.toml")
    try:
        shutil.copyfile(toml_filepath, dest_filepath)
        return True
    except FileNotFoundError:
        return False


def remove_setup_py(lib_path: StrPath) -> bool:
    """Library function for removing `setup.py

    :param StrPath lib_path: The repository path
    """

    setup_py_filepath = os.path.join(lib_path, "setup.py")
    try:
        os.remove(setup_py_filepath)
        return True
    except FileNotFoundError:
        return False


@app.command()
def toml_swap(
    bundle_path: str, tomls_folder: str
) -> list[LocalLibFunc_IterResult[bool]]:
    """Bundle function for swapping from `setup.py` to `pyproject.toml`

    :param str bundle_path: The filepath to the bundle
    """

    return iter_local_bundle_with_func(
        bundle_path,
        [
            (copypaste_toml, (tomls_folder,), {}),
            (remove_setup_py, (), {}),
        ],
    )

@app.command()
def add_requirements_files(bundle_path: str, reqs_folder: str) -> list[LocalLibFunc_IterResult[bool]]:
    """Bundle function to copy/paste the requirements files
    
    :param str bundle_path: The filepath to the bundle
    :param str reqs_folder: The filepath to the folder containing the requirements files
    """

    return iter_local_bundle_with_func(
        bundle_path,
        [
            (overwrite_reqs, (reqs_folder, "_req.txt", "requirements.txt"), {}),
            (overwrite_reqs, (reqs_folder, "_req_opt.txt", "optional_requirements.txt"), {}),
        ]
    )


if __name__ == "__main__":
    app()
