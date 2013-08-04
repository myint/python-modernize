check:
	pep8 libmodernize python-modernize setup.py
	pylint --errors-only --include-ids=yes --disable=E1101 --rcfile=/dev/null libmodernize python-modernize setup.py
	check-manifest --ignore=.travis.yml,Makefile,MANIFEST.in,test.cram
	python setup.py --long-description | rst2html.py --strict > /dev/null
	scspell libmodernize setup.py README.rst

readme:
	@restview --long-description --strict
