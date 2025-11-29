# 自定义用户认证的后端：实现多账号的登录
from django.contrib.auth.backends import ModelBackend
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

from meiduo_mall.apps.users.models import User
from . import constants

'''进行token的解密,并返回user'''
def check_verify_email_token(token):
    s = Serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES) #邮件验证链接有效期:1天
    try:
        data = s.loads(token)
    # 如果token过期了，就返回none
    except BadData:
        return None
    else:
        user_id = data['user_id']
        email = data['email']
        try: # 因为这一步要进行查询数据库，所以要try一下
          user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user




"""生成邮箱激活链接，并返回链接url"""
def generate_verify_email_url(user):
    s = Serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES) #邮件验证链接有效期:1天
    data = {'user_id': user.id,'email': user.email}
    token = s.dumps(data) # 进行加密
    return settings.EMAIL_VERIFY_URL + '?token=' + token.decode()



"""将判断username是手机号还是用户名的过程进行封装，以便以后可以重复使用"""
def get_user_by_account(account):
    # 要校验username是用户名还是手机号
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # username == 手机号
            user = User.objects.get(mobile=account)
        else:
            # username == 用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

"""自定义用户认证后端"""
class UsernameMobileBackend(ModelBackend):
    # 重写用户认证方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 查询用户
        user = get_user_by_account(username)
        # 如果查询到用户，需要校验密码
        if user and user.check_password(password):
            return user
        else:
            return None
        # 返回user