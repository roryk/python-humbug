#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys
import itertools

from setuptools import setup, find_packages


def recur_expand(target_root, dir):
  for root, _, files in os.walk(dir):
    paths = [os.path.join(root, f) for f in files]
    if len(paths):
      yield os.path.join(target_root, root), paths

def version():
  version_py = os.path.join(os.path.dirname(__file__), "humbug", "__init__.py")
  with open(version_py) as in_handle:
    version_line = itertools.dropwhile(lambda x: not x.startswith("__version__"),
                                       in_handle).next()
  version = version_line.split('=')[-1].strip().replace('"', '')
  return version


setup(name='humbug',
      version=version(),
      description='Bindings for the Humbug message API',
      author='Humbug, Inc.',
      author_email='humbug@humbughq.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Communications :: Chat',
      ],
      url='https://humbughq.com/dist/api/',
      packages=['humbug'],
      data_files=[('share/humbug/examples', ["examples/humbugrc", "examples/send-message"])] + \
          list(recur_expand('share/humbug', 'integrations/')) + \
          [('share/humbug/demos',
            [os.path.join("demos", relpath) for relpath in
            os.listdir("demos")])],
      scripts=["bin/humbug-send"],
      install_requires=["simplejson",
                        "requests"]
     )
