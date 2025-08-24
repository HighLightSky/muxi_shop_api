# muxi_shop_api

muxi商城API后端接口服务器，使用Django REST开发。

高考暑假2025.7-2025.8开发，教程来自`imooc.com`。完全按照教程开发。

第一次接触中大型web实战项目，进一步了解电商网站的基础运行逻辑。项目只实现了基础功能，包括用户登录、用户信息修改、商品信息、订单信息、购物车信息、评论信息。这些功能还有很多值得优化的方面。



文件树及解释

```
├── apps  # 将所有的应用放在一个文件夹下方便管理
│   ├── address  # 与用户关联的地址操作，暂未开发
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── cart # 购物车操作
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── comment  # 商品的评论
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── goods  # 商品操作
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── menu  # 首页菜单数据动态渲染操作
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── order  # 订单操作
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── user  # 用户操作
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── db.sqlite3
├── manage.py  # 启动服务器等操作
├── muxi_shop_api
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py  # django配置文件
│   ├── urls.py  # 总url入口
│   └── wsgi.py
├── static  # 从后端请求的图片数据，主要是商品配图
├── tree.py
├── utils
│   ├── ResponseMessage.py  # 加工API返回信息，给出请求返回状态和JSON封装操作
│   ├── __init__.py
│   ├── jwt_auth.py  # 用户登录权限验证操作
│   └── password_encode.py  # 给密码的加密解密操作
```

## 在开发模式下启动服务器

项目还没有做过生产环境测试和部署，教程中有Nginx部署的教程，由于开发时间有限，这部分内容暂未学习。

运行以下命令启动服：

```
python manage.py runserver
```

