from API.models import *
from rest_framework import serializers


# 自动系列化处理简单字段数据获取
class RolesSerializer(serializers.Serializer):
    # 以下字段必须要跟数据库中的字段对应，或者取什么字段，就要对应什么字段
    id = serializers.IntegerField()
    title = serializers.CharField()


# 自动序列化处理复杂关系的数据获取一（手动操作粒度控制）
class UserInfoSerializer1(serializers.Serializer):
    # 普通字段获取详细数据
    username = serializers.CharField()
    password = serializers.CharField()

    # choices字段获取详细数据
    user_type = serializers.CharField(source='get_user_type_display')
    # 在内部会对每一行的数据执行一下row.source的值，然后自动判断这个值是否可被调用，
    #     如果可以被调用就会自动加括号进行调用，如果source的值是一个字符串，那么直接返回了这个字符串所对应的字段内容
    #     如果写成了get_user_type_display,那么这个方法就会被自动执行，获取到文本信息

    # 外键关联获取详细数据
    group = serializers.CharField(source='group.title')

    # ManyToMany字段获取详细数据
    roles = serializers.SerializerMethodField()  # 自定义显示（外键或者choices字段都可以进行自定义的获取）

    def get_roles(self, row):  # row表示当前处理表的类对象
        roleObj = row.roles.all()
        ret = []
        for item in roleObj:
            ret.append({'id': item.id, 'title': item.title}, )
        return ret


# 自动序列化处理复杂关系的数据获取二(内置基本的操作,也可以混合使用：)
class UserInfoSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='get_user_type_display')
    roles = serializers.SerializerMethodField()
    group = serializers.HyperlinkedIdentityField(view_name='api:gp', lookup_field='group_id',
                                                 lookup_url_kwarg='pk')  # 默认生成url

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'user_type', 'roles', 'group']

    def get_roles(self, row):  # row表示当前处理表的类对象
        roleObj = row.roles.all()
        ret = []
        for item in roleObj:
            ret.append({'id': item.id, 'title': item.title}, )
        return ret


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['title']
        depth = 0
