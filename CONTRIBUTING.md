# tamcolors developers guide

## install tamcolors
* install tamcolors: "pip install -e .[dev]" note you will need a compiler on your machine

## run tests 
* run tests: "./run_tests.py"

## build docs
* build docs: "./tamcolors/docs/build_docs.bat"

## create/push pypi packages
* python setup.py sdist bdist_wheel
* twine upload dist/*
* twine username: CharlesMcMarrow
* twine password: XXXXXXXXX
