from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import exceptions
from API.models import *
import hashlib
import time
from API.utils.permission import MyPermission


def md5(user):
    # 生成随机token字符串
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def order_dict():
    # 模拟订单
    ORDERDICT = {
        1: {
            'name': 'girlfriend',
            'age': 20,
            'gender': '女',
            'content': '波大腿长'
        },
        2: {
            'name': '小三',
            'age': 18,
            'gender': '女',
            'content': '波更大腿更长'
        }
    }
    return ORDERDICT


class AuthView(APIView):
    authentication_classes = []  # 不需要进行认证
    def post(self, request, *args, **kwargs):
        self.dispatch
        ret = {'code': 1000, 'msg': None}
        try:
            name = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            userObj = UserInfo.objects.filter(username=name, password=pwd).first()
            if userObj:
                # 为用户登陆创建随机字符串
                token = md5(name)
                # 存在就更新否则就创建
                UserToken.objects.update_or_create(user=userObj, defaults={'token': token})
                ret['token'] = token
            else:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'

        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'

        return JsonResponse(ret)

from rest_framework.permissions import AllowAny
class OrderView(APIView):
    # 订单(只让SVIP客户访问)
    def get(self, request, *args, **kwargs):
        token = request._request.GET.get('token')
        if not token:
            return JsonResponse('用户未登陆!')
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = order_dict()
        except Exception as e:
            ret['code'] = 1001
            ret['msg'] = '访问错误'
        return JsonResponse(ret)
