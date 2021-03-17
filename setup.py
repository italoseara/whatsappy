from setuptools import setup

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
)