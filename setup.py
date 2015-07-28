#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Setup for Admin CFDI '''

from setuptools import setup, find_packages
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(name='Admin-CFDI',
      version='0.3.0',
      description='Herramienta para administracion de CFDIs',
      license='GPL 3.0',
      author='Ver contributors.txt',
      author_email='public@mauriciobaeza.net',
      url='https://facturalibre.net/servicios/',
      packages=find_packages(),
      install_requires=reqs,
      package_data={'': ['img/*.png', 'img/*.gif', 'ui/*', 'template/*']},
      scripts=[
        'admin-cfdi','descarga-cfdi', 'cfdi2pdf', 'admin-cfdi.pyw',
        'descarga-cfdi.cmd', 'cfdi2pdf.cmd']
    )

# vim: ts=4 et sw=4
