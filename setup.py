from pathlib import Path
from setuptools import setup, find_packages


requirements = list()
with Path("requirements.txt").open(encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()
        if line:
            requirements.append(line)


setup(
    name="nlm-ingestor",
    version="1.0.5",
    description="Parsers and ingestors for different file types and formats",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nlmatics/nlm-ingestor",
    author="Ambika Sukla",
    author_email="ambika.sukla@nlmatics.com",
    license="Apache License 2.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "ingestor_utils/*.txt",
            "ingestor_models/symspell/*.txt"
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
