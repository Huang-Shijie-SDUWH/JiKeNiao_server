# JiKeNiao_server


## 项目运行
Flask运行
```
python3 app.py
```
QQ机器人服务运行

```
python3 geek_qqbot.py
```

## 技术栈

#### QQ机器人框架
  
  go-cqhtttp
  文档：https://docs.go-cqhttp.org/
 #### 服务框架
  
  Flask
  
 #### 项目结构
   app.py //flask逻辑
   geek_qqbot.py //极客鸟自动发单接单qq机器人逻辑
   qqbot_api.py //我自己封装的简单的go-cqhttp的python库
 
 ## 现在存在的bug
   服务器不停的情况下，第一次发单可以正常接单，但是第二次发单，输入接单后，会出现不能接单的情况，应该是数据库没有及时同步造成的，但是我不知道怎么改
   
 ## 现在的功能
   志愿者注册
   通过小程序接单，发单
   通过小程序提交反馈
   通过secret查询订单

 ## 现在还差的功能
   志愿者退单
   每月末总结学时
   志愿者自己查询学时什么的
   管理员订单查询
   管理员注册
   
 ## 功能截图
![](https://i.postimg.cc/QNKbS17z/image.png)
![](https://i.postimg.cc/YCRfj3cv/image.png)
![](https://i.postimg.cc/sDFJLx9g/image.png)
![](https://i.postimg.cc/bwp9z55X/image.png)
![](https://i.postimg.cc/PxtgYKJ0/image.png)
