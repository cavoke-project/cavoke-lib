import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cavoke",
    version="0.0.1",
    author="Alex Kovrigin",
    author_email="a.kovrigin0@gmail.com",
    description="Python library for easy creation of text-based and table games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/waleko/cavoke",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
