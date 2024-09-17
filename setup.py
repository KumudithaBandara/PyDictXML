from setuptools import setup, find_packages

setup(
    name="PyDictXML",
    version="1.0.1",
    description="PyDictXML is a high-performance Python library designed to seamlessly replace dicttoxml, offering users an improved experience in XML string generation.",  # Short description
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KumudithaBandara/PyDictXML",
    author="Kumuditha Bandara",
    author_email="kumu.bandara.kb97@gmail.com",
    license="GPLv2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "PyDictXML=dicttoxml:main",
        ],
    },
)
