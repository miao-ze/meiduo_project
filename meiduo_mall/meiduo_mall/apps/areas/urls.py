from django.urls import path,re_path

from meiduo_mall.apps.areas.views import AreaView

urlpatterns = [
    re_path(r'^areas/$',AreaView.as_view(),),
]
