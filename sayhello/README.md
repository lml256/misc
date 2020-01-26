这是一个用Flask框架写的留言板程序  
开始之前，请先确保你的机器上有Python3.6及以上环境，并确保安装了Pipenv，Pipenv是个优秀的包管理器，如果你还没有安装的话，请执行以下命令安装  
```pip install pipenv```  
然后执行以下命令
```
git clone git@github.com:Varpc/sayhello.git
cd sayhello
pipenv install --dev
pipenv shell
set FLASK_APP=sayhello
set FLASK_ENV=development
flask forge  # 初始化数据库，并生成虚拟数据，你可以使用--count来指定生成的数据条数
flask run
```
然后，你就可以在[http://127.0.0.1:5000/](http://127.0.0.1:5000/)看到效果了

@2018-11-14