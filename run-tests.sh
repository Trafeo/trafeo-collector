#!/bin/bash
CUR=`pwd`
# Run all of the tests in the tests/ directory
echo -n 'Running unit tests in tests/'
cd tests
python -m unittest discover --pattern=*.py
cd $CUR