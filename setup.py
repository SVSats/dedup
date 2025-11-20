from setuptools import setup, find_packages

setup(
    name="dedup",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["dedup-cli=dedup.cli:main"],
        "gui_scripts": ["dedup-gui=dedup.gui:main"],
    },
    python_requires=">=3.8",
    author="SVSats",
    description="Eliminador seguro de archivos duplicados para Linux.",
)
