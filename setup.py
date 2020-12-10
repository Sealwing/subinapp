#!/usr/bin/env python

from distutils.core import setup

setup(
    name='subinapp',
    version='0.1.0',
    description='Helpers for In App Purchases and Subscriptions validation on backend',
    author='sealwing',
    author_email='sealinsky@gmail.com',
    license='MIT',
    requires=['inapppy'],
    packages=['subinapp', 'subinapp.core', 'subinapp.interface']
)
