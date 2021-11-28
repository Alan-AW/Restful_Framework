import hashlib
import time, json
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import serializers  # 序列化
from rest_framework import exceptions  # 抛异常
from rest_framework.parsers import JSONParser, FormParser  # 解析器
from rest_framework.response import Response  # 渲染器
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination  # 分页
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning  # 版本控制
from rest_framework.generics import GenericAPIView  # 视图1
from rest_framework.viewsets import GenericViewSet  # 视图2
from rest_framework.viewsets import ModelViewSet    # 视图3
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, HTMLFormRenderer
from API.models import *
from API.utils.permission import SVIPPermission  # 自定义权限
from API.utils.throttle import VisitThrottle  # 自定义节流
from API.utils.version import GetParamVersion  # 自定义get传参获取版本
from API.utils.serializer import RolesSerializer, UserInfoSerializer1, UserInfoSerializer, GroupSerializer  # 自定义序列化


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


# 序列化生成hypermedialink对应的视图
class GroupView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        groupObj = UserGroup.objects.filter(id=pk).first()
        ser = GroupSerializer(instance=groupObj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


# 序列化验证用户提交的数据
class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=10, error_messages={'required': '标题不能为空'}, validators=[])

    def validate_title(self, value):
        # 自定义验证规则
        raise exceptions.ValidationError('就不给你通过')
        # return value

# 序列化验证用户提交的数据
class UserGroupView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问
    def post(self, request, *args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        response = {}
        if ser.is_valid():
            response['status'] = ser.validated_data
        else:
            response['status'] = ser.errors
        return JsonResponse(response)


# 分页序列化
class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


# 分页
class PagerView(APIView):
    authentication_classes = []  # 不需要进行认证
    permission_classes = []  # 不需要权限就能访问

    def get(self, request, *args, **kwargs):
        allObj = Role.objects.all()  # 获取数据
        pg = MyCursorPagination()  #  创建分页对象
        # 获取分页之后的结果
        page_roles = pg.paginate_queryset(queryset=allObj, request=request, view=self)
        ser = PagerSerializer(instance=page_roles, many=True)  # 对分页结果进行序列化处理返回

        return pg.get_paginated_response(ser.data)  # 自动生成上一页和下一页的链接以及总数据量
        # return Response(ser.data)


# 自定义分页
class MyPageNumberFunc(PageNumberPagination):
    """
        127.0.0.1:8000/api/v1/page/?page=1&size=5
        表示当前请求为查看第一页，显示5条数据
        page 和 size 可以单独使用
    """
    page_size = 2  # 分页默认显示数据条数
    max_page_size = 10  # 分页最大数据显示条数
    page_query_param = 'page'  # get传参获取页码
    page_size_query_param = 'size'  # get传参获取到显示条数


class MyPagenumberFuncTo(LimitOffsetPagination):
    """
    这种分页方式表示直接从数据库的某一个位置往后取出多少条数据
    127.0.0.1:8000/api/v1/page/?offset=2&limt=5
    表示当前需要从数据库中取出第2到第5条数据
    """
    default_limit = 2  # 分页默认显示数据条数
    max_limit = None  # 当前页显示数据的最大条数
    limit_query_param = 'limit'  # get传参指定终止位置
    offset_query_param = 'offset'  # get传参指定起始位置


class MyCursorPagination(CursorPagination):
    """
    加密页码
    视图中返回应使用以下方式
        pg = MyCursorPagination()  #  创建分页对象
        page_roles = pg.paginate_queryset(queryset=allObj, request=request, view=self)
        ser = PagerSerializer(instance=page_roles, many=True)  # 对分页结果进行序列化处理返回
        return pg.get_paginated_response(ser.data)  # 自动生成上一页和下一页的链接以及总数据量
    返回结果中的翻页链接
    "next": "http://127.0.0.1:8000/api/v1/ser/pager1/?cursor=cD04",
    "previous": "http://127.0.0.1:8000/api/v1/ser/pager1/?cursor=cj0xJnA9Nw%3D%3D",
    """
    cursor_query_param = 'cursor'  # get传参指定页码
    page_size = 2  # 每页显示数量
    ordering = 'id'  # 排序规则
    page_size_query_param = 'size'  # get传参指定显示条数
    max_page_size = 10  # 分页最大数据显示条数


# 视图（无用）
class NewView(GenericAPIView):  # APIView
    queryset = Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
    def get(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)


# 视图
class NewView2(GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
    def list(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)


# 视图
class MyModelView(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination


class TestView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer, HTMLFormRenderer]
    def get(self, request, *args, **kwargs):
        return Response('hh')









