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
    # 用户登录
    re_path(r'^login/$',views.LoginView.as_view(),name='login'),
    # 用户退出
    re_path(r'^logout/$',views.LogoutView.as_view(),name='logout'),
    # 用户中心页面
    re_path(r'^info/$',views.UserInfoView.as_view(),name='info'),
    # 添加邮箱
    re_path(r'^emails/$',views.EmailView.as_view()),
    # 邮箱激活链接的视图
    re_path(r'^emails/verification/$',views.VerifyEmailView.as_view()),
    # 展示收货地址 users:address
    re_path(r'addresses/$',views.AddressView.as_view(),name='address'),
    # 新增收货地址
    re_path(r'^addresses/create/$',views.AddressCreateView.as_view()),
    # 修改（更新）和删除地址
    re_path(r'^addresses/(?P<address_id>\d+)/$',views.UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    re_path(r'^addresses/(?P<address_id>\d+)/default/$',views.DefaultAddressView.as_view()),
    # 设置地址标题
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),

]

