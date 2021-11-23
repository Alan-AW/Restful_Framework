from django.urls import path, re_path, include
from API.views import AuthView, OrderView, UserView, ParserView, RolesView, UserInfoView

urlpatterns = [
    re_path('auth/$', AuthView.as_view(), name='auth'),
    re_path('user/$', UserView.as_view(), name='user'),
    re_path('order/$', OrderView.as_view(), name='order'),
    re_path('parser/$', ParserView.as_view(), name='parser'),
    re_path('ser/roles/$', RolesView.as_view(), name='roles'),
    re_path('ser/userinfo/$', UserInfoView.as_view(), name='userinfo'),
]
