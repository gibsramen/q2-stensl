import ast
import re

from setuptools import setup, find_packages

_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("q2_stensl/__init__.py", "rb") as f:
    hit = _version_re.search(f.read().decode("utf-8")).group(1)
    version = str(ast.literal_eval(hit))

setup(
    name="q2_stensl",
    version=version,
    author="Liat Shenav",
    packages=find_packages(),
    scripts=["q2_stensl/stensl.R"],
    entry_points={
        "qiime2.plugins": ["stensl=q2_stensl.plugin_setup:plugin"]
    }
)
