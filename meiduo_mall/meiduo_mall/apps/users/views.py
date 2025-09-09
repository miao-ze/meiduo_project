from django.shortcuts import render
from django.urls import reverse
from django.views import View


# Create your views here.

class RegisterView(View):

    """用户注册"""
    def get(self,request):
        """提供用户注册页面"""
        path = reverse('users:register') #注意：不要有空格
        print(path) #可以打印出当前的路由地址
        return render(request,'register_text.html')

    """实现用户注册的业务逻辑"""
    def post(self,request):
        pass