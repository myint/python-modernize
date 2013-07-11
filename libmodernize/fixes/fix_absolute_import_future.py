"""Like lib2to3.fixes.fix_import, but add the absolute_import future to all
files"""
from lib2to3.fixes import fix_import
from libmodernize import add_future

class FixAbsoluteImportFuture(fix_import.FixImport):
    def finish_tree(self, tree, name):
        if tree.children:
            add_future(tree, 'absolute_import')
