from django.urls import path, re_path, include
from rest_framework.routers import Route
from API.views import *

roter = Route()
roter.register(AuthView)

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
    re_path('ser/new_view/$', NewView.as_view(), name='new_view'),
    re_path('ser/new_view2/$', NewView2.as_view({'get': 'list'}), name='new_view2'),
    re_path('ser/model_view/(?P<pk>\d+)/$',MyModelView.as_view({
                                                            'get': 'retrieve',  # 查
                                                            'delete': 'destroy',  # 删
                                                            'put': 'update',      # （增）更新
                                                            'patch': 'partial_update'   # （改）局部更新
                                                            }),name='model_view')
]
