import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bgetlib",
    version="1.0.0",
    author="Joseph Chris",
    author_email="joseph@josephcz.xyz",
    description="A bilibili API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baobao1270/bgetlib",
    packages=["bgetlib", "bgetlib.Data"],
    install_requires=[
        "xyz.josephcz.dict2class>=1.0.0",
        "xyz.josephcz.dictmapper>=1.1.0",
        "requests>=2.25.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
