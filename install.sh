#!/bin/bash
python_interpreter=""

read -p "----------------------
| Python interpreter |
----------------------
Default: /usr/bin/python3
(Сlick Enter for choose default)
If you wont to change, write: " python_interpreter


if [ -z "$python_interpreter" ]; then
    /usr/bin/python3 -m venv env
else
    `$python_interpreter -m venv env`
fi

source env/bin/activate
pip install -U pip && pip install -r requirements.txt

python src/manage.py collectstatic
python src/manage.py migrate
python src/manage.py runserver --insecure