# -*- coding: utf-8 -*-

__version__ = '0.0.6.dev0'

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

install_requires = [
    'amnesiacms'
]

setup(
    name='amnesia_multilingual',
    version=__version__,
    description='amnesia CMS',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Julien Cigar',
    author_email='julien@perdition.city',
    url='https://github.com/silenius/amnesia_multilingual',
    keywords='web wsgi pyramid cms sqlalchemy',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
