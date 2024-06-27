## Pie Audio - Simple audio editor with plug-ins support

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Documentation
[English](https://github.com/uselessvevo/pie-audio/tree/main/docs/en/piekit) • [Русский](https://github.com/uselessvevo/pie-audio/tree/main/docs/ru/piekit)

Before I start, I want to say a special thanks to the creators of the [spyder-ide](https://github.com/spyder-ide/spyder) project, as some code is based on it.

## Installing and running the application
Since the project is under active development, the installation package available on pypi is not yet available. This means that you will need the git versioning program and the pip package manager. Let's get started.

* Clone the project via git: `git clone https://github.com/uselessvevo/pie-audio`
* Create virtual environment via `python3-venv`
* Install all dependencies (`python -m pip install -r requirements.txt`) or install through the package manager (`pip install .`)
* Run the program: `python pie-audio.py` or `pie-audio.exe`

## Development 
* Type `pyside6-genpyi all --feature snake_case` to generate the PySide6's [snake case feature](https://doc-snapshots.qt.io/qtforpython-6.2/considerations.html#snake-case)
* Set `PIE_IS_DEV_ENV` environment variable to `1`

Then you need to mark the plugins directory as the source directory. After that, you good to go and write your own code :)