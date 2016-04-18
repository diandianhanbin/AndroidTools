#安卓性能测试工具

##说明
工具是基于Python2.x写的,第三方依赖包仅有ConfigParser.

网络框架是使用Django,因此你的电脑必须要有Django环境.不会配置的请自行Google.

当然,工具是基于adb进行性能测试的,因此你的电脑还必须要有adb环境,具体方式请Google.

前端是使用Bootstrap和jQuery写的,走势图使用百度Echarts生成.

##使用方式
1. Clone到本地
2. 进入Android_Monitor文件
3. python manage.py runserver
4. 浏览器打开http://127.0.0.1:8000/datashow

##注意
1. 我在Mac环境下测试没问题,Windows可能需要微调.
2. Monkey如果和其他监控同时用工具打开,有几率会出现异常停止的情况,目前赞为解决.
3. 目前为个人使用,因此除错机制可能不完善,请正确的使用它.
4. 请不要使用PyCharm2016.1来执行,目前Pycharm2016.1有bug,会报错adb command not found

##展示图

![客户端](http://7xsgl3.com1.z0.glb.clouddn.com/6E2A853B-7FA1-46DB-970B-E153C53EB2AD.png)

![web端](http://7xsgl3.com1.z0.glb.clouddn.com/D40ABEF3-5AFF-4107-8DE9-1219E92A724E.png)

![内存监控](http://7xsgl3.com1.z0.glb.clouddn.com/3F7C7D57-9435-4DFE-9CAC-08AB2F5D7619.png)

![cpu监控](http://7xsgl3.com1.z0.glb.clouddn.com/20C18466-D2BE-4BF8-A848-57F6EC551E0F.png)

![流量监控](http://7xsgl3.com1.z0.glb.clouddn.com/02C218C4-5922-439C-A63B-10BC5661C5F4.png)