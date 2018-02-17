import os
from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

with open('requirements.txt') as f:
    required = f.readlines()


setup(
    name='smspy',
    version='0.4.4',
    description='A python module for sending free sms via website way2sms',
    long_description=long_description,
    author='Rohit Gupta',
    url='https://github.com/guptarohit/smspy',
    py_modules=['smspy'],
    install_requires=required,
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
