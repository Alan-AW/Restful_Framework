"""
一、django restframework框架源码执行流程

    库支持：djangorestframework
    导  包：from rest_framework.views import APIView
    在APIView的源码中重写了dispatch方法：（源码入口）
"""
from rest_framework.views import APIView


class HomeView(APIView):

    def get(self, request):
        self.dispatch(request)
        pass

    def disspatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        # 1.对原生request进行了加工
        request = self.initialize_request(request, *args, **kwargs)

        """
        --->def initialize_request(self, request, *args, **kwargs):
                parser_context = self.get_parser_context(request)
                return Request(
                    request,
                    parsers=self.get_parsers(),
                    authenticators=self.get_authenticators(), 
                        --->def get_authenticators(self):
                                return [auth() for auth in self.authentication_classes]
                                --->authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES  # 读取了api_view的配置文件
                        返回了一个对象列表 -- [auth() for auth in self.authentication_classes]
                        读取了restframework框架的配置文件authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
        ----------->到目前为止新的request对象一级封装了两个对象：原生request+对象列表
                    # 原生request对象：  request._request             
                    # 获取认证类的对象：  request.authenticators

                    negotiator=self.get_content_negotiator(),
                    parser_context=parser_context
                )
            """
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            # 2.认证
            self.initial(request, *args, **kwargs)
            """
            --->def initial(self, request, *args, **kwargs):
                    self.format_kwarg = self.get_format_suffix(**kwargs)
                    neg = self.perform_content_negotiation(request)
                    request.accepted_renderer, request.accepted_media_type = neg
                    version, scheme = self.determine_version(request, *args, **kwargs)
                    request.version, request.versioning_scheme = version, scheme
                    # 3.实现认证
                    self.perform_authentication(request)
                        --->def perform_authentication(self, request):
                                request.user  
                                # 此处的request不是原生的request对象了，是被dispatch加工过后新的request对象，
                                  user方法应该去Request类中查找
                                @property -- 属性装饰器，所以上一步调用的时候没有使用括号进行调用，而是直接使用了user属性
                            --->def user(self):
                                    if not hasattr(self, '_user'):
                                        with weap_attrobuteerrors():
                                            # 4.获取认证对象进行一步步的认证
                                            self._auththenticate()
                                        --->    def _authenticate(self):
                                                    for authenticator in self.authenticators:
                                                        try:
                                                            # 5.最终认证位置
                                                            user_auth_tuple = authenticator.authenticate(self)
                                                            --->    def authenticate(self, request):
                                                                        return (self.force_user, self.force_token)
                                                        except exceptions.APIException:
                                                            self._not_authenticated()
                                                            raise
                                                        if user_auth_tuple is not None:
                                                            self._authenticator = authenticator
                                                            self.user, self.auth = user_auth_tuple
                                                            return
                                                    self._not_authenticated()              
                                    return self._user
                    self.check_permissions(request)
                    self.check_throttles(request)
            """
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


"""
如果仅仅实现认证直接写上以下内容即可：

1.自定义一个认证类
class MyAuthentication(object):
    def authenticate(self, request):
        # 自定义用户登陆认证
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户登陆认证不通过!')
        return ('username', None)  --->返回的第一个对象被放到request.user中了

    def authenticate_header(self, val):
        # 自定义认证固定写法
        pass

2.视图类中加入这个对象列表
class HomeView(APIView):
    # 自定义用户认证的对象列表
    authentication_classes = [MyAuthentication]
"""
