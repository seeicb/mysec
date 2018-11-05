mysec 是一款信息收集工具，实际上是给nmap,subDomainsBrute和sublist3r这三款工具做了个web界面。:joy:

可以对指定的域名进行子域名查找，并对所有的子域名IP进行端口扫描，最后汇总。



本项目需要先安装nmap，异步任务使用了celery，需要redis数据库支持。

安装
```
git clone https://github.com/seeicb/mysec.git
cd mysec
创建python3虚拟环境
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
安装项目依赖
pip install -r requirements.txt
```

数据库生成
```
python manage.py makemigrations
python manage.py migrate
```


启动运行
```
service redis-server start
python manage.py celery worker --loglevel=info
python manage.py runserver
```
