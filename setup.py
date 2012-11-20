#!/usr/bin/env python

from distutils.core import setup

setup(
      name = 'socketcache'
   ,  version = '0.1.0'
   ,  description = 'Maintains a cache of socket objects'
   ,  long_description = """A simple pure python cache of UDP socket objects, supporting a \
custom TTL, IPv{4,6} and random balancing. Intended to assist in sending a lot of UDP packets \
to a host addressed by FQDN without burdening the local resolver. The local machine may not \
have a caching resolver at all, making it a good idea for the application to manage a cache itself."""
   ,  author = 'Derp Ston'
   ,  author_email = 'derpston+pypi@sleepygeek.org'
   ,  url = 'https://github.com/derpston/python-socketcache'
   ,  packages = ['']
   ,  package_dir = {'': 'src'}
   )

