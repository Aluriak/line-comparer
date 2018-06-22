

r: run
rc: run-no-colors
run:
	python line_comparer.py data/test-simple.txt
run-no-colors:
	python line_comparer.py data/test-simple.txt --no-colors


t: test
test:
	python -m pytest ./*.py --doctest-module -vv
