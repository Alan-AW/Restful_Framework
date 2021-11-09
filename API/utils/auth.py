from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from API.models import *


class Authtication(BaseAuthentication):
    # 自定义用户认证
    def authenticate(self, request):
        token = request._request.GET.get('token')
        tokenObj = UserToken.objects.filter(token=token).first()
        # 认证失败，抛出异常
        if not tokenObj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 认证成功：直接返回这个元组即可；
        # 在restframework内部会将这两个字段赋值给request，以供后续操作使用
        return (tokenObj.user, tokenObj)

    def authenticate_header(self, request):
        # 认证失败的时候给浏览器返回的响应头
        pass
