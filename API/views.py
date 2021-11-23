import hashlib
import time, json
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning
from API.models import *
from API.utils.permission import SVIPPermission
from API.utils.throttle import VisitThrottle
from API.utils.version import GetParamVersion
from API.utils.serializer import RolesSerializer, UserInfoSerializer1, UserInfoSerializer, GroupSerializer


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
            'content': '善解人意'
        },
        2: {
            'name': '小三',
            'age': 18,
            'gender': '女',
            'content': '温柔体贴'
        }
    }
    return ORDERDICT


# 认证
class AuthView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问
    throttle_classes = []  # 不进行节流控制
    versioning_class = GetParamVersion  # 版本控制

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


# 权限
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


# 版本
class UserView(APIView):
    def get(self, request, *args, **kwargs):
        self.dispatch
        response = dict()
        v = request.version
        return JsonResponse(v, safe=False)


# 解析器：
class ParserView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问

    # parser_classes = [JSONParser, FormParser]  # 解析器，全局已配置
    def post(self, request, *args, **kwargs):
        """
        使用了 parser_classes = [JSONParser] 该配置之后，表示服务器允许用户发送JSON格式数据
        注意：他只能解析content-type: application/json的请求头，其他的不做解析
        FormParser可以解析content-type: application/x-www-form-urlencoded。
        比如：请求头可以是：content-type: application/json 与 json格式的类字典数据
        """

        print(request.data)

        """
    --->1.获取用户请求头
        2.获取用户请求体
        3.根据用户请求头和parser_classes = [JSONParser, FormParser]中支持的请求头进行比较
        4.匹配解析器进行解析
        5.将解析结果赋值给request.data
        """

        return JsonResponse('parser', safe=False)


# 序列化
class RolesView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问

    def get(self, request):
        # 序列化方式一：
        # roles = list(Role.objects.all().values('id', 'title'))
        # ret = json.dumps(roles, ensure_ascii=False)

        # 序列化方式二 -- ser.data 已经是转换完成的结果了
        # roles = Role.objects.all()
        # ser = RolesSerializer(instance=roes, many=True)  # many=True表示有多条数据
        # ret = json.dumps(ser.data, ensure_ascii=False)

        # 序列化方式三  -- ser.data 已经是转换完成的结果了
        roles = Role.objects.all().first()
        ser = RolesSerializer(instance=roes, many=False)  # 只有一条数据的话many=Flase
        ret = json.dumps(ser.data, ensure_ascii=False)

        return JsonResponse(ret)


# 多数据序列化
class UserInfoView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问

    def get(self, request, *args, **kwargs):
        userObj = UserInfo.objects.all()
        ser = UserInfoSerializer(instance=userObj, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)


# 序列化生成hypermedialink
class GroupView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        groupObj = UserGroup.objects.filter(id=pk).first()
        ser = GroupSerializer(instance=groupObj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
