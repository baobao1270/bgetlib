import setuptools
import bgetlib
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.read().strip().replace("\r", "").split("\n")

setuptools.setup(
    name=bgetlib.__title__,
    version=os.environ.get("BUILD_VERSION", "3.2.6"),
    author=bgetlib.__author__,
    author_email=bgetlib.__author_email__,
    description=bgetlib.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=bgetlib.__url__,
    license=bgetlib.__license__,
    packages=["bgetlib"],
    package_data={'': ['LICENSE'], "bgetlib": ["ffmpeg.exe"]},
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    project_urls={
        "Source": bgetlib.__source__,
        "Documentation": bgetlib.__url__
    }
)
