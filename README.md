# Pie Audio - Simple audio editor with plug-ins support

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Documentation
[English](https://github.com/uselessvevo/pie-audio/tree/main/docs/en/piekit) • [Русский](https://github.com/uselessvevo/pie-audio/tree/main/docs/ru/piekit)

Before I start, I want to say a special thanks to the creators of the [spyder-ide](https://github.com/spyder-ide/spyder) project, as some of the code is based on it.

## Installing and running the application
Since the project is currently under active development, the installation package available at [pypi](https://pypi.org/) is not yet available. This means that you will need the `git` versioning program and the `pip` package manager. Let's get started, shall we?

1. Download the project via `git`: ` git clone https://github.com/uselessvevo/pie-audio`.
2. Unpack the archive wherever you want
3. Install all dependencies (`pip install -r requirements/default.txt`) or install via package manager (`pip install .`)
4. Run the program: `python pie-audio.py` or `pie-audio.exe`

## Development

1. We're using the `snake_case` feature - that means, you need to generate `*.pyi` files by typing this command: `pyside6-genpyi all --feature snake_case`
2. Mark plugins directory as source directory