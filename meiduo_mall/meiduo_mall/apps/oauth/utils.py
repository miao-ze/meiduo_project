from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
from meiduo_mall.apps.oauth.constants import ACCESS_TOKEN_EXPIRES
"""进行openid的解密"""
def check_access_token(access_token_openid):
    # 创建序列化器对象
    s = Serializer(settings.SECRET_KEY, expires_in=ACCESS_TOKEN_EXPIRES)
    # 进行反序列化
    try:
        data = s.loads(access_token_openid)
    # 如果过期了，就返回none
    except BadData:
        return None
    # 返回openid明文
    else:
        return data.get("openid")



"""进行openid的加密"""
def generate_access_token(openid):
    # 创建序列化器对象
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=ACCESS_TOKEN_EXPIRES) #过期时间600秒
    # 准备待序列化的字典数据
    data = {'openid': openid}
    # 调用dumps方法进行序列化
    token = s.dumps(data)
    # 返回加密后的openid数据
    return token.decode()

