#!/usr/bin/env python3
"""
Setup script for TerminAI
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sudothink",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An intelligent terminal assistant that uses OpenAI's GPT-4 to help with complex shell tasks",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sudothink",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "sudothink=sudothink.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="terminal, ai, openai, shell, automation, productivity",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/sudothink/issues",
        "Source": "https://github.com/yourusername/sudothink",
        "Documentation": "https://github.com/yourusername/sudothink#readme",
    },
) 