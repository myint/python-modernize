# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer for print future import."""

# Local imports
from lib2to3 import pytree
from lib2to3 import fixer_base
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Name
from lib2to3.fixer_util import FromImport, Newline

from libmodernize import check_future_import


class FixPrintImport(fixer_base.BaseFix):

    """Add future import for print_function.

    This version properly respects shebangs.

    From:
    https://github.com/facebook/tornado/blob/master/maint/scripts/custom_fixers

    """

    BM_compatible = True

    PATTERN = """
              simple_stmt< any* bare='print' any* > | print_stmt
              """

    def start_tree(self, tree, filename):
        self.found_future_import = False

    def new_future_import(self, old):
        new = FromImport('__future__',
                         [Name('print_function', prefix=' ')])
        if old is not None:
            new.prefix = old.prefix
        return new

    def transform(self, node, results):
        self.found_future_import = True
        return self.new_future_import(node)

    def finish_tree(self, tree, filename):
        for node in tree.children:
            if 'print_function' in check_future_import(node):
                # already imported
                return

        if self.found_future_import:
            return
        if not isinstance(tree, pytree.Node):
            # Empty files (usually __init__.py) show up as a single Leaf
            # instead of a Node, so leave them alone
            return
        first_stmt = tree.children[0]
        if is_docstring(first_stmt):
            # Skip a line and add the import after the docstring
            tree.insert_child(1, Newline())
            pos = 2
        elif first_stmt.prefix:
            # No docstring, but an initial comment (perhaps a #! line).
            # Transfer the initial comment to a new blank line.
            newline = Newline()
            newline.prefix = first_stmt.prefix
            first_stmt.prefix = ''
            tree.insert_child(0, newline)
            pos = 1
        else:
            # No comments or docstring, just insert at the start
            pos = 0
        tree.insert_child(pos, self.new_future_import(None))
        tree.insert_child(pos + 1, Newline())  # terminates the import stmt


# copied from fix_tuple_params.py
def is_docstring(stmt):
    return isinstance(stmt, pytree.Node) and \
        stmt.children[0].type == token.STRING
