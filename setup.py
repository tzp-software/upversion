try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from versionup import get_version
version = get_version()

config = {
    'name' : 'versionup',
    'version': version,
    'author': 'kyle roux',
    'author_email' : 'jstacoder@gmail.com',
    #'install_requires' : ['nose'],
        }
setup(**config)