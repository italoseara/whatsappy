from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="whatsappy-py",
    version="3.0.0",
    description="Whatsappy is a Python library for creating whatsapp bots.",
    packages=["whatsappy"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
        "Topic :: Internet",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "selenium ~= 3.141.0",
        "Send2Trash ~= 1.5.0",
        "webdriver-manager ~= 3.2.2",
        "rich ~= 10.9.0",
        "qrcode ~= 7.3",
    ],
    extra_requires={
        "dev": [
            "pytest>=3.7",
        ]
    },
    url="https://github.com/italoseara/whatsappy",
    author="Italo Seara",
    author_email="italo.sseara@gmail.com",
    license="MIT",
)
