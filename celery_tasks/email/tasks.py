from django.core.mail import send_mail
from django.conf import settings

from meiduo_project.celery_tasks.main import celery_app

"""定义发送验证邮箱的方法
注意：band-->保证task对象会作为第一个参数自动传入
     retry_backoff-->异常自动重试的时间间隔
     max_retries-->异常自动重试次数上限
"""
@celery_app.task(band=True,name='send_verify_email',retry_backoff=3)
def send_verify_email(self,to_email,verify_url):

    # send_mail('标题','普通邮件正文','收件人列表','富文本邮件正文（html）')
    #由于正文就是html，所以我们设计普通邮件正文为空：即不填
    subject = '美多商城邮箱验证'
    html_message = '<p>尊敬的用户您好</p>'\
                   '<p>感谢您使用美多商城。</p>'\
                   '<p>您的邮箱为：%s。请点击此链接激活您的邮箱</p>'\
                   '<p><a href="%s">%s</a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject,'',settings.EMAIL_FROM,[to_email],html_message=html_message)
    except Exception as e:
        #触发错误重试，最多重试3次
        raise self.retry(exc=e,max_retries=3)


