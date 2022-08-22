#!/bin/bash

docker build -f Dockerfile -t xingsu1021/pthelper:v2.0.0 .

docker tag xingsu1021/pthelper:v2.0.0 xingsu1021/pthelper:latest