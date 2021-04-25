from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="whatsappy-py",
    version="2.0.4",
    description="Whatsappy is a Python library for creating whatsapp bots.",
    packages=["whatsappy"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "selenium ~= 3.141.0",
        "Send2Trash ~= 1.5.0",
        "webdriver-manager ~= 3.2.2",
        "opencv-python ~= 4.5.1.48",
    ],
    extra_requires={
        "dev": [
            "pytest>=3.7",
        ]
    },
    url="https://github.com/italoseara/whatsappy",
    author="Italo Seara",
    author_email="italos.seara@gmail.com",
    license="MIT",
)