# pull official base image
FROM python:3.9-slim-buster

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
    apt-get install -y apt-utils gnupg libgl1-mesa-glx libglib2.0

RUN pip install --upgrade pip -i https://pypi.mirrors.ustc.edu.cn/simple/

RUN pip install --no-cache-dir --upgrade pip -i https://pypi.mirrors.ustc.edu.cn/simple/
#RUN pip install --no-cache-dir --upgrade setuptools -i https://pypi.mirrors.ustc.edu.cn/simple/

COPY requirements.txt .

#将需要的包体全部打包成直接安装的包whl
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

#安装nginx
#RUN apt install curl gnupg2 ca-certificates lsb-release -y
#RUN curl -o /tmp/nginx_signing.key https://nginx.org/keys/nginx_signing.key && \
COPY nginx_signing.key /tmp
RUN  cat /tmp/nginx_signing.key | apt-key add -

RUN echo "deb http://nginx.org/packages/debian buster nginx" > /etc/apt/sources.list.d/nginx.list && \
    apt update && \
    #apt install nginx supervisor -y && \
    apt install nginx -y && \
    rm -f /etc/nginx/conf.d/default.conf && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log 

#RUN pip install --no-cache-dir supervisor -i https://pypi.mirrors.ustc.edu.cn/simple/

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/vhost.conf /etc/nginx/conf.d/vhost.conf
COPY conf/supervisord.conf /etc/supervisord.conf
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

RUN apt-get purge gnupg -y && \
    apt-get autoremove -y && \
    apt-get clean

# copy project
COPY . $APP_HOME

RUN ln -s /home/data/www/db /db && \
    ln -s /home/data/www/logs /logs && \
    ln -s /home/data/www/backups /backups && \
    rm -rf conf && \
    rm -rf docker-compose.yml && \
    rm -rf Dockerfile && \
    rm -rf README.md && \
    rm -rf requirements.txt && \
    rm -rf db/* logs/* backups/* \
    rm -rf .git*

EXPOSE 80
#apt-get安装路径
#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
#pip安装路径
#CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]

CMD ["/usr/local/bin/start.sh"]