from django.db import models

from meiduo_project.meiduo_mall.utils.models import BaseModel
from meiduo_mall.apps import users

"""QQ登录用户数据"""
class OauthQQUser(BaseModel):
    QQ_user = models.ForeignKey('users.User',on_delete=models.CASCADE,verbose_name='QQ用户')
    QQ_openid = models.CharField(max_length=64,verbose_name='QQ_openid',db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name

"""微博登录用户数据(不一定会使用到)"""
class OauthWeiBoUser(BaseModel):
    WeiBo_user = models.ForeignKey('users.User',on_delete=models.CASCADE,verbose_name='微博用户')
    WeiBo_openid = models.CharField(max_length=64,verbose_name='WeiBo_openid',db_index=True)
    class Meta:
        db_table = 'tb_oauth_WeiBo'
        verbose_name = '微博登录用户数据'
        verbose_name_plural = verbose_name