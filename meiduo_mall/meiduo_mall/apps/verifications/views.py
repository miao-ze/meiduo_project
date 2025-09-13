from django_redis import get_redis_connection
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# from meiduo_mall.apps.verifications.libs.captcha.captcha import captcha
from meiduo_mall.apps.verifications.libs.captcha.captcha_test import captcha
from . import constants

"""进行图形验证--[后端逻辑]"""
class ImageCodeView(View):
    def get(self, request, uuid):
        # 1.接受和校验参数：此步骤在路由中就已经写好了

        # 2.实现业务的主体逻辑(生成，保存，响应图形验证码)
        # 2.1 生成（要准备扩展包captcha，准备redis2号库）
        text,image =  captcha.generate_captcha()

        # 2.2 保存文本text（保存到redis中）
        redis_conn = get_redis_connection('verify_code')
        # 语法：redis_conn.set('key','time','value')
        redis_conn.setex('img_%s' % uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text) #要设置过期时间

        # 响应结果
        # 语法：HttpResponse('请求体','数据类型')
        return HttpResponse(image, content_type='image/jpg')