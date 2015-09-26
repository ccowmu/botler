CONFIG=config.json

setup: virtualenv requirements

virtualenv: bin/

run:
	PYTHONPATH=. bin/python botler.py ${CONFIG}

bin/:
	virtualenv -p python3 .

requirements:
	bin/pip install -r requirements.txt

.PHONY: setup virtualenv requirements test

