from django.urls import re_path

from . import views

app_name = 'verifications'
urlpatterns = [
    # 图形验证码
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$',views.ImageCodeView.as_view()),
    # 短信验证码
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SMSCodeView.as_view()),
    # MS.MIAO专用短信服务通道
    re_path(r'^sms_codes/miao/(?P<mobile>1[3-9]\d{9})/$',views.MsMiaoSendSms.as_view()),
    # 判断短信验证码
    # re_path(r'^check_sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.CheckSmsCode.as_view()),
]