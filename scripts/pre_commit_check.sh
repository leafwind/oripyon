#!/bin/bash
source venv/bin/activate

echo "# -------------------"
echo "# running nosetests"
echo "# -------------------"
python -m pytest --cov=./ --cov-config=.coveragerc

echo "# -------------------"
echo "# pyflakes"
echo "# -------------------"
pyflakes app/ tests/
flake8 . --count --exit-zero --max-complexity=15 --max-line-length=120 --statistics --exclude=venv,taiwan_area_map,line-user-info

echo "# -------------------"
echo "# pylint"
echo "# -------------------"
pylint -d all -e W0611,W0612,W0613,W0614 --reports=n --msg-template='{msg_id} {path}:{line} {msg} ({symbol})' app/ tests/
