from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import exceptions
from API.models import *
import hashlib
import time


def md5(user):
    # 生成随机token字符串
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    def get(self, request, *args, **kwargs):
        username = request._request.GET.get('username')
        return JsonResponse(username, safe=False)

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            name = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            userObj = UserInfo.objects.filter(username=name, password=pwd).first()
            if not userObj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为用户登陆创建随机字符串
            token = md5(name)
            # 存在就更新否则就创建
            UserToken.objects.update_or_create(user=userObj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'

        return JsonResponse(ret)

