#!/bin/sh
# This is a comment!
echo Setting app packges
npm install

echo Running Script
python setup_test.py

echo Validating Script outputs
python validate_data.py