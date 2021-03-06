::

    Python
       _ __  ___  __| |___ _ _ _ _ (_)______
      | '  \/ _ \/ _` / -_) '_| ' \| |_ / -_)
      |_|_|_\___/\__,_\___|_| |_||_|_/__\___|

.. image:: https://travis-ci.org/myint/python-modernize.svg?branch=master
    :target: https://travis-ci.org/myint/python-modernize
    :alt: Build status

python-modernize is a very thin wrapper around lib2to3 to utilize it to make
Python 2 code more modern with the intention of eventually porting it over to
Python 3. This is an unofficial fork (of
https://github.com/mitsuhiko/python-modernize) that runs on both Python 2 and
3.

It does not guarantee, but it attempts to spit out a Python 2/3
compatible codebase.

Unicode Literal Control:

- By default modernize will leave literals alone.
- The ``--future-unicode`` flag imports the ``unicode_literals`` from the
  ``__future__`` module. This requires Python 2.6 and later and will require
  that you mark bytestrings with ``b''`` and native strings in ``str(b'')`` or
  something similar that survives the transformation.


Installation
------------

From pip::

    $ pip install --upgrade modernize3k


Usage
-----

Preview changes on a file or directory::

    $ python-modernize example.py

Write the changes::

    $ python-modernize --write example.py

Modify doctests rather than normal code::

    $ python-modernize --write --doctests example.py


Tests
-----

The tests use cram_::

    $ cram --indent=4 test.cram

.. _cram: https://pypi.python.org/pypi/cram
