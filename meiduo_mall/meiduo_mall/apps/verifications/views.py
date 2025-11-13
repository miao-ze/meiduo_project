from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django import http
import random

from meiduo_mall.apps.verifications.libs.captcha.captcha import captcha
from meiduo_mall.apps.verifications import constants
from utils.response_code import RETCODE


"""短信验证码"""
class SMSCodeView(View):
    def get(self, request,mobile):
        # 接受参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 进行图形验证码的校验
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图形验证码已失效'})# code=4001
        # 进行删除redis中的图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 进行对比
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码有误'})# code=4001
        # 进行发送短信验证码
        sms_code = '%06d' % random.randint(0,999999)
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES,sms_code)# 300秒
        # 现在暂时无法使用容联云进行发送---我可无法进行企业认证，只好返回到前端了
        return http.JsonResponse({'code':RETCODE.OK,'sms_code':sms_code,'errmsg':'发送短信验证码成功'}) # code=0


'''图形验证码——后端逻辑'''
class ImageCodeView(View):
    def get(self,request,uuid):
        # 生成
        text,image = captcha.generate_captcha()
        # 连接redis数据库后保存
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s'% uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text)# 300秒
        # 响应验证码
        return http.HttpResponse(image,content_type='image/jpg')
