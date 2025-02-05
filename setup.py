from setuptools import setup, find_packages

setup(
    name="genomescript",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "pysam>=0.21.0",
        "numpy>=1.26.0",
        "biopython>=1.81",
    ],
    author="nucleumdna",
    author_email="contact@nucleumdna.com",
    description="A comprehensive genomic analysis framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nucleumdna/GenomeScript",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.13",
)
