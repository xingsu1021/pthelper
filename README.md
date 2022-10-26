
使用Djano编写PT助手(主用签到)，代码完全开放，欢迎有兴趣的小伙伴进行修改发布。禁止用于商业用途。

由于涉及ocr本地验证，因此docker镜像相对比较大。


docker部署

```shell
docker pull xingsu1021/pthelper

仓库地址: https://hub.docker.com/repository/docker/xingsu1021/pthelper
```

本地部署需要Python3.9+(如果cpu不支持avx则使用3.8)

```shell
pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
```

默认账号:admin
默认密码:123456


# 在线升级说明

```js
1、在线git升级  
2、由于可能涉及表结构变更，因此建议更新后重启docker
```
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/update.png)

# v2.2.3 说明
```shell
  1、新增签到代理支持
```

# v2.2.2 说明

```shell
  1、新增备份恢复功能。
  2、支持mysql作为后端数据库
  3、此版本不支持在线升级使用。
```

# v2.2.1 说明

```shell
  1、新增U2签到。
```

# v2.2.0 说明

```shell
  1、新增RSS订阅功能。
  2、新增RSS订阅后直接发送TR下载,(QB未测试但已集成)。
  3、此版本不支持在线升级使用。
```
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/rss.png)

# v2.1.0 说明

```shell
  1、优化企业微信提示
  2、ocr使用飞浆，并使用自己的学习模块
  3、此版本为独立，建议升级替换。(在原镜像上升级也可以使用)
  4、由于某些站点rss访问频率限制，因此在多个同站点规则的情况下，最好时间分开或阅读相关站点说明，防止封号
```

# v2.0.1 说明

```shell
  1、开放计划任务配置
  2、支持签到失败重试(忽略cookie失效站点),建议失败重试时间设置5分钟以上(由于sqlite单进程模式，因此重试和签到不要放在同一个分钟或小时，建议差距2分钟以上)
```

# v2.0 说明

```shell
  1、如果无北洋园，U2（后期增加）账号者，不推荐使用这个版本
  2、由于使用飞浆PaddleOCR,因此不在支持alpine镜像,镜像改为python:3.8-slim-buster,体积进一步增加
  3、Docker原型基于J4125 CPU，因此镜像使用飞浆版本只能使用noavx版本的python3.8(https://www.paddlepaddle.org.cn/whl/linux/mkl/noavx/stable.html)
  4、由于目前使用的nas或小主机的CPU绝大多数都没有avx,也无显卡（独享N卡）,因此暂不提供avx版本,GPU版本
  5、简化签到结果显示
```

v2.0 签到截图
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/iyuu2.png)

# v1.0 说明

1、支持签到功能
2、支持配置导出导入
3、支持签到信息发送IYUU,Telegram,邮箱,企业微信

## 支持站点

由于开放签到功能，因此不在罗列支持站点。基本支持所有通用站，具体可以参考系统。

特殊站由于特殊原因独立进行开发配置，系统有类型说明。如有特殊站目前没有支持的，可以发issues给我，我会根据情况（我有号的情况）进行添加。

## 暂时不支持站点

由于强CF模式无法绕过，因此放弃（常规模拟浏览器也不行），以下罗列为已知但不限于的站点

站点 |
--- |
馒头 |
学校(btschool) |

## 截图

1. IYUU  
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/iyuu.png)
2. Telegram  
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/tg.png)
3. 邮箱  
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/mail.png)
4. 补签  
![](https://raw.githubusercontent.com/xingsu1021/pthelper/master/static/screenshot/buqian.png)

# docker-compose.yml

默认sqlite
```dockerfile
version: '3.7'
services:
  pthelper:
    image: pthelper:latest
    container_name: pthelper
    restart: always
    volumes:
      - 你的目录:/db
      - 你的目录:/logs
      - 你的目录:/backups
    ports:
      - "你的端口:80"
```
Mysql需要修改config/env.prod中的mysql信息
```dockerfile
version: '3.7'
services:
  pthelper:
    image: pthelper:latest
    container_name: pthelper
    restart: always
    environment:
      APP_ENV: prod
    volumes:
      - 你的目录:/db
      - 你的目录:/logs
      - 你的目录:/backups
      - 你的目录:/conf
    ports:
      - "你的端口:80"
```
```shell
APP_ENV: prod 指定使用env.prod配置文件

DATABASE_URL=mysql://root:123456@127.0.0.1:3306/pthelper?charset=utf8mb4&use_unicode=true&ssl_disabled=true&sql_mode=TRADITIONAL
root       数据库用户名
123456     数据库密码
127.0.0.1  数据库地址
3306       数据库端口
pthelper   数据库名称
```
#sqlite迁移到mysql步骤
```shell
1、系统管理---》备份恢复，点击备份
2、关闭docker
3、在conf目录下创建或修改env.prod，配置你使用的mysql,并创建你配置的数据库

DEBUG=True
DATABASE_URL=mysql://root:123456@127.0.0.1:3306/pthelper?charset=utf8mb4&use_unicode=true&ssl_disabled=true&sql_mode=TRADITIONAL

4、启动docker
5、系统管理---》备份恢复，选择要恢复的文件，然后点击恢复
6、刷新页面，重新登录系统
```

## 感谢

带带弟弟OCR通用验证码识别：<https://github.com/sml2h3/ddddocr>  
爱语飞飞：<https://iyuu.cn>  
         <https://github.com/ledccn/IYUUPlus>  
PTPP：<https://github.com/ronggang/PT-Plugin-Plus>  
PTPP增强版：白大版PTPP@菩提蛋（没找到仓库：（）  
飞浆：<https://github.com/PaddlePaddle/PaddleOCR>

## 以下忽略，只做个人记录

-------------------------------------------------------------

# 本地启动测试命令

APP_ENV=prod python manage.py runserver 0.0.0.0:80

# 编译镜像

docker build  -t pthelper:v1.0 .

# py文件编译pyc

python -O -m compileall -b .

# 上传镜像

docker commit 4f7d7c5a8b58 xingsu1021/pthelper:latest
docker push xingsu1021/pthelper
