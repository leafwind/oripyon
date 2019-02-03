#!/bin/bash
source venv/bin/activate

echo "# -------------------"
echo "# running nosetests"
echo "# -------------------"
nosetests --with-coverage --cover-erase --cover-inclusive --cover-package=app

echo "# -------------------"
echo "# pyflakes"
echo "# -------------------"
pyflakes app/ tests/

echo "# -------------------"
echo "# pylint"
echo "# -------------------"
pylint -d all -e W0611,W0612,W0613,W0614 --reports=n --msg-template='{msg_id} {path}:{line} {msg} ({symbol})' app/ tests/
