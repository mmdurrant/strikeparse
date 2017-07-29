# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='strikeparse',
    version='0.2dev',
    # packages=['strikeparse',],
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    include_package_data=True,
    install_requires = ['sortedcontainers']
)
