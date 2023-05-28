.PHONY: algos

all: build

lint: chiakilang chiakilisp
	pylint chiakilang chiakilisp

test:
	find tests -name \*.cl -exec ./chiakilang {} \;  # <---- using local files

algos:
	find algos/cl/ -name \*.cl -exec ./chiakilang --settingsless {} \; # algos

build: chiakilang chiakilisp setup.cfg
	rm -rf dist/*  # <------ do not forget to clean the ./dist directory first
	python -m build

upload: lint test build
	python -m twine upload --repository pypi --verbose ./dist/chiakilisp-*.whl

install: lint test build
	pip install --force-reinstall dist/chiakilisp-*.whl  # force reinstall pkg

build-upload-install: lint build
	python -m twine upload --repository pypi --verbose ./dist/chiakilisp-*.whl
	pip install --force-reinstall dist/chiakilisp-*.whl  # force reinstall pkg
