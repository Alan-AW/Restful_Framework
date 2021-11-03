"""
一、django restframework框架源码执行流程

    库支持：djangorestframework
    导  包：from rest_framework.views import APIView
    在APIView的源码中重写了dispatch方法：
"""
def dispatch(self, request, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs

    # 此处对原生request进行了增加
    request = self.initialize_request(request, *args, **kwargs)

    """
    源码：
        def initialize_request(self, request, *args, **kwargs):
            parser_context = self.get_parser_context(request)
            return Request(
                request,
                parsers=self.get_parsers(),
                authenticators=self.get_authenticators(),  
                    返回了一个对象列表 -- [auth() for auth in self.authentication_classes]
                    读取了restframework框架的配置文件authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
----------------到目前位置新的request对象一级封装了两个对象：原生request+对象列表
                # 原生request对象：  request._request             
                # 获取认证类的对象：  request.authenticators
                    
                negotiator=self.get_content_negotiator(),
                parser_context=parser_context
            )
        """
    self.request = request
    self.headers = self.default_response_headers  # deprecate?

    try:
        self.initial(request, *args, **kwargs)


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