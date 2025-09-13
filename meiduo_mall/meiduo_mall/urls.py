"""
URL configuration for meiduo_mall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 使用namespace的方法二
    # user
    path('', include(('meiduo_mall.apps.users.urls', 'users'), namespace='users')),
    # contents：首页信息
    path('', include(('meiduo_mall.apps.contents.urls', 'contents'), namespace='contents')),
    # verifications
    path('', include('meiduo_mall.apps.verifications.urls')),
]
