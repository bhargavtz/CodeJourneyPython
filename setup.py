#!/usr/bin/env python
"""Setup configuration for CodeJourneyPython package."""

from setuptools import setup, find_packages

setup(
    name="codejourneypython",
    version="0.1.0",
    description="A comprehensive Python learning platform with AI agents, ML projects, and data engineering",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="bhargav_sz",
    license="MIT",
    packages=find_packages(where="projects"),
    package_dir={"": "projects"},
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "isort>=5.13.0",
            "mypy>=1.7.0",
        ],
        "ml": [
            "pandas>=2.1.0",
            "numpy>=1.26.0",
            "scikit-learn>=1.3.0",
        ],
        "agents": [
            "anthropic>=0.7.0",
            "openai>=1.6.0",
            "langchain>=0.1.0",
        ],
        "web": [
            "fastapi>=0.109.0",
            "uvicorn>=0.27.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
