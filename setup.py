import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cavoke",
    version="0.1.0",
    author="Alex Kovrigin",
    author_email="a.kovrigin0@gmail.com",
    description="Python library for easy creation of text-based and table games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/waleko/cavoke",
    packages=setuptools.find_packages(),
    package_dir={"": "src"},
    python_requires=">=3.7, <4",
    requires=["dataclasses>=0.6"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
