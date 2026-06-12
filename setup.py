"""Legacy shim so `pip install -e .` works on older pip (<21.3) too.

All real metadata lives in pyproject.toml; this just enables editable installs
on systems whose pip predates PEP 660.
"""
from setuptools import setup

setup()
