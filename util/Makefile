pep8 = pep8 --show-pep8 --show-source

lint-pep8:
	${pep8} *.py

lint-pylint:
	pylint t*.py

graph:
	pylint --import-graph=dependency.dot tree.py
	dot -Tpng dependency.dot -o dependency.png
	rm dependency.dot
