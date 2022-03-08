#!/bin/bash

#初始化数据库
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
#gunicorn pthelper.wsgi:application --bind 0.0.0.0:8000 -w 4 --threads 2 --daemon

#nginx -g 'daemon off;'