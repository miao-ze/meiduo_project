from jinja2 import Environment
from django.urls import reverse
# staticfiles.storage：静态文件的存储，可以获取到静态文件的前缀
from django.contrib.staticfiles.storage import staticfiles_storage

def jinja2_environment(**options):

    env = Environment(**options)

    env.globals.update({
        # 1.需求：{{ static('静态文件相对路径') }}
        'static':staticfiles_storage.url,
        # 2.需求 {{ url('路由的命名空间') }}
        'url':reverse
    })

    return env