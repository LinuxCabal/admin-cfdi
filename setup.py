#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Setup for Admin CFDI '''

from setuptools import setup, find_packages

setup(name='Admin-CFDI',
      version='0.2.7',
      description='Herramienta para administracion de CFDIs',
      license='GPL 3.0',
      author='Mauricio Baeza',
      author_email='correopublico@mauriciobaeza.org',
      url='https://facturalibre.net/servicios/',
      packages=find_packages(),
      install_requires=['pygubu', 'selenium', 'pyqrcode', 'pysimplesoap'],
      package_data = {'': ['img/*.png', 'img/*.gif', 'ui/*']},
      scripts=['admin-cfdi','descarga-cfdi'])

# vim: ts=4 et sw=4
