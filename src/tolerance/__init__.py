# coding=utf-8
"""
tolerance

tolerance is a function decorator to make a tolerant function; a function
which does not raise any exceptions even there are exceptions.
This concept is quite useful for making stable product or ``prefer_int`` types
of code described in Usage section.

"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('__version__', 'tolerate', 'argument_switch_generator')
import os.path
from pkg_resources import get_distribution
from pkg_resources import DistributionNotFound

DISTRIBUTION_NAME = 'tolerance'

# get version information from setup.py
try: 
    _dist = get_distribution(DISTRIBUTION_NAME)
    if not __file__.startswith(os.path.join(_dist.location,
                                            DISTRIBUTION_NAME)):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version

# shortcut
from tolerance.decorators import tolerate
from tolerance.utils import argument_switch_generator

VERSION = tuple(map(tolerate(lambda x: x)(int), __version__.split('.')))
