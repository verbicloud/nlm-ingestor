from setuptools import setup, find_packages

setup(
    name="nlm-ingestor",
    version="0.1.7",
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
        ]
    },
    install_requires=[
        "flask",
        "flask_restful",
        "flask_jsonpify",
        "gunicorn",
        "werkzeug",
        "tika",
        "bs4",
        "nltk",
        "python-magic",
        "numpy",
        "tqdm",
        "symspellpy>=6.7.0",
        "pandas>=1.2.4",
        "mistune==2.0.3",
        "lxml==4.9.1",
        "unidecode",
        "nlm-utils",
    ],
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
