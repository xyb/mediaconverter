test: unittest

unittest:
	pytest

coverage:
	pytest --cov-report html --cov-report xml
