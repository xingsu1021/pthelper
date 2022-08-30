
使用Djano编写PT助手(主用签到)，代码完全开放，欢迎有兴趣的小伙伴进行修改发布。禁止用于商业用途。

由于涉及ocr本地验证，因此docker镜像相对比较大。


docker部署

```shell
docker pull xingsu1021/pthelper
```

本地部署需要Python3.9+

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


# v2.0.1 说明

```shell
  1、开放计划任务配置
  2、支持签到失败重试(忽略cookie失效站点),建议失败重试时间设置5分钟以上
```

# v2.0 说明

```shell
  1、如果无北洋园，U2（后期增加）账号者，不推荐使用这个版本
  2、由于使用飞浆PaddleOCR,因此不在支持alpine镜像,镜像改为python:3.8-slim-buster,体积进一步增加
  3、Docker原型基于J4125 CPU，因此镜像使用飞浆版本只能使用noavx版本的python3.8(https://www.paddlepaddle.org.cn/whl/linux/mkl/noavx/stable.html)
  4、由于目前使用的nas或小主机的CPU绝大多数都没有avx,也无显卡（独享N卡）,因此暂不提供avx版本,GPU版本
  5、简化签到结果显示
```

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

```dockerfile
version: '3.7'
services:
  flexget:
    image: pthelper:v1.0
    container_name: pthelper
    restart: always
    volumes:
      - /home/data/docker-compose/pthelper/db:/db
      - /home/data/docker-compose/pthelper/logs:/logs
      - /home/data/docker-compose/pthelper/backups:/backups
    ports:
      - "58000:80"
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

python manage.py runserver --settings=pthelper.local_settings

# 编译镜像

docker build  -t pthelper:v1.0 .

# py文件编译pyc

python -O -m compileall -b .

# 上传镜像

docker commit 4f7d7c5a8b58 xingsu1021/pthelper:latest
docker push xingsu1021/pthelper
