check:
	pep8 libmodernize python-modernize setup.py
	pylint \
		--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' \
		--errors-only \
		--disable=E1101 \
		--rcfile=/dev/null \
		libmodernize python-modernize setup.py
	check-manifest
	python setup.py --long-description | rstcheck -
	scspell setup.py README.rst

readme:
	@restview --long-description --strict
