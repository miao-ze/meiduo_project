from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 由于子应用的创建路径改变了，变成了第二个meiduo_mall(项目的配置文件中了),为了让项目可以找到所以要进行name属性的路径设置
    # 将 name 需要改为子应用的全限定路径（需要用sys.path）知道系统的导包路径：为这个项目（第一个meiduo_mall）
    name = 'meiduo_mall.apps.users'
