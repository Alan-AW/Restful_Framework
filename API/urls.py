from django.urls import path, re_path, include
from API.views import AuthView, OrderView, UserView

urlpatterns = [
    re_path('auth/$', AuthView.as_view(), name='auth'),
    re_path('user/$', UserView.as_view(), name='user'),
    re_path('order/$', OrderView.as_view(), name='order'),
]
