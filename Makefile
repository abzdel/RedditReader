install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py
	#black tests/*.py

lint:
	pylint --disable=R,C tests/*.py

test:
	pytest tests/test-invoke.py

all: install test format