from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 继承自AbstractUser,表明使用django默认的用户模型类
class User(AbstractUser):
    """由于默认的模型类中没用用户的手机号，所以要自定义一个字段"""
    mobile = models.CharField(max_length=11, unique=True,verbose_name='手机号')

    class Meta:
        # 自定义表明
        db_table = 'tb_user'

        # 用来在admin站点来显示可以显示中文（可以不写）
        verbose_name = '用户'
        verbose_name_plural = verbose_name #设置复数

    # 进行调试（通过输出数据）
    def __str__(self):
        return self.mobile



