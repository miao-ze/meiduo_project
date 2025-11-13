from django.urls import path,re_path
from . import views
# 使用namespace的方法一
app_name = 'users'

urlpatterns = [
    # 用户注册： reverse(user:register) == '/register/'
    re_path(r'^register/$',views.RegisterView.as_view(),name='register'),
    # 判断用户名是否重复
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{4,20})/count/$',views.UsernameCountView.as_view()),
    # 判断手机号是否重复
    re_path(r'^mobiles/(?P<mobile>[1-9]{2}[0-9]{9})/count/$',views.MobileCountView.as_view()),
]

