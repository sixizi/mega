#开发规范
##目录说明
* api  公用调用接口
* docs 各类文档
* lib  公用库
* mega_web  网站项目
* scripts   脚本
* tests		测试代码及文档

##  依赖包
python 2.6/2.7

Django-1.6.5

python-daemon 1.5.5  <a>https://pypi.python.org/pypi/python-daemon/1.5.5]</a>

##api
接口规范
##docs
##lib
###DB
数据库访问方式：

1.使用models类 见mega_web/models/*

2.使用MySQLdb  见lib/PyMysql

##mega_web
mega   主页

管理    资源管理

调度
##mega_service
TCP 通信数据包规范：

        """        work instance:{'HEAD':'MEGA','TYPE':'CMD','VALUE':'ls'}
        keys:
            HEAD:    for safe interactive,should be MEGA
            TYPE:    cmd,task,other
            VALUE:   what to do : ls
            TIME:    when to do : 0 once  ,
            REPEAT:  lifecycle of job   day,week,month
            TARGET:    uniqeu identify for server or instance or database.
        """


##scripts
##tests
路径:tests/*
####api
* api_resource.py  资源池管理接口测试用例

  