all: build

lint: chiakilang chiakilisp
	pylint chiakilang chiakilisp

build: chiakilisp chiakilang setup.cfg
	rm -rf dist/*  # <------ do not forget to clean the ./dist directory first
	python -m build

install: build
	pip install --force-reinstall dist/chiakilisp-*.whl  # force reinstall pkg

upload: build
	python -m twine upload --repository pypi --verbose ./dist/chiakilisp-*.whl
