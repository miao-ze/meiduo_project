from Lib.http.client import HTTPResponse
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
import re
from meiduo_mall.apps.users.models import User
from django.contrib.auth import login
from utils.response_code import RETCODE
# Create your views here.



class UsernameCountView(View):
    """判断用户名是否重复"""
    def get(self, request,username):
        # 1.接受和校验参数：此步骤在编写路由时就已经做好了（因为路由用了正则来进行匹配接受）
        # 2.实现主体业务逻辑：使用username查询对应的记录的条数
        count = User.objects.filter(username=username).count()
        # 3.返回结果：json数据返回,注意：HttpResponse（字典格式）
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','count':count})

class RegisterView(View):

    """用户注册"""
    def get(self,request):
        """提供用户注册页面"""
        path = reverse('users:register') #注意：不要有空格
        print(path) #可以打印出当前的路由地址
        return render(request, 'register_text（miao）.html')

    """实现用户注册的业务逻辑"""
    def post(self,request):
        # 编写后端逻辑

        # 1.接受参数：明确前端的请求形式，表单参数
        values = request.POST #post方式的数据是（）
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        # 2.校验参数：前后端的校验需要分开来，避免恶意用户越过前端逻辑发送请求，要保证后端的数据安全（前后端的校验逻辑相同）
        # 2.1 判断所提交的数据是否齐全（可以使用all方法来进行判断，这个方法更加简单）
        # all的语法：all([])判断列表中的数据是否为空，如果有一个为空，放回false
        if not all([username,password,password2,mobile,allow]): #加上not表示：确实有一个为空，执行下方的代码
            return http.HttpResponseForbidden('缺少必传参数') # 使用这个方法来进行返回表示：返回403状态

        # 2.2 判断用户名是否是4-20个字符
        if not re.match('^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入4-20个字符的用户名')
        # 2.3 判断密码是否是8-20个字符
        if not re.match('^[a-zA-Z0-9]{8,20}$',password):
            return http.HttpResponseForbidden('请输入8-20位数的密码')
        # 2.4 判断再次输入的密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('再次输入的密码不一致')
        # 2.5 判断手机号是否合法
        if not re.match('^[1-9]{2}[0-9]{9}$',mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 2.6 判断用户是否勾选了协议
        if allow != 'on': #注意在这里后端返回的是on，所以用on来进行判断
            return http.HttpResponseForbidden('请勾选用户协议')
        # 3.保存注册数据（将注册数据保存到mysql数据库中）：是注册业务的核心
        try:
           user =  User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            # 运行到此：表示注册失败
            return render(request,'register_text（miao）.html',{'register_errmsg':'注册失败'})
        # 进行状态保持:login其封装了写入session的操作login(request,用户对象)
        login(request,user)
        # 4.响应结果
        # 相当于redirect('/')
        path = reverse('contents:index')
        print('首页的路由地址：',path)
        return redirect(reverse('contents:index'))
