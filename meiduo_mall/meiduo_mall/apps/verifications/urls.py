from django.urls import re_path
from meiduo_mall.apps.verifications import views
app_name = 'verifications'
urlpatterns = [
    # 顺便进行路径参数的校验
    re_path(r'^register/image_codes/(?P<uuid>[\w-]+)/$',views.ImageCodeView.as_view()),
]


