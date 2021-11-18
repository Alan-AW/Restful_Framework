from django.urls import path, re_path, include
from API.views import AuthView, OrderView

urlpatterns = [
    re_path('auth/$', AuthView.as_view(), name='auth'),
    re_path('order/$', OrderView.as_view(), name='order'),
]
