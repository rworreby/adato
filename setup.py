import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="adato",
    version="0.1.0",
    description="Allpurpose Document Annotation Tool for Active Learning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rworreby/adato",
    author="Robin Worreby",
    author_email="robin@worreby.ch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "adato=adato.__main__:main",
        ]
    },
)
