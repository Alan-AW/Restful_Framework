import json
from django.shortcuts import render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import exceptions


class MyAuthentication(object):
    def authenticate(self, request):
        # 自定义用户登陆认证
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户登陆认证不通过!')
        return ('user', None)

    def authenticate_header(self, val):
        # 自定义认证固定写法
        pass


class HomeView(APIView):
    # 自定义用户认证的对象列表
    authentication_classes = [MyAuthentication]

    def get(self, request):
        self.dispatch(request)
        ret = {
            'code': 100,
            'msg': 'success'
        }
        return HttpResponse(json.dumps(ret), status=201)

    def post(self, request):
        return HttpResponse(json.dumps('POST'))

    def put(self, request):
        return HttpResponse(json.dumps('PUT'))

    def delete(self, request):
        return HttpResponse(json.dumps('DELETE'))
