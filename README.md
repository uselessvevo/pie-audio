## Pie Audio - Simple audio editor with plug-ins support

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

[English docs](https://github.com/uselessvevo/pie-audio/tree/docs/docs/en/piekit) • [Русская документация](https://github.com/uselessvevo/pie-audio/tree/docs/docs/ru/piekit)

## Special thanks
I want to appreciate the [spyder-ide](https://github.com/spyder-ide/spyder) project - part of the code is based on this project.

## Before the start
> *Notice*: At this moment, this application still in deep development and there is no reason to create installation package. First you need to download/clone the application:

1. Download via git - `git clone https://github.com/uselessvevo/pie-audio.git `
2. Initialize virtual environment - `python -m venv venv`
3. Set up [the configuration module](https://github.com/uselessvevo/pie-audio/blob/docs/docs/en/piekit/Configs.md)
4. Run program - `python ./pie-audio.py`

To install this app: `pip install .`

## Development

1. We're using the `snake_case` feature - that means, you need to generate `*.pyi` files by typing this command: `pyside6-genpyi all --feature snake_case`
2. Start the `pie-audio-server`
