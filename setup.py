from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as file:
    long_description = file.read()

setup(
    name='acetone',
    version='0.1.0',
    description="Glue code removal.",
    long_description=long_description,
    url='https://github.com/prokopst/acetone',
    author='Stanislav Prokop',
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    keywords="dependency injection ioc inversion of control service locator",
    packages=find_packages(exclude=['tests', 'tutorials']),
)
