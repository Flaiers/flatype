#!/bin/bash
python_interpreter=""

read -p "----------------------
| Python interpreter |
----------------------
Default: /usr/bin/python3
If you wont to change, write: " python_interpreter


if [ -z "$python_interpreter" ]; then
    /usr/bin/python3 -m venv env
else
    `$python_interpreter -m venv env`
fi

source env/bin/activate
pip install -U pip && pip install --no-cache-dir -r requirements.txt

cd src/

python manage.py collectstatic
python manage.py migrate
python manage.py runserver --insecure