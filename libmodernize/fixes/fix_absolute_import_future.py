"""Like lib2to3.fixes.fix_import, but add the absolute_import future to all
files."""

from lib2to3.fixes import fix_import
from lib2to3.pygram import python_symbols

from libmodernize import add_future_import

class FixAbsoluteImportFuture(fix_import.FixImport):

    def start_tree(self, tree, name):
        super(FixAbsoluteImportFuture, self).start_tree(tree, name)
        self.found_import = False

    def transform(self, node, results):
        value = super(FixAbsoluteImportFuture, self).transform(node, results)
        if value:
            self.found_import = True
        return value

    def finish_tree(self, tree, name):
        #if self.found_import:
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
