from django.apps import AppConfig


class ContentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 注意每次创建app时，要进行修改
    name = 'meiduo_mall.apps.contents'