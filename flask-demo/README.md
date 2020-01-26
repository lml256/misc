这是一个练习flask时写的一个小demo  
如何使用  
首先clone后进入到根目录，依次执行如下命令
```
py -3 -m venv venv
venv\Scripts\activate
python -m pip  install --upgrade pip
pip install -e .
```
由于较老版本的pip会造成依赖安装不全的情况，所以在以上命令中先升级下pip
然后启动项目
```
set FLASK_APP=flaskr
flask init-db
flask run
```
然后就可以在[http://127.0.0.1:5000/]( http://127.0.0.1:5000/ )看到效果啦


我不记得什么时候写的了，大概：
@2018-11