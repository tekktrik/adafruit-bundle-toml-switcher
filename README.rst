adafruit-bundle-toml-switcher
=============================

A script to convert the Adafruit Bundle from setup.py to pyproject.toml

Installation
============

- Update submodules
- Run bash script
- Run toml program

Notes
=====

SCM version is removed from `pyproject.toml` since field testing

Usage
=====

- make sure all libraries are at ABSOLUTE CURRENT `main`
- check for `optional_requirements.txt`
- get_dependencies.check-dependencies to get list of requirements
- manually clean requirements as necessary, including marking optional with preceding OPTIONAL:
- run clean_dependencies.clean-dependencies to tidy up the requirements
- run build_toml.generate-toml-files to create `pyproject.toml` files
- run file_generation.overwrite-workflows to overwrite CI files
- run file_generation.add-requirements-files to overwrite requirements files
- run file_generation.toml-swap to swap `setup.py` for `pyproject.toml`
- check the modifications made to the libraries
- push the code to `main` (upstream, if on a fork)
- readd optional dependencies that already exist (adafruitio, ssd1306, others...)
