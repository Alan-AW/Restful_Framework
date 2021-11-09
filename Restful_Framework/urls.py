from django.urls import path
from API.views import *

urlpatterns = [
    # 用户登陆验证
    path('api/v1/auth/', AuthView.as_view(), name='auth_login')
]
