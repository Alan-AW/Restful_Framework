from django.urls import path, re_path, include
from API.views import AuthView, OrderView, UserView, ParserView, RolesView, UserInfoView, GroupView, UserGroupView, PagerView

urlpatterns = [
    re_path('auth/$', AuthView.as_view(), name='auth'),
    re_path('user/$', UserView.as_view(), name='user'),
    re_path('order/$', OrderView.as_view(), name='order'),
    re_path('parser/$', ParserView.as_view(), name='parser'),
    re_path('ser/roles/$', RolesView.as_view(), name='roles'),
    re_path('ser/userinfo/$', UserInfoView.as_view(), name='userinfo'),
    re_path('ser/group/(?P<pk>\d+)/$', GroupView.as_view(), name='gp'),
    re_path('ser/user_gp/$', UserGroupView.as_view(), name='user_gp'),
    re_path('ser/pager1/$', PagerView.as_view(), name='pager'),
]
