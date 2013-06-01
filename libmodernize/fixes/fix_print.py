# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer for print.

Change:
    'print'          into 'print()'
    'print ...'      into 'print(...)'
    'print ... ,'    into 'print(..., end=" ")'
    'print >>x, ...' into 'print(..., file=x)'

No changes are applied if print_function is imported from __future__

"""

from __future__ import unicode_literals

from lib2to3 import patcomp, pytree, fixer_base
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Name, Call, Comma, FromImport, Newline, String

from libmodernize import check_future_import

parend_expr = patcomp.compile_pattern(
    """atom< '(' [arith_expr|atom|power|term|STRING|NAME] ')' >"""
)


class FixPrint(fixer_base.BaseFix):

    BM_compatible = True

    PATTERN = """
              simple_stmt< any* bare='print' any* > | print_stmt
              """

    def start_tree(self, tree, filename):
        self.found_print = False

    def transform(self, node, results):
        assert results

        bare_print = results.get('bare')

        if bare_print:
            # Special-case print all by itself
            bare_print.replace(Call(Name('print'), [],
                               prefix=bare_print.prefix))
            return
        assert node.children[0] == Name('print')
        args = node.children[1:]
        if len(args) == 1 and parend_expr.match(args[0]):
            # We don't want to keep sticking parens around an
            # already-parenthesised expression.
            return

        sep = end = file = None
        if args and args[-1] == Comma():
            args = args[:-1]
            end = ' '
        if args and args[0] == pytree.Leaf(token.RIGHTSHIFT, '>>'):
            assert len(args) >= 2
            file = args[1].clone()
            args = args[3:]  # Strip a possible comma after the file expression
        # Now synthesize a print(args, sep=..., end=..., file=...) node.
        l_args = [arg.clone() for arg in args]
        if l_args:
            l_args[0].prefix = ''
        if sep is not None or end is not None or file is not None:
            if sep is not None:
                self.add_kwarg(l_args, 'sep', String(repr(sep)))
            if end is not None:
                self.add_kwarg(l_args, 'end', String(repr(end)))
            if file is not None:
                self.add_kwarg(l_args, 'file', file)
        n_stmt = Call(Name('print'), l_args)
        n_stmt.prefix = node.prefix

        self.found_print = True
        return n_stmt

    def add_kwarg(self, l_nodes, s_kwd, n_expr):
        # XXX All this prefix-setting may lose comments (though rarely)
        n_expr.prefix = ''
        n_argument = pytree.Node(self.syms.argument,
                                 (Name(s_kwd),
                                  pytree.Leaf(token.EQUAL, '='),
                                  n_expr))
        if l_nodes:
            l_nodes.append(Comma())
            n_argument.prefix = ' '
        l_nodes.append(n_argument)

    def finish_tree(self, tree, filename):
        if not self.found_print:
            return

        for node in tree.children:
            if 'print_function' in check_future_import(node):
                # already imported
                return

        add_future_import('print_function', tree)


def add_future_import(name, tree):
    """Add future import.

    From: https://github.com/facebook/tornado

    Copyright 2009 Facebook

    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License. You may obtain
    a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.

    """
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
    tree.insert_child(
        pos,
        FromImport('__future__', [Name(name, prefix=' ')]))
    tree.insert_child(pos + 1, Newline())  # terminates the import stmt


# copied from fix_tuple_params.py
def is_docstring(stmt):
    return isinstance(stmt, pytree.Node) and \
        stmt.children[0].type == token.STRING
