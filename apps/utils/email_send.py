# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/2/12 09:55'
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MXonline.settings import EMAIL_FROM


def random_str(randomlength=18):
    """
    生成随机字符串
    :return:
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type=send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "慕学在线注册链接"
        email_body = "请点击如下链接激活账户： http://127.0.0.1:9999/active/{0}".format(code)
        # print email_body
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "慕学在线密码重置"
        email_body = "请点击如下链接重置密码： http://127.0.0.1:9999/reset/{0}".format(code)
        # print email_body
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = "慕学在线邮箱更新"
        email_body = "请点击如下链接激活邮箱验证码： {0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass







