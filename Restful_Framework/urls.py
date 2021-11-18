from django.urls import path, re_path, include
from API.views import AuthView, OrderView

urlpatterns = [
    # 用户登陆验证
    path('api/v1/auth/', AuthView.as_view(), name='auth_login'),
    path('api/v1/order/', OrderView.as_view(), name='orderer'),
    # 版本控制
    re_path(r'^api/(?P<version>[v1|v2]+)', include(('API.urls', 'API'), namespace='api')),
]
