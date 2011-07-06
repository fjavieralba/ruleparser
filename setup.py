# -*- coding: utf-8 -*-
from distutils.core import setup

import ruleparser 

setup(name = 'ruleparser',
      version = '1.0',
      description = 'Tagging Rules Engine',
      author = ruleparser.__author__,
      author_email = ruleparser.__email__,
      url = 'http://labs.paradigmatecnologico.com',
      data_files = [('/etc/ruleparser', ['conf/package.conf'])],
      packages = ['ruleparser'],
      scripts = ['scripts/execute_package.py']
      )
