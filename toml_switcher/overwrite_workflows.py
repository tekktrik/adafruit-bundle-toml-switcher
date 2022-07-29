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
    if not os.path.exists(copy_filepath):
        return
    copy_filepath = os.path.join(lib_path, copy_local_filepath)
    shutil.copyfile(template_filepath, copy_filepath)


def overwrite_workflows(bundle_path: str) -> list[LocalLibFunc_IterResult[None]]:
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
