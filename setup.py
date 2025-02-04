from setuptools import setup, find_packages

setup(
    name="GenomeScript",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pysam",
        "numpy",
        "tensorflow",
        "keras",
        "py-ecc"
    ],
    entry_points={
        'console_scripts': [
            'genomescript=genomescript_compiler:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
