"""Like lib2to3.fixes.fix_import, but add the absolute_import future to all
files."""

from lib2to3.fixes import fix_import
from lib2to3.pygram import python_symbols

from libmodernize import add_future_import


class FixAbsoluteImportFuture(fix_import.FixImport):

    def finish_tree(self, tree, name):
        super(FixAbsoluteImportFuture, self).finish_tree(tree, name)

        for node in tree.children:
            if not (node.type == python_symbols.simple_stmt and node.children):
                continue

            node = node.children[0]
            if (
                node.type == python_symbols.import_name or
                (node.type == python_symbols.import_from and
                 node.children[1].value != '__future__')
            ):
                add_future_import(tree, 'absolute_import')
                break
