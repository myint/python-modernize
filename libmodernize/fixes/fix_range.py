# Copyright 2008 Armin Ronacher.
# Licensed to PSF under a Contributor Agreement.

from __future__ import unicode_literals

from lib2to3 import fixer_base
from lib2to3.fixer_util import touch_import


class FixRange(fixer_base.BaseFix):

    BM_compatible = True
    order = 'pre'

    PATTERN = """
    power< name='range'|'xrange'
        trailer< '('
            arglist< (
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any) |
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any) |
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any)
            ) >
        ')' >
    >
    """

    def transform(self, node, results):
        touch_import('six.moves', 'range', node)
        results['name'][0].value = 'range'
