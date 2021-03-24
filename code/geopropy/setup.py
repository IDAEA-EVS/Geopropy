import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geopropy", 
    version="0.1-alpha",
    author="Ashkan Hassanzadeh",
    author_email="Ashkanhassanzadeh@gmail.com ",
    description="Automatic 3D Geological Cross Section Generation",
    long_description=long_description,
    long_description_content_type="markdown",
    url="https://github.com/...",
    packages=setuptools.find_packages(),
    install_requires = ['math',
                       'pypyodbc',
                       'time'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: agpl-3.0 License",
        "Operating System :: Windows",
    ],
    python_requires='=2.7',
)