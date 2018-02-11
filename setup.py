import os
import sys
from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


with open('requirements.txt') as f:
    required = f.readlines()


setup(
    name='way2sms',
    version='0.1.0',
    description='A python module to send sms via way2sms.com.',
    long_description=long_description,
    author='Rohit Gupta',
    url='https://github.com/guptarohit/way2sms',
    py_modules=['way2sms'],
    install_requires=required,
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)