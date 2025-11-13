
import smtplib
from email.mime.text import MIMEText

password = 'duflpcqbhhekdifd'
# 定义全局变量（一些配置信息）
send_by = '2161998657@qq.com' # 我的邮箱账户
mail_host = 'smtp.qq.com'     # 访问的主机
mail_port = 465               # 端口号
'''2.定义发验证码的函数'''
def send_email(send_to,content,subject='验证码'): # 参数分别是：向谁发送，发送内容
    # 示例化一个对象
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = send_by
    message['To'] = send_to
    message['Subject'] = subject
    # 使用第三方服务发送()  ==>传入服务的主机地址，和端口号
    smtp = smtplib.SMTP_SSL(mail_host, mail_port,'utf-8')
    # 登录邮箱（）==>传入邮箱账号和密码
    smtp.login(send_by,password)
    smtp.sendmail(send_by,send_to,message.as_string())
    print('发送成功！！')
    print(content)
'''3.将验证码和邮箱联系起来''' # 使用前要传入email_code数据
def send_email_code(email_code,send_to):
    content = str("【验证码】您的验证码是:") + email_code + "，5分钟内有效。如非本人操作，请忽略本条信息"
    try:
        send_email(send_to=send_to,content=content)
        return email_code
    except Exception as e:
        print('发送验证码错误：',e)
        return False
if __name__ == '__main__':
    # 调用方法
    send_to = 'wyys22@qq.com'
    # 传入发送对象的qq账户，调用send_email_code方法,
    verification_code = send_email_code(email_code='232321', send_to=send_to) #email_code:为要发送的验证码
    print(verification_code)