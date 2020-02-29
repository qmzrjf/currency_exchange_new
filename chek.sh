 #! /bin/bash

python src/manage.py check
flake8
python src/manage.py test
pip check