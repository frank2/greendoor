#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'greendoor'
    ,version = '0.1.0'
    ,author = 'frank2'
    ,author_email = 'frank2@dc949.org'
    ,description = 'An authenticated gevent.backdoor'
    ,license = 'GPLv3'
    ,keywords = 'memory_management ctypes'
    ,url = 'https://github.com/frank2/greendoor'
    ,package_dir = {'greendoor': 'greendoor'}
    ,packages = ['greendoor']
    ,install_requires = ['gevent>=1.2.2']
    ,classifiers = [
        'Development Status :: 4 - Beta'
        ,'Topic :: Software Development :: Libraries'
        ,'License :: OSI Approved :: GNU General Public License v3 (GPLv3)']
)
