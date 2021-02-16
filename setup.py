"""
setup.py for financio
"""

import os

from setuptools import setup, find_packages

from playwright_migrate import __version__


this_dir = os.path.abspath(os.path.dirname(__file__))


NAME = "Python Playwright Migrate"
VERSION = __version__
PACKAGES = find_packages(exclude=["ez_setup"])
DESCRIPTION = "Migrate test cases from Playwright pre-release to 1.8+ API"
URL = "https://github.com/jmmjsolutions/playwright-python-migrate"
LICENSE = "Apache License Version 2.0"
LONG_DESCRIPTION = open(os.path.join(this_dir, "README.rst")).read()
REQUIREMENTS = [
    _f
    for _f in open(os.path.join(this_dir, "requirements.txt")).read().splitlines()
    if _f
]
AUTHOR = "Mark J. Rees"
AUTHOR_EMAIL = "mark@jmmjsolutions.com"
KEYWORDS = ("test", "testing", "migration")
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Testing",
]
CONSOLE_SCRIPTS = [
    'playwright_migrate = playwright_migrate.main:main',
]


params = dict(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    install_requires=REQUIREMENTS,
    # metadata for upload to PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
    entry_points={"console_scripts": CONSOLE_SCRIPTS},
)

setup(**params)