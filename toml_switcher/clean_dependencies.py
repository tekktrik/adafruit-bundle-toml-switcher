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

        optional_reqs = []

        req_fp = os.path.join(output_dir, req_fn)
        with open(req_fp, mode="w", encoding="utf-8") as reqfile:
            reqfile.write(
                "# SPDX-FileCopyrightText: 2022 Alec Delaney, for Adafruit Industries\n"
            )
            reqfile.write("#\n")
            reqfile.write("# SPDX-License-Identifier: Unlicense\n")
            if reqlist:
                reqfile.write("\n")
            for req in reqlist:
                if req.startswith("OPTIONAL:"):
                    optional_reqs.append(req[9:])
                    continue
                reqfile.write(req + "\n")

        opt_fp = os.path.splitext(req_fp)[0] + "_opt.txt"

        with open(opt_fp, mode="w", encoding="utf-8") as optfile:
            optfile.write(
                "# SPDX-FileCopyrightText: 2022 Alec Delaney, for Adafruit Industries\n"
            )
            optfile.write("#\n")
            optfile.write("# SPDX-License-Identifier: Unlicense\n")
            if optional_reqs:
                optfile.write("\n")
            for opt in optional_reqs:
                optfile.write(opt + "\n")


if __name__ == "__main__":
    app()
