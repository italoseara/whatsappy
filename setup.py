from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='whatsappy',
    version='0.0.1',
    description='Whatsappy is a Python library for creating whatsapp bots.',
    py_modules=['wpp'],
    package_dir={'': 'whatsappy'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "selenium ~= 3.141.0",
        "Send2Trash ~= 1.5.0",
        "webdriver-manager ~= 3.2.2",
    ],
    extra_requires = {
        "dev": [
            "pytest>=3.7",
        ]
    },
    url='https://github.com/italoseara/whatsappy',
    author='Italo Seara',
    author_email='italos.seara@gmail.com',
)