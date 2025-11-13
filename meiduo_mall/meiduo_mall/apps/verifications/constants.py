#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 校验码常量模块 }
# @Date: 2021/09/24 20:18


# 图形验证码有效期，单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 短信验证码有效期，单位：秒
SMS_CODE_REDIS_EXPIRES = 300

# 60s内是否重复发送的标记
SEND_SMS_CODE_INTERVAL = 60
