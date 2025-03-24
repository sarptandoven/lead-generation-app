#!/bin/bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install setuptools wheel
pip install -r requirements.txt

chmod +x build.sh
