from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from django.conf import settings as sys
import time

VISIT_RECORD = {}

# 自定义节流方法
"""
class VisitThrottle(BaseThrottle):
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 获取用户IP
        remote_addr = self.get_ident(request)
        c_time = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [c_time, ]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        # 控制时间
        while history and history[-1] < c_time - sys.VISIT_CONTORE_TIME:
            history.pop()

        # 控制频率
        if len(history) < sys.VISIT_CONTORE_LENGTH:
            history.insert(0, c_time)
            return True  # 可以访问

        # return False  # 不可以访问

    def wait(self):
        # 提示信息，还需要等多少秒之后才可以访问
        c_time = time.time()
        history = self.history[-1]
        wait_time = sys.VISIT_CONTORE_TIME - (c_time - history)
        return wait_time
"""


# 内置节流方法 -- 匿名用户
class VisitThrottle(SimpleRateThrottle):
    scope = 'happy'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


# 内置节流方法 -- 登陆用户
class UserThrottle(SimpleRateThrottle):
    scope = 'user'

    def get_cache_key(self, request, view):
        return request.user.username
