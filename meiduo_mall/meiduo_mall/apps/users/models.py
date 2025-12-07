from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.models import BaseModel
from meiduo_mall.apps import areas


# 继承自AbstractUser,表明使用django默认的用户模型类
class User(AbstractUser):
    """由于默认的模型类中没用用户的手机号，所以要自定义一个字段"""
    mobile = models.CharField(max_length=11, unique=True,verbose_name='手机号')
    # 为了（用户中心）的开发，现在补充email_active字段
    email_active = models.BooleanField(default=False,verbose_name='邮箱验证状态')
    # 添加默认收货地址
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        # 自定义表明
        db_table = 'tb_user'
        # 用来在admin站点来显示可以显示中文（可以不写）
        verbose_name = '用户'
        verbose_name_plural = verbose_name #设置复数

    # 进行调试（通过输出数据）
    def __str__(self):
        return self.mobile

class Address(BaseModel):
    """
    用户地址
    """
    # Address模型类中的外键指向Areas / models里面的Area，指明外键ForeignKey时，可以使用字符串来定义应用名.模型类名
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']



