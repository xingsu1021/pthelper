#!/bin/bash

#初始化数据库
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80

#/usr/sbin/unitd --no-daemon --control 0.0.0.0:60081 --user root --group root
#windows
#set APP_ENV=prod
#python3 manage.py migrate
#python3 manage.py runserver 0.0.0.0:80