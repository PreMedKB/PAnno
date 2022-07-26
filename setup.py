#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['pandas==1.3.2', 'numpy==1.19.5', 'pybedtools==0.9.0']

test_requirements = ['pandas==1.3.2', 'numpy==1.19.5', 'pybedtools==0.9.0']

setup(
    author="Yaqing Liu",
    author_email='yaqing.liu@outlook.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Clinical Pharmacogenomics Annotation Tool for Genomic Testing.",
    entry_points={
        'console_scripts': [
            'cpat=cpat.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cpat',
    name='cpat',
    packages=find_packages(include=['cpat', 'cpat.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PreMedKB/CPAT',
    version='0.1.0',
    zip_safe=False,
)
