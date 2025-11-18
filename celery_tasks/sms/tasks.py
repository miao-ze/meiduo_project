# 定义任务
from .yuntongxun.only_miao_can_send_sms_code import send_sms_codes
from celery_tasks.main import celery_app


# 使用装饰器来装饰异步任务，保证celery识别任务
@celery_app.task(name='send_sms_codes')
def send_sms_code(mobile,sms_code):
    """发送短信验证码的异步任务"""
    num = None
    try:
        send_sms_codes(mobile=mobile, sms_code=sms_code)  # 自定义使用容联云进行发送
        num = 0
    except Exception as e:
        num = 1
        print(e)
    # 成功返回0，失败返回1
    finally:
        return num