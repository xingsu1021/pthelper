# pull official base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

# create the appropriate directories
ENV APP_HOME=/home/data/www
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# install dependencies
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y git libgomp1

# copy project
#COPY . $APP_HOME
RUN git clone https://github.com/xingsu1021/pthelper.git ${APP_HOME}

RUN pip install whl/python_Levenshtein-0.12.2-cp38-cp38-linux_x86_64.whl 
RUN pip install whl/future-0.18.2-py3-none-any.whl

#将需要的包体全部打包成直接安装的包whl
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

#RUN pip install --no-cache-dir whl/paddlepaddle-2.3.2-cp38-cp38-linux_x86_64.whl -i https://mirror.baidu.com/pypi/simple

RUN pip install --no-cache-dir https://paddle-wheel.bj.bcebos.com/2.3.2/linux/linux-cpu-mkl-noavx/paddlepaddle-2.3.2-cp38-cp38-linux_x86_64.whl -i https://mirror.baidu.com/pypi/simple

#容器报错ImportError: libGL.so.1: cannot open shared object file: No such file or dir
RUN pip uninstall opencv-python -y
RUN pip install --no-cache-dir opencv-contrib-python==4.4.0.46 opencv-python-headless==4.4.0.46 -i https://pypi.mirrors.ustc.edu.cn/simple/ --force
#RUN pip install --no-cache-dir opencv-contrib-python==4.4.0.46 -i https://pypi.mirrors.ustc.edu.cn/simple/
#RUN pip install --no-cache-dir opencv-python-headless==4.4.0.46 -i https://pypi.mirrors.ustc.edu.cn/simple/


COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /root/.cache && \
    rm -rf whl

RUN ln -s /home/data/www/db /db && \
    ln -s /home/data/www/logs /logs && \
    ln -s /home/data/www/backups /backups

EXPOSE 80

CMD ["/usr/local/bin/start.sh"]
