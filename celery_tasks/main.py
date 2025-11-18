# celery的入口文件
from celery import Celery

# 创建celery实例（生产者）
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])


# 启动步骤：celery -A celery_tasks.main worker -l info -P gevent
# 切换目录：在仓库根目录下，使用 cd 命令切换到能看到 celery_tasks 包的目录。
# 执行命令：在终端输入 “celery -A celery_tasks.main worker -l info -P gevent” 命令，执行后 Celery 会加载配置、注册任务，知道中间人位置和要执行的任务。
