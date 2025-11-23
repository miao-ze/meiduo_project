# 主要是用于第三方登录时提供补充字段
from django.db import models


"""为模型类补充字段"""
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    class Meta:
        # 此处是用来说明是抽象模型类，用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True