#!/bin/bash

virtualenv venv --no-site-packages -p python3.7
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
