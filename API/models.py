from django.db import models


class UserGroup(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'group'


class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)

    group = models.ForeignKey(to='UserGroup', on_delete=models.CASCADE)
    roles = models.ManyToManyField(to='Role')

    class Meta:
        db_table = 'userinfo'


class UserToken(models.Model):
    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
    token = models.CharField(verbose_name='token', max_length=64)

    class Meta:
        db_table = 'user_token'


class Role(models.Model):
    title = models.CharField(verbose_name='角色名称', max_length=32)

    class Meta:
        db_table = 'roles'
