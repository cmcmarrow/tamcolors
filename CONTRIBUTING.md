# tamcolors developers guide

## Note
This is a guild for people who want to help develop tamcolros.
If you just want to use tamcolors please just "pip install tamcolors"

## install tamcolors Windows
* Have Visual Studio Installed with C/C++ tools
* Then run "./build_scripts/build_win_env.bat

## install tamcolors Linux
* Have a C/C++ compiler on your machine
* Then run "./build_scripts/build_linux_env.bat

## install tamcolors Mac
* Have a C/C++ compiler on your machine VIA XCODE
* Then run "./build_scripts/build_mac_env.bat

## run tests 
* run tests: "./run_tests.py"
* run slow tests: "./run_slow_tests.py"

## build docs
* build docs: "./tamcolors/docs/build_docs.bat"

## check manifest
* make/check manifest "check-manifest"

## create/push pypi packages
* python setup.py sdist bdist_wheel
* twine upload dist/*
* twine username: CharlesMcMarrow
* twine password: XXXXXXXXX
