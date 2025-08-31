from django.urls import path,re_path
from . import views
# 使用namespace的方法一
# app_name = 'users'

urlpatterns = [
    # 用户注册： reverse(user:register) == '/register/'
    re_path(r'^register/$',views.RegisterView.as_view(),name='register'),
]

