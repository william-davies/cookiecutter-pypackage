.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help lint lint/flake8
        {%- if cookiecutter.use_black == 'y' %} lint/black{% endif %}
.DEFAULT_GOAL := help

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_SLUG = {{ cookiecutter.project_slug }}
PYTHON_INTERPRETER_VERSION = {{ cookiecutter.python_interpreter_version }}

ifeq (,$(shell which conda))
	HAS_CONDA=False
else
	HAS_CONDA=True
endif

ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER_VERSION)))
	PYTHON_INTERPRETER=python3
else
	PYTHON_INTERPRETER=python
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

#################################################################################
# HELP                                                                          #
#################################################################################

define PRINT_HELP_PYSCRIPT
import re
import sys

makefile_lines = sys.stdin.readlines()
target_comment_pairs = []
idx = 0
while idx < len(makefile_lines):
    comment_match = re.match(r"^## ([\w ]+)$$", makefile_lines[idx])
    if comment_match:
        comment = comment_match.group(1)
        idx += 1
        target_match = re.match(r"^([\w/-]+):.*\n$$", makefile_lines[idx])
        target = target_match.group(1)
        target_comment_pairs.append((target, comment))
    idx += 1

max_target_length = 0
for target, _ in target_comment_pairs:
    if len(target) > max_target_length:
        max_target_length = len(target)

for target, comment in target_comment_pairs:
    print(f"{target:{max_target_length + 1}} {comment}")

endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

#################################################################################
# NON-HELP COMMANDS                                                             #
#################################################################################

## Set up Python interpreter environment
create_environment:
	ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
		conda create --name $(PROJECT_SLUG) python=$(PYTHON_INTERPRETER_VERSION)
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_SLUG)"
	else
		$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
		@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
		export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
		@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_SLUG) --python=$(PYTHON_INTERPRETER)"
		@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_SLUG)"
	endif

## Install Python Dependencies
install_requirements: clean test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	pre-commit install

## Test Python environment is set up correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := $(PYTHON_INTERPRETER) -c "$$BROWSER_PYSCRIPT"

## Remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test

## Remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## Remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## Remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

## Check style with flake8
lint/flake8:
	flake8 {{ cookiecutter.project_slug }} tests

{%- if cookiecutter.use_black == 'y' %}
## Check style with black
lint/black:
	black --check {{ cookiecutter.project_slug }} tests
{%- endif %}

## Check style
lint: lint/flake8{%- if cookiecutter.use_black == 'y' %} lint/black{%- endif %}

## Run tests quickly with the default Python
test:
{%- if cookiecutter.use_pytest == 'y' %}
	pytest
{%- else %}
	$(PYTHON_INTERPRETER) setup.py test
{%- endif %}

## Run tests on every Python version with tox
test-all:
	tox

## Check code coverage quickly with the default Python
coverage:
{%- if cookiecutter.use_pytest == 'y' %}
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	coverage run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

## Generate Sphinx HTML documentation, including API docs
docs:
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

## Compile the docs watching for changes
servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

## Package and upload a release
release: dist
	twine upload dist/*

## Builds source and wheel package
dist: clean
	$(PYTHON_INTERPRETER) setup.py sdist
	$(PYTHON_INTERPRETER) setup.py bdist_wheel
	ls -l dist

