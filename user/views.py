from django.shortcuts import render, HttpResponse, redirect


# Create your views here.
# 获取一个基础响应
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# 返回模板数据
def user_index(request):
    return render(request, 'index.html')


# 模板数据里面传递参数
def template(request):
    # 当这里有一些入参需要传递到模板时可以按照下面的规则进行编写
    name = '张三'  # 基础变量
    dataList = [1, 2, 3]
    data = {
        'name': '李四',
        'age': 18,
        'sex': '男'
    }
    return render(request, 'template.html', {'name': name, 'data': dataList, 'dictData': data})


def something(req):
    # 这里的参数req是一个对象，封装了用户发送过来的所有请求相关数据
    # 1、获取请求方法
    print(req.method)

    # 2、获取get请求url上面请求参数
    print(req.GET)

    # 3、将字符串内容返回给请求者
    # return HttpResponse("Hello, world. You're at the polls index.")

    # 4、返回一个页面  render是读取html的内容 然后渲染成一个字符串在返回给用户的浏览器
    # return render(req, 'index.html')

    # 5、让浏览器重定向到指定的地址
    return redirect('https://www.baidu.com')


# 登录案例
def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')
    else:
        print(req.POST)  # 这个是获取POST的请求参数
        name = req.POST.get('name')  # 获取里面的参数值
        psw = req.POST.get('psw')
        if name == 'root' and psw == '123456':
            return HttpResponse("登录成功")
        else:
            return render(req, 'login.html', {'error_msg': '用户名或密码错误'})


# 引入当前数据库
from user import models


def orm(req):
    # 创建数据
    # models.Test.objects.create(username='root', password='123456', email='root@163.com', phone='12345678901',
    #                            address='北京', city='北京',
    #                            )
    # 删除数据
    # models.Test.objects.filter(username='admin').delete()

    # 更新数据
    # models.Test.objects.filter(id=2).update(username='root1')

    # 获取所有的数据  每一行都是一个对象
    user_list = models.Test.objects.all()
    print(user_list)
    return HttpResponse("Hello, world. You're at the polls index.")
