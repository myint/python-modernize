import re
from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.fixer_util import touch_import, Name, Call

_literal_re = re.compile(r"[uU][rR]?[\'\"]")


class FixUnicode(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """
        STRING |
        power< name='unicode'
            trailer< '(' [any] ')' >
            any *
        >
    """

    def transform(self, node, results):
        if 'name' in results:
            touch_import(None, 'six', node)
            name = results['name']
            name.replace(Name('six.text_type', prefix=name.prefix))
        elif node.type == token.STRING and _literal_re.match(node.value):
            touch_import(None, 'six', node)
            new = node.clone()
            new.value = new.value[1:]
            new.prefix = ''
            node.replace(Call(Name('six.', prefix=node.prefix), [new]))
