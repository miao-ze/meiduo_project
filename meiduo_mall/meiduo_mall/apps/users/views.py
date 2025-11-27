from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
from django_redis import get_redis_connection
from django.contrib.auth import authenticate  #导入django自带的用户认证系统
from django.contrib.auth import logout
import re,json,logging
from django.contrib.auth.mixins import LoginRequiredMixin

from meiduo_mall.apps.users.models import User
from django.contrib.auth import login
from utils.response_code import RETCODE
from utils.views import LoginRequiredJSONMixin
from meiduo_project.celery_tasks.email.tasks import send_verify_email
# Create your views here.

# 创建日志输出器
logger = logging.getLogger('django')

"""添加邮箱"""
class EmailView(LoginRequiredJSONMixin,View):
    def put(self,request): # put表示更新数据，更新数据时使用
        # 取出email数据
        json_str = request.body.decode() #先拿出原始数据：注意body类型是bytes
        json_dict = json.loads(json_str) #转化成字典
        email = json_dict.get('email')
        # 对email进行校验
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}@(192|163|qq)\.com$',email):
            return http.HttpResponseForbidden('参数email有误')
        # 将用户输入的邮箱保存到用户模型数据库的email字段中:

        try: # 进行数据库操作时都要进行try
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':RETCODE.DBERR,'errmsg':'添加邮箱失败'})

        # 发送邮箱验证码
        send_verify_email()
        # 响应结果
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})

"""用户中心页面"""
class UserInfoView(LoginRequiredMixin,View):
    # 关于：LoginRequiredMixin
    # login_url = '/login'   # 没登陆是要重定向的地址：可以在dev系统环境中进行配置:LOGIN_URL = '/login'
    # login_redirect = 'redirect_to'    # 默认为"next" 如：如果是没有登录的状态时点击用户中心时，在login_url所提供的登录页面的url路径是：www.meiduo.site/login/?next=/info/
    # 提供用户中心页面
    def get(self, request):
        #Django的AuthenticationMiddleware中间件会在处理请求时，
        #根据session中存储的用户ID，去数据库的用户表（默认是auth_user表，或自定义的用户模型表）中查询对应的用户对象，
        #然后将其赋值给request.user
        context = {
            'username':request.user.username,
            'mobile':request.user.mobile,
            'email':request.user.email,
            'email_active':request.user.email_active,
        }
        return render(request,'user_center_info（miao）.html',context)

"""用户退出登录"""
class LogoutView(View):
    def get(self, request):
        # 清除状态保持
        logout(request)
        # 删除cookie中的username
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        # 返回响应结果
        return response

"""用户的登录"""
class LoginView(View):
    # 提供用户登录页面
    def get(self, request):
        return render(request, 'login（miao）.html')
    # 实现用户的登录的逻辑
    def post(self, request):
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 校验参数
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        # 认证用户：查询该账号是否存在，存在则校验密码
        # user = User.objects.get(username=username)
        # user.check_password(password)
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login（miao）.html',{'account_errmsg':'账号或密码错误'})
        # 状态保持
        login(request, user)
        # 判断remembered的存在，来确定状态保持的周期
        if remembered != 'on': #没有记住
            request.session.set_expiry(0) #使用默认的
        else:#记住时：状态保持周期为两周
            request.session.set_expiry(None)
        # 响应结果:将username缓存到cookie中
        # 注意取出next
        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到首页
            response =  redirect(reverse('contents:index'))
        response.set_cookie('username',user.username,max_age=3600 * 24 * 15) #（'key','val','expiry'）
        return response

"""判断用户名是否重复"""
class UsernameCountView(View):
    def get(self, request,username):
        # 1.接受和校验参数：此步骤在编写路由时就已经做好了（因为路由用了正则来进行匹配接受）
        # 2.实现主体业务逻辑：使用username查询对应的记录的条数
        count = User.objects.filter(username=username).count()
        # 3.返回结果：json数据返回,注意：HttpResponse（字典格式）
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','count':count}) #code=0

"""判断手机号是否重复"""
class MobileCountView(View):
    def get(self, request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','count':count})

"""用户注册"""
class RegisterView(View):
    def get(self,request):
        """提供用户注册页面"""
        path = reverse('users:register') #注意：不要有空格
        print(path) #可以打印出当前的路由地址
        return render(request, 'register_text（miao）.html')

    """实现用户注册的业务逻辑"""
    def post(self,request):
        # 编写后端逻辑

        # 1.接受参数：明确前端的请求形式，表单参数
        # values = request.POST #post方式的数据是（）
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_pwd = request.POST.get('confirm_pwd')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        sms_code_client = request.POST.get('sms_code')

        # 2.校验参数：前后端的校验需要分开来，避免恶意用户越过前端逻辑发送请求，要保证后端的数据安全（前后端的校验逻辑相同）
        # 2.1 判断所提交的数据是否齐全（可以使用all方法来进行判断，这个方法更加简单）
        # all的语法：all([])判断列表中的数据是否为空，如果有一个为空，放回false
        if not all([username,password,confirm_pwd,mobile,allow]): #加上not表示：确实有一个为空，执行下方的代码
            return http.HttpResponseForbidden('缺少必传参数') # 使用这个方法来进行返回表示：返回403状态

        # 2.2 判断用户名是否是4-20个字符
        if not re.match('^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入4-20个字符的用户名')
        # 2.3 判断密码是否是8-20个字符
        if not re.match('^[a-zA-Z0-9]{8,20}$',password):
            return http.HttpResponseForbidden('请输入8-20位数的密码')
        # 2.4 判断再次输入的密码是否一致
        if password != confirm_pwd:
            return http.HttpResponseForbidden('再次输入的密码不一致')
        # 2.5 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 2.6 判断用户是否勾选了协议
        if allow != 'on': #注意在这里后端返回的是on，所以用on来进行判断
            return http.HttpResponseForbidden('请勾选用户协议')
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)  #注意是有有效期的
        if sms_code_server is None:
            return render(request,'register_text（miao）.html',{'sms_code_errmsg':'短信验证码已经失效'})
        sms_code_server = sms_code_server.decode() #注意要将重redis中取出的数据进行类型的转化
        if sms_code_server != sms_code_client:
            return render(request,'register_text（miao）.html',{'sms_code_errmsg':'验证码有误'})
        # 3.保存注册数据（将注册数据保存到mysql数据库中）：是注册业务的核心
        try:
           user =  User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            # 运行到此：表示注册失败
            return render(request,'register_text（miao）.html',{'register_errmsg':'注册失败'})
        # 进行状态保持:login其封装了写入session的操作login(request,用户对象)
        login(request,user)
        # 4.响应结果
        # 响应结果:将username缓存到cookie中
        response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)  # （'key','val','expiry'）
        return response
