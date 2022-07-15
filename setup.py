import os
from setuptools import setup


if __name__ == "__main__":
    os.environ['PYTHONSTARTUP'] = 'cloudykit.bootstrap:setup_main'
    setup()
