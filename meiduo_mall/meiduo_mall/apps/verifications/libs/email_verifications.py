import random
import smtplib
from email.mime.text import MIMEText

password = 'duflpcqbhhekdifd'
# 定义全局变量（一些配置信息）
send_by = '2161998657@qq.com' # 我的邮箱账户
mail_host = 'smtp.qq.com'     # 访问的主机
mail_port = 465               # 端口号



'''1.定义生成四位数字的随机验证码'''
def code(n = 4):
    s = ''
    for i in range(n):
        number = random.randint(0,9)
        upper_alpha = chr(random.randint(65, 90)) #65到90指的是大写字符对应的ASC码
        lower_alpha = chr(random.randint(90,120))
        char = random.choice([upper_alpha, lower_alpha,number])
        s += str(char)
    return s


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

'''3.将验证码和邮箱联系起来'''
def send_email_code(send_to):
    verificate_code = code()
    content = str("【验证码】您的验证码是:") + verificate_code + "，5分钟内有效。如非本人操作，请忽略本条信息，"
    try:
        send_email(send_to=send_to,content=content)
        return verificate_code
    except Exception as e:
        print('发送验证码错误：',e)
        return False


if __name__ == '__main__':
    # 调用方法
    send_to = 'wyys22@qq.com'
    # 传入发送对象的qq账户，调用send_email_code方法
    verificate_code = send_email_code(send_to=send_to)
    print(verificate_code)