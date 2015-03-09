#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Setup for Admin CFDI '''

from distutils.core import setup

setup(name='Admin-CFDI',
      version='0.2.6',
      description='Herramienta para administracion de CFDIs',
      license='GPL 3.0',
      author='Mauricio Baeza',
      author_email='correopublico@mauriciobaeza.org',
      url='https://facturalibre.net/servicios/',
      install_requires=['pygubu', 'selenium', 'pyqrcode', 'pysimplesoap'],
      py_modules=['pyutil', 'values', 'template'],
      scripts=['admincfdi.py'])

# vim: ts=4 et sw=4
