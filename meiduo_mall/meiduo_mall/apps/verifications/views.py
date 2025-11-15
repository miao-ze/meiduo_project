from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django import http
import random,logging

from meiduo_mall.apps.verifications.libs.captcha.captcha import captcha
from meiduo_mall.apps.verifications import constants
from utils.response_code import RETCODE

# 创建日志输出器(用来记录短信验证码)
logger = logging.getLogger('django')

"""短信验证码"""
class SMSCodeView(View):
    def get(self, request,mobile):
        # 接受参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 先连接到redis数据库
        redis_conn = get_redis_connection('verify_code')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'发送短信过于频繁'}) #code=4002
        # 进行图形验证码的校验
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
        logger.info(sms_code) #进行短信验证码的日志记录
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES,sms_code)# 300秒
        # 保存发送短信验证码的标记
        redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, value=1)  # 60秒
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
