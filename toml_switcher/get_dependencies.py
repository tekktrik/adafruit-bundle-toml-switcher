# SPDX-FileCopyrightText: 2022 Alec Delaney, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
``get_dependencies.py``
=======================

Functionality for getting and recording dependencies from the bundle libraries

* Author(s): Alec Delaney

"""

from typing import Any
import os
import typer
from iterate_libraries import iter_local_bundle_with_func, LocalLibFunc_IterResult
from library_functions import StrPath
from setup_py_parser import parse_setup_py

app = typer.Typer()


@app.command()
def check_dependencies(
    output_dir: str = "reqlists", bundle_path: str = "submodules/bundle"
) -> None:
    """Check the ``requirements.txt`` and ``setup.py`` dependencies and record them.
    If they don't match, record both notify the user

    :param str output_dir: The output directory filepath
    :param str bundle_path: The filepath to the bundle directory
    """

    results = check_all_repo_deps(bundle_path)

    os.makedirs(output_dir)

    for result in results:
        lib_path, lib_results = result
        reqs_dict = lib_results[0]
        req_base = os.path.join(output_dir, os.path.basename(lib_path))
        if "union" in reqs_dict:
            req_file = req_base + "_req.txt"
            with open(req_file, mode="w", encoding="utf-8") as reqfile:
                reqfile.write("".join([req + "\n" for req in reqs_dict["union"]]))
        else:
            os.mkdir(req_base)
            req_file = os.path.join(req_base, os.path.basename(req_base)) + "_req.txt"
            with open(req_file, mode="w", encoding="utf-8") as reqfile:
                reqfile.write("### setup.py ###\n")
                reqfile.write("".join([req + "\n" for req in reqs_dict["setup.py"]]))
                reqfile.write("=========================================\n")
                reqfile.write("### requirements.txt ###\n")
                reqfile.write(
                    "".join([req + "\n" for req in reqs_dict["requirements.txt"]])
                )


def check_repo_deps(lib_path: StrPath) -> dict[str, list[str]]:
    """Check the dependencies of a given repository

    :param StrPath lib_path: The repository path
    """

    setup_py_fp = os.path.join(lib_path, "setup.py")
    req_txt_fp = os.path.join(lib_path, "requirements.txt")

    try:
        with open(setup_py_fp, mode="r", encoding="utf-8") as setuppy:
            setup_py_contents = setuppy.read()

        setup_py_vars = parse_setup_py(setup_py_contents, ["install_requires"])
        setup_py_set: set[str] = set(setup_py_vars["install_requires"])
    except FileNotFoundError:
        setup_py_set = None

    with open(req_txt_fp, mode="r", encoding="utf-8") as reqtxt:
        requirements_txt_set: set[str] = {
            line.strip()
            for line in reqtxt
            if line.strip() and not line.strip().startswith("#")
        }

    if setup_py_set:
        parsed_setup_set = set()
        for req in setup_py_set:
            if req != "Adafruit-Blinka":
                parsed_setup_set.add(req.lower().replace("_", "-"))
            else:
                parsed_setup_set.add(req)
        setup_py_set = parsed_setup_set

    if requirements_txt_set:
        parsed_req_set = set()
        for req in requirements_txt_set:
            if req != "Adafruit-Blinka":
                parsed_req_set.add(req.lower().replace("_", "-"))
            else:
                parsed_req_set.add(req)
        requirements_txt_set = parsed_req_set

    if setup_py_set and setup_py_set != requirements_txt_set:
        # setup != req
        # Write setup.py AND req.txt
        return {
            "requirements.txt": requirements_txt_set,
            "setup.py": setup_py_set,
        }

    # Only req
    # Write req.txt
    return {"union": requirements_txt_set}


def check_all_repo_deps(
    bundle_path: str,
) -> list[LocalLibFunc_IterResult[dict[str, Any]]]:
    """Check all bundles in the repo

    :param str bundle_path: The filepath to the bundle"""

    return iter_local_bundle_with_func(bundle_path, [(check_repo_deps, (), {})])


if __name__ == "__main__":
    app()
