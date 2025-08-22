# 直接使用django中的key当作盐
from datetime import datetime, timedelta, UTC

import jwt
from rest_framework.authentication import BaseAuthentication

from muxi_shop_api.settings import SECRET_KEY


def create_token(payload, timeout=1000000):
    headers = {
        'alg': 'HS256',
        'typ': 'jwt'
    }

    payload['exp'] = datetime.now(UTC) + timedelta(minutes=timeout)  # token过期时间

    result = jwt.encode(headers=headers, payload=payload, key=SECRET_KEY, algorithm='HS256')
    return result


def get_payload(token):
    result = {"status": False, "data": None, "error": None}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        result["status"] = True
        result["data"] = payload
    except jwt.exceptions.DecodeError:
        result["error"] = "认证失败"
    except jwt.exceptions.ExpiredSignatureError:
        result["error"] = "token已经失效"
    except jwt.exceptions.InvalidTokenError:
        result["error"] = "无效的非法的token"

    # 如果登录成功，status返回True,失败为False
    return result


class JwtQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get("token")
        result_payload = get_payload(token)

        # 该方法需返回 (user, auth) 元组（例如 user 是用户对象，auth 是 Token 对象）
        return (result_payload, token)


class JwtHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # print(request.META)
        token = request.META.get("HTTP_AUTHORIZATION") # 谷歌浏览器用HTTP_AUTHORIZATION获取，postman有区别
        # print(token)
        result_payload = get_payload(token)

        # 该方法需返回 (user, auth) 元组（例如 user 是用户对象，auth 是 Token 对象）
        return (result_payload, token)