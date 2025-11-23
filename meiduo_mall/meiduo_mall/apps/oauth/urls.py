from django.urls import re_path
from meiduo_mall.apps.oauth import views

app_name = 'oauth'
urlpatterns = [
    # 提供QQ登录扫码页面
    re_path('^qq/login/$',views.QQAuthURLView.as_view()),
    # 处理QQ登录回调
    re_path('^oauth_callback/$',views.QQAuthUserView.as_view()),
]