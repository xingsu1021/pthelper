
使用Djano编写PT助手，代码完全开放，欢迎有兴趣的小伙伴进行修改发布。禁止用于商业用途。

由于涉及ocr本地验证，因此docker镜像相对比较大。

docker部署

```shell
docker pull xingsu1021/pthelper
```

本地部署需要Python3.9+

```shell
pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
```

# v1.0 说明

1、支持签到功能
2、支持配置导出导入
3、支持签到信息发送IYUU，Telegram，邮箱

## 支持站点

站点 | 签到支持|
--- |--- |
红豆饭(hdfans) |  ✔
壹PT吧(1ptba) | ✔
铂金学院(ptchina) | ✔
瓷器(hdchina) | ✔
芒果(3wmg) | ✔
碟粉(discfan) | ✔
杜比(hddolby) | ✔
阿童木(hdatmos) | ✔
聆音(soulvoice) | ✔
铂金家(pthome) | ✔
高清时间(hdtime) | ✔
高清地带(hdzone) | ✔
海棠(htpt) | ✔
观众(audiences) | ✔
老师(nicept) | ✔
家园(hdhome) | ✔
时间(pttime) | ✔
柠檬(lemonhd) | ✔
我堡(ourbits) | ✔
猫站(pterclub) | ✔
城市(hdcity) | ✔
高清视界(hdarea) | ✔
白兔(hares) | ✔
A-SOUL(asf) | ✔
听听歌(totheglory) | ✔
52PT(52pt) | ✔
海胆(haidan) | ✔
皇后(open) | ✔
天空(hdsky) | ✔
备胎(beitai) | ✘
马杀鸡(msg) | ✘
奥申(oshen) | ✘
爱薇(avgv) | ✘
吐鲁番(eastgame) | ✘
小蚂蚁(hdmayi) | ✘
朋友(keepfrds) | ✘
北洋园(tjupt) | ✘
他吹吹风(et8)) | ✘
海带(hd) | ✘
海豹(greatposterwall) | ✘

## 暂时不支持站点

站点 |
--- |
馒头 |

## 已知问题站点

站点 |--- |
--- |--- |
学校(btschool) | ✔

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

**带带弟弟OCR通用验证码识别：<https://github.com/sml2h3/ddddocr>
** 爱语飞飞：<https://iyuu.cn>
**<https://github.com/ledccn/IYUUPlus>
** PTPP：<https://github.com/ronggang/PT-Plugin-Plus>
** PTPP增强版：白大版PTPP@菩提蛋（没找到仓库：（）

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
