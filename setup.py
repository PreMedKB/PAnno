#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
  readme = readme_file.read()

with open('HISTORY.md') as history_file:
  history = history_file.read()

requirements = ['pandas>=1.3.2', 'numpy>=1.19.5', 'pyranges>=0.0.117']

test_requirements = ['pandas>=1.3.2', 'numpy>=1.19.5', 'pyranges>=0.0.117']

setup(
    author="Yaqing Liu",
    author_email='yaqing.liu@outlook.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        'Natural Language :: English',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="PAnno is a Pharmacogenomics Annotation tool for clinical genomic testing.",
    entry_points={
        'console_scripts': [
            'panno=panno.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['pharmacology', 'drug responses', 'genomics', 'bioinformatics'],
    name='panno',
    packages=find_packages(include=['panno', 'panno.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PreMedKB/PAnno',
    version='0.2.1',
    zip_safe=False,
)
