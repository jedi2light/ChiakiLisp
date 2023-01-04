all: build

lint: chiakilang chiakilisp
	pylint chiakilang chiakilisp

build: chiakilang chiakilisp setup.cfg
	rm -rf dist/*  # <------ do not forget to clean the ./dist directory first
	python -m build

upload: lint build
	python -m twine upload --repository pypi --verbose ./dist/chiakilisp-*.whl

install: lint build
	pip install --force-reinstall dist/chiakilisp-*.whl  # force reinstall pkg

build-upload-install: lint build
	python -m twine upload --repository pypi --verbose ./dist/chiakilisp-*.whl
	pip install --force-reinstall dist/chiakilisp-*.whl  # force reinstall pkg