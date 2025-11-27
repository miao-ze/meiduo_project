# celery的入口文件
from celery import Celery
import os,sys
from pathlib import Path


# 获取项目根目录（meiduo_project）的绝对路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent # 这里的__file__是当前Celery入口文件的路径，需确保它在meiduo_project目录下
# 把根目录加入sys.path
sys.path.insert(10,os.path.join(PROJECT_ROOT))


# 为celery使用django配置文件进行设置
'''
在email的tasks任务中使用了django的setting里的数据信息，但是celery和django是两个不同的程序，
为了然celery可以使用django的程序所以要在这里进行文件的配置
'''
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_project.meiduo_mall.meiduo_mall.settings.dev'

# 创建celery实例（生产者）
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])


# 启动步骤：celery -A celery_tasks.main worker -l info -P gevent
# 切换目录：在仓库根目录下，使用 cd 命令切换到能看到 celery_tasks 包的目录。
# 执行命令：在终端输入 “celery -A celery_tasks.main worker -l info -P gevent” 命令，执行后 Celery 会加载配置、注册任务，知道中间人位置和要执行的任务。
