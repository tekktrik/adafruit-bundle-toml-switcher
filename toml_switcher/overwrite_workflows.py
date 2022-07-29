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


@app.command()
def overwrite_workflow(
    lib_path: StrPath, template_filepath: StrPath, copy_local_filepath: StrPath
) -> None:
    """Function for copying files to repositories

    :param StrPath lib_path: The repository path
    :param StrPath template_filepath: The filepath of the template to copy
    :param StrPath copy_local_filepath: The local, relative path of the file in the repository
    """
    copy_filepath = os.path.join(lib_path, copy_local_filepath)
    if not os.path.exists(copy_filepath):
        return
    shutil.copyfile(template_filepath, copy_filepath)


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
