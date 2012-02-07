"""
Virtstrap
=========

A bootstrapping mechanism for virtualenv, buildout, and shell scripts.
"""
from setuptools import setup, find_packages
import sys


# Installation requirements
REQUIREMENTS = [
    'virtualenv',
    'pyyaml',
    'jinja2',
]

if sys.version_info < (2, 7):
    REQUIREMENTS.append('argparse>=1.2.1')

setup(
    name="virtstrap",
    version="0.3.0-alpha",
    license="MIT",
    author="Reuven V. Gonzales",
    url="https://github.com/ravenac95/virtstrap",
    author_email="reuven@tobetter.us",
    description="A bootstrapping mechanism for virtualenv+pip and shell scripts",
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='*nix',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'vstrap = virtstrap.runner:main',
        ],
    },
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
    ],
)
