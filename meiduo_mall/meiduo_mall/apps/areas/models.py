from django.db import models

# Create your models here.
"""省市区"""

'''
自关联字段的外键指向自身，所以models.ForeignKey('self')
使用related_name指明父级查询子集数据的语法（mysql默认的对象语法是:模型类对象.模型名小写_set,由于现在指定为了'subs'，所以现在的语法为:模型类对象.subs）
'''
class Area(models.Model):
    name = models.CharField(max_length=20,verbose_name='名称')
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,related_name='subs',null=True,blank=True,verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'
    def __str__(self):
        return self.name




