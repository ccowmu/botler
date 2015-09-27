CONFIG=config.json

setup: virtualenv requirements

virtualenv: bin/

run:
	PYTHONPATH=. bin/python botler.py ${CONFIG}

bin/:
	virtualenv -p python3 .

requirements:
	bin/pip install -r requirements.txt

clean:
	rm -rf bin include lib pip-selfcheck.json ./**/*.pyc ./**/__pycache__/

.PHONY: setup virtualenv requirements test

