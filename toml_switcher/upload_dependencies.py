# SPDX-FileCopyrightText: 2022 Alec Delaney, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
``upload_dependencies.py``
==========================

Functionality for uploading dependencies from the bundle libraries

* Author(s): Alec Delaney

"""

import os
import typer
from github import Github
from github.InputFileContent import InputFileContent

app = typer.Typer()

@app.command()
def gist_upload_dir(gh_token: str, directory: str = "reqlists") -> None:
    """Upload the directory as a gist of multiple files

    :param str gh_token: The GitHub token used for authorization
    :param str directory: The directory to upload:
    """

    gist_filepaths = [os.path.join(directory, file) for file in os.listdir(directory)]

    gist_payload = {}

    for gist_filepath in gist_filepaths:
        with open(gist_filepath, mode="r", encoding="utf-8") as gistfile:
            contents = gistfile.read()
            if contents:
                ifc = InputFileContent(contents)
                gist_payload[os.path.basename(gist_filepath)] = ifc

    github = Github(gh_token)
    user = github.get_user()
    user.create_gist(
        public=True,
        files=gist_payload,
        description="A collection of all the requirements from the Adafruit CircuitPython Bundle",
    )
