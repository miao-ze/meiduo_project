import logging
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django import http
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
import re
from django_redis import get_redis_connection

from meiduo_project.meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.apps.oauth.models import OauthQQUser
from meiduo_mall.apps.oauth.utils import generate_access_token, check_access_token
from meiduo_mall.apps.users.models import User
# 创建日志输出器
logger = logging.getLogger('django')

"""处理QQ登录的回调"""
class QQAuthUserView(View):
    # 处理QQ登录的回调业务逻辑
    def get(self, request):
        # 用户扫码后会得到code，之后用这个code获取access_token
        code = request.GET.get('code')
        if code is None:
            return http.HttpResponseForbidden('获取code失败')
        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 使用code获取access_token
            access_token = oauth.get_access_token(code)
            # 使用access_token获取openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('oAuth2.0认证失败')
        #################到此处已获取openid，接下来要使用openid来判断该QQ用户是否是绑定过美多商城的用户
        try:
            oauth_user = OauthQQUser.objects.get(openid=openid)
        # openid未绑定美多商城用户
        except OauthQQUser.DoesNotExist:
            access_token_openid = generate_access_token(openid)
            context = {'access_token_openid': access_token_openid}
            return render(request,'oauth_callback.html',context)
        # openid已绑定美多商城用户:oauth_user.user表示从QQ登录模型类对象中找到对应的用户模型类对象
        else:
            login(request, oauth_user.user)  #状态保持
            # 响应QQ登录结果
            response =  redirect(reverse('contents:index'))
            response.set_cookie('username',oauth_user.user,max_age=3600*24*14) #写入缓存
            return response

    # 处理用户绑定页面的后端逻辑
    def post(self,request):
        # 先进行参数的提取，和参数的检验
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token_openid = request.POST.get('access_token_openid')
        # 校验参数
        if not all([mobile, password, sms_code_client]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')
        # 判断密码是否合法
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位数的密码')
        # 判断邮箱验证码是否一致（重点）
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_error': '无效的短信验证码'})
        if sms_code_server.decode() != sms_code_client:
            return render(request, 'oauth_callback.html', {'sms_code_error': '输入的短信验证码有误'})
        # 进行openid的判断（先判断openid是否过期）
        openid = check_access_token(access_token_openid)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': 'openid已经失效'})
        # 现在使用openid进行数据查询（如果该用户是存在的则校验密码，不存在的就创建新用户）
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 运行在这，说明不存在，要创建用户,这时user进行了重新的赋值
            user = User.objects.create_user(mobile=mobile, password=password, username=mobile)
        else:
            # 运行到这，说明用户原来就存在，进行校验密码
            if not user.check_password(password):
                return render(request, 'oauth_callback.html', {'account_errmsg': '账号或密码错误'})
        # 不管是已存在的用户或是刚刚创建的用户，都要进行openid的绑定
        try:
            oauth_qq_user = OauthQQUser.objects.create(openid=openid, user=user)
        except Exception as e:
            logger.error(e)
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': '账号或密码错误'})
        # 最后进行（登录，状态保持，写入缓存，重定向操作）
        login(request, oauth_qq_user.user)
        next = request.GET.get('state')
        response = redirect(next)
        response.set_cookie('username', oauth_qq_user.user.username, max_age=3600 * 24 * 15)
        return response



# Create your views here.
"""提供QQ登录扫码页面"""
class QQAuthURLView(View):
    def get(self,request):
        # 接受next
        next = request.GET.get('next')
        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,redirect_uri=settings.QQ_REDIRECT_URI,state=next)
        # 生成QQ登录扫码链接地址
        login_url = oauth.get_qq_url()
        # 进行响应
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'OK','login_url':login_url})
