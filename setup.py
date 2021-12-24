import setuptools
import codecs
import os


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="fmcclient",
    packages=setuptools.find_packages(),
    version=get_version("fmcclient/__init__.py"),
    license="GPL 3.0 https://www.gnu.org/licenses/gpl-3.0.txt",
    description="fmcclient",
    author="Aaron K. Hackney",
    author_email="aaron_309@yahoo.com",
    url="https://github.com/aaronhackney/fmcclient",
    download_url="",
    # keywords=["word1", "word2"],
    install_requires=["requests >= 2.25.1", "setuptools >= 51.1.2"],
    # entry_points={"console_scripts": ["pyftd = pyftd.__main__:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
