from meiduo_mall.apps.contents.views import IndexView
from django.urls import path, re_path

app_name = 'contents'

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
]


