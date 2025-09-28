"""
Setup script for Python Sudoku Generator and Solver.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()
                    and not line.startswith("#")]

setup(
    name="python-sudoku-generator-solver",
    version="2.0.0",
    author="Joe Carlson",
    author_email="joe@callmejoe.net",
    description="A comprehensive Sudoku puzzle generator and solver with multiple difficulty levels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joecarlson/python-sudoku-generator-solver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "mypy>=1.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sudoku-generator=sudoku_modern:main",
        ],
    },
    keywords="sudoku puzzle generator solver game logic",
    project_urls={
        "Bug Reports": "https://github.com/joecarlson/python-sudoku-generator-solver/issues",
        "Source": "https://github.com/joecarlson/python-sudoku-generator-solver",
        "Documentation": "https://github.com/joecarlson/python-sudoku-generator-solver#readme",
    },
)
