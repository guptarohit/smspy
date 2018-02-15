import os
from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

required = ['beautifulsoup4', 'requests']


setup(
    name='way2sms',
    version='0.4.0',
    description='A python module to send sms via way2sms.com.',
    long_description=long_description,
    author='Rohit Gupta',
    url='https://github.com/guptarohit/way2sms',
    py_modules=['way2sms'],
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
