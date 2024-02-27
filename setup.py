import importlib.util
import pathlib
import setuptools
import typing


KEYWORDS = [
        "metadata management",
        "filesystems"
    ]


def parse_requirements_file (filename: str) -> typing.List:
    """read and parse a Python `requirements.txt` file, returning as a list of str"""
    results: list = []

    with pathlib.Path(filename).open() as f:
        for l in f.readlines():
            results.append(l.strip().replace(" ", "").split("#")[0])

    return results


if __name__ == "__main__":
    base_packages = parse_requirements_file("requirements.txt")

    setuptools.setup(
        name="fsmirror",
        version = 0.3,
        url="https://github.com/wesmadrigal/fsmirror",
        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        install_requires = base_packages,
        extras_require = {
            "base": base_packages,
            },

        author="Wes Madrigal",
        author_email="wes@kurve.ai",
        license="MIT",

        description="A metadata management package based on filesystem mirroring.",
        long_description = pathlib.Path("README.md").read_text(),
        long_description_content_type = "text/markdown",

        keywords = ", ".join(KEYWORDS),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            ],

        project_urls = {
            "Source" : "http://github.com/wesmadrigal/fsmirror",
            "Issue Tracker" : "https://github.com/wesmadrigal/fsmirror/issues"
            },

        include_package_data=True,
        zip_safe=False,
        )
