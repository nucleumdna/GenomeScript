from setuptools import setup, find_packages

setup(
    name="nucleum",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "pysam>=0.21.0",
        "numpy>=1.26.0",
        "biopython>=1.81",
    ],
    author="Alexandru Ciocan",
    author_email="your.email@example.com",
    description="A genomic analysis framework with support for multiple file formats",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nucleum",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.13",
)
