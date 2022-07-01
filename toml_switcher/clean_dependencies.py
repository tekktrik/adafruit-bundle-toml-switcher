# SPDX-FileCopyrightText: 2022 Alec Delaney, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
``clean_dependencies.py``
=========================

Functionality for cleaning the dependency lists

* Author(s): Alec Delaney

"""

from typing import Optional
import os
import typer

app = typer.Typer()


@app.command()
def clean_dependencies(
    input_dir: str = "reqlists", output_dir: Optional[str] = None
) -> None:
    """Read the dependency lists, clean them, and rewrite them to a new directory

    :param str input_dir: The input directory name
    :param str output_dir: The output directory name
    """

    req_dict: dict[str, list[str]] = {}

    for file in os.listdir(input_dir):
        req_fp = os.path.join(input_dir, file)
        reqlist = []
        with open(req_fp, mode="r", encoding="utf-8") as reqfile:
            for line in reqfile:
                req = line.strip()
                if req.lower().replace("_", "-").startswith("adafruit-blinka"):
                    reqlist.insert(0, req)
                else:
                    reqlist.append(req)
        req_dict[file] = reqlist

    cap_dict = {}

    for dict_name, dict_req in req_dict.items():
        dict_req = [req.replace(" ", "") for req in dict_req]
        if dict_req and dict_req[0].lower().replace("_", "-").startswith(
            "adafruit-blinka"
        ):
            dict_req[0] = (
                dict_req[0]
                .lower()
                .replace("_", "-")
                .replace("adafruit-blinka", "Adafruit-Blinka")
            )
        cap_dict[dict_name] = dict_req

    if output_dir:
        save_cleaned_deps(cap_dict, output_dir)


def save_cleaned_deps(
    requirements: dict[str, list[str]], output_dir: str = "cleanreqs"
) -> None:
    """Save the cleaned requirements lists

    :param dict requirements: The requirements dict
    :param str output_dir: The output directory of clean requirements
    """

    os.makedirs(output_dir)

    for req_fn, reqlist in requirements.items():
        req_fp = os.path.join(output_dir, req_fn)
        with open(req_fp, mode="w", encoding="utf-8") as reqfile:
            reqfile.write("".join(req + "\n" for req in reqlist))


if __name__ == "__main__":
    app()
