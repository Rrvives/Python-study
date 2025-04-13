from django.db import models


# 必须继承models.Model这个类
class Test(models.Model):
    # 下面都是创建字段
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


# 创建数据
# Test.objects.create(username='admin', password='123456', email='admin@qq.com', phone='12345678901', address='北京', city='北京')

"""
ORM会将上面的语句转换成sql语句
"""